from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from uuid import UUID
from datetime import datetime

from app.database import get_session
from app.models.question import Question
from app.models.topic import Topic
from app.schemas.question import QuestionCreate, QuestionRead, QuestionUpdate
from app.dependencies import get_current_user

router = APIRouter(tags=["Questions"])

# 1. Create Question (Needs Topic ID)
@router.post("/topics/{topic_id}/questions", response_model=QuestionRead)
def create_question(
    topic_id: UUID,
    question_data: QuestionCreate,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    # Verify topic ownership
    topic = session.get(Topic, topic_id)
    if not topic or topic.user_id != user_id:
        raise HTTPException(status_code=404, detail="Topic not found or access denied")

    new_question = Question(
        topic_id=topic_id,
        question_text=question_data.question_text,
        answer_text=question_data.answer_text
    )
    session.add(new_question)
    session.commit()
    session.refresh(new_question)
    return new_question

# 2. List Questions for a Topic
@router.get("/topics/{topic_id}/questions", response_model=List[QuestionRead])
def list_questions(
    topic_id: UUID,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    topic = session.get(Topic, topic_id)
    if not topic or topic.user_id != user_id:
        raise HTTPException(status_code=404, detail="Topic not found or access denied")
    
    return topic.questions

# 3. Get Single Question
@router.get("/questions/{question_id}", response_model=QuestionRead)
def get_question(
    question_id: UUID,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    question = session.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Check ownership via parent topic
    if question.topic.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
        
    return question

# 4. Update Question (Text or Markdown)
@router.put("/questions/{question_id}", response_model=QuestionRead)
def update_question(
    question_id: UUID,
    update_data: QuestionUpdate,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    question = session.get(Question, question_id)
    if not question or question.topic.user_id != user_id:
        raise HTTPException(status_code=404, detail="Question not found")
    
    if update_data.question_text is not None:
        question.question_text = update_data.question_text
    if update_data.answer_text is not None:
        question.answer_text = update_data.answer_text
    
    session.add(question)
    session.commit()
    session.refresh(question)
    return question

# 5. Delete Question
@router.delete("/questions/{question_id}")
def delete_question(
    question_id: UUID,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    question = session.get(Question, question_id)
    if not question or question.topic.user_id != user_id:
        raise HTTPException(status_code=404, detail="Question not found")
    
    session.delete(question)
    session.commit()
    return {"message": "Question deleted"}

# 6. Revision Counter Endpoint
@router.post("/questions/{question_id}/revise", response_model=QuestionRead)
def revise_question(
    question_id: UUID,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    question = session.get(Question, question_id)
    if not question or question.topic.user_id != user_id:
        raise HTTPException(status_code=404, detail="Question not found")
    
    question.revision_count += 1
    question.last_revised_at = datetime.utcnow()
    
    session.add(question)
    session.commit()
    session.refresh(question)
    return question