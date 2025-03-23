from pydantic import BaseModel


class ConversationsRequest(BaseModel):
    user_id: str
