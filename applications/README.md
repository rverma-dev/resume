# Applications

- `applications.json` powers the local dashboard.
- `applications.jsonl` is the append-only audit ledger.
- `index.html` redirects to the public GitHub Pages tracker at `/jobs/`.
- `resumes/<application-id>/resume.md` is the resume snapshot for an approved
  application and is published as a printable page at
  `/applications/resumes/<application-id>/`.
- `resumes/<application-id>/theme.md` stores the role-specific tailoring notes.

Keep the JSON files deterministic where possible. Append new decisions to the
JSONL ledger instead of rewriting history.

Import a dashboard approval batch locally with:

```bash
python3 recruiting/scripts/import_approvals.py ~/Downloads/approval-batch.json
```
