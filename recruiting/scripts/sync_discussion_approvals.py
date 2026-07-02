#!/usr/bin/env python3
"""Import approval batches pasted into a GitHub Discussion.

The static dashboard cannot safely write to GitHub from the browser because it
would need a token. Instead, it copies an approval JSON payload for a human to
paste into a configured Discussion. This script is intended for GitHub Actions:
it reads discussion comments with GITHUB_TOKEN, imports unseen approval batches,
and records processed comment IDs in applications/approval_inbox.json.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

from pipeline_common import REPO_ROOT, save_json, utc_now


DEFAULT_STATE_PATH = REPO_ROOT / "applications" / "approval_inbox.json"
GRAPHQL_URL = "https://api.github.com/graphql"
FENCE_RE = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL | re.IGNORECASE)


def load_json(path: Path, default):
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def graphql(token: str, query: str, variables: dict) -> dict:
    request = urllib.request.Request(
        GRAPHQL_URL,
        data=json.dumps({"query": query, "variables": variables}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.github+json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"GitHub GraphQL request failed: {exc.code} {body}") from exc
    if payload.get("errors"):
        raise SystemExit(json.dumps(payload["errors"], indent=2))
    return payload["data"]


def fetch_comments(token: str, owner: str, repo: str, discussion_number: int) -> list[dict]:
    query = """
    query($owner: String!, $repo: String!, $number: Int!, $after: String) {
      repository(owner: $owner, name: $repo) {
        discussion(number: $number) {
          comments(first: 100, after: $after) {
            pageInfo { hasNextPage endCursor }
            nodes {
              id
              url
              body
              bodyText
              createdAt
              updatedAt
              author { login }
            }
          }
        }
      }
    }
    """
    comments = []
    after = None
    while True:
        data = graphql(token, query, {"owner": owner, "repo": repo, "number": discussion_number, "after": after})
        discussion = (data.get("repository") or {}).get("discussion")
        if not discussion:
            raise SystemExit(f"Discussion #{discussion_number} not found in {owner}/{repo}.")
        page = discussion["comments"]
        comments.extend(page["nodes"])
        if not page["pageInfo"]["hasNextPage"]:
            return comments
        after = page["pageInfo"]["endCursor"]


def parse_payloads(comment: dict) -> list[dict]:
    body = comment.get("body") or comment.get("bodyText") or ""
    candidates = [match.group(1) for match in FENCE_RE.finditer(body)]
    stripped = body.strip()
    if stripped.startswith("{") and stripped.endswith("}"):
        candidates.append(stripped)

    payloads = []
    for candidate in candidates:
        try:
            payload = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if payload.get("schema_version") == "approval.batch.v1" and payload.get("action") == "approve_for_tailoring":
            payloads.append(payload)
    return payloads


def import_payload(payload: dict) -> dict:
    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
        temp_path = Path(handle.name)
    try:
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "recruiting" / "scripts" / "import_approvals.py"), str(temp_path)],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        return json.loads(result.stdout)
    finally:
        temp_path.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", default=os.environ.get("GITHUB_REPOSITORY_OWNER") or "rverma-dev")
    parser.add_argument("--repo", default=(os.environ.get("GITHUB_REPOSITORY") or "rverma-dev/resume").split("/", 1)[-1])
    parser.add_argument("--discussion-number", type=int, default=int(os.environ.get("APPROVAL_DISCUSSION_NUMBER") or "0"))
    parser.add_argument("--state-path", type=Path, default=DEFAULT_STATE_PATH)
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN is required.")
    if not args.discussion_number:
        print(json.dumps({"ok": True, "configured": False, "message": "APPROVAL_DISCUSSION_NUMBER is not set."}, indent=2))
        return 0

    state = load_json(args.state_path, {
        "schema_version": "approval_inbox.v1",
        "updated_at": None,
        "processed_comment_ids": [],
        "processed_batch_ids": [],
        "events": [],
    })
    processed_comments = set(state.get("processed_comment_ids") or [])
    processed_batches = set(state.get("processed_batch_ids") or [])
    imported = []
    skipped = []

    for comment in fetch_comments(token, args.owner, args.repo, args.discussion_number):
        comment_id = comment["id"]
        if comment_id in processed_comments:
            continue
        payloads = parse_payloads(comment)
        if not payloads:
            skipped.append({"comment_id": comment_id, "reason": "no_approval_payload"})
            continue
        for payload in payloads:
            batch_id = payload.get("batch_id")
            if batch_id in processed_batches:
                skipped.append({"comment_id": comment_id, "batch_id": batch_id, "reason": "batch_already_processed"})
                continue
            result = import_payload(payload)
            imported.append({"comment_id": comment_id, "batch_id": batch_id, "result": result, "url": comment.get("url")})
            processed_batches.add(batch_id)
        processed_comments.add(comment_id)

    if imported:
        state["updated_at"] = utc_now()
        state["processed_comment_ids"] = sorted(processed_comments)
        state["processed_batch_ids"] = sorted(processed_batches)
        state["events"] = (state.get("events") or []) + imported
        save_json(args.state_path, state)

    print(json.dumps({
        "ok": True,
        "configured": True,
        "discussion": f"{args.owner}/{args.repo}#{args.discussion_number}",
        "imported": len(imported),
        "skipped": len(skipped),
        "imported_batches": [item["batch_id"] for item in imported],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
