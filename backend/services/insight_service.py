import json
from datetime import date, timedelta
from sqlalchemy.orm import Session
from models.health_insight import HealthInsight
from services.llm_service import call_llm
from services.analytics_service import get_all_metrics_summary
from services.anomaly_service import detect_anomalies
from services.correlation_service import calculate_correlation_matrix


def generate_weekly_summary(db: Session, user_id: int, user_profile: dict = None) -> HealthInsight:
    end_date = date.today()
    start_date = end_date - timedelta(days=7)

    metrics_summary = get_all_metrics_summary(db, user_id, days=7)
    anomalies = detect_anomalies(db, user_id, days=7)
    correlations = calculate_correlation_matrix(db, user_id, days=30)

    profile_str = ""
    if user_profile:
        profile_str = f"User profile: {user_profile.get('gender', 'unknown')}, height: {user_profile.get('height_cm', 'unknown')}cm"

    system_prompt = """You are a personal health advisor. Generate a weekly health summary
for this user based on their data.

IMPORTANT: You are given pre-calculated statistics — do NOT invent
numbers. Use ONLY the data provided below.

Write a 150–200 word health insight with:
1. Overall assessment (1–2 sentences)
2. Top positive finding this week
3. Top concern and specific recommendation
4. Correlation insight (if any significant ones found)
5. One specific actionable tip for next week

Tone: Warm, encouraging, specific. Like a knowledgeable friend — not
a clinical report. Use the exact numbers provided.

Return plain text only (no JSON, no markdown headers)."""

    user_content = f"""{profile_str}
Period: {start_date} to {end_date}

Metric statistics this week:
{json.dumps(metrics_summary, indent=2)}

Anomalies detected this week:
{json.dumps(anomalies, indent=2)}

Significant correlations found:
{json.dumps(correlations.get('significant_pairs', []), indent=2)}"""

    content = call_llm(system_prompt, user_content)

    insight = HealthInsight(
        user_id=user_id,
        insight_type="weekly_summary",
        metric_context=json.dumps(list(metrics_summary.keys())),
        content=content,
        data_summary_used=json.dumps(metrics_summary),
        period_start=start_date,
        period_end=end_date,
    )
    db.add(insight)
    db.commit()
    db.refresh(insight)
    return insight


def explain_anomaly(db: Session, user_id: int, anomaly: dict) -> str:
    metrics_summary = get_all_metrics_summary(db, user_id, days=7)

    system_prompt = """A health anomaly was detected in this user's data. Explain it in 
plain language and suggest possible causes and actions.

Write 3–4 sentences:
1. What was unusual (use the specific number)
2. 2–3 possible explanations for this reading
3. What they should do (monitor, consult doctor, lifestyle change)

Be reassuring but appropriately cautious. 
Never diagnose. Suggest doctor consultation for serious metrics."""

    user_content = f"""Anomaly details:
{json.dumps(anomaly, indent=2)}

User's recent context (last 7 days average):
{json.dumps(metrics_summary, indent=2)}"""

    return call_llm(system_prompt, user_content)


def explain_correlations(db: Session, user_id: int) -> str:
    correlations = calculate_correlation_matrix(db, user_id, days=60)
    significant = correlations.get("significant_pairs", [])
    if not significant:
        return "Not enough data to find significant correlations yet. Keep logging daily!"

    system_prompt = """Explain these health correlations found in this user's data.

For each correlation, write 2–3 sentences explaining:
- What this pattern means in practical terms
- What this suggests they should focus on
- One specific action they can take

Keep it conversational. Use "your" to make it personal.
Maximum 100 words per correlation."""

    user_content = f"""Statistically significant correlations:
{json.dumps(significant, indent=2)}"""

    return call_llm(system_prompt, user_content)


def answer_health_qa(db: Session, user_id: int, question: str, goals: list = None) -> str:
    metrics_summary = get_all_metrics_summary(db, user_id, days=30)
    anomalies = detect_anomalies(db, user_id, days=30)

    system_prompt = """You are a personal health data assistant. Answer this user's
question about their health data.

Rules:
- Answer ONLY from the data provided — never invent numbers
- If the data cannot answer the question, say so clearly
- Include specific numbers from their data
- Keep under 100 words
- Never diagnose medical conditions
- If they ask about symptoms or medical concerns, recommend a doctor"""

    user_content = f"""User's data summary (last 30 days):
{json.dumps(metrics_summary, indent=2)}

Recent anomalies: {json.dumps(anomalies[:5], indent=2)}
Goals: {json.dumps(goals or [], indent=2)}

User question: "{question}" """

    return call_llm(system_prompt, user_content)
