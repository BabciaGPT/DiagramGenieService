import base64

from fastapi import APIRouter, HTTPException, Depends
from plantuml_generator.core.generator import PlantUMLGenerator
from rest.middleware.token_middleware import verify_token
from rest.models.UmlCode import UmlCode

plantuml_generator = PlantUMLGenerator()

plantuml_router = APIRouter(prefix="/plantuml", tags=["PlantUML"])


@plantuml_router.post(
    "/generateDiagram",
    response_model=str,
    dependencies=[Depends(verify_token)],
)
async def generate_diagram(uml_code: UmlCode):
    try:
        img = plantuml_generator.generate_from_code(uml_code.uml_code)
        img_base64 = base64.b64encode(img).decode("utf-8")
        return img_base64
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate diagram: {str(e)}"
        )
