# docsforge

<p align="center">
  <img src="https://img.shields.io/badge/status-active-brightgreen" alt="Status"/>
  <img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT"/>
  <img src="https://img.shields.io/badge/deps-none-lightgrey" alt="No dependencies"/>
</p>

> **Auto-build every document in your repo.** Drop a `.docmeta.yml` next to
> your `main.tex`, `generate.cjs`, or `paper.md`, add one line to a workflow,
> and every push produces fresh PDFs (and .docx where applicable) attached
> to a rolling GitHub Release.

**No local install. No LaTeX on your laptop. Edit in the browser, download
from Releases.** Works for one doc or twenty. Add new docs by adding one
file.

---

## Why?

Every serious document — a thesis, a resume, a whitepaper, a project
report — deserves the same treatment good code gets: version-controlled
source, reproducible builds, and a stable download URL that never rots.
docsforge is the smallest useful pipeline that gives you that:

- **Edit from anywhere** — github.com's browser editor works on a phone.
- **One rolling `latest` release** — bookmarks never break; recruiters get
  a stable URL.
- **Polyglot** — LaTeX, Word/`.docx` via [`docx`](https://www.npmjs.com/package/docx),
  or Markdown via [`pandoc`](https://pandoc.org). Mix them in one repo.
- **Zero YAML boilerplate per doc.** Discovery scans for `.docmeta.yml`
  and builds every doc it finds, in parallel.
- **Rerun anytime** — every workflow has a manual `workflow_dispatch`
  trigger.

---

## Quick start (60 seconds)

**Step 1.** In your repo, add a workflow at `.github/workflows/build.yml`:

```yaml
name: Build docs
on:
  push: { branches: [main] }
  workflow_dispatch:
permissions:
  contents: write
jobs:
  build:
    uses: OJ-Uday/docsforge/.github/workflows/build-docs.yml@main
```

**Step 2.** Next to each document, add a tiny `.docmeta.yml`:

```yaml
# thesis/.docmeta.yml
type: latex           # latex | node-docx | markdown-pandoc
entry: main.tex       # path relative to this file
output_name: My_Thesis
needs_bibtex: true    # LaTeX only
```

**Step 3.** Push. That's it. Your PDFs appear at:

```
https://github.com/<you>/<repo>/releases/latest
```

Named exactly what you put in `output_name`.

---

## Supported doc types

| Type | Source language | Outputs | Runtime |
| --- | --- | --- | --- |
| **`latex`** | `.tex` files (+ optional `bibtex`) | `<output_name>.pdf` | TeX Live (full) via [`xu-cheng/latex-action`](https://github.com/xu-cheng/latex-action) |
| **`node-docx`** | Node.js script using the [`docx`](https://www.npmjs.com/package/docx) library | `<output_name>.docx`, `<output_name>.pdf` (if `docx_to_pdf.py` sibling exists) | Node 20 + Python 3.11 |
| **`markdown-pandoc`** | Any pandoc-flavoured Markdown | `<output_name>.pdf` | pandoc + xelatex |

Each doc's builder runs in its own parallel job. Two docs = two concurrent
jobs. Fail-fast is off — one broken doc doesn't stop the others.

More builders (typst, asciidoctor, quarto…) are easy to add — see
[`docs/BUILDERS.md`](docs/BUILDERS.md).

---

## Full `.docmeta.yml` schema

```yaml
# Required
type: latex | node-docx | markdown-pandoc
entry: <path relative to this file>

# Optional
output_name: <string>          # default: name of this folder
needs_bibtex: true | false     # latex only; default false
```

See [`docs/DOCMETA.md`](docs/DOCMETA.md) for the full schema and the
default behaviour of every field.

---

## Consumer workflow inputs

The reusable workflow accepts a few knobs:

```yaml
jobs:
  build:
    uses: OJ-Uday/docsforge/.github/workflows/build-docs.yml@main
    with:
      release_tag: latest              # default
      release_name: "Latest build"     # default
      commit_previews: true            # default; auto-commit PNG previews
      artifact_retention_days: 30      # default
```

---

## Example

See [`examples/resume-node-docx/`](examples/resume-node-docx/) for a fully
working `.docx`+`.pdf` resume built with the `docx` library, complete with
a Workday-passing ATS layout. Uses `type: node-docx`.

---

## Design notes

- **Reusable workflow, not composite action.** A reusable workflow gets its
  own runner, its own permission scopes, and its own concurrency group.
  Cleaner isolation than piling steps onto the caller's job.
- **Discovery via `.docmeta.yml`**, not workflow inputs. Add a new doc by
  adding one file, not by editing YAML wiring.
- **One rolling release**, not one per commit. Bookmarks don't rot;
  recruiters get a stable link. If you want per-commit versioned releases,
  fork and tweak.
- **No dependencies on your part.** The workflow installs everything it
  needs on the runner. Your repo doesn't need to check in a `Dockerfile`
  or a `flake.nix`.
- **Fail-open discovery.** A malformed `.docmeta.yml` emits a warning and
  is skipped; other docs still build.

---

## Contributing

PRs welcome. To add a new builder type:

1. Add a `matrix.type == '<yours>'` branch in
   `.github/workflows/build-docs.yml`.
2. Document its expected `.docmeta.yml` shape in `docs/DOCMETA.md`.
3. Ideally add a working example under `examples/`.

Please don't add builders that require secrets to install — this workflow
runs with `contents: write` and nothing else on purpose.

---

## Licence

MIT. See [`LICENSE`](LICENSE).

Built by [@OJ-Uday](https://github.com/OJ-Uday). Not affiliated with
GitHub, Anthropic, Overleaf, or any of the tools this workflow orchestrates.
