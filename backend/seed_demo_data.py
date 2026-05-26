"""
Seed Demo Data for Personal Health Tracker
Run: python backend/seed_demo_data.py
Creates a demo user + admin with realistic health logs, goals, and insights.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import date, timedelta, datetime
from database import SessionLocal, engine, Base
from models.user import User
from models.health_log import HealthLog
from models.health_goal import HealthGoal
from models.health_insight import HealthInsight
import bcrypt
import random

# Ensure tables exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


# --------------- USERS ---------------
def seed_users():
    existing = db.query(User).filter(User.email == "hamza.malik@demo.com").first()
    if existing:
        print(f"Demo user already exists (id={existing.id}), deleting and re-seeding...")
        db.query(HealthInsight).filter(HealthInsight.user_id == existing.id).delete()
        db.query(HealthGoal).filter(HealthGoal.user_id == existing.id).delete()
        db.query(HealthLog).filter(HealthLog.user_id == existing.id).delete()
        db.delete(existing)
        db.commit()

    admin = db.query(User).filter(User.email == "admin@test.com").first()
    if admin:
        print(f"Admin already exists (id={admin.id}), deleting and re-seeding...")
        db.query(HealthInsight).filter(HealthInsight.user_id == admin.id).delete()
        db.query(HealthGoal).filter(HealthGoal.user_id == admin.id).delete()
        db.query(HealthLog).filter(HealthLog.user_id == admin.id).delete()
        db.delete(admin)
        db.commit()

    demo_user = User(
        full_name="Hamza Malik",
        email="hamza.malik@demo.com",
        hashed_password=hash_password("demo123"),
        role="user",
        date_of_birth=date(1995, 3, 15),
        gender="male",
        height_cm=175.0,
        preferred_provider="auto",
        is_active=True,
    )
    db.add(demo_user)

    admin_user = User(
        full_name="Admin",
        email="admin@test.com",
        hashed_password=hash_password("test123"),
        role="admin",
        is_active=True,
    )
    db.add(admin_user)
    db.commit()
    db.refresh(demo_user)
    db.refresh(admin_user)
    print(f"Created demo user: id={demo_user.id}, email=hamza.malik@demo.com")
    print(f"Created admin user: id={admin_user.id}, email=admin@test.com")
    return demo_user


# --------------- HEALTH LOGS ---------------
def seed_health_logs(user_id: int):
    """Generate 60 days of realistic health log data with natural variations."""
    random.seed(42)  # Reproducible
    today = date.today()
    logs = []

    # Base values with daily variation
    base = {
        "weight_kg": 78.5,
        "systolic_bp": 122,
        "diastolic_bp": 78,
        "heart_rate_bpm": 72,
        "sleep_hours": 7.0,
        "sleep_quality": 3,
        "mood_score": 6,
        "energy_level": 6,
        "water_litres": 2.0,
        "steps": 8000,
        "calories_consumed": 2100,
        "exercise_minutes": 25,
    }

    notes_pool = [
        "Felt great today, morning jog went well",
        "Stressful day at work, ate comfort food",
        "Good sleep, woke up refreshed",
        "Skipped exercise, too tired",
        "Had a productive day, ate balanced meals",
        "Slight headache in the afternoon",
        "Weekend relaxation, walked in the park",
        "Gym session - legs day",
        "Drank extra water today",
        "Late night, poor sleep quality",
        "Meal prepped for the week",
        "Feeling motivated, hit 10k steps!",
        "Rainy day, stayed indoors",
        "Had a cheat meal - pizza night",
        "Morning yoga, felt centered",
        None, None, None, None, None,  # Many days without notes
    ]

    for i in range(60):
        log_date = today - timedelta(days=59 - i)

        # Skip some days randomly (10% chance) to create gaps
        if random.random() < 0.10 and i not in [0, 59]:
            continue

        # Weight trends down slightly over time (fitness journey)
        weight = base["weight_kg"] - (i * 0.03) + random.gauss(0, 0.3)

        # BP fluctuates naturally
        systolic = int(base["systolic_bp"] + random.gauss(0, 5))
        diastolic = int(base["diastolic_bp"] + random.gauss(0, 3))
        if systolic <= diastolic:
            systolic = diastolic + random.randint(15, 25)

        # HR varies with exercise
        hr = int(base["heart_rate_bpm"] + random.gauss(0, 5))

        # Sleep varies day to day
        sleep = round(base["sleep_hours"] + random.gauss(0, 1.0), 1)
        sleep = max(4.0, min(10.0, sleep))
        sleep_q = max(1, min(5, int(base["sleep_quality"] + random.gauss(0.5, 0.8))))

        # Mood and energy correlated with sleep
        sleep_bonus = 1 if sleep > 7.5 else (-1 if sleep < 5.5 else 0)
        mood = max(1, min(10, int(base["mood_score"] + sleep_bonus + random.gauss(0, 1.2))))
        energy = max(1, min(10, int(base["energy_level"] + sleep_bonus + random.gauss(0, 1.0))))

        # Water intake
        water = round(base["water_litres"] + random.gauss(0, 0.4), 1)
        water = max(0.5, min(4.0, water))

        # Steps - higher on weekdays, weekends vary
        day_of_week = log_date.weekday()
        step_base = 9000 if day_of_week < 5 else 6000
        steps = int(step_base + random.gauss(0, 2000))
        steps = max(1000, steps)

        # Calories
        cals = int(base["calories_consumed"] + random.gauss(0, 200))
        cals = max(1200, min(3000, cals))

        # Exercise - some days 0, some days high
        exercise = int(base["exercise_minutes"] + random.gauss(0, 15))
        exercise = max(0, min(120, exercise))
        if random.random() < 0.15:
            exercise = 0  # Rest day

        log = HealthLog(
            user_id=user_id,
            log_date=log_date,
            weight_kg=round(weight, 1),
            systolic_bp=systolic,
            diastolic_bp=diastolic,
            heart_rate_bpm=hr,
            sleep_hours=sleep,
            sleep_quality=sleep_q,
            mood_score=mood,
            energy_level=energy,
            water_litres=water,
            steps=steps,
            calories_consumed=cals,
            exercise_minutes=exercise,
            notes=random.choice(notes_pool),
        )
        logs.append(log)

    db.add_all(logs)
    db.commit()
    print(f"Created {len(logs)} health logs over 60 days")
    return logs


# --------------- GOALS ---------------
def seed_goals(user_id: int):
    today = date.today()
    goals = [
        HealthGoal(
            user_id=user_id,
            metric="weight_kg",
            goal_type="reach",
            target_value=75.0,
            start_date=today - timedelta(days=30),
            target_date=today + timedelta(days=60),
            is_active=True,
        ),
        HealthGoal(
            user_id=user_id,
            metric="steps",
            goal_type="minimum",
            target_value=10000,
            start_date=today - timedelta(days=14),
            is_active=True,
        ),
        HealthGoal(
            user_id=user_id,
            metric="sleep_hours",
            goal_type="minimum",
            target_value=7.5,
            start_date=today - timedelta(days=21),
            is_active=True,
        ),
        HealthGoal(
            user_id=user_id,
            metric="water_litres",
            goal_type="minimum",
            target_value=2.5,
            start_date=today - timedelta(days=7),
            is_active=True,
        ),
        HealthGoal(
            user_id=user_id,
            metric="exercise_minutes",
            goal_type="minimum",
            target_value=30,
            start_date=today - timedelta(days=14),
            is_active=True,
        ),
    ]
    db.add_all(goals)
    db.commit()
    print(f"Created {len(goals)} health goals")


# --------------- INSIGHTS ---------------
def seed_insights(user_id: int):
    today = date.today()
    insights = [
        HealthInsight(
            user_id=user_id,
            insight_type="weekly_summary",
            content="This week you maintained a solid routine with 6 out of 7 days logged. Your weight is trending downward at a healthy pace (-0.2 kg/week). Sleep averaged 7.2 hours — slightly below your 7.5h goal. Mood and energy levels were stable at 7/10. You hit your 10k step goal 4 out of 7 days. Consider adding an extra glass of water daily — your average of 2.1L is below the 2.5L target. Exercise was consistent with an average of 28 minutes, close to your 30-minute goal.",
            period_start=today - timedelta(days=7),
            period_end=today,
            created_at=datetime.utcnow(),
        ),
        HealthInsight(
            user_id=user_id,
            insight_type="correlation",
            content="Strong positive correlation found between sleep hours and next-day mood score (r=0.72, p<0.01). On nights you sleep 7.5+ hours, your mood averages 7.8 vs 5.9 on nights below 6 hours. Also observed: exercise minutes positively correlate with sleep quality (r=0.58).",
            period_start=today - timedelta(days=30),
            period_end=today,
            created_at=datetime.utcnow() - timedelta(days=3),
        ),
        HealthInsight(
            user_id=user_id,
            insight_type="anomaly_explanation",
            content="Your heart rate of 92 bpm on May 10 was flagged as an anomaly (Z-score: 2.8). This was likely correlated with your note about a stressful day at work, lower sleep (5.2h the night before), and higher caffeine-related calorie intake (2,400 cal vs your 2,100 average).",
            period_start=today - timedelta(days=10),
            period_end=today - timedelta(days=10),
            created_at=datetime.utcnow() - timedelta(days=7),
        ),
    ]
    db.add_all(insights)
    db.commit()
    print(f"Created {len(insights)} health insights")


# --------------- MAIN ---------------
def main():
    print("=" * 60)
    print("  Seeding Personal Health Tracker Demo Data")
    print("=" * 60)
    print()

    demo_user = seed_users()
    seed_health_logs(demo_user.id)
    seed_goals(demo_user.id)
    seed_insights(demo_user.id)

    print()
    print("=" * 60)
    print("  Seed complete!")
    print()
    print("  Demo User:  hamza.malik@demo.com / demo123")
    print("  Admin:      admin@test.com / test123")
    print("=" * 60)


if __name__ == "__main__":
    main()
    db.close()
