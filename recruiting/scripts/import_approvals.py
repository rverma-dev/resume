#!/usr/bin/env python3
"""Import a dashboard approval batch and create application records."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from pipeline_common import (
    BASE_RESUME_PATH,
    REPO_ROOT,
    RESUME_SNAPSHOT_ROOT,
    append_ledger,
    clean_text,
    load_applications,
    load_jobs,
    repo_relative,
    save_applications,
    save_jobs,
    short_hash,
    slugify,
    utc_now,
)


def load_payload(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if payload.get("schema_version") != "approval.batch.v1":
        raise SystemExit("Expected schema_version=approval.batch.v1.")
    return payload


def make_application_id(job: dict, now: str) -> str:
    company = slugify(job.get("company") or "company", "company", 28)
    role = slugify(job.get("role") or job.get("title") or "role", "role", 36)
    seed = job.get("dedupe_key") or job.get("job_id") or f"{company}-{role}"
    return f"app-{now[:10].replace('-', '')}-{company}-{role}-{short_hash(seed, 8)}"


def write_theme(path: Path, job: dict, application_id: str, now: str) -> None:
    theme = job.get("resume_theme") or {}
    pointers = theme.get("key_pointers") or []
    evidence_refs = theme.get("evidence_refs") or []
    people = job.get("people") or []
    lines = [
        f"# Resume Theme: {clean_text(job.get('company'))} - {clean_text(job.get('role'))}",
        "",
        f"- Application ID: `{application_id}`",
        f"- Job ID: `{clean_text(job.get('job_id'))}`",
        f"- Source: {clean_text(job.get('source'))} {clean_text(job.get('source_url'))}",
        f"- Approved at: {now}",
        f"- Fit score: {job.get('fit_score') if job.get('fit_score') is not None else ''}",
        "",
        "## Positioning",
        "",
        clean_text(theme.get("positioning")) or clean_text(job.get("fit_reason")) or "TBD during tailoring.",
        "",
        "## Key Pointers",
        "",
    ]
    lines.extend([f"- {pointer}" for pointer in pointers] or ["- TBD during tailoring."])
    lines.extend(["", "## Evidence References", ""])
    lines.extend([f"- {ref}" for ref in evidence_refs] or ["- Must be backed by `resume/base_resume.md` or `work/` evidence before use."])
    lines.extend(["", "## People / Connections", ""])
    if people:
        for person in people:
            name = clean_text(person.get("name"))
            role = clean_text(person.get("role"))
            relationship = clean_text(person.get("relationship"))
            lines.append(f"- {name}{f' - {role}' if role else ''}{f' ({relationship})' if relationship else ''}")
    else:
        lines.append("- No connection signal captured yet.")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("approval_batch", type=Path, help="approval-batch JSON exported from jobs dashboard")
    args = parser.parse_args()

    payload = load_payload(args.approval_batch)
    now = utc_now()
    data_jobs = load_jobs()
    data_apps = load_applications()
    jobs = data_jobs.get("jobs", [])
    applications = data_apps.get("applications", [])

    selected_ids = set(payload.get("job_ids") or [])
    selected_jobs_from_payload = {job.get("job_id"): job for job in payload.get("jobs", []) if isinstance(job, dict)}
    by_job_id = {job.get("job_id"): job for job in jobs if job.get("job_id")}
    existing_app_by_job = {app.get("job_id"): app for app in applications if app.get("job_id")}

    created = []
    skipped = []

    for job_id in sorted(selected_ids):
        job = by_job_id.get(job_id) or selected_jobs_from_payload.get(job_id)
        if not job:
            skipped.append({"job_id": job_id, "reason": "job_not_found"})
            continue
        if job_id in existing_app_by_job:
            skipped.append({"job_id": job_id, "reason": "application_already_exists", "application_id": existing_app_by_job[job_id].get("application_id")})
            continue

        application_id = make_application_id(job, now)
        snapshot_dir = RESUME_SNAPSHOT_ROOT / application_id
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        resume_snapshot_path = snapshot_dir / "resume.md"
        theme_path = snapshot_dir / "theme.md"
        shutil.copyfile(BASE_RESUME_PATH, resume_snapshot_path)
        write_theme(theme_path, job, application_id, now)

        application = {
            "application_id": application_id,
            "job_id": job_id,
            "dedupe_key": job.get("dedupe_key"),
            "source": job.get("source"),
            "source_job_id": job.get("source_job_id"),
            "source_url": job.get("source_url"),
            "company": job.get("company"),
            "role": job.get("role"),
            "location": job.get("location"),
            "status": "approved",
            "approval_status": "approved",
            "approval_batch_id": payload.get("batch_id"),
            "approved_at": now,
            "updated_at": now,
            "applied_at": None,
            "applied_date": None,
            "fit_score": job.get("fit_score"),
            "fit_reason": job.get("fit_reason"),
            "people": job.get("people") or [],
            "connections_summary": job.get("connections_summary"),
            "resume_theme": job.get("resume_theme") or {},
            "resume_snapshot_path": repo_relative(resume_snapshot_path),
            "resume_theme_path": repo_relative(theme_path),
            "submitted_resume_path": None,
            "notes": ["Approved for tailoring; no application submitted by this script."],
        }
        applications.append(application)
        existing_app_by_job[job_id] = application
        created.append(application)

        if job_id in by_job_id:
            by_job_id[job_id]["status"] = "approved"
            by_job_id[job_id]["approval_status"] = "approved"
            by_job_id[job_id]["application_id"] = application_id
            by_job_id[job_id]["resume_snapshot_path"] = repo_relative(resume_snapshot_path)
            by_job_id[job_id]["updated_at"] = now

        append_ledger({
            "event": "application_approved",
            "approval_batch_id": payload.get("batch_id"),
            "application_id": application_id,
            "job_id": job_id,
            "company": application.get("company"),
            "role": application.get("role"),
            "resume_snapshot_path": application.get("resume_snapshot_path"),
            "resume_theme_path": application.get("resume_theme_path"),
        })

    data_jobs["jobs"] = jobs
    data_apps["applications"] = applications
    save_jobs(data_jobs)
    save_applications(data_apps)

    print(json.dumps({
        "created": len(created),
        "skipped": skipped,
        "application_ids": [app["application_id"] for app in created],
        "repo": str(REPO_ROOT),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
