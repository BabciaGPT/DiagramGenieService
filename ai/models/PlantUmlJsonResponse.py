from pydantic import BaseModel


class PlantUmlJsonResponse(BaseModel):
    description: str
    plantuml_code: str
