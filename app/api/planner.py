from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os, json, datetime

router = APIRouter()

# ── Pydantic models ────────────────────────────────────────────
class Exam(BaseModel):
    subject: str
    date: str          # "2026-03-15"
    time: str          # "09:00 AM"
    venue: Optional[str] = "Main Hall"
    difficulty: Optional[str] = "medium"  # easy / medium / hard

class ScheduleRequest(BaseModel):
    student_name: str
    exams: List[Exam]
    daily_study_hours: Optional[int] = 6
    preferences: Optional[str] = ""

class ScheduleSlot(BaseModel):
    date: str
    day: str
    subject: str
    duration_hours: float
    topic_focus: str
    priority: str   # high / medium / low
    tip: str

class ScheduleResponse(BaseModel):
    schedule: List[ScheduleSlot]
    summary: str
    total_days: int


# ── Helpers ────────────────────────────────────────────────────
def _days_until(date_str: str) -> int:
    try:
        target = datetime.date.fromisoformat(date_str)
        return max((target - datetime.date.today()).days, 1)
    except:
        return 7


def _generate_fallback_schedule(req: ScheduleRequest) -> ScheduleResponse:
    """Smart rule-based scheduler when AI is unavailable."""
    slots: List[ScheduleSlot] = []
    today = datetime.date.today()

    # Sort exams by date
    sorted_exams = sorted(req.exams, key=lambda e: e.date)

    difficulty_weights = {"easy": 1.0, "medium": 1.5, "hard": 2.0}

    for exam in sorted_exams:
        days_left = _days_until(exam.date)
        weight = difficulty_weights.get(exam.difficulty or "medium", 1.5)
        study_days = max(min(days_left - 1, 7), 1)

        # Allocate hours weighted by difficulty
        hours_per_day = round(min(req.daily_study_hours * (weight / 4), 3.0), 1)

        topics = [
            f"Core concepts & definitions — {exam.subject}",
            f"Previous year questions — {exam.subject}",
            f"Formula sheet & problem solving — {exam.subject}",
            f"Mock test & weak area revision — {exam.subject}",
            f"Final quick revision — {exam.subject}",
        ]

        priority_map = {0: "high", 1: "high", 2: "medium", 3: "medium", 4: "low"}

        for i in range(study_days):
            study_date = today + datetime.timedelta(days=i)
            if study_date.isoformat() >= exam.date:
                break
            day_name = study_date.strftime("%A")
            topic = topics[i % len(topics)]
            priority = priority_map.get(min(i, 4), "medium")
            tip = (
                "Start strong — first impressions of material stick!" if i == 0 else
                "Focus on weak areas identified yesterday." if i == 1 else
                "Practice problems are key — theory alone won't help." if i == 2 else
                "Take breaks every 45 min using the Pomodoro technique." if i == 3 else
                "Light revision only — avoid new topics before the exam."
            )
            slots.append(ScheduleSlot(
                date=study_date.isoformat(),
                day=day_name,
                subject=exam.subject,
                duration_hours=hours_per_day,
                topic_focus=topic,
                priority=priority,
                tip=tip,
            ))

    # Add exam day reminder slots
    for exam in sorted_exams:
        exam_date = datetime.date.fromisoformat(exam.date)
        slots.append(ScheduleSlot(
            date=exam.date,
            day=exam_date.strftime("%A"),
            subject=f"📝 EXAM: {exam.subject}",
            duration_hours=0,
            topic_focus=f"{exam.time} | {exam.venue or 'Main Hall'} — Quick revision only",
            priority="high",
            tip="Get good sleep the night before. Eat a proper breakfast. Arrive 15 min early.",
        ))

    slots.sort(key=lambda s: s.date)
    total_days = len(set(s.date for s in slots))
    subjects_str = ", ".join(e.subject for e in sorted_exams)

    return ScheduleResponse(
        schedule=slots,
        summary=f"AI Schedule for {req.student_name}: {total_days} study days covering {subjects_str}. "
                f"Daily target: {req.daily_study_hours}h. Harder subjects get more time automatically.",
        total_days=total_days,
    )


# ── Endpoint ────────────────────────────────────────────────────
@router.post("/generate-schedule", response_model=ScheduleResponse)
async def generate_schedule(req: ScheduleRequest):
    """Generate an AI-powered personalized study schedule."""
    GEMINI_KEY = os.getenv("GEMINI_API_KEY")

    if GEMINI_KEY:
        try:
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")

            exams_text = "\n".join(
                f"- {e.subject}: {e.date} at {e.time} ({e.difficulty} difficulty)"
                for e in req.exams
            )
            today = datetime.date.today().isoformat()

            prompt = f"""You are an expert academic planner. Create a detailed day-by-day study schedule.

Student: {req.student_name}
Today: {today}
Daily study hours available: {req.daily_study_hours}h
Preferences: {req.preferences or 'None specified'}

Upcoming exams:
{exams_text}

Return ONLY a valid JSON object with this exact structure:
{{
  "schedule": [
    {{
      "date": "YYYY-MM-DD",
      "day": "Monday",
      "subject": "Subject Name",
      "duration_hours": 2.0,
      "topic_focus": "What to study",
      "priority": "high/medium/low",
      "tip": "One actionable study tip"
    }}
  ],
  "summary": "Brief overall strategy summary",
  "total_days": 10
}}

Rules:
- Only include dates from today until the last exam date
- Harder subjects get more hours per day
- Mark exam days with subject prefix "📝 EXAM: " and duration_hours: 0
- Include 1 practical study tip per slot
- Sort by date ascending"""

            response = model.generate_content(prompt)
            text = response.text.strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            data = json.loads(text.strip())
            return ScheduleResponse(**data)

        except Exception as e:
            print(f"Gemini schedule generation failed: {e}. Using fallback.")

    return _generate_fallback_schedule(req)


@router.get("/exam-timetable/{student_id}")
async def get_exam_timetable(student_id: int):
    """Returns the exam timetable for a student (mock data — connect to your DB)."""
    # TODO: Replace with DB query when exam_schedule table is ready
    today = datetime.date.today()
    exams = [
        {"id": 1, "subject": "Computer Networks",      "code": "CN301",  "date": (today + datetime.timedelta(days=8)).isoformat(),  "time": "09:00 AM", "venue": "Hall A", "difficulty": "hard"},
        {"id": 2, "subject": "Operating Systems",      "code": "OS302",  "date": (today + datetime.timedelta(days=12)).isoformat(), "time": "02:00 PM", "venue": "Hall B", "difficulty": "hard"},
        {"id": 3, "subject": "Theory of Computation",  "code": "TOC303", "date": (today + datetime.timedelta(days=16)).isoformat(), "time": "09:00 AM", "venue": "Hall A", "difficulty": "medium"},
        {"id": 4, "subject": "Advanced Java",           "code": "AJ304",  "date": (today + datetime.timedelta(days=20)).isoformat(), "time": "02:00 PM", "venue": "Hall C", "difficulty": "medium"},
        {"id": 5, "subject": "Software Engineering",   "code": "SE305",  "date": (today + datetime.timedelta(days=24)).isoformat(), "time": "09:00 AM", "venue": "Hall B", "difficulty": "easy"},
    ]
    return {"exams": exams, "semester": "April 2026 End Semester Examinations"}
