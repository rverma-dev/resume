#!/usr/bin/env python3
"""Import an application status update from a GitHub Issue payload."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pipeline_common import append_ledger, load_applications, load_jobs, save_applications, save_jobs, utc_now


ALLOWED_STATUSES = {
    "approved",
    "tailoring",
    "ready",
    "needs_manual",
    "applied",
    "interview",
    "rejected",
    "offer",
    "archived",
}


def load_payload(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if payload.get("schema_version") != "application.status.v1":
        raise SystemExit("Expected schema_version=application.status.v1.")
    if payload.get("action") != "update_application_status":
        raise SystemExit("Expected action=update_application_status.")
    if payload.get("status") not in ALLOWED_STATUSES:
        raise SystemExit(f"Unsupported status: {payload.get('status')}")
    if not payload.get("application_id"):
        raise SystemExit("application_id is required.")
    return payload


def append_note(row: dict, note: str) -> None:
    if not note:
        return
    notes = row.setdefault("notes", [])
    if note not in notes:
        notes.append(note)


def update_application(app: dict, payload: dict, now: str) -> dict:
    previous_status = app.get("status") or "approved"
    status = payload["status"]
    reason = payload.get("reason") or ""
    blocker = payload.get("blocker") or ""

    app["status"] = status
    app["updated_at"] = now
    app["status_reason"] = reason
    app["last_status_update_id"] = payload.get("update_id")

    if status == "applied":
        applied_at = payload.get("applied_at") or now
        app["approval_status"] = "applied"
        app["applied_at"] = applied_at
        app["applied_date"] = applied_at[:10]
        app["manual_action_required"] = False
        if payload.get("submitted_resume_path"):
            app["submitted_resume_path"] = payload.get("submitted_resume_path")
    elif status == "needs_manual":
        app["approval_status"] = "approved"
        app["manual_action_required"] = True
        app["manual_action_reason"] = blocker or reason or "Manual application follow-up required."
        app["manual_action_at"] = now
    elif status in {"rejected", "archived"}:
        app["approval_status"] = "archived"
        app["manual_action_required"] = False
    else:
        app["approval_status"] = "approved"
        app["manual_action_required"] = False

    append_note(app, reason)
    append_note(app, blocker)
    return {"previous_status": previous_status, "status": status}


def update_job(job: dict | None, payload: dict, now: str) -> None:
    if not job:
        return
    status = payload["status"]
    job["updated_at"] = now
    if status == "applied":
        job["status"] = "applied"
        job["approval_status"] = "applied"
    elif status == "needs_manual":
        job["status"] = "needs_manual"
        job["approval_status"] = "approved"
    elif status in {"rejected", "archived"}:
        job["status"] = "archived"
        job["approval_status"] = "archived"
    else:
        job["status"] = status
        job["approval_status"] = "approved"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("status_update", type=Path, help="application status JSON exported from an issue")
    args = parser.parse_args()

    payload = load_payload(args.status_update)
    now = utc_now()
    data_apps = load_applications()
    data_jobs = load_jobs()
    applications = data_apps.get("applications", [])
    jobs = data_jobs.get("jobs", [])
    by_app_id = {app.get("application_id"): app for app in applications if app.get("application_id")}
    by_job_id = {job.get("job_id"): job for job in jobs if job.get("job_id")}

    application_id = payload["application_id"]
    app = by_app_id.get(application_id)
    if not app:
        raise SystemExit(f"application_not_found: {application_id}")

    result = update_application(app, payload, now)
    update_job(by_job_id.get(app.get("job_id") or payload.get("job_id")), payload, now)

    append_ledger({
        "event": "application_status_updated",
        "application_update_id": payload.get("update_id"),
        "application_id": application_id,
        "job_id": app.get("job_id") or payload.get("job_id"),
        "company": app.get("company"),
        "role": app.get("role"),
        "previous_status": result["previous_status"],
        "status": result["status"],
        "reason": payload.get("reason") or "",
        "blocker": payload.get("blocker") or "",
    })

    data_apps["applications"] = applications
    data_jobs["jobs"] = jobs
    save_applications(data_apps)
    save_jobs(data_jobs)

    print(json.dumps({
        "updated": 1,
        "application_id": application_id,
        "status": payload["status"],
        "previous_status": result["previous_status"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
