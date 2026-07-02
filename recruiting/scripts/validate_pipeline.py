#!/usr/bin/env python3
"""Validate recruiting pipeline JSON files and ledger integrity."""

from __future__ import annotations

import json
from pathlib import Path

from pipeline_common import APPLICATIONS_PATH, JOBS_PATH, LEDGER_PATH, REPO_ROOT


def read_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def require_unique(rows: list[dict], field: str, label: str, allow_empty: bool = False) -> list[str]:
    errors = []
    seen = {}
    for row in rows:
        value = row.get(field)
        if not value:
            if not allow_empty:
                errors.append(f"{label} missing {field}: {row}")
            continue
        if value in seen:
            errors.append(f"{label} duplicate {field}: {value}")
        seen[value] = True
    return errors


def validate_jsonl(path: Path) -> list[str]:
    errors = []
    if not path.exists():
        return [f"Missing ledger: {path}"]
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"{path.relative_to(REPO_ROOT)}:{line_number}: {exc}")
    return errors


def main() -> int:
    errors = []
    jobs_data = read_json(JOBS_PATH)
    apps_data = read_json(APPLICATIONS_PATH)
    jobs = jobs_data.get("jobs", [])
    applications = apps_data.get("applications", [])

    errors.extend(require_unique(jobs, "job_id", "jobs"))
    errors.extend(require_unique(jobs, "dedupe_key", "jobs"))
    errors.extend(require_unique(applications, "application_id", "applications"))
    errors.extend(require_unique(applications, "job_id", "applications"))
    errors.extend(validate_jsonl(LEDGER_PATH))

    valid_job_ids = {job.get("job_id") for job in jobs}
    for app in applications:
        if app.get("job_id") not in valid_job_ids:
            errors.append(f"application {app.get('application_id')} references unknown job_id {app.get('job_id')}")
        for field in ("resume_snapshot_path", "submitted_resume_path"):
            value = app.get(field)
            if value and not (REPO_ROOT / value).exists():
                errors.append(f"application {app.get('application_id')} missing {field}: {value}")

    if errors:
        print("\n".join(errors))
        return 1

    print(json.dumps({
        "ok": True,
        "jobs": len(jobs),
        "applications": len(applications),
        "ledger": str(LEDGER_PATH.relative_to(REPO_ROOT)),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
