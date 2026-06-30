import json
from datetime import datetime

from google import genai

from app.config import settings

# Initialize Gemini client
client = genai.Client(api_key=settings.GEMINI_API_KEY)


async def analyze_task(task):
    """
    Analyze a task using Gemini AI and return structured insights.
    """

    current_time = datetime.now().strftime("%d %B %Y, %I:%M %p")

    prompt = f"""
You are an expert AI productivity coach.

Today's date and time:
{current_time}

Your job is to help users finish their work before deadlines.

Analyze the following task using these criteria:

1. Deadline proximity
2. Estimated work required
3. User importance
4. Risk of procrastination
5. Overall urgency

Return ONLY valid JSON in the following format.

{{
    "priority_score": 8,
    "urgency": "High",
    "difficulty": "Medium",
    "completion_probability": 85,
    "recommended_start": "Today evening",
    "risk": "Waiting until tomorrow increases the chance of missing the deadline.",
    "reason": "The deadline is close and the task requires multiple hours of work."
}}

Task Details

Title:
{task.title}

Description:
{task.description}

Deadline:
{task.deadline}

Estimated Hours:
{task.estimated_hours}

Importance:
{task.priority}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        # Remove markdown if Gemini wraps JSON
        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        return json.loads(text)

    except json.JSONDecodeError:
        return {
            "error": "Gemini returned invalid JSON.",
            "raw_response": response.text
        }

    except Exception as e:
        return {
            "error": str(e)
        }