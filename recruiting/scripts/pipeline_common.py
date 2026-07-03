#!/usr/bin/env python3
"""Shared helpers for the local recruiting pipeline."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


REPO_ROOT = Path(__file__).resolve().parents[2]
JOBS_PATH = REPO_ROOT / "jobs" / "index.json"
APPLICATIONS_PATH = REPO_ROOT / "applications" / "applications.json"
LEDGER_PATH = REPO_ROOT / "applications" / "applications.jsonl"
BASE_RESUME_PATH = REPO_ROOT / "resume" / "base_resume.md"
RESUME_SNAPSHOT_ROOT = REPO_ROOT / "applications" / "resumes"

TRACKING_PARAMS = {
    "currentJobId",
    "keywords",
    "origin",
    "refId",
    "refresh",
    "sortBy",
    "trackingId",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def short_hash(value: str, length: int = 12) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:length]


def slugify(value: str, fallback: str = "item", max_length: int = 72) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    slug = re.sub(r"-+", "-", slug)
    return (slug or fallback)[:max_length].strip("-") or fallback


def clean_text(value) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def load_json(path: Path, default):
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=False)
        handle.write("\n")


def append_ledger(event: dict) -> None:
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {"schema_version": "applications.ledger.v1", "created_at": utc_now(), **event}
    with LEDGER_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")


def repo_relative(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def canonical_url(value: str) -> str:
    value = clean_text(value)
    if not value:
        return ""
    split = urlsplit(value)
    query = [(key, val) for key, val in parse_qsl(split.query, keep_blank_values=True) if key not in TRACKING_PARAMS and not key.startswith("utm_")]
    clean_query = urlencode(query, doseq=True)
    return urlunsplit((split.scheme.lower(), split.netloc.lower(), split.path.rstrip("/"), clean_query, ""))


def listify(value) -> list:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return value
    return [value]


def normalize_people(value) -> list[dict]:
    people = []
    for person in listify(value):
        if isinstance(person, dict):
            name = clean_text(person.get("name") or person.get("full_name") or person.get("title"))
            if not name and not person.get("profile_url"):
                continue
            people.append({
                "name": name,
                "relationship": clean_text(person.get("relationship") or person.get("connection_degree")),
                "role": clean_text(person.get("role") or person.get("headline")),
                "profile_url": clean_text(person.get("profile_url") or person.get("url")),
                "notes": clean_text(person.get("notes")),
            })
        else:
            name = clean_text(person)
            if name:
                people.append({"name": name, "relationship": "", "role": "", "profile_url": "", "notes": ""})
    return people


def normalize_resume_theme(value) -> dict:
    if isinstance(value, dict):
        return {
            "name": clean_text(value.get("name") or value.get("theme") or value.get("title")),
            "positioning": clean_text(value.get("positioning") or value.get("summary")),
            "key_pointers": [clean_text(item) for item in listify(value.get("key_pointers") or value.get("pointers")) if clean_text(item)],
            "evidence_refs": [clean_text(item) for item in listify(value.get("evidence_refs")) if clean_text(item)],
        }
    text = clean_text(value)
    return {"name": text, "positioning": "", "key_pointers": [], "evidence_refs": []}


def coerce_score(value):
    if value is None or value == "":
        return None
    try:
        return max(0, min(100, int(round(float(value)))))
    except (TypeError, ValueError):
        return None


def source_job_id(candidate: dict) -> str:
    return clean_text(
        candidate.get("linkedin_job_id")
        or candidate.get("source_job_id")
        or candidate.get("external_job_id")
        or candidate.get("job_posting_id")
    )


def make_dedupe_key(candidate: dict) -> str:
    source = clean_text(candidate.get("source") or "manual").lower()
    external_id = source_job_id(candidate)
    if source == "linkedin" and external_id:
        return f"linkedin:{external_id}"
    url = canonical_url(candidate.get("source_url") or candidate.get("url") or candidate.get("job_url"))
    if url:
        return f"url:{url}"
    company = slugify(clean_text(candidate.get("company")), "unknown")
    role = slugify(clean_text(candidate.get("role") or candidate.get("title")), "unknown")
    location = slugify(clean_text(candidate.get("location")), "unknown")
    return f"normalized:{company}|{role}|{location}"


def make_job_id(candidate: dict, dedupe_key: str) -> str:
    existing = clean_text(candidate.get("job_id"))
    if existing:
        return slugify(existing, "job", 96)
    source = clean_text(candidate.get("source") or "manual").lower()
    external_id = source_job_id(candidate)
    if source == "linkedin" and external_id:
        return f"linkedin-{slugify(external_id, 'job', 64)}"
    company = slugify(clean_text(candidate.get("company")), "company", 36)
    role = slugify(clean_text(candidate.get("role") or candidate.get("title")), "role", 36)
    return f"job-{company}-{role}-{short_hash(dedupe_key, 8)}"


def normalize_job(candidate: dict, batch_id: str, now: str) -> dict:
    source = clean_text(candidate.get("source") or "manual").lower() or "manual"
    role = clean_text(candidate.get("role") or candidate.get("title"))
    source_url = canonical_url(candidate.get("source_url") or candidate.get("url") or candidate.get("job_url"))
    dedupe_key = make_dedupe_key({**candidate, "source": source, "role": role, "source_url": source_url})
    job_id = make_job_id({**candidate, "source": source, "role": role}, dedupe_key)

    return {
        "job_id": job_id,
        "dedupe_key": dedupe_key,
        "source": source,
        "source_job_id": source_job_id(candidate),
        "source_url": source_url,
        "company": clean_text(candidate.get("company")),
        "role": role,
        "location": clean_text(candidate.get("location")),
        "work_type": clean_text(candidate.get("work_type")),
        "experience_level": clean_text(candidate.get("experience_level")),
        "compensation_signals": [clean_text(item) for item in listify(candidate.get("compensation_signals") or candidate.get("compensation")) if clean_text(item)],
        "status": clean_text(candidate.get("status") or "discovered"),
        "approval_status": clean_text(candidate.get("approval_status") or "unreviewed"),
        "batch_id": clean_text(candidate.get("batch_id") or batch_id),
        "fit_score": coerce_score(candidate.get("fit_score") if "fit_score" in candidate else candidate.get("score")),
        "fit_reason": clean_text(candidate.get("fit_reason") or candidate.get("score_reason")),
        "fit_signals": [clean_text(item) for item in listify(candidate.get("fit_signals")) if clean_text(item)],
        "risk_flags": [clean_text(item) for item in listify(candidate.get("risk_flags")) if clean_text(item)],
        "people": normalize_people(candidate.get("people") or candidate.get("connections")),
        "connections_summary": clean_text(candidate.get("connections_summary")),
        "resume_theme": normalize_resume_theme(candidate.get("resume_theme")),
        "application_id": clean_text(candidate.get("application_id")) or None,
        "resume_snapshot_path": clean_text(candidate.get("resume_snapshot_path")) or None,
        "discovered_at": clean_text(candidate.get("discovered_at") or now),
        "updated_at": now,
        "notes": [clean_text(item) for item in listify(candidate.get("notes")) if clean_text(item)],
    }


def merge_job(existing: dict, incoming: dict, now: str) -> dict:
    merged = dict(existing)
    preserve_if_set = {"job_id", "dedupe_key", "discovered_at", "application_id", "resume_snapshot_path"}
    for key, value in incoming.items():
        if key in preserve_if_set and merged.get(key):
            continue
        if value not in (None, "", []):
            merged[key] = value
    merged["updated_at"] = now
    return merged


def load_jobs() -> dict:
    return load_json(JOBS_PATH, {"schema_version": "jobs.index.v2", "updated_at": None, "jobs": []})


def save_jobs(data: dict) -> None:
    data["schema_version"] = "jobs.index.v2"
    data["updated_at"] = utc_now()
    data["jobs"] = sorted(data.get("jobs", []), key=lambda row: (row.get("batch_id") or "", row.get("fit_score") or -1, row.get("updated_at") or ""), reverse=True)
    save_json(JOBS_PATH, data)


def load_applications() -> dict:
    return load_json(APPLICATIONS_PATH, {"schema_version": "applications.index.v2", "updated_at": None, "applications": []})


def save_applications(data: dict) -> None:
    data["schema_version"] = "applications.index.v2"
    data["approval_required"] = True
    data["allow_auto_apply"] = bool(data.get("allow_auto_apply", False))
    data["updated_at"] = utc_now()
    data["applications"] = sorted(data.get("applications", []), key=lambda row: row.get("approved_at") or row.get("updated_at") or "", reverse=True)
    save_json(APPLICATIONS_PATH, data)
