# Jobs

`index.html` is the GitHub Pages tracker at `/jobs/`.

`index.json` is the deduplicated job inventory. Jobs may be discovered by MCP
tools or imported manually. Do not remove processed jobs; mark their status
instead.

The public dashboard is read-only. Its multiselect approval button copies an
`approval-batch.v1` JSON payload. Paste that payload into the recruiting
approval GitHub Discussion; `.github/workflows/sync-approval-discussion.yml`
polls that Discussion and imports unseen batches into application records and
resume snapshots.

The workflow is inert until the repository variable
`APPROVAL_DISCUSSION_NUMBER` is set to the approval Discussion number. To import
an approval batch manually instead:

```bash
python3 recruiting/scripts/import_approvals.py approval-batch.json
```
