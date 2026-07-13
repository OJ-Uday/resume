#!/usr/bin/env python3
"""
docx_to_pdf.py — convert Uday_Ojha_Resume.docx → Uday_Ojha_Resume.pdf.

Uses python-docx to read the generated resume, and reportlab to render an
ATS-friendly one-page PDF that mirrors the docx's layout. Every string is
selectable text (no images, no rasterised sections), which is exactly what
ATS parsers want.

This exists because LibreOffice / pandoc aren't installed on this machine and
Microsoft Word's own "Save as PDF" is a manual step. Running this from CI or
a Makefile keeps the two artifacts in lockstep.
"""

from __future__ import annotations
import sys, re
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, black

ACCENT = HexColor("#1F4E79")
BODY_PT = 10
SMALL_PT = 9.5
NAME_PT = 16.5
HEAD_PT = 10.5

# Try to register a real Calibri if the system has it (macOS ships something
# similar); fall back to Helvetica which every reportlab install has.
FONT = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
for path, name in (
    ("/Library/Fonts/Calibri.ttf", "Calibri"),
    ("/System/Library/Fonts/Supplemental/Calibri.ttf", "Calibri"),
    ("/Library/Fonts/Microsoft/Calibri.ttf", "Calibri"),
):
    try:
        if Path(path).exists():
            pdfmetrics.registerFont(TTFont(name, path))
            FONT = name
            # try bold companion
            bold = path.replace(".ttf", " Bold.ttf")
            if Path(bold).exists():
                pdfmetrics.registerFont(TTFont(name + "-Bold", bold))
                FONT_BOLD = name + "-Bold"
            break
    except Exception:
        pass

MARGIN_L = 36
MARGIN_R = 36
MARGIN_T = 28
MARGIN_B = 22


def emu_to_pt(emu: int) -> float:
    """docx uses EMUs (English Metric Units); 914400 per inch, 72pt per inch."""
    return emu / 914400.0 * 72.0


def sizes(run) -> tuple[float, bool, str | None]:
    """Return (size_pt, bold, hyperlink_target)."""
    # size in half-points via w:sz
    size = None
    r = run._element
    rPr = r.find(qn("w:rPr"))
    if rPr is not None:
        sz = rPr.find(qn("w:sz"))
        if sz is not None:
            size = int(sz.get(qn("w:val"))) / 2.0
    bold = run.bold or False
    return (size or BODY_PT), bool(bold), None


# ── extract paragraphs with structure ────────────────────────────────

class Line:
    """One paragraph, flattened."""
    def __init__(self, runs, is_heading=False, is_bullet=False, is_center=False,
                 is_role=False, spacing_after=4):
        self.runs = runs  # list of (text, size_pt, bold, color, link)
        self.is_heading = is_heading
        self.is_bullet = is_bullet
        self.is_center = is_center
        self.is_role = is_role       # role line: title — org [tab] date
        self.spacing_after = spacing_after

    def plain(self) -> str:
        return "".join(r[0] for r in self.runs)


def extract_hyperlink_text(p_elem) -> dict[int, str]:
    """Map w:hyperlink → target URL by id (via document rels)."""
    return {}   # simplified — reportlab draws visible text; if needed we could add link boxes


def parse_paragraph(p) -> Line:
    """Convert a python-docx Paragraph to our Line."""
    # Detect heading by the accent color + bold + allCaps we set in generate.cjs
    # Detect bullet by w:numPr presence
    # Detect role line by tab-stop presence
    p_elem = p._element
    is_bullet = p_elem.find(qn("w:pPr") + "/" + qn("w:numPr")) is not None
    pPr = p_elem.find(qn("w:pPr"))
    tabs = pPr.find(qn("w:tabs")) if pPr is not None else None
    is_role = tabs is not None
    jc = pPr.find(qn("w:jc")) if pPr is not None else None
    is_center = jc is not None and jc.get(qn("w:val")) == "center"

    runs = []
    is_heading = False
    # Walk children: w:r (runs) and w:hyperlink (containing runs)
    def process_run(r_elem, force_link=None):
        # Collect run properties
        rPr = r_elem.find(qn("w:rPr"))
        size = BODY_PT
        color = black
        bold = False
        if rPr is not None:
            sz = rPr.find(qn("w:sz"))
            if sz is not None:
                size = int(sz.get(qn("w:val"))) / 2.0
            b = rPr.find(qn("w:b"))
            if b is not None:
                v = b.get(qn("w:val"))
                bold = v is None or v.lower() in ("1", "true", "on")
            col = rPr.find(qn("w:color"))
            if col is not None:
                cv = col.get(qn("w:val"))
                if cv and cv != "auto":
                    color = HexColor("#" + cv)
            caps = rPr.find(qn("w:caps"))
            if caps is not None:
                # section-heading style
                nonlocal is_heading
                is_heading = True
        # Text (may be multiple <w:t> or <w:tab>)
        text_parts = []
        for child in r_elem:
            if child.tag == qn("w:t"):
                text_parts.append(child.text or "")
            elif child.tag == qn("w:tab"):
                text_parts.append("\t")
        text = "".join(text_parts)
        if not text:
            return
        runs.append((text, size, bold, color, force_link))

    # Iterate top-level children in order (runs + hyperlinks)
    for child in p_elem:
        tag = child.tag
        if tag == qn("w:r"):
            process_run(child)
        elif tag == qn("w:hyperlink"):
            # collect inner runs, mark them as links
            r_id = child.get(qn("r:id"))
            for r in child.findall(qn("w:r")):
                process_run(r, force_link=r_id)

    # spacing
    spacing_after = 4
    if pPr is not None:
        sp = pPr.find(qn("w:spacing"))
        if sp is not None and sp.get(qn("w:after")) is not None:
            spacing_after = int(sp.get(qn("w:after"))) / 20.0  # twips → pt
    if is_heading:
        spacing_after = max(spacing_after, 3)
    return Line(runs, is_heading=is_heading, is_bullet=is_bullet,
                is_center=is_center, is_role=is_role, spacing_after=spacing_after)


def hyperlink_targets(doc: Document) -> dict[str, str]:
    """Map w:hyperlink r:id → URL by inspecting document.part.rels."""
    return {rel.rId: rel.target_ref for rel in doc.part.rels.values() if "hyperlink" in rel.reltype}


# ── render to reportlab canvas ───────────────────────────────────────

