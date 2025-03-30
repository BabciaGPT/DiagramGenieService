from enum import Enum


class MessageType(str, Enum):
    SYSTEM = "system"
    USER = "user"
