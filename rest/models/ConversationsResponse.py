from typing import Dict

from pydantic import BaseModel


class ConversationsResponse(BaseModel):
    conversations: Dict[str, str]
