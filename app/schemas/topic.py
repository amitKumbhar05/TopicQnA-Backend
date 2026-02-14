from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class TopicCreate(BaseModel):
    name: str

class TopicUpdate(BaseModel):
    name: str

class TopicRead(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    # We do not return user_id to the frontend typically, but can if needed