"""
async-qa.py — Trigger an async QA session on your current project

This is the Managed Agents equivalent of running /qa in Claude Code,
but it runs server-side and produces a downloadable report.

Prerequisites:
    pip install anthropic

Environment variables:
    ANTHROPIC_API_KEY        — your Anthropic API key
    CLAUDE_OS_QA_AGENT_ID   — agent ID from: ant beta agents create --file qa-runner.yaml
    CLAUDE_OS_ENV_ID         — environment ID from: ant beta environments create
    GITHUB_TOKEN             — PAT with repo read access (if using GitHub mount)

Usage:
    # Mount via GitHub (recommended for clean state):
    python async-qa.py --github owner/repo --branch main

    # Or upload the current directory's files:
    python async-qa.py --local ./my-project

    # After the run, the QA report is saved to ./qa-report.md
"""

import argparse
import os
import time
from pathlib import Path

import anthropic

# ── Config ────────────────────────────────────────────────────────────────────

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
QA_AGENT_ID = os.environ["CLAUDE_OS_QA_AGENT_ID"]
ENVIRONMENT_ID = os.environ["CLAUDE_OS_ENV_ID"]
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")


# ── Session helpers ───────────────────────────────────────────────────────────


def run_qa_session(resources: list[dict]) -> str:
    """
    Create a QA session, stream output, download the report.
    Returns the path to the saved report.
    """
    print("[qa] Creating session...")
    session = client.beta.sessions.create(
        agent={"type": "agent", "id": QA_AGENT_ID},
        environment_id=ENVIRONMENT_ID,
        title="Claude OS QA run",
        resources=resources,
    )
    session_id = session.id
    print(f"[qa] Session: {session_id}")

    # Stream-first: open before sending the kickoff
    print("[qa] Running... (streaming output)\n")
    with client.beta.sessions.stream(session_id=session_id) as stream:
        client.beta.sessions.events.send(
            session_id=session_id,
            events=[
                {
                    "type": "user.message",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Run the full QA pass on the project in /workspace/repo:\n"
                                "Phase 1 — test suite\n"
                                "Phase 2 — lint\n"
                                "Phase 3 — top 3 performance bottlenecks\n"
                                "Phase 4 — write the QA report to "
                                "/mnt/session/outputs/qa-report.md\n"
                            ),
                        }
                    ],
                }
            ],
        )

        for event in stream:
            if event.type == "agent.message":
                for block in event.content:
                    if block.type == "text":
                        print(block.text, end="", flush=True)

            elif event.type == "agent.thinking":
                # Optional: show thinking blocks for debugging
                pass

            elif event.type == "session.status_idle":
                stop_type = getattr(event.stop_reason, "type", None)
                if stop_type != "requires_action":
                    print("\n\n[qa] Agent finished.")
                    break

            elif event.type == "session.status_terminated":
                print("\n[qa] Session terminated.")
                break

    # Download the report from session outputs
    report_path = _download_report(session_id)

    # Archive session
    _wait_then_archive(session_id)
    print(f"[qa] Session archived.")

    return report_path


def _download_report(session_id: str, retries: int = 5) -> str:
    """
    Download qa-report.md from session outputs.
    There is a brief indexing lag after session goes idle — retry once or twice.
    """
    for attempt in range(retries):
        files = client.beta.files.list(session_id=session_id)
        report_files = [f for f in files.data if "qa-report" in f.filename]
        if report_files:
            file = report_files[0]
            content = client.beta.files.download(file.id)
            output_path = "./qa-report.md"
            with open(output_path, "wb") as fp:
                fp.write(content.read())
            print(f"\n[qa] Report saved: {output_path}")
            return output_path

        if attempt < retries - 1:
            print(f"[qa] Waiting for report to be indexed... ({attempt + 1}/{retries})")
            time.sleep(2)

    print("[qa] Warning: no qa-report.md found in session outputs.")
    return ""


def _wait_then_archive(session_id: str, retries: int = 10) -> None:
    """Poll until the session is no longer running, then archive."""
    for _ in range(retries):
        s = client.beta.sessions.retrieve(session_id)
        if s.status != "running":
            break
        time.sleep(0.3)
    client.beta.sessions.archive(session_id)


# ── Resource builders ─────────────────────────────────────────────────────────


def github_resources(repo: str, branch: str) -> list[dict]:
    """Mount a GitHub repo branch as a session resource."""
    if not GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN is required for GitHub repo mounting.")
    return [
        {
            "type": "github_repository",
            "url": f"https://github.com/{repo}",
            "authorization_token": GITHUB_TOKEN,
            "mount_path": "/workspace/repo",
            "checkout": {"type": "branch", "name": branch},
        }
    ]


def local_resources(project_dir: str) -> list[dict]:
    """
    Upload key project files and mount them as session resources.
    This is a best-effort approach — for full fidelity use GitHub mounting.
    Uploads: source files, tests, config, SPECS.md, requirements.txt / package.json.
    """
    project_path = Path(project_dir).resolve()
    extensions = {".py", ".ts", ".js", ".go", ".rb", ".java", ".json", ".yaml", ".yml", ".toml", ".md"}
    skip_dirs = {"node_modules", ".git", "__pycache__", ".venv", "venv", "dist", "build", ".mypy_cache"}

    resources = []
    for file_path in project_path.rglob("*"):
        if file_path.is_file():
            if any(part in skip_dirs for part in file_path.parts):
                continue
            if file_path.suffix not in extensions:
                continue
            if file_path.stat().st_size > 5 * 1024 * 1024:  # skip > 5 MB
                continue

            rel_path = file_path.relative_to(project_path)
            print(f"[qa] Uploading: {rel_path}")
            with open(file_path, "rb") as fp:
                uploaded = client.beta.files.upload(file=fp)
            resources.append(
                {
                    "type": "file",
                    "file_id": uploaded.id,
                    "mount_path": f"/workspace/repo/{rel_path}",
                }
            )

    if not resources:
        raise ValueError(f"No uploadable files found in {project_dir}")

    print(f"[qa] Uploaded {len(resources)} files.")
    return resources


# ── CLI ───────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Run an async Claude OS QA session on your project."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--github",
        metavar="OWNER/REPO",
        help="Mount a GitHub repo (requires GITHUB_TOKEN)",
    )
    group.add_argument(
        "--local",
        metavar="DIR",
        help="Upload files from a local directory",
    )
    parser.add_argument(
        "--branch",
        default="main",
        help="Branch to checkout (GitHub mode only, default: main)",
    )
    args = parser.parse_args()

    print("\n=== Claude OS Async QA ===\n")

    if args.github:
        resources = github_resources(repo=args.github, branch=args.branch)
    else:
        resources = local_resources(project_dir=args.local)

    report_path = run_qa_session(resources)

    if report_path:
        print(f"\nDone. Report: {report_path}")
        with open(report_path) as fp:
            print("\n" + "─" * 60 + "\n")
            print(fp.read())
    else:
        print("\nDone. No report file was produced (check session output above).")


if __name__ == "__main__":
    main()
