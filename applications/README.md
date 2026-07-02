# Applications

- `applications.json` powers the local dashboard.
- `applications.jsonl` is the append-only audit ledger.
- `index.html` redirects to the public GitHub Pages tracker at `/jobs/`.

Keep the JSON files deterministic where possible. Append new decisions to the
JSONL ledger instead of rewriting history.
