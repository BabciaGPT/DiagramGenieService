from typing import List

from pydantic import BaseModel


class ConversationsResponse(BaseModel):
    conversations_titles: List[str]
