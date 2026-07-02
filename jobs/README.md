# Jobs

`index.html` is the GitHub Pages tracker at `/jobs/`.

`index.json` is the deduplicated job inventory. Jobs may be discovered by MCP
tools or imported manually. Do not remove processed jobs; mark their status
instead.

The public dashboard is read-only. Its multiselect approval button opens a
prefilled GitHub Issue containing an `approval-batch.v1` JSON payload. Submit
that issue to queue approval; `.github/workflows/sync-approval-issues.yml`
polls open issues for approval payloads, imports unseen batches into
application records and resume snapshots, comments, labels the issue
`approval-imported`, and closes it. The issue composer pre-populates
`recruiting-approval` and `approval-pending` labels when GitHub accepts them,
but the importer does not require those labels.

To import an approval batch manually instead:

```bash
python3 recruiting/scripts/import_approvals.py approval-batch.json
```
