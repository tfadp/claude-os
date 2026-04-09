"""
pr-review-bot.py — GitHub PR review bot using Claude Managed Agents

This is the Managed Agents equivalent of running /review on a PR.
Point a GitHub webhook at this script (or call it from GitHub Actions).

Prerequisites:
    pip install anthropic flask python-dotenv

Environment variables:
    ANTHROPIC_API_KEY           — your Anthropic API key
    CLAUDE_OS_REVIEWER_AGENT_ID — agent ID from: ant beta agents create --file reviewer.yaml
    CLAUDE_OS_ENV_ID            — environment ID from: ant beta environments create
    GITHUB_TOKEN                — PAT with repo + PR comment permissions
    GITHUB_WEBHOOK_SECRET       — (optional) validate webhook signatures

Usage:
    # Run once to create the agent and environment (if you haven't already):
    #   ant beta agents create --file agents/reviewer.yaml
    #   ant beta environments create --name claude-os-reviewer --networking unrestricted
    #
    # Set the IDs in your environment, then:
    python pr-review-bot.py

    # Or call review_pr() directly from GitHub Actions:
    python -c "
    from pr_review_bot import review_pr
    import sys
    review_pr(
        repo='owner/repo',
        pr_number=int(sys.argv[1]),
        branch=sys.argv[2],
    )
    " 42 feature-branch
"""

import json
import os
import time

import anthropic

# ── Config ────────────────────────────────────────────────────────────────────

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
REVIEWER_AGENT_ID = os.environ["CLAUDE_OS_REVIEWER_AGENT_ID"]
ENVIRONMENT_ID = os.environ["CLAUDE_OS_ENV_ID"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


# ── Core review logic ─────────────────────────────────────────────────────────


def review_pr(repo: str, pr_number: int, branch: str) -> str:
    """
    Run the Claude OS reviewer agent on a GitHub PR branch.
    Returns the review text to post as a PR comment.

    Args:
        repo:       "owner/repo" (e.g. "acme/backend")
        pr_number:  GitHub PR number
        branch:     the PR's head branch (e.g. "feature/auth-refactor")
    """
    print(f"[review] Starting review session for {repo}#{pr_number} ({branch})")

    # Create a session with the reviewer agent.
    # The agent config (model, system, tools) lives on the agent object —
    # sessions just reference it by ID.
    session = client.beta.sessions.create(
        agent={"type": "agent", "id": REVIEWER_AGENT_ID},
        environment_id=ENVIRONMENT_ID,
        title=f"PR #{pr_number} review — {repo}",
        resources=[
            {
                "type": "github_repository",
                "url": f"https://github.com/{repo}",
                "authorization_token": GITHUB_TOKEN,
                "mount_path": "/workspace/repo",
                "checkout": {"type": "branch", "name": branch},
            }
        ],
    )
    session_id = session.id
    print(f"[review] Session created: {session_id}")

    # Stream-first: open the stream before sending the kickoff message.
    # Events emitted before the stream opens are missed.
    review_text = _run_session(
        session_id=session_id,
        message=(
            f"Review the recent changes on branch `{branch}` in /workspace/repo.\n\n"
            "Focus on:\n"
            "1. Run the test suite and report results\n"
            "2. Review the git diff (git diff main..HEAD) for issues\n"
            "3. Check SPECS.md in .claude/ if it exists\n"
            "4. Score the changes and list issues by severity\n"
        ),
    )

    # Clean up the session
    _wait_for_idle_then_archive(session_id)
    print(f"[review] Session archived: {session_id}")

    return review_text


def _run_session(session_id: str, message: str) -> str:
    """
    Send a message, stream events, and collect agent text output.
    Returns all agent.message text concatenated.
    """
    collected_text: list[str] = []

    with client.beta.sessions.stream(session_id=session_id) as stream:
        # Send the kickoff while the stream is live
        client.beta.sessions.events.send(
            session_id=session_id,
            events=[
                {
                    "type": "user.message",
                    "content": [{"type": "text", "text": message}],
                }
            ],
        )

        for event in stream:
            if event.type == "agent.message":
                for block in event.content:
                    if block.type == "text":
                        collected_text.append(block.text)
                        print(block.text, end="", flush=True)

            elif event.type == "session.status_idle":
                stop_type = getattr(event.stop_reason, "type", None)
                if stop_type != "requires_action":
                    # Normal end — agent is done
                    break

            elif event.type == "session.status_terminated":
                break

    return "".join(collected_text)


def _wait_for_idle_then_archive(session_id: str, retries: int = 10) -> None:
    """
    Brief poll to confirm the session is idle before archiving.
    The SSE stream emits idle slightly before the queryable status reflects it.
    """
    for _ in range(retries):
        s = client.beta.sessions.retrieve(session_id)
        if s.status != "running":
            break
        time.sleep(0.3)

    client.beta.sessions.archive(session_id)


# ── GitHub comment posting ────────────────────────────────────────────────────


def post_pr_comment(repo: str, pr_number: int, body: str) -> None:
    """Post a comment on a GitHub PR using the REST API."""
    import urllib.request

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    payload = json.dumps({"body": body}).encode()
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        print(f"[github] Comment posted — status {resp.status}")


# ── Flask webhook handler (optional) ──────────────────────────────────────────


def create_webhook_app():
    """
    Returns a Flask app that handles GitHub PR webhooks.
    Register this URL as a GitHub webhook with content-type application/json.
    """
    from flask import Flask, abort, request

    app = Flask(__name__)

    @app.route("/webhook", methods=["POST"])
    def webhook():
        event = request.headers.get("X-GitHub-Event", "")
        if event != "pull_request":
            return "ok", 200

        payload = request.get_json(force=True)
        action = payload.get("action", "")
        if action not in ("opened", "synchronize", "reopened"):
            return "ok", 200

        pr = payload["pull_request"]
        repo = payload["repository"]["full_name"]
        pr_number = pr["number"]
        branch = pr["head"]["ref"]

        print(f"[webhook] PR event: {action} — {repo}#{pr_number} ({branch})")

        # Run review (blocks until done; use a task queue in production)
        review_text = review_pr(repo=repo, pr_number=pr_number, branch=branch)
        post_pr_comment(repo=repo, pr_number=pr_number, body=review_text)

        return "ok", 200

    return app


# ── Entry point ───────────────────────────────────────────────────────────────


if __name__ == "__main__":
    import sys

    # Direct invocation: python pr-review-bot.py owner/repo 42 feature-branch
    if len(sys.argv) == 4:
        repo_arg, pr_arg, branch_arg = sys.argv[1], sys.argv[2], sys.argv[3]
        print(f"\n=== Claude OS PR Review Bot ===\n")
        review = review_pr(repo=repo_arg, pr_number=int(pr_arg), branch=branch_arg)
        print(f"\n\n--- Posting to GitHub ---\n")
        post_pr_comment(repo=repo_arg, pr_number=int(pr_arg), body=review)
    else:
        # Webhook server mode
        app = create_webhook_app()
        app.run(host="0.0.0.0", port=8080, debug=False)
