import json
from typing import Dict, Any
from openai import OpenAI
import os

from .schemas import MeetingSummary # why? 
from __future__ import annotations # why? 

client = OpenAI()

prompts = [MODEL_PROMPT, MODEL_PROMPT2]

# omit introductions, include times, dates, opposing views  
MODEL_PROMPT2 = 
"""
You are a professional meeting assistant.

Given a raw meeting transcript, you must produce:
1) A concise summary (max 200 words, omitting any hello's and how you've been's) 
2) A bullet-style list of key decisions made
3) A bullet-style list of action items

Always respond in strict JSON with the following structure:

{
  "summary": "string",
  "decisions": ["string", ...],
  "action_items": ["string", ...]
}

- "summary": overview of what was discussed and concluded ( include conflicting details and opposing views, as well as their resolution if it was reached)
- "decisions": each item is a clear decision (if there is a time, date or actor associated, mention that) 
- "action_items": each item in the form "Owner — Action (if there is a time, date or actor associated, mention that)
Do not include any other keys or text outside the JSON.
"""

MODEL_PROMPT = 

"""
You are a professional meeting assistant.

Given a raw meeting transcript, you must produce:
1) A concise summary (max 200 words)
2) A bullet-style list of key decisions made
3) A bullet-style list of action items

Always respond in strict JSON with the following structure:

{
  "summary": "string",
  "decisions": ["string", ...],
  "action_items": ["string", ...]
}

- "summary": overview of what was discussed and concluded.
- "decisions": each item is a clear decision, no extra commentary.
- "action_items": each item in the form "Owner — Action (Due date if mentioned)".
Do not include any other keys or text outside the JSON.
"""


def _call_llm_for_summary(transcript: str) -> Dict[str, Any]:
    """
    Calls OpenAI Chat Completion API to get a structured meeting summary.
    """
    model_name = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")

    response = client.chat.completions.create(
        model=model_name,
        temperature=0.1, # check for diff temps later 
        messages=[
            {"role": "system", "content": MODEL_PROMPT},
            {"role": "user",
            "content": "Meeting transcript:\n\n" + transcript,
            },
        ],
    )
    content = response.choices[0].message.content 
    # Try to parse JSON; if it fails, fall back to a degenerate structure    ## 
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # Fallback: stuff content into summary, leave lists empty
        data = {
            "summary": content,
            "decisions": [],
            "action_items": [],
        }

    # sanity defaults
    data.setdefault("summary", "")
    data.setdefault("decisions", [])
    data.setdefault("action_items", [])

    return data


def summarize_transcript(transcript: str) -> MeetingSummary:
    """
    High-level function that returns a MeetingSummary Pydantic object.
    """
    raw = _call_llm_for_summary(transcript)

    summary = str(raw.get("summary", "")).strip()
    decisions = [str(x).strip() for x in raw.get("decisions", []) if str(x).strip()]
    action_items = [str(x).strip() for x in raw.get("action_items", []) if str(x).strip()]

    return MeetingSummary(
        summary=summary,
        decisions=decisions,
        action_items=action_items,
    )
