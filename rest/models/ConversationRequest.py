from pydantic import BaseModel


class ConversationRequest(BaseModel):
    conversation_id: str
