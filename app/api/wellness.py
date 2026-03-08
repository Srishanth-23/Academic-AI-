import os
import httpx
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

SYSTEM_PROMPT = """You are Serene, a warm and empathetic AI wellness companion for college students.
Your role is to:
- Listen actively and validate students' feelings
- Help with stress, exam anxiety, burnout, and academic pressure
- Provide practical mental health tips (breathing exercises, study breaks, sleep hygiene)
- Encourage professional help (college counsellor) when needed
- Keep responses SHORT (2-4 sentences), warm, and non-clinical
- Never diagnose medical conditions
- Always end with an encouraging question or a suggested technique

Tone: Warm, supportive, human, non-robotic. Avoid generic responses."""

# Rule-based fallback responses (offline / no API key)
FALLBACK_RESPONSES = {
    "stress": "Exam stress is completely normal — your brain is actually working hard! 🌿 Try the 4-7-8 breath: inhale 4s, hold 7s, exhale 8s. What's stressing you most right now — time, difficulty, or something else?",
    "anxious": "Feeling anxious before exams is your nervous system trying to protect you — it's not weakness. 💚 Ground yourself: name 5 things you can see around you right now. What does your anxiety feel like physically?",
    "burnout": "Burnout is real and it's telling you something important. Rest isn't a reward — it's fuel. 🌙 Have you taken even a 10-minute break today, away from your screen?",
    "sad": "It's okay to not be okay sometimes. Sadness is a signal worth listening to. 💜 You don't have to figure everything out right now. What's one small thing that usually brings you even a tiny bit of comfort?",
    "tired": "Your body and mind are asking for rest — that's not laziness, that's wisdom. 😴 Have you been sleeping enough? Even a 20-minute nap can reset your focus significantly.",
    "lonely": "Loneliness in college is more common than it looks. You're not alone in feeling alone. 🤝 Have you reached out to anyone today — even just a text to a friend or family member?",
    "fail": "One exam or grade doesn't define your path. Many successful people have failed and rebuilt. 💪 What's one thing you learned from this experience, even a small one?",
    "motivation": "Motivation comes in waves — and that's okay. Start impossibly small: just 5 minutes of studying, one page. 📖 What's the very next smallest step you could take right now?",
    "sleep": "Poor sleep makes everything harder — memory, mood, focus. 🌙 Try a consistent sleep time and no screens 30 min before bed. What does your typical bedtime routine look like?",
    "help": "Reaching out is the bravest step. Your college has a counselling centre — talking to someone trained can make a huge difference. 💬 Would you like some tips on how to start that conversation?",
}

def get_fallback(message: str) -> str:
    message_lower = message.lower()
    for keyword, response in FALLBACK_RESPONSES.items():
        if keyword in message_lower:
            return response
    # Generic fallback
    return (
        "Thank you for sharing that with me. 💚 Whatever you're going through, you don't have to face it alone.\n\n"
        "Try this: take one slow deep breath right now — in through your nose, out through your mouth.\n\n"
        "Can you tell me a bit more about what's been on your mind?"
    )


class ChatMessage(BaseModel):
    role: str  # "user" or "model"
    text: str


class WellnessChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []


@router.post("/chat")
async def wellness_chat(req: WellnessChatRequest):
    """AI wellness chatbot powered by Gemini, with rule-based fallback."""

    # Prefer Gemini if API key is configured
    if GEMINI_API_KEY:
        try:
            contents = [{"role": "user", "parts": [{"text": SYSTEM_PROMPT + "\n\nStart the conversation warmly."}]}]

            # Add chat history
            for msg in (req.history or []):
                contents.append({"role": msg.role, "parts": [{"text": msg.text}]})

            # Add current user message
            contents.append({"role": "user", "parts": [{"text": req.message}]})

            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(
                    f"{GEMINI_URL}?key={GEMINI_API_KEY}",
                    json={"contents": contents, "generationConfig": {"maxOutputTokens": 300, "temperature": 0.8}}
                )
                res.raise_for_status()
                data = res.json()
                reply = data["candidates"][0]["content"]["parts"][0]["text"]
                return {"reply": reply, "source": "gemini"}

        except Exception as e:
            # Fall through to rule-based
            pass

    # Rule-based fallback
    reply = get_fallback(req.message)
    return {"reply": reply, "source": "local"}


@router.get("/tips")
def wellness_tips():
    """Return daily mental wellness tips."""
    return {
        "tips": [
            {"emoji": "🌿", "title": "Box Breathing", "body": "Inhale 4s → Hold 4s → Exhale 4s → Hold 4s. Repeat 4 times."},
            {"emoji": "📵", "title": "Phone-Free Focus", "body": "Study for 25 min, phone face-down. You'll retain 40% more."},
            {"emoji": "💧", "title": "Stay Hydrated", "body": "Even mild dehydration reduces focus by up to 20%."},
            {"emoji": "🚶", "title": "Walk It Off", "body": "A 10-min walk boosts mood for up to 2 hours via endorphins."},
            {"emoji": "😴", "title": "Sleep = Memory", "body": "Your brain consolidates everything you studied during deep sleep."},
        ]
    }
