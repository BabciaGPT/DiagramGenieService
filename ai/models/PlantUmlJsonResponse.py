from pydantic import BaseModel, Field


class PlantUmlJsonResponse(BaseModel):
    """
    A response model for PlantUML JSON responses.
    """

    title: str = Field(..., description="The title of the PlantUML diagram.")
    description: str = Field(..., description="A description of the PlantUML diagram.")
    plantuml_code: str | None = Field(
        None, description="The PlantUML code, if available."
    )
