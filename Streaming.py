from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List
import asyncio

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


# Root Route


@app.get("/")
async def root():

    return {
        "status": "Mock backend running"
    }


# Streaming generator

async def fake_streaming_response(message: str):

    response_text = f"You said: {message}"

    for char in response_text:

        yield char

        await asyncio.sleep(0.05)


# Chat Route


@app.post("/chat")
async def chat(req: ChatRequest):

    # Store user message
    user_message = {
        "role": "user",
        "content": req.message
    }

    conversation.append(user_message)

    # Final assistant message
    assistant_response = f"You said: {req.message}"

    assistant_message = {
        "role": "assistant",
        "content": assistant_response
    }

    conversation.append(assistant_message)

    return StreamingResponse(
        fake_streaming_response(req.message),
        media_type="text/plain"
    )


# Get full conversation


@app.get("/conversation")
async def get_conversation():

    return {
        "messages": conversation
    }