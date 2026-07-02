# Jobs

`index.html` is the GitHub Pages tracker at `/jobs/`.

`index.json` is the deduplicated job inventory. Jobs may be discovered by MCP
tools or imported manually. Do not remove processed jobs; mark their status
instead.

The public dashboard is read-only. Its multiselect buttons open prefilled
GitHub Issues containing either an `approval-batch.v1` or `rejection-batch.v1`
JSON payload. Submit the issue to queue the decision;
`.github/workflows/sync-approval-issues.yml` polls open issues for recruiting
decision payloads.

Approval issues import unseen batches into application records and resume
snapshots, then comment, label the issue `approval-imported`, and close it.
Rejection issues mark jobs `approval_status=blocked` and `status=archived`,
then comment, label the issue `rejection-imported`, and close it. The issue
composer pre-populates labels when GitHub accepts them, but the importer does
not require those labels.

To import an approval batch manually instead:

```bash
python3 recruiting/scripts/import_approvals.py approval-batch.json
```

To import a rejection batch manually instead:

```bash
python3 recruiting/scripts/import_rejections.py rejection-batch.json
```
