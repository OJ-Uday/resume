# Uday Ojha — Resume

Programmatically-generated, ATS-friendly resume. One page. Zero tables. Real text. Same source → identical `.docx` + `.pdf`.

**Latest build:** [`Uday_Ojha_Resume.pdf`](Uday_Ojha_Resume.pdf) · [`Uday_Ojha_Resume.docx`](Uday_Ojha_Resume.docx)

---

## Why not just edit a Word doc

Because Word docs quietly rot. Every drag-drop reflow, every "convert to PDF" nudges the layout, and the ATS parsers that most companies run mid-application are picky about the exact XML the docx tree emits. Storing the resume as a **script** solves three real problems at once:

- **Reproducibility.** `node generate.cjs` produces byte-similar output every time. The Git history shows what changed and when — no "which version of this file is on my laptop" panic before an application deadline.
- **ATS compatibility.** Most ATS parsers (Workday, Greenhouse, Lever, iCIMS) fail badly on tables, columns, headers/footers, and text boxes. The generator here uses only real paragraphs, real `w:numPr` bullets, and centered runs in the body — all shapes those parsers handle correctly. No tables. No headers/footers.
- **Diffing is a superpower.** Reviewing "should I add this bullet?" is one commit-diff away. Editing three phrases in one session doesn't require finding them by scrolling; it's `sed`-able if you want.

The output pair (`.docx` + `.pdf`) is committed alongside the source, so anyone can download either directly without running the generator.

---

## Files

| File | Purpose |
|---|---|
| `generate.cjs` | Source of truth. Node script using the [`docx`](https://www.npmjs.com/package/docx) library to emit `Uday_Ojha_Resume.docx`. |
| `docx_to_pdf.py` | Reads the generated docx and renders a matching one-page PDF via `python-docx` + `reportlab`. Text is selectable (ATS-friendly). |
| `Uday_Ojha_Resume.docx` | Committed output — send this to any ATS that asks for Word. |
| `Uday_Ojha_Resume.pdf`  | Committed output — send this to humans and to systems that prefer PDF. |
| `package.json` / `package-lock.json` | Node deps for the docx generator. |

---

## Editing

Everything lives in `generate.cjs`. The file is short (~180 lines) and readable — sections are labelled with `// ── section ───` comment banners. The most common edits:

- **Add / change a bullet in Experience or Projects** — find the `bullet([{ text: "..." }])` call in the right section and edit the string. Multiple runs (mixed bold + regular) look like:
  ```js
  bullet([
    { text: "vetlock", bold: true },
    { text: " — behavioral diff for npm updates. 17 detectors …" },
  ])
  ```
- **Add a new role** — copy an existing `roleLine(...)` + one or more `bullet(...)` pair. `roleLine` takes `(title, org, date)`. The date is right-aligned via a tab stop; parsers see it as one paragraph.
- **Rename or reorder a section** — the `sectionHeading("...")` calls define the labels. Order = source order.
- **Adjust density if things spill to page 2** — reduce a bullet's word count, or trim the summary. Font sizes / margins are constants at the top of `generate.cjs` (`BODY`, `SMALL`) but nudging them is a big commitment — prefer trimming content.

---

## Regenerating

Once. Every time. Both artifacts. Commit them.

```bash
# Node deps for the docx generator (~5 MB, one-time)
npm install

# Regenerate the .docx
node generate.cjs
# → written 12156 bytes

# Convert to PDF (needs python-docx + reportlab)
python3 -m pip install --user python-docx reportlab
python3 docx_to_pdf.py
# → wrote Uday_Ojha_Resume.pdf (15976 bytes)

# Commit both — always as a pair, they must not drift
git add Uday_Ojha_Resume.docx Uday_Ojha_Resume.pdf generate.cjs
git commit -m "resume: <what changed and why>"
```

For the fastidious: MS Word's own "Save as PDF" produces slightly nicer typography than reportlab, but the ATS parsing is identical. Use whichever you prefer — the generator only owns the `.docx`.

---

## ATS notes

Actively avoided (each is a real failure mode for real parsers):

- ✅ **No tables.** Workday and iCIMS routinely mangle column-based layouts.
- ✅ **No headers/footers.** Workday's Illinois parsing engine (and its clones) strip Word's real `<w:hdr>` / `<w:ftr>` XML entirely — the name goes into the void. This resume's header is a normal centered paragraph in the body.
- ✅ **No text boxes / floating shapes.** Same problem, worse.
- ✅ **No icons.** Fine for humans, invisible to ATS.
- ✅ **Real `w:numPr` bullets, not Unicode "•" glyphs prefixing a paragraph.** Parsers understand the former as a list; the latter as an odd character.
- ✅ **Standard section names** — `Summary`, `Technical Skills`, `Experience`, `Projects`, `Education`. Every parser has these in its taxonomy.
- ✅ **Dates in a stable format** (`Jan 2026 – Jul 2026`). Some parsers stumble on `Jan '26–Jul '26`.
- ✅ **Contact info in plain text** — email, phone, links. No mailto: shortcuts that render only as underline in the docx tree.
- ✅ **PDF text is selectable** — Cmd-A / Cmd-C on the PDF gives you the resume as text. If you can't select, an ATS OCR pass will misread half the words.

---

## Sanity check before you send

```bash
# 1. Open the PDF. Read it top to bottom.
open Uday_Ojha_Resume.pdf

# 2. Cmd-A, Cmd-C from the PDF, then paste into a plain-text editor.
#    That's roughly what an ATS sees. Look for missing bullets, wrong dates,
#    swapped column order.

# 3. Upload to a free ATS scorer (e.g. Jobscan, Resume Worded) and read the
#    parsed-fields view — is it grouping bullets under the right role?
```

---

## License

Public domain equivalent — the content is my personal history. Do whatever with the code (`generate.cjs`, `docx_to_pdf.py`); if this template is useful to you, fork it.
