from pydantic import BaseModel


class ProjectRequest(BaseModel):
    project_id: str
