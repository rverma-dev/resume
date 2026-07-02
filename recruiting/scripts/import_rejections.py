#!/usr/bin/env python3
"""Import a dashboard rejection batch and archive rejected job records."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pipeline_common import append_ledger, load_jobs, save_jobs, utc_now


def load_payload(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if payload.get("schema_version") != "rejection.batch.v1":
        raise SystemExit("Expected schema_version=rejection.batch.v1.")
    if payload.get("action") != "reject_for_now":
        raise SystemExit("Expected action=reject_for_now.")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rejection_batch", type=Path, help="rejection-batch JSON exported from jobs dashboard")
    args = parser.parse_args()

    payload = load_payload(args.rejection_batch)
    now = utc_now()
    data_jobs = load_jobs()
    jobs = data_jobs.get("jobs", [])
    selected_ids = set(payload.get("job_ids") or [])
    by_job_id = {job.get("job_id"): job for job in jobs if job.get("job_id")}

    rejected = []
    skipped = []

    for job_id in sorted(selected_ids):
        job = by_job_id.get(job_id)
        if not job:
            skipped.append({"job_id": job_id, "reason": "job_not_found"})
            continue
        if job.get("application_id") or job.get("approval_status") in {"approved", "applied"}:
            skipped.append({"job_id": job_id, "reason": "already_approved_or_applied"})
            continue

        job["status"] = "archived"
        job["approval_status"] = "blocked"
        job["updated_at"] = now
        notes = job.setdefault("notes", [])
        reason = payload.get("reason") or "Rejected from dashboard issue loop."
        if reason not in notes:
            notes.append(reason)
        rejected.append(job)

        append_ledger({
            "event": "job_rejected",
            "rejection_batch_id": payload.get("batch_id"),
            "job_id": job_id,
            "company": job.get("company"),
            "role": job.get("role"),
            "reason": reason,
        })

    data_jobs["jobs"] = jobs
    save_jobs(data_jobs)

    print(json.dumps({
        "rejected": len(rejected),
        "skipped": skipped,
        "job_ids": [job.get("job_id") for job in rejected],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
