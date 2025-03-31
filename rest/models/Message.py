from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from rest.models.MessageType import MessageType


class Message(BaseModel):
    message: str
    diagram_base64: Optional[str] = None
    code: str | None = None
    message_type: MessageType
    timestamp: datetime = datetime.now()
