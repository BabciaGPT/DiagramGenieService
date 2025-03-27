from pydantic import BaseModel


class UserCreated(BaseModel):
    message: str
    uid: str
