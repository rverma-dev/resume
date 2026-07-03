# Resume Snapshots

Each approved application gets its own immutable folder here:

```text
applications/resumes/<application-id>/
  resume.md
  theme.md
```

`resume.md` starts as a printable Jekyll page around `resume/base_resume.md` and
is published at `/applications/resumes/<application-id>/`. Keep the title as
`Base Resume` while the snapshot is still the base resume. Update that snapshot
for the target role before applying, then record the final submitted path in
`applications/applications.json`.
