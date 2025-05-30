from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from tutor_agent.agent import tutor_agent
from utils import add_user_query_to_history, call_agent_async

load_dotenv()

app = FastAPI()

GOOGLE_API_KEY= os.getenv("GOOGLE_API_KEY")

# Allow CORS only from your deployed frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://kkkiiiirran.github.io"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session Setup 
session_service = InMemorySessionService()
APP_NAME = os.getenv("APP_NAME", "Tutor Agent")
USER_ID = os.getenv("USER_ID", "Tutor")

initial_state = {
    "user_name": "User",
    "history": []
}

# runner
runner = Runner(agent=tutor_agent, app_name=APP_NAME, session_service=session_service)

@app.on_event("startup")
async def startup_event():
    global SESSION_ID
    new_session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state
    )
    SESSION_ID = new_session.id

# Root test endpoint
@app.get("/")
async def root():
    return {"message": "Tutor Agent backend is running"}

# Request/Response Schema
class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str

# Endpoint
@app.post("/ask", response_model=AnswerResponse)
async def ask_question(req: QuestionRequest):
    user_input = req.question

    # Add question to history
    await add_user_query_to_history(
        session_service, APP_NAME, USER_ID, SESSION_ID, user_input
    )

    # Get agent response
    response = await call_agent_async(runner, USER_ID, SESSION_ID, user_input)

    return {"answer": response}
