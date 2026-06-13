from io import BytesIO
from html import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


def safe_text(value) -> str:
    return escape(str(value or "").replace("‑", "-").replace("–", "-").replace("—", "-"))


def percentage(value) -> str:
    try:
        return f"{round(float(value) * 100)}%"
    except Exception:
        return "N/A"


def generate_resume_report_pdf(data: dict) -> bytes:
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.4 * cm,
        bottomMargin=1.4 * cm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=14,
    )

    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=12,
        spaceAfter=8,
    )

    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=6,
    )

    small_style = ParagraphStyle(
        "SmallStyle",
        parent=styles["BodyText"],
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#475569"),
    )

    story = []

    story.append(Paragraph("Resume Polisher AI Report", title_style))

    metadata = [
        ["Target Role", safe_text(data.get("target_role"))],
        ["Location", safe_text(data.get("location"))],
        ["Work Type", safe_text(data.get("work_type"))],
        ["Work Mode", safe_text(data.get("work_mode"))],
    ]

    metadata_table = Table(metadata, colWidths=[4 * cm, 12 * cm])
    metadata_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E0E7FF")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#0F172A")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#CBD5E1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    story.append(metadata_table)
    story.append(Spacer(1, 12))

    polished_bullets = data.get("polished_bullets", [])

    if polished_bullets:
        before_scores = [item.get("score_before", 0) for item in polished_bullets]
        after_scores = [item.get("score_after_estimate", 0) for item in polished_bullets]

        avg_before = sum(before_scores) / len(before_scores)
        avg_after = sum(after_scores) / len(after_scores)
        improvement = avg_after - avg_before
    else:
        avg_before = 0
        avg_after = 0
        improvement = 0

    top_job_fit = 0
    job_matches = data.get("job_matches", [])
    if job_matches:
        top_job_fit = max(job.get("fit_score", 0) for job in job_matches)

    score_table_data = [
        ["Metric", "Value"],
        ["Average Before Score", percentage(avg_before)],
        ["Average After Score", percentage(avg_after)],
        ["Improvement", f"+{round(improvement * 100)} pts"],
        ["Top Job Fit", percentage(top_job_fit)],
        ["Polished Bullets", str(len(polished_bullets))],
    ]

    score_table = Table(score_table_data, colWidths=[7 * cm, 9 * cm])
    score_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#CBD5E1")),
                ("PADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    story.append(Paragraph("Performance Summary", heading_style))
    story.append(score_table)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Polished Resume Bullets", heading_style))

    for index, item in enumerate(polished_bullets, start=1):
        story.append(Paragraph(f"<b>{index}. Original</b>", normal_style))
        story.append(Paragraph(safe_text(item.get("original")), small_style))

        story.append(Paragraph("<b>Polished</b>", normal_style))
        story.append(Paragraph(safe_text(item.get("polished")), normal_style))

        score_line = (
            f"<b>Score:</b> {percentage(item.get('score_before'))} "
            f"→ {percentage(item.get('score_after_estimate'))}"
        )
        story.append(Paragraph(score_line, normal_style))

        feedback = item.get("feedback", [])
        if feedback:
            story.append(Paragraph("<b>Feedback</b>", normal_style))
            for feedback_item in feedback:
                story.append(Paragraph(f"• {safe_text(feedback_item)}", small_style))

        story.append(Spacer(1, 10))

    story.append(PageBreak())
    story.append(Paragraph("Suggested Job Matches", heading_style))

    for index, job in enumerate(job_matches, start=1):
        story.append(
            Paragraph(
                f"<b>{index}. {safe_text(job.get('company'))} — {safe_text(job.get('role'))}</b>",
                normal_style,
            )
        )

        story.append(
            Paragraph(
                f"Location: {safe_text(job.get('location'))}<br/>"
                f"Work Type: {safe_text(job.get('work_type'))}<br/>"
                f"Work Mode: {safe_text(job.get('work_mode'))}<br/>"
                f"Fit Score: {percentage(job.get('fit_score'))}<br/>"
                f"Career URL: {safe_text(job.get('career_url'))}",
                small_style,
            )
        )

        for reason in job.get("reasons", []):
            story.append(Paragraph(f"• {safe_text(reason)}", small_style))

        story.append(Spacer(1, 10))

    summary_feedback = data.get("summary_feedback", [])
    if summary_feedback:
        story.append(Paragraph("Summary Feedback", heading_style))
        for item in summary_feedback:
            story.append(Paragraph(f"• {safe_text(item)}", normal_style))

    doc.build(story)

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes