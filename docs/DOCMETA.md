# `.docmeta.yml` schema

Every folder that should be built by docsforge contains one
`.docmeta.yml` file. Discovery is recursive; you can nest doc folders
under a project root as deep as you like.

## Fields

### `type` — required

The builder to run. One of:

- **`latex`** — Runs `latexmk` against a `.tex` entry point using the
  full TeX Live docker image. Optionally runs `bibtex` mid-compile.
- **`node-docx`** — Runs `node <entry>` in the folder to produce a
  `.docx`. If a `docx_to_pdf.py` file exists alongside the entry, it
  is also run to produce a matching `.pdf`.
- **`markdown-pandoc`** — Runs `pandoc <entry> -o <output>.pdf`
  through `xelatex`.

### `entry` — required

Path to the primary source file, **relative to the `.docmeta.yml`**.

Examples:

```yaml
entry: main.tex          # LaTeX at the folder root
entry: generate.cjs      # Node script
entry: paper.md          # Markdown source
```

### `output_name` — optional

Base name of the produced file(s), without extension. If omitted,
defaults to the folder name.

Example: `output_name: Uday_Ojha_Thesis` produces
`Uday_Ojha_Thesis.pdf` on the release page. If the builder also emits
a docx (node-docx type), you get `Uday_Ojha_Thesis.docx` too.

### `needs_bibtex` — LaTeX only

Runs `bibtex <entry-without-extension>` between the first and second
`pdflatex` passes. Set to `true` for any thesis using `natbib` or
`biber`.

**Default:** `false`.

## Full example

```yaml
# thesis/.docmeta.yml
type: latex
entry: main.tex
output_name: Uday_Ojha_Thesis
needs_bibtex: true
```

```yaml
# resume/.docmeta.yml
type: node-docx
entry: generate.cjs
output_name: Uday_Ojha_Resume
```

```yaml
# essays/gitops-post-mortem/.docmeta.yml
type: markdown-pandoc
entry: post.md
output_name: GitOps_Post_Mortem
```
