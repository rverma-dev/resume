# Autonomous Recruiting Pipeline

This repository can be used as a local, evidence-backed recruiting pipeline.
The pipeline is intentionally constrained: it may tailor resumes and generate
research packages only from evidence stored in this repository.

## Safety Contract

- Never invent experience, projects, metrics, responsibilities, relationships,
  compensation, visa facts, or technologies.
- Every generated resume claim must be traceable to `resume/base_resume.md` or
  evidence under `work/`.
- Never overwrite `resume/base_resume.md`.
- Never apply to a role unless external application tooling is configured and
  the run is explicitly authorized for applications.
- If a required application answer is not present in repository evidence, pause
  and ask for user input.
- Record every decision in `applications/applications.jsonl`.

## Pipeline

1. Discover up to 10 jobs per scheduled batch from configured MCP/browser
   sources, or import them manually into `jobs/index.json`.
2. Score each job against the rubric in `recruiting/config.json`.
3. Apply the level comparison policy in `recruiting/config.json`: use
   source-backed compensation and level signals, preferably a Levels.fyi
   comparison URL when comparing Salesforce with a target company. Treat title
   mappings as inferred unless the source explicitly supports them, and record
   uncertainty in `risk_flags`. Do not let uncertainty force a downlevel: the
   pipeline is stretch-first, so credible Staff / Principal / Architect roles
   should remain high-priority, while safe below-target roles should be
   penalized unless compensation or company fit is exceptional.
   Apply the compensation research policy before rejecting for pay: Salesforce,
   Amazon, Coupang, and Mastercard are target-capable at the right senior band,
   so sparse or lower public medians should be treated as directional evidence,
   not a compensation ceiling.
4. Apply the location policy in `recruiting/config.json`: do not limit discovery
   to India; prefer India, UAE, global remote open to India/UAE, or relocation
   with sponsorship; avoid US-only roles because the candidate does not have
   H1B; treat UAE as viable because the candidate can self-sponsor.
5. Match the company against `network.txt` and `avoid.txt`.
6. Review the dashboard, multiselect roles, and open a prefilled GitHub
   approval or rejection issue.
7. Submit the decision issue. The issue body carries only selected `job_ids`;
   the scheduled recruiting issue workflow resolves full job details from
   `jobs/index.json`, imports unseen approval batches into application records
   and resume snapshots under `applications/resumes/<application-id>/`, and
   records rejection batches by marking jobs `approval_status=blocked` and
   `status=archived`. The workflow records the processed issue number in
   `applications/approval_inbox.json`, comments, labels the issue
   `approval-imported` or `rejection-imported`, and closes it.
8. Generate company-specific artifacts under `companies/<company-slug>/`.
9. Generate an ATS-friendly PDF from the company resume.
10. Apply only when external tooling is available and the run is authorized.
11. After an actual submission, open or emit an `application.status.v1` issue
   with `status=applied`. If browser/computer-use automation cannot safely
   navigate or submit, open or emit the same schema with `status=needs_manual`
   and a blocker. The scheduler imports that status into
   `applications/applications.json`, `jobs/index.json`, and
   `applications/applications.jsonl`.
12. Refresh the dashboard at `jobs/index.html`.

## Local Commands

Import discovered jobs from a JSON payload:

```bash
python3 recruiting/scripts/upsert_jobs.py discovered-jobs.json --limit 10
```

Import dashboard approvals:

```bash
python3 recruiting/scripts/import_approvals.py approval-batch.json
```

Import dashboard rejections:

```bash
python3 recruiting/scripts/import_rejections.py rejection-batch.json
```

Import recruiting decision batches from GitHub issues:

```bash
GITHUB_TOKEN=... python3 recruiting/scripts/sync_issue_approvals.py
```

Import an application status update:

```bash
python3 recruiting/scripts/import_application_status.py application-status.json
```

Validate the tracker:

```bash
python3 recruiting/scripts/validate_pipeline.py
```

## Expected Company Folder

```text
companies/<company-slug>/
  resume.md
  resume.pdf
  research.md
  application.json
  network.md
  intro.md
  recruiter_message.md
  assets/
```

## Evidence Sources

Use these locations for retrieval:

- `resume/base_resume.md`
- `work/ADRs/`
- `work/RFCs/`
- `work/design_docs/`
- `work/planning/`
- `work/architecture/`
- `work/incident_reviews/`
- `work/project_docs/`
- `work/collaboration/`

Private/internal evidence may be stored locally under `work/private/`; it is
available to local tailoring runs but must not be committed or published.

If a claim cannot be tied to one of those sources, do not use it.
