from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)


def generate_report(
    filepath,
    before_score,
    after_score,
    cleaning_log,
    executive_summary="AI summary unavailable",
    dataset_name="Uploaded Dataset"
):
    """
    Generate a professional executive PDF report.
    """

    doc = SimpleDocTemplate(
        filepath,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0F172A"),
        fontSize=24,
        spaceAfter=20
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Heading2"],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#2563EB"),
        fontSize=14,
        spaceAfter=30
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=15,
        spaceAfter=10
    )

    normal_style = styles["BodyText"]

    elements = []

    # ======================================================
    # Cover Page
    # ======================================================

    elements.append(Spacer(1, 0.7 * inch))

    elements.append(
        Paragraph("🧹 CleanAI", title_style)
    )

    elements.append(
        Paragraph(
            "LLM-Powered Data Cleaning Assistant",
            subtitle_style
        )
    )

    elements.append(Spacer(1, 0.5 * inch))

    elements.append(
        Paragraph(
            "<b>Executive Data Quality Report</b>",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1, 0.3 * inch))

    metadata_table = Table([
        ["Dataset", dataset_name],
        ["Generated", datetime.now().strftime("%d %B %Y")],
        ["Time", datetime.now().strftime("%I:%M %p")],
        ["Report Type", "Executive Summary"]
    ], colWidths=[140, 260])

    metadata_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#2563EB")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("BACKGROUND", (0,1), (-1,-1), colors.HexColor("#F8FAFC")),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0,0), (-1,0), 8),
        ("TOPPADDING", (0,1), (-1,-1), 8)
    ]))

    elements.append(metadata_table)

    elements.append(PageBreak())

    # ======================================================
    # Executive Summary
    # ======================================================

    elements.append(
        Paragraph("Executive Summary", heading_style)
    )

    elements.append(
        Paragraph(executive_summary, normal_style)
    )

    elements.append(Spacer(1, 0.3 * inch))

    # ======================================================
    # Quality Score
    # ======================================================

    elements.append(
        Paragraph("Data Quality Improvement", heading_style)
    )

    improvement = after_score - before_score

    quality_table = Table([
        ["Metric", "Value"],
        ["Before Score", str(before_score)],
        ["After Score", str(after_score)],
        ["Improvement", f"{improvement:+}"]
    ], colWidths=[180,180])

    quality_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1E40AF")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("BACKGROUND", (0,1), (-1,-1), colors.HexColor("#EFF6FF")),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold")
    ]))

    elements.append(quality_table)

    elements.append(Spacer(1, 0.3 * inch))

    # ======================================================
    # Cleaning Metrics
    # ======================================================

    elements.append(
        Paragraph("Cleaning Metrics", heading_style)
    )

    emails_fixed = sum("Email" in log for log in cleaning_log)
    countries_fixed = sum("Country" in log for log in cleaning_log)
    duplicates_removed = sum("duplicate" in log.lower() for log in cleaning_log)

    metrics_table = Table([
        ["Metric","Count"],
        ["Emails Fixed", str(emails_fixed)],
        ["Countries Standardized", str(countries_fixed)],
        ["Duplicate Actions", str(duplicates_removed)],
        ["Total Cleaning Actions", str(len(cleaning_log))]
    ], colWidths=[220,120])

    metrics_table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#2563EB")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("BACKGROUND",(0,1),(-1,-1),colors.HexColor("#F8FAFC")),
        ("GRID",(0,0),(-1,-1),0.5,colors.grey),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("ALIGN",(1,1),(-1,-1),"CENTER")
    ]))

    elements.append(metrics_table)

    elements.append(Spacer(1,0.3*inch))

    # ======================================================
    # Cleaning Actions Table
    # ======================================================

    elements.append(
        Paragraph("Cleaning Actions", heading_style)
    )

    action_rows = [["#", "Action"]]

    for i, log in enumerate(cleaning_log, start=1):
        action_rows.append([str(i), log])

    actions_table = Table(
        action_rows,
        colWidths=[35,425]
    )

    actions_table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#0F172A")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),0.25,colors.grey),
        ("BACKGROUND",(0,1),(-1,-1),colors.white),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("BOTTOMPADDING",(0,0),(-1,0),8),
        ("TOPPADDING",(0,1),(-1,-1),6)
    ]))

    elements.append(actions_table)

    elements.append(Spacer(1,0.3*inch))

    # ======================================================
    # Footer
    # ======================================================

    elements.append(
        Paragraph("Report generated by CleanAI", subtitle_style)
    )

    doc.build(elements)