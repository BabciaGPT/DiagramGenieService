from typing import Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Request model for the chatbot.
    - conversation_id: Optional identifier for a session if you want to separate multiple conversations.
    - message: The incoming message from the user.
    """

    message: str = Field(..., description="Incoming message from the user")
    conversation_id: str = Field(
        ..., description="Optional session identifier for the conversation"
    )
