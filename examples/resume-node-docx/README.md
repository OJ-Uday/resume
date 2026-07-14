# Example — `node-docx` resume

Working example of a `node-docx` builder producing an ATS-friendly
resume (Workday-passing) as both `.docx` and `.pdf` from one Node script.

## Files

| File | Purpose |
| --- | --- |
| `.docmeta.yml` | Tells docsforge to build this folder as `node-docx` |
| `generate.cjs` | Source of truth. Emits `Uday_Ojha_Resume_Example.docx` |
| `docx_to_pdf.py` | Reads the docx and renders a matching one-page PDF |
| `package.json` / `package-lock.json` | Node deps for the docx generator |
| `Uday_Ojha_Resume.docx` / `.pdf` | Last committed outputs |

## Build locally

```bash
npm install
node generate.cjs             # emits Uday_Ojha_Resume.docx
python3 -m pip install --user python-docx reportlab
python3 docx_to_pdf.py        # emits Uday_Ojha_Resume.pdf
```

Or push the repo and let docsforge do it.

## Copy this example for your own resume

```bash
cp -r examples/resume-node-docx/ ../my-resume/
# edit generate.cjs (the top of the file names, sections, bullets)
# commit and push — docsforge rebuilds automatically
```

## Why `node-docx`?

Because Workday, iCIMS, Greenhouse, Lever, and every other ATS parser
handles `.docx` more reliably than PDF. Same source produces both, so
you send the parser what it wants and the human what looks nice. See
the [main README](../../README.md) for the design rationale, and
[docs/BUILDERS.md](../../docs/BUILDERS.md) for the runtime contract of
this builder type.
