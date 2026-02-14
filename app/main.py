from fastapi import FastAPI
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware  

from app.database import engine
from app.models import Topic, Question
from app.routers import topics, questions

app = FastAPI(title="Topic & Question Tracker")

origins = [
    "http://localhost:5173",     
    "http://127.0.0.1:5173",     
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       
    allow_credentials=True,      
    allow_methods=["*"],         
    allow_headers=["*"],         
)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Serverless Backend is Running"}

# Register Routers
app.include_router(topics.router)
app.include_router(questions.router)