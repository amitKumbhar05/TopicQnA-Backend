import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, ForeignKey
from sqlmodel import Field, SQLModel, Relationship
from .topic import Topic

class Question(SQLModel, table=True):
    __tablename__ = "questions"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    topic_id: uuid.UUID = Field(
        sa_column=Column(
            ForeignKey("topics.id", ondelete="CASCADE")
        )
    )

    question_text: str
    answer_text: str
    revision_count: int = Field(default=0)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_revised_at: Optional[datetime] = None

    topic: Topic = Relationship(back_populates="questions")
