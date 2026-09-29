"""Export the required Markdown documents to readable PDFs using reportlab."""

from html import escape
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/pdf"
INK = colors.HexColor("#172b43")
BLUE = colors.HexColor("#245e84")


def inline(text):
    """Escape text and translate the supported inline Markdown formatting."""
    text = escape(text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    return re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', text)


def document_styles(wide):
    """Build consistent paragraph styles for portrait and landscape pages."""
    styles = getSampleStyleSheet()
    body_size = 10 if wide else 10.5
    styles.add(
        ParagraphStyle(
            name="Body",
            fontName="Helvetica",
            fontSize=body_size,
            leading=body_size * 1.45,
            textColor=INK,
            spaceAfter=7,
            alignment=TA_LEFT,
            allowWidows=0,
            allowOrphans=0,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Cell", parent=styles["Body"], fontSize=8.5, leading=11.5, spaceAfter=0
        )
    )
    for style_name, size in [("Title", 22), ("Heading1", 16), ("Heading2", 12)]:
        styles[style_name].fontName = "Helvetica-Bold"
        styles[style_name].fontSize = size
        styles[style_name].leading = size * 1.2
        styles[style_name].textColor = BLUE
        styles[style_name].spaceBefore = 10
        styles[style_name].spaceAfter = 8
        styles[style_name].keepWithNext = True
    return styles


def read_table(lines, index):
    """Consume Markdown table rows, excluding the header separator."""
    rows = []
    while index < len(lines) and lines[index].strip().startswith("|"):
        cells = [cell.strip() for cell in lines[index].strip().strip("|").split("|")]
        if not all(re.fullmatch(r":?-+:?", cell) for cell in cells):
            rows.append(cells)
        index += 1
    return rows, index


def make_table(rows, width, cell_style):
    """Lay out a striped table with repeated headers and content-sized columns."""
    weights = [
        max(9, min(max(len(row[col]) for row in rows), 65)) ** 0.7
        for col in range(len(rows[0]))
    ]
    table = Table(
        [[Paragraph(inline(cell), cell_style) for cell in row] for row in rows],
        colWidths=[width * weight / sum(weights) for weight in weights],
        repeatRows=1,
        hAlign="LEFT",
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dfeaf3")),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.white, colors.HexColor("#f5f8fb")],
                ),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LINEBELOW", (0, 0), (-1, 0), 0.7, BLUE),
                ("LINEBELOW", (0, 1), (-1, -1), 0.2, colors.HexColor("#d4dce5")),
            ]
        )
    )
    return table


def read_paragraph(lines, index, style):
    """Join wrapped lines while preserving numbered items and table introductions."""
    paragraph = [lines[index].strip()]
    index += 1
    while (
        index < len(lines)
        and lines[index].strip()
        and not lines[index].lstrip().startswith(("#", "|"))
    ):
        if re.match(r"^\d+\. ", lines[index].strip()):
            break
        paragraph.append(lines[index].strip())
        index += 1
    body = Paragraph(inline(" ".join(paragraph)), style)
    next_line = next((item.strip() for item in lines[index:] if item.strip()), "")
    if next_line.startswith("|"):
        body.keepWithNext = True
    return body, index


def build_story(lines, width, styles, wide):
    """Convert the supported block-level Markdown into reportlab flowables."""
    story = []
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        if line.startswith("|"):
            rows, index = read_table(lines, index)
            story.extend([make_table(rows, width, styles["Cell"]), Spacer(1, 10)])
            continue
        heading = re.match(r"^(#{1,3}) (.*)", line)
        if heading:
            if not wide and heading[2] == "Coverage comparison":
                story.append(PageBreak())
            style = {1: "Title", 2: "Heading1", 3: "Heading2"}[len(heading[1])]
            story.append(Paragraph(inline(heading[2]), styles[style]))
            index += 1
            continue
        body, index = read_paragraph(lines, index, styles["Body"])
        story.append(body)
    return story


def footer(canvas, document):
    """Add the assignment identifier and page number to each exported page."""
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#ccd8e3"))
    canvas.line(42, 32, document.pagesize[0] - 42, 32)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(INK)
    canvas.drawString(42, 20, "SecureBank | Homework 4 | A4ld0")
    canvas.drawRightString(document.pagesize[0] - 42, 20, f"Page {document.page}")
    canvas.restoreState()


def export(source, name, wide=False):
    """Export one Markdown source to the submission PDF directory."""
    page_size = landscape(A4) if wide else A4
    lines = source.read_text(encoding="utf-8").splitlines()
    story = build_story(lines, page_size[0] - 84, document_styles(wide), wide)
    doc = SimpleDocTemplate(
        str(OUT / name),
        pagesize=page_size,
        leftMargin=42,
        rightMargin=42,
        topMargin=32,
        bottomMargin=45,
        title=lines[0].lstrip("# "),
        author="Aldo Ramon Velazquez Fonseca",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUT / name)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    export(
        ROOT / "design/test-design-document.md", "test-design-document.pdf", wide=True
    )
    export(ROOT / "reports/analysis-report.md", "analysis-report.pdf")
