# Builders

Each builder is a `matrix.type == '<name>'` branch in
`.github/workflows/build-docs.yml`. They share a common contract:

1. Run inside the folder holding the `.docmeta.yml`.
2. Produce at least one `.pdf` (and optionally a `.docx`) in that
   folder.
3. Leave everything else on disk alone — the workflow only cares about
   PDFs and DOCX files it finds in the working folder after your build
   step finishes.

Naming: whatever the builder emits gets copied to
`<output_name>.pdf` / `<output_name>.docx` for the release. You do
not have to name your build outputs; the workflow renames them.

## `latex`

**Uses:** [`xu-cheng/latex-action@v3`](https://github.com/xu-cheng/latex-action).

**Runtime:** full TeX Live docker image (packaged by xu-cheng). Every
LaTeX package you have used successfully on Overleaf works here.

**Options honoured:**

- `needs_bibtex: true` — runs `bibtex` after the first pdflatex pass.
  latexmk otherwise. If you use `biber` (not bibtex), open an issue —
  it's a one-line change.
- `entry: <file>.tex` — the root file, relative to `.docmeta.yml`.

**Notes:**

- Compiled with `-pdf -f -interaction=nonstopmode -halt-on-error`.
  Fails fast on any LaTeX error.
- No shell-escape (`-shell-escape` is off). Avoid packages that
  require it, like `minted`.

## `node-docx`

**Runtime:** Node.js 20 + Python 3.11 on ubuntu-latest.

**Contract:**

- Your folder has `package.json` and `package-lock.json`.
- `node <entry>` produces a `.docx` at the same folder.
- Optionally, a `docx_to_pdf.py` script (any signature — the workflow
  just runs it with `python3 docx_to_pdf.py`) produces a matching
  `.pdf`. `python-docx` and `reportlab` are pre-installed for you.

**Why this shape:** the [`docx`](https://www.npmjs.com/package/docx)
npm library lets you emit Word-compatible XML from a script. Word is
still the format many ATS parsers prefer, and PDF from the same source
guarantees identical content.

See [`examples/resume-node-docx/`](../examples/resume-node-docx/) for a
complete working example (a Workday-passing ATS resume).

## `markdown-pandoc`

**Runtime:** ubuntu-latest with `pandoc`, `texlive-xetex`,
`texlive-fonts-recommended`, `texlive-latex-extra`, and `fonts-lmodern`
installed on-the-fly.

**Options honoured:**

- `entry: <file>.md` — the markdown source.

**Notes:**

- xelatex engine, 1-inch margins, Latin Modern Roman font.
- If you want a different template, put a `template.tex` in the folder
  and modify the pandoc invocation — future feature, PRs welcome.

## Adding a new builder type

1. Give it a `matrix.type == '<yours>'` guarded block in
   `.github/workflows/build-docs.yml`. The block must install any
   runtime it needs (don't rely on runner defaults for anything niche).
2. Ensure the outputs land in `${{ matrix.dir }}`.
3. Document its `.docmeta.yml` fields in `docs/DOCMETA.md`.
4. Add an example under `examples/`.
5. Send a PR.

Builders that need secrets (e.g. paid font APIs) are out of scope —
docsforge intentionally runs with `contents: write` only.
