from typing import List, Optional
from pydantic import BaseModel

class TranscriptRequest(BaseModel):
    # transcript blueprint 
    transcript: str

class MeetingSummary(BaseModel):
    # response blueprint 
    summary: str
    decisions: List[str]
    action_items: List[str]

class ErrorResponse(BaseModel):
    # general error blueprint 
    detail: str
