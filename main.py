from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Mock Conversational Chat API",
    version="1.0.0"
)


# Enable CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# In-memory conversation store

conversation: List[dict] = []


# Request Schema

class ChatRequest(BaseModel):
    message: str


# Routes


@app.get("/")
async def root():

    return {
        "status": "Mock backend running"
    }


# Send message


@app.post("/chat")
async def chat(req: ChatRequest):

    # User message
    user_message = {
        "role": "user",
        "content": req.message
    }

    # Mock assistant response
    assistant_message = {
        "role": "assistant",
        "content": f"You said: {req.message}"
    }

    # Store messages
    conversation.append(user_message)
    conversation.append(assistant_message)

    # Return assistant response
    return {
        "response": assistant_message["content"]
    }


# Fetch entire conversation


@app.get("/conversation")
async def get_conversation():

    return {
        "messages": conversation
    }