from pydantic import BaseModel
from typing import List

from rest.models.Message import Message


class Project(BaseModel):
    user_id: str
    title: str
    description: str
    diagrams: List[Message]
