from pydantic import BaseModel

from rest.models.Conversation import Conversation


class ConversationResponse(BaseModel):
    conversation_id: str
    conversation: Conversation
