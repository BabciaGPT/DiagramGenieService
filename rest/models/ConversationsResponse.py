from typing import List

from pydantic import BaseModel


class ConversationsResponse(BaseModel):
    user_id: str
    conversations_titles: List[str]
