from typing import Dict, List

from pydantic import BaseModel


class ConversationsResponse(BaseModel):
    conversations: List[Dict[str, str]]
