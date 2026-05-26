import io
import json
from datetime import date, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from sqlalchemy.orm import Session

from services.analytics_service import get_all_metrics_summary, get_streak
from services.anomaly_service import detect_anomalies
from services.correlation_service import calculate_correlation_matrix
from services.llm_service import call_llm

PRIMARY_COLOR = HexColor("#0EA5E9")
ACCENT_COLOR = HexColor("#10B981")


def generate_health_report(db: Session, user_id: int, user_name: str, days: int = 30, doctor_name: str = None) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.75 * inch, bottomMargin=0.75 * inch)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle("CustomTitle", parent=styles["Title"], fontSize=24, textColor=PRIMARY_COLOR)
    heading_style = ParagraphStyle("CustomHeading", parent=styles["Heading2"], textColor=PRIMARY_COLOR, spaceAfter=12)
    body_style = styles["BodyText"]

    elements = []

    # Cover page
    elements.append(Spacer(1, 2 * inch))
    elements.append(Paragraph("Personal Health Report", title_style))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Paragraph(f"Patient: {user_name}", styles["Heading3"]))
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    elements.append(Paragraph(f"Period: {start_date} to {end_date}", body_style))
    elements.append(Paragraph(f"Generated: {date.today()}", body_style))
    if doctor_name:
        elements.append(Paragraph(f"Prepared for: Dr. {doctor_name}", body_style))
    elements.append(PageBreak())

    # Gather data
    metrics_summary = get_all_metrics_summary(db, user_id, days=days)
    anomalies = detect_anomalies(db, user_id, days=days)
    correlations = calculate_correlation_matrix(db, user_id, days=days)
    streak = get_streak(db, user_id)

    # Executive summary (LLM)
    elements.append(Paragraph("Executive Summary", heading_style))
    try:
        exec_summary = call_llm(
            "You are a medical report writer. Write a professional 200-word executive summary of this patient's health data. Be factual and use the numbers provided. Do not diagnose.",
            f"Patient: {user_name}\nPeriod: {days} days\nLogging streak: {streak} days\nMetrics:\n{json.dumps(metrics_summary, indent=2)}"
        )
        elements.append(Paragraph(exec_summary, body_style))
    except Exception:
        elements.append(Paragraph("Executive summary could not be generated.", body_style))
    elements.append(Spacer(1, 0.3 * inch))

    # Vital statistics table
    elements.append(Paragraph("Vital Statistics", heading_style))
    if metrics_summary:
        table_data = [["Metric", "Average", "Min", "Max", "Latest", "Trend"]]
        metric_labels = {
            "weight_kg": "Weight (kg)", "systolic_bp": "Systolic BP",
            "diastolic_bp": "Diastolic BP", "heart_rate_bpm": "Heart Rate",
            "sleep_hours": "Sleep (hrs)", "sleep_quality": "Sleep Quality",
            "mood_score": "Mood", "energy_level": "Energy",
            "water_litres": "Water (L)", "steps": "Steps",
            "calories_consumed": "Calories", "exercise_minutes": "Exercise (min)"
        }
        for metric, stats in metrics_summary.items():
            label = metric_labels.get(metric, metric)
            table_data.append([
                label,
                str(stats["mean"]), str(stats["min"]), str(stats["max"]),
                str(stats["latest"]), stats["trend_direction"]
            ])

        table = Table(table_data, colWidths=[1.5 * inch, 0.9 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch, 1 * inch])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), PRIMARY_COLOR),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, HexColor("#F0F9FF")]),
        ]))
        elements.append(table)
    elements.append(Spacer(1, 0.3 * inch))

    # Anomalies
    if anomalies:
        elements.append(Paragraph("Detected Anomalies", heading_style))
        for a in anomalies[:10]:
            elements.append(Paragraph(
                f"• <b>{a['metric']}</b> on {a['date']}: {a['value']} "
                f"(expected range: {a['expected_range']}, severity: {a['severity']})",
                body_style
            ))
        elements.append(Spacer(1, 0.3 * inch))

    # Correlations
    sig_pairs = correlations.get("significant_pairs", [])
    if sig_pairs:
        elements.append(Paragraph("Significant Correlations", heading_style))
        for pair in sig_pairs[:5]:
            elements.append(Paragraph(
                f"• {pair['metric_a']} ↔ {pair['metric_b']}: "
                f"{pair['direction']} {pair['strength']} correlation "
                f"(r={pair['correlation']}, p={pair['p_value']})",
                body_style
            ))
        elements.append(Spacer(1, 0.3 * inch))

    # Disclaimer
    elements.append(Spacer(1, 0.5 * inch))
    disclaimer_style = ParagraphStyle("Disclaimer", parent=body_style, fontSize=8, textColor=colors.grey)
    elements.append(Paragraph(
        "DISCLAIMER: This report is for informational purposes only. It does not constitute medical advice. "
        "Consult a qualified healthcare professional for medical decisions.",
        disclaimer_style
    ))

    doc.build(elements)
    return buffer.getvalue()
