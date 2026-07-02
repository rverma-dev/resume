# Applications

- `applications.json` powers the local dashboard.
- `applications.jsonl` is the append-only audit ledger.
- `index.html` is the browser dashboard.

Keep the JSON files deterministic where possible. Append new decisions to the
JSONL ledger instead of rewriting history.
