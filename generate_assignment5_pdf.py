from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).parent
MD_FILE = ROOT / "Assignment_5_Report.md"
PDF_FILE = ROOT / "Assignment_5_Report.pdf"


def build_story(md_text: str):
    styles = getSampleStyleSheet()
    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        spaceAfter=6,
    )
    heading = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#0B2E4F"),
        spaceBefore=8,
        spaceAfter=6,
    )
    title = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0B2E4F"),
    )

    story = []
    for raw in md_text.splitlines():
        line = raw.strip()
        if not line:
            story.append(Spacer(1, 0.2 * cm))
            continue

        if line.startswith("# "):
            story.append(Paragraph(line[2:], title))
            story.append(Spacer(1, 0.2 * cm))
            continue

        if line.startswith("## "):
            story.append(Paragraph(line[3:], heading))
            continue

        if line.startswith("### "):
            story.append(Paragraph(line[4:], heading))
            continue

        if line.startswith("- "):
            story.append(Paragraph(f"&bull; {line[2:]}", body))
            continue

        paragraph = (
            line.replace("`", "")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("  ", " ")
        )
        story.append(Paragraph(paragraph, body))

    failed_img = ROOT / "evidence" / "failed-run.png"
    success_img = ROOT / "evidence" / "successful-run.png"

    if failed_img.exists():
        story.append(Spacer(1, 0.3 * cm))
        story.append(Paragraph("Failed Run Screenshot", heading))
        story.append(Image(str(failed_img), width=16 * cm, height=9 * cm))

    if success_img.exists():
        story.append(Spacer(1, 0.3 * cm))
        story.append(Paragraph("Successful Run Screenshot", heading))
        story.append(Image(str(success_img), width=16 * cm, height=9 * cm))

    return story


def main() -> None:
    if not MD_FILE.exists():
        raise FileNotFoundError(f"Missing input file: {MD_FILE}")

    md_text = MD_FILE.read_text(encoding="utf-8")
    story = build_story(md_text)

    doc = SimpleDocTemplate(
        str(PDF_FILE),
        pagesize=A4,
        leftMargin=1.8 * cm,
        rightMargin=1.8 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
    )
    doc.build(story)
    print(f"Generated: {PDF_FILE}")


if __name__ == "__main__":
    main()