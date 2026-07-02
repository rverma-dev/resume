#!/usr/bin/env python3
"""Import approval batches from GitHub Issues.

The static dashboard opens a prefilled issue composer because browser code must
not carry a GitHub write token. This script is intended for GitHub Actions: it
polls open approval issues, imports unseen approval batches, records processed
issue numbers in applications/approval_inbox.json, comments on each processed
issue, and closes it.
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
import urllib.parse
import urllib.request
from pathlib import Path

from pipeline_common import REPO_ROOT, save_json, utc_now


DEFAULT_STATE_PATH = REPO_ROOT / "applications" / "approval_inbox.json"
DEFAULT_LABELS = []
IMPORTED_LABEL = "approval-imported"
API_ROOT = "https://api.github.com"
FENCE_RE = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL | re.IGNORECASE)


def load_json(path: Path, default):
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def github_request(token: str, method: str, path: str, payload: dict | None = None):
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        f"{API_ROOT}{path}",
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else None
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"GitHub API request failed: {method} {path}: {exc.code} {body}") from exc


def fetch_approval_issues(token: str, owner: str, repo: str, labels: list[str]) -> list[dict]:
    issues = []
    page = 1
    while True:
        params = {
            "state": "open",
            "sort": "created",
            "direction": "asc",
            "per_page": "100",
            "page": str(page),
        }
        if labels:
            params["labels"] = ",".join(labels)
        query = urllib.parse.urlencode(params)
        batch = github_request(token, "GET", f"/repos/{owner}/{repo}/issues?{query}")
        issue_batch = [issue for issue in batch if "pull_request" not in issue]
        issues.extend(issue_batch)
        if len(batch) < 100:
            return issues
        page += 1


def parse_payloads(issue: dict) -> list[dict]:
    body = issue.get("body") or ""
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


def issue_labels(issue: dict) -> list[str]:
    labels = []
    for label in issue.get("labels") or []:
        if isinstance(label, dict) and label.get("name"):
            labels.append(label["name"])
        elif isinstance(label, str):
            labels.append(label)
    return labels


def mark_issue_processed(token: str, owner: str, repo: str, issue: dict, batch_ids: list[str], status: str) -> None:
    number = issue["number"]
    body = [
        f"{status} by the scheduled recruiting approval sync.",
        "",
        f"- Batches: {', '.join(batch_ids)}",
        f"- Processed at: {utc_now()}",
        "",
        "The static tracker will update after the workflow commit and GitHub Pages deploy.",
    ]
    github_request(token, "POST", f"/repos/{owner}/{repo}/issues/{number}/comments", {"body": "\n".join(body)})
    labels = [label for label in issue_labels(issue) if label != "approval-pending"]
    for label in ("recruiting-approval", IMPORTED_LABEL):
        if label not in labels:
            labels.append(label)
    github_request(token, "PATCH", f"/repos/{owner}/{repo}/issues/{number}", {"state": "closed", "labels": labels})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", default=os.environ.get("GITHUB_REPOSITORY_OWNER") or "rverma-dev")
    parser.add_argument("--repo", default=(os.environ.get("GITHUB_REPOSITORY") or "rverma-dev/resume").split("/", 1)[-1])
    parser.add_argument("--labels", default=os.environ.get("APPROVAL_ISSUE_LABELS") or ",".join(DEFAULT_LABELS))
    parser.add_argument("--state-path", type=Path, default=DEFAULT_STATE_PATH)
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN is required.")

    labels = [label.strip() for label in args.labels.split(",") if label.strip()]
    state = load_json(args.state_path, {
        "schema_version": "approval_inbox.v1",
        "updated_at": None,
        "processed_issue_numbers": [],
        "processed_batch_ids": [],
        "last_processed_issue_number": 0,
        "events": [],
    })
    processed_issues = set(state.get("processed_issue_numbers") or [])
    processed_batches = set(state.get("processed_batch_ids") or [])
    original_processed_issues = set(processed_issues)
    original_processed_batches = set(processed_batches)
    imported = []
    skipped = []

    for issue in fetch_approval_issues(token, args.owner, args.repo, labels):
        issue_number = issue["number"]
        if issue_number in processed_issues:
            continue
        payloads = parse_payloads(issue)
        if not payloads:
            skipped.append({"issue_number": issue_number, "reason": "no_approval_payload"})
            continue

        issue_imported_batches = []
        issue_seen_batches = []
        for payload in payloads:
            batch_id = payload.get("batch_id")
            if batch_id in processed_batches:
                skipped.append({"issue_number": issue_number, "batch_id": batch_id, "reason": "batch_already_processed"})
                issue_seen_batches.append(batch_id)
                continue
            result = import_payload(payload)
            imported.append({"issue_number": issue_number, "batch_id": batch_id, "result": result, "url": issue.get("html_url")})
            issue_imported_batches.append(batch_id)
            processed_batches.add(batch_id)

        if issue_imported_batches:
            mark_issue_processed(token, args.owner, args.repo, issue, issue_imported_batches, "Imported")
            processed_issues.add(issue_number)
        elif issue_seen_batches:
            mark_issue_processed(token, args.owner, args.repo, issue, issue_seen_batches, "Already imported")
            processed_issues.add(issue_number)

    if imported or processed_issues != original_processed_issues or processed_batches != original_processed_batches:
        state["updated_at"] = utc_now()
        state["processed_issue_numbers"] = sorted(processed_issues)
        state["processed_batch_ids"] = sorted(processed_batches)
        state["last_processed_issue_number"] = max(processed_issues) if processed_issues else state.get("last_processed_issue_number", 0)
        state["events"] = (state.get("events") or []) + imported
        save_json(args.state_path, state)

    print(json.dumps({
        "ok": True,
        "issue_labels": labels,
        "imported": len(imported),
        "skipped": len(skipped),
        "imported_batches": [item["batch_id"] for item in imported],
        "last_processed_issue_number": max(processed_issues) if processed_issues else state.get("last_processed_issue_number", 0),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
