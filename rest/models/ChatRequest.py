from typing import Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Request model for the chatbot.
    - user_id: Unique identifier for the user.
    - session_id: Optional identifier for a session if you want to separate multiple conversations.
    - message: The incoming message from the user.
    """

    user_id: str = Field(..., description="Unique identifier for the user")
    message: str = Field(..., description="Incoming message from the user")
    session_id: Optional[str] = Field(
        None, description="Optional session identifier for the conversation"
    )
