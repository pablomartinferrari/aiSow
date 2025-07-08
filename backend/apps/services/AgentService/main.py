from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sys, os

# Ensure AgentService is importable
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.agent_service import AgentService

app = FastAPI()

# Allow CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
agent_service = AgentService()


class ChatRequest(BaseModel):
    project_id: str
    message: str
    top_n: Optional[int] = 5


class ChatResponse(BaseModel):
    reply: str
    context: List[str]
    meta: List[dict]


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    result = agent_service.chat(
        request.project_id, request.message, top_n=request.top_n
    )
    return result


@app.on_event("shutdown")
def shutdown_event():
    agent_service.close()
