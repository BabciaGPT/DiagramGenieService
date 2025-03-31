from pydantic import BaseModel, Field


class ChatCreateRequest(BaseModel):
    message: str = Field(..., description="Incoming message from the user")
