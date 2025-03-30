from typing import Optional, List

from pydantic import BaseModel, Field

from rest.models.Message import Message


class ChatResponse(BaseModel):
    """
    Response model from the chatbot.
    """

    conversation_id: str = Field(
        ..., description="Unique identifier for the conversation"
    )
    message: Message = Field(..., description="Message from the chatbot")
