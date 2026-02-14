import uuid
from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship

# Forward reference for type hinting (circular import prevention)
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .question import Question

class Topic(SQLModel, table=True):
    __tablename__ = "topics"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(index=True)  # Firebase UID
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship: If Topic is deleted, delete all associated Questions (Cascade)
    questions: List["Question"] = Relationship(
        back_populates="topic", 
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )