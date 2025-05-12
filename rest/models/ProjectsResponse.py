from pydantic import BaseModel
from typing import List


class ProjectsResponse(BaseModel):
    projects: List[dict]
