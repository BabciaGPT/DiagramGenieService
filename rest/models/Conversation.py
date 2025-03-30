from typing import List

from pydantic import BaseModel

from rest.models.Message import Message


class Conversation(BaseModel):
    title: str
    messages: List[Message]
