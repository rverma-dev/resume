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

1. Discover jobs from configured MCP/browser sources, or import them manually
   into `jobs/index.json`.
2. Score each job against the rubric in `recruiting/config.json`.
3. Match the company against `network.txt` and `avoid.txt`.
4. Generate company-specific artifacts under `companies/<company-slug>/`.
5. Generate an ATS-friendly PDF from the company resume.
6. Apply only when external tooling is available and the run is authorized.
7. Update `applications/applications.json` and
   `applications/applications.jsonl`.
8. Refresh the dashboard at `applications/index.html`.

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
