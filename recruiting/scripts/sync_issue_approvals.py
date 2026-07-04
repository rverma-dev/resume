#!/usr/bin/env python3
"""Import recruiting decision batches from GitHub Issues.

The static dashboard opens prefilled issue composers because browser code must
not carry a GitHub write token. This script is intended for GitHub Actions. It
polls open recruiting decision issues, imports unseen approval, rejection, or
application-status payloads, records processed issue numbers in
applications/approval_inbox.json, comments on each processed issue, and closes
it.
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

from pipeline_common import REPO_ROOT, load_applications, load_jobs, save_applications, save_jobs, save_json, utc_now


DEFAULT_STATE_PATH = REPO_ROOT / "applications" / "approval_inbox.json"
DEFAULT_LABELS = []
APPROVAL_IMPORTED_LABEL = "approval-imported"
REJECTION_IMPORTED_LABEL = "rejection-imported"
APPLICATION_STATUS_IMPORTED_LABEL = "application-status-imported"
API_ROOT = "https://api.github.com"
FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL | re.IGNORECASE)
PENDING_LABELS = {"approval-pending", "rejection-pending", "status-pending"}


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
        elif payload.get("schema_version") == "rejection.batch.v1" and payload.get("action") == "reject_for_now":
            payloads.append(payload)
        elif payload.get("schema_version") == "application.status.v1" and payload.get("action") == "update_application_status":
            payloads.append(payload)
    return payloads


def payload_identifier(payload: dict) -> str:
    return payload.get("batch_id") or payload.get("update_id") or json.dumps(payload, sort_keys=True)


def imported_label(payload: dict) -> str:
    if payload.get("schema_version") == "rejection.batch.v1":
        return REJECTION_IMPORTED_LABEL
    if payload.get("schema_version") == "application.status.v1":
        return APPLICATION_STATUS_IMPORTED_LABEL
    return APPROVAL_IMPORTED_LABEL


def import_payload(payload: dict) -> dict:
    if payload.get("schema_version") == "approval.batch.v1":
        script = "import_approvals.py"
    elif payload.get("schema_version") == "rejection.batch.v1":
        script = "import_rejections.py"
    elif payload.get("schema_version") == "application.status.v1":
        script = "import_application_status.py"
    else:
        raise SystemExit(f"Unsupported payload schema_version: {payload.get('schema_version')}")

    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
        temp_path = Path(handle.name)
    try:
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "recruiting" / "scripts" / script), str(temp_path)],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        return json.loads(result.stdout)
    finally:
        temp_path.unlink(missing_ok=True)


def set_value(row: dict, key: str, value) -> bool:
    if value in (None, "") or row.get(key) == value:
        return False
    row[key] = value
    return True


def annotate_issue_metadata(payload: dict, result: dict, issue: dict) -> dict:
    issue_number = issue.get("number")
    issue_url = issue.get("html_url") or ""
    if not issue_number:
        return {"applications": 0, "jobs": 0}

    data_apps = load_applications()
    data_jobs = load_jobs()
    applications = data_apps.get("applications", [])
    jobs = data_jobs.get("jobs", [])
    by_app_id = {app.get("application_id"): app for app in applications if app.get("application_id")}
    by_job_id = {job.get("job_id"): job for job in jobs if job.get("job_id")}

    touched_apps = set()
    touched_jobs = set()

    def annotate_app(app_id: str, prefix: str) -> None:
        app = by_app_id.get(app_id)
        if not app:
            return
        changed = False
        changed |= set_value(app, f"{prefix}_issue_number", issue_number)
        changed |= set_value(app, f"{prefix}_issue_url", issue_url)
        changed |= set_value(app, f"{prefix}_issue_label", f"#{issue_number}")
        if changed:
            touched_apps.add(app_id)
        job_id = app.get("job_id")
        if job_id:
            annotate_job(job_id, prefix)

    def annotate_job(job_id: str, prefix: str) -> None:
        job = by_job_id.get(job_id)
        if not job:
            return
        changed = False
        changed |= set_value(job, f"{prefix}_issue_number", issue_number)
        changed |= set_value(job, f"{prefix}_issue_url", issue_url)
        changed |= set_value(job, f"{prefix}_issue_label", f"#{issue_number}")
        if changed:
            touched_jobs.add(job_id)

    schema_version = payload.get("schema_version")
    if schema_version == "approval.batch.v1":
        app_ids = set(result.get("application_ids") or [])
        for skipped in result.get("skipped") or []:
            if isinstance(skipped, dict) and skipped.get("application_id"):
                app_ids.add(skipped["application_id"])
        for app_id in app_ids:
            annotate_app(app_id, "approval")
        for job_id in payload.get("job_ids") or []:
            annotate_job(job_id, "approval")
    elif schema_version == "rejection.batch.v1":
        for job_id in result.get("job_ids") or []:
            annotate_job(job_id, "rejection")
    elif schema_version == "application.status.v1":
        app_id = result.get("application_id") or payload.get("application_id")
        if app_id:
            annotate_app(app_id, "status")

    if touched_apps:
        data_apps["applications"] = applications
        save_applications(data_apps)
    if touched_jobs:
        data_jobs["jobs"] = jobs
        save_jobs(data_jobs)
    return {"applications": len(touched_apps), "jobs": len(touched_jobs)}


def issue_labels(issue: dict) -> list[str]:
    labels = []
    for label in issue.get("labels") or []:
        if isinstance(label, dict) and label.get("name"):
            labels.append(label["name"])
        elif isinstance(label, str):
            labels.append(label)
    return labels


def mark_issue_processed(token: str, owner: str, repo: str, issue: dict, payload_ids: list[str], status: str, label: str) -> None:
    number = issue["number"]
    body = [
        f"{status} by the scheduled recruiting issue sync.",
        "",
        f"- Payloads: {', '.join(payload_ids)}",
        f"- Processed at: {utc_now()}",
        "",
        "The static tracker will update after the workflow commit and GitHub Pages deploy.",
    ]
    github_request(token, "POST", f"/repos/{owner}/{repo}/issues/{number}/comments", {"body": "\n".join(body)})
    labels = [existing for existing in issue_labels(issue) if existing not in PENDING_LABELS]
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
            skipped.append({"issue_number": issue_number, "reason": "no_supported_payload"})
            continue

        issue_imported_payloads = []
        issue_seen_payloads = []
        issue_imported_labels = set()
        issue_seen_labels = set()
        for payload in payloads:
            payload_id = payload_identifier(payload)
            if payload_id in processed_batches:
                skipped.append({"issue_number": issue_number, "payload_id": payload_id, "reason": "payload_already_processed"})
                issue_seen_payloads.append(payload_id)
                issue_seen_labels.add(imported_label(payload))
                continue
            result = import_payload(payload)
            result["issue_metadata_updates"] = annotate_issue_metadata(payload, result, issue)
            imported.append({"issue_number": issue_number, "payload_id": payload_id, "result": result, "url": issue.get("html_url")})
            issue_imported_payloads.append(payload_id)
            issue_imported_labels.add(imported_label(payload))
            processed_batches.add(payload_id)

        if issue_imported_payloads:
            label = sorted(issue_imported_labels)[0]
            mark_issue_processed(token, args.owner, args.repo, issue, issue_imported_payloads, "Imported", label)
            processed_issues.add(issue_number)
        elif issue_seen_payloads:
            label = sorted(issue_seen_labels)[0]
            mark_issue_processed(token, args.owner, args.repo, issue, issue_seen_payloads, "Already imported", label)
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
        "imported_payloads": [item["payload_id"] for item in imported],
        "last_processed_issue_number": max(processed_issues) if processed_issues else state.get("last_processed_issue_number", 0),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