def render(lines: list[Line], hlinks: dict[str, str], out_pdf: Path) -> None:
    w, h = LETTER
    c = canvas.Canvas(str(out_pdf), pagesize=LETTER)
    c.setTitle("Uday Ojha — Resume")
    c.setAuthor("Uday Ojha")
    c.setSubject("Software Engineer resume")
    c.setKeywords([
        "software engineer", "typescript", "go", "react", "node.js",
        "clickhouse", "kubernetes", "gitops", "aws", "cybersecurity",
        "reverse engineering", "supply chain security", "sast", "vetlock",
    ])

    y = h - MARGIN_T
    max_width = w - MARGIN_L - MARGIN_R

    def wrap(text: str, font_name: str, size: float, width: float) -> list[str]:
        """Greedy wrap by words. Preserves inner spaces."""
        if not text:
            return [""]
        words = text.split(" ")
        lines_out, cur = [], ""
        for word in words:
            candidate = word if not cur else cur + " " + word
            if pdfmetrics.stringWidth(candidate, font_name, size) <= width:
                cur = candidate
            else:
                if cur:
                    lines_out.append(cur)
                cur = word
        if cur:
            lines_out.append(cur)
        return lines_out or [""]

    def draw_run_stream(x_start, y, runs, width, first_line_indent=0, hanging_indent=0):
        """Draw a sequence of runs with per-run font/color, wrapping across the width."""
        line_height_leading = 1.20   # multiplier — tight but readable
        x = x_start + first_line_indent
        cur_line = []      # (text, font, size, color, link)
        cur_width = 0.0
        base_size = BODY_PT
        for text, size, bold, color, link in runs:
            base_size = size
            font_name = FONT_BOLD if bold else FONT
            # tokenize preserving spaces so we can wrap word-by-word
            tokens = re.split(r'(\s+)', text)
            for tok in tokens:
                if not tok:
                    continue
                tw = pdfmetrics.stringWidth(tok, font_name, size)
                if cur_width + tw > width and cur_line:
                    # flush
                    xx = x
                    for (t, f, s, col, lk) in cur_line:
                        c.setFont(f, s); c.setFillColor(col)
                        c.drawString(xx, y, t)
                        tw2 = pdfmetrics.stringWidth(t, f, s)
                        if lk:
                            c.linkURL(lk, (xx, y - 1, xx + tw2, y + s), relative=0)
                        xx += tw2
                    y -= size * line_height_leading
                    x = x_start + hanging_indent
                    cur_line, cur_width = [], 0.0
                    if tok.isspace():
                        continue
                url = hlinks.get(link) if link else None
                cur_line.append((tok, font_name, size, color, url))
                cur_width += tw
        # flush trailing
        xx = x
        for (t, f, s, col, lk) in cur_line:
            c.setFont(f, s); c.setFillColor(col)
            c.drawString(xx, y, t)
            tw2 = pdfmetrics.stringWidth(t, f, s)
            if lk:
                c.linkURL(lk, (xx, y - 1, xx + tw2, y + s), relative=0)
            xx += tw2
        return y - base_size * line_height_leading

    for line in lines:
        if not line.runs:
            y -= 1   # empty paragraphs shouldn't cost real vertical space
            continue

        if line.is_heading:
            # Section heading with accent underline
            y -= 2  # small breathing room before section (was 4)
            text = line.plain()
            c.setFont(FONT_BOLD, HEAD_PT)
            c.setFillColor(ACCENT)
            c.drawString(MARGIN_L, y, text)
            # underline
            c.setStrokeColor(ACCENT)
            c.setLineWidth(0.6)
            c.line(MARGIN_L, y - 2, w - MARGIN_R, y - 2)
            y -= HEAD_PT * 1.30
            continue

        if line.is_center:
            # Centered header/subheader
            total_w = 0
            for text, size, bold, color, link in line.runs:
                fn = FONT_BOLD if bold else FONT
                total_w += pdfmetrics.stringWidth(text, fn, size)
            x = MARGIN_L + (max_width - total_w) / 2.0
            base_size = line.runs[0][1] if line.runs else BODY_PT
            for text, size, bold, color, link in line.runs:
                fn = FONT_BOLD if bold else FONT
                c.setFont(fn, size); c.setFillColor(color)
                c.drawString(x, y, text)
                tw = pdfmetrics.stringWidth(text, fn, size)
                url = hlinks.get(link) if link else None
                if url:
                    c.linkURL(url, (x, y - 1, x + tw, y + size), relative=0)
                x += tw
            y -= base_size * 1.22
            continue

        if line.is_role:
            # Title — org (left) [tab] date (right). We split on the \t char.
            left_runs = []
            right_runs = []
            saw_tab = False
            for text, size, bold, color, link in line.runs:
                if "\t" in text:
                    parts = text.split("\t")
                    left_runs.append((parts[0], size, bold, color, link))
                    if len(parts) > 1:
                        right_runs.append((parts[1], size, bold, color, link))
                    saw_tab = True
                else:
                    (right_runs if saw_tab else left_runs).append((text, size, bold, color, link))
            # draw left
            x = MARGIN_L
            base_size = BODY_PT
            for text, size, bold, color, link in left_runs:
                base_size = size
                fn = FONT_BOLD if bold else FONT
                c.setFont(fn, size); c.setFillColor(color)
                c.drawString(x, y, text)
                x += pdfmetrics.stringWidth(text, fn, size)
            # draw right aligned
            rx = w - MARGIN_R
            for text, size, bold, color, link in reversed(right_runs):
                fn = FONT_BOLD if bold else FONT
                rx -= pdfmetrics.stringWidth(text, fn, size)
            xx = rx
            for text, size, bold, color, link in right_runs:
                fn = FONT_BOLD if bold else FONT
                c.setFont(fn, size); c.setFillColor(color)
                c.drawString(xx, y, text)
                xx += pdfmetrics.stringWidth(text, fn, size)
            y -= base_size * 1.22
            continue

        if line.is_bullet:
            # Bullet + hanging indent
            bullet_x = MARGIN_L + 10
            text_x = MARGIN_L + 22
            c.setFont(FONT, BODY_PT); c.setFillColor(black)
            c.drawString(bullet_x, y, "•")
            y = draw_run_stream(text_x, y, line.runs, max_width - 22)
            continue

        # plain paragraph
        y = draw_run_stream(MARGIN_L, y, line.runs, max_width)

    c.save()


def main() -> None:
    here = Path(__file__).parent
    docx_path = here / "Uday_Ojha_Resume.docx"
    pdf_path = here / "Uday_Ojha_Resume.pdf"
    if not docx_path.exists():
        print(f"error: {docx_path} not found. run `node generate.cjs` first.", file=sys.stderr)
        sys.exit(1)

    doc = Document(str(docx_path))
    hlinks = hyperlink_targets(doc)
    lines = [parse_paragraph(p) for p in doc.paragraphs]
    render(lines, hlinks, pdf_path)
    print(f"wrote {pdf_path.name} ({pdf_path.stat().st_size} bytes)")
    print(f"font used: {FONT}")


if __name__ == "__main__":
    main()
