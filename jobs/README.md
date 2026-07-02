# Jobs

`index.html` is the GitHub Pages tracker at `/jobs/`.

`index.json` is the deduplicated job inventory. Jobs may be discovered by MCP
tools or imported manually. Do not remove processed jobs; mark their status
instead.

The public dashboard is read-only. Its multiselect approval button downloads an
`approval-batch.v1` JSON file; import that file locally to create application
records and resume snapshots:

```bash
python3 recruiting/scripts/import_approvals.py ~/Downloads/approval-batch.json
```
