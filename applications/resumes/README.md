# Resume Snapshots

Each approved application gets its own immutable folder here:

```text
applications/resumes/<application-id>/
  resume.md
  theme.md
```

`resume.md` starts as a printable Jekyll page around the selected canonical
resume source and is published at `/applications/resumes/<application-id>/`.
IC roles use `resume/base_resume.md` and are labeled `IC Resume`; management
roles use `_includes/platform-leadership-resume.md` and are labeled
`Director Platform Resume`. Update the snapshot for the target role before
applying, then record the final submitted path in `applications/applications.json`.
