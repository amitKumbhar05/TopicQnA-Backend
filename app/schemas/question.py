from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID

class QuestionCreate(BaseModel):
    question_text: str
    answer_text: str  # Frontend sends Markdown string here

class QuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    answer_text: Optional[str] = None

class QuestionRead(BaseModel):
    id: UUID
    topic_id: UUID
    question_text: str
    answer_text: str
    revision_count: int
    created_at: datetime
    last_revised_at: Optional[datetime] = None