# Example — `node-docx` resume, phone-editable

Working example of a `node-docx` builder producing an ATS-friendly
resume (Workday-passing) as both `.docx` and `.pdf` from a
Markdown-driven pipeline. **You can edit this end-to-end from the
GitHub mobile app.**

## Files

| File | Purpose |
| --- | --- |
| `.docmeta.yml` | Tells docsforge to build this folder as `node-docx` |
| **`content.md`** | **What the resume says.** Plain Markdown, phone-friendly. Edit this. |
| `generate.cjs` | Layout engine. Parses `content.md` into a Word-compatible XML tree via the [`docx`](https://www.npmjs.com/package/docx) library. Owns font, size, margins, ATS structure — not the words. |
| `docx_to_pdf.py` | Reads the generated docx and renders a matching one-page PDF via `python-docx` + `reportlab`. Text is selectable (ATS-safe). |
| `package.json` | Node deps for `generate.cjs` (one dep: `docx`) |
| `Uday_Ojha_Resume.docx` / `.pdf` | Last committed outputs |

## Editing (from a phone or a laptop)

**Only ever edit `content.md`.** The Markdown schema is documented in
an HTML comment at the top of the file. Common edits:

- **Add a bullet** — drop a new `-` line under a role.
- **Rename a section** — change the `## Section Name` heading.
- **Add a role** — add a new `### Title — Org · Date` header block,
  then its bullets underneath.
- **Update contact** — the pipe-separated line under `# NAME`.
- **Bold text inline** — wrap with `**double asterisks**`.

Never touch `generate.cjs` to change what's *on* the resume. Only
touch it if you want to change *how* the resume looks (fonts, colours,
margins, section rule).

## Build locally

```bash
npm install
node generate.cjs             # reads content.md → emits Uday_Ojha_Resume.docx
python3 -m pip install --user python-docx reportlab
python3 docx_to_pdf.py        # emits Uday_Ojha_Resume.pdf
```

Or push and let docsforge do it in ~30 seconds on a fresh runner.

## Copy this example for your own resume

```bash
# From a laptop, once:
cp -r examples/resume-node-docx/ ../my-resume/
# Edit content.md with your details (name, contact, sections).
# Commit and push. docsforge rebuilds automatically on every push
# thereafter, so future edits happen entirely on your phone.
```

Change the `output_name` in `.docmeta.yml` if you want the outputs
named something other than `Uday_Ojha_Resume_Example`.

## Why Markdown + `docx`?

Two problems, solved together:

- **ATS parsers** (Workday, Greenhouse, Lever, iCIMS) handle real
  `.docx` structure more reliably than PDF. Real `<w:numPr>` bullets,
  real headings, real paragraphs — no tables, no headers/footers, no
  icons. The `docx` npm library emits exactly that XML.
- **Phone editing** requires a source format that survives touchscreen
  typos. Markdown does; raw docx-building JavaScript does not (missing
  commas silently break the build).

The parser in `generate.cjs` is intentionally strict — an unknown
line shape throws with a line number so you can fix it. Fail-loud
beats silent malformed output.

See the [main README](../../README.md) for the design rationale, and
[docs/BUILDERS.md](../../docs/BUILDERS.md) for the runtime contract of
the `node-docx` builder type.
