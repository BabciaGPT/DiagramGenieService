from pydantic import BaseModel


class ConversationRequest(BaseModel):
    user_id: str
    conversation_id: str
