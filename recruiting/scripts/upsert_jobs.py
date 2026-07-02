#!/usr/bin/env python3
"""Merge discovered jobs into jobs/index.json with deterministic dedupe."""

from __future__ import annotations

import argparse
import json
import sys

from pipeline_common import append_ledger, load_jobs, merge_job, normalize_job, save_jobs, short_hash, utc_now


def read_payload(path: str | None):
    if path and path != "-":
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    return json.load(sys.stdin)


def payload_jobs(payload):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        return payload.get("jobs") or payload.get("candidates") or []
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", default="-", help="JSON file containing jobs, or '-' for stdin")
    parser.add_argument("--batch-id", help="Batch id to assign when incoming jobs omit one")
    parser.add_argument("--limit", type=int, default=10, help="Maximum incoming jobs to import")
    args = parser.parse_args()

    payload = read_payload(args.input)
    candidates = payload_jobs(payload)
    if not isinstance(candidates, list):
        raise SystemExit("Expected a JSON list or an object with a jobs array.")

    now = utc_now()
    payload_batch_id = payload.get("batch_id") if isinstance(payload, dict) else None
    batch_seed = json.dumps(candidates[: args.limit], sort_keys=True, default=str)
    batch_id = args.batch_id or payload_batch_id or f"batch-{now[:10].replace('-', '')}-{short_hash(batch_seed, 8)}"

    data = load_jobs()
    existing_jobs = data.get("jobs", [])
    by_job_id = {job.get("job_id"): index for index, job in enumerate(existing_jobs) if job.get("job_id")}
    by_dedupe = {job.get("dedupe_key"): index for index, job in enumerate(existing_jobs) if job.get("dedupe_key")}

    inserted = 0
    updated = 0
    skipped = 0

    for candidate in candidates[: args.limit]:
        if not isinstance(candidate, dict):
            skipped += 1
            continue
        normalized = normalize_job(candidate, batch_id, now)
        index = by_job_id.get(normalized["job_id"])
        if index is None:
            index = by_dedupe.get(normalized["dedupe_key"])

        if index is None:
            existing_jobs.append(normalized)
            new_index = len(existing_jobs) - 1
            by_job_id[normalized["job_id"]] = new_index
            by_dedupe[normalized["dedupe_key"]] = new_index
            inserted += 1
            append_ledger({
                "event": "job_discovered",
                "batch_id": batch_id,
                "job_id": normalized["job_id"],
                "dedupe_key": normalized["dedupe_key"],
                "company": normalized["company"],
                "role": normalized["role"],
                "fit_score": normalized["fit_score"],
            })
        else:
            existing_jobs[index] = merge_job(existing_jobs[index], normalized, now)
            updated += 1
            append_ledger({
                "event": "job_updated",
                "batch_id": batch_id,
                "job_id": existing_jobs[index].get("job_id"),
                "dedupe_key": existing_jobs[index].get("dedupe_key"),
                "company": existing_jobs[index].get("company"),
                "role": existing_jobs[index].get("role"),
            })

    data["active_batch_id"] = batch_id
    data["last_scheduler_run_at"] = now
    data["jobs_per_scheduler_run"] = args.limit
    data["jobs"] = existing_jobs
    save_jobs(data)

    print(json.dumps({
        "batch_id": batch_id,
        "inserted": inserted,
        "updated": updated,
        "skipped": skipped,
        "jobs_total": len(existing_jobs),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
