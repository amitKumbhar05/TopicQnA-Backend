from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from uuid import UUID

from app.database import get_session
from app.models.topic import Topic
from app.schemas.topic import TopicCreate, TopicRead, TopicUpdate
from app.dependencies import get_current_user

router = APIRouter(prefix="/topics", tags=["Topics"])

@router.post("/", response_model=TopicRead)
def create_topic(
    topic_data: TopicCreate, 
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    new_topic = Topic(name=topic_data.name, user_id=user_id)
    session.add(new_topic)
    session.commit()
    session.refresh(new_topic)
    return new_topic

@router.get("/", response_model=List[TopicRead])
def list_topics(
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    # Filter by logged-in user
    statement = select(Topic).where(Topic.user_id == user_id)
    results = session.exec(statement).all()
    return results

@router.put("/{topic_id}", response_model=TopicRead)
def update_topic(
    topic_id: UUID,
    topic_data: TopicUpdate,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    topic = session.get(Topic, topic_id)
    if not topic or topic.user_id != user_id:
        raise HTTPException(status_code=404, detail="Topic not found or access denied")
    
    topic.name = topic_data.name
    session.add(topic)
    session.commit()
    session.refresh(topic)
    return topic

@router.delete("/{topic_id}")
def delete_topic(
    topic_id: UUID,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    topic = session.get(Topic, topic_id)
    if not topic or topic.user_id != user_id:
        raise HTTPException(status_code=404, detail="Topic not found or access denied")
    
    session.delete(topic)
    session.commit()
    return {"message": "Topic and related questions deleted"}