from pydantic import BaseModel
from rest.models.Project import Project


class ProjectResponse(BaseModel):
    project_id: str
    project: Project
