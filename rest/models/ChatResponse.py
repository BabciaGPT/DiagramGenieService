from typing import Optional, List

from pydantic import BaseModel, Field


class ChatResponse(BaseModel):
    """
    Response model from the chatbot.
    """

    reply: str = Field(..., description="Chatbot's response")
    uml_diagram: Optional[str] = Field(
        None, description="Generated UML diagram (e.g., in PlantUML format)"
    )
    conversation_id: str = Field(
        ..., description="Unique identifier for the conversation"
    )
