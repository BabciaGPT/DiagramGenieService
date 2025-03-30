import base64
import json
import os
import uuid
from platform import system

from fastapi import APIRouter, HTTPException, Depends

from ai.client.OpenAiClient import OpenAIClient
from ai.models.PlantUmlJsonResponse import PlantUmlJsonResponse
from plantuml_generator.core.generator import PlantUMLGenerator
from rest.middleware.token_middleware import verify_token
from rest.models.ChatRequest import ChatRequest
from rest.models.ChatResponse import ChatResponse
from rest.models.Message import Message
from rest.models.MessageType import MessageType

chat_router = APIRouter(prefix="/chat", tags=["Chat"])
client = OpenAIClient()
generator = PlantUMLGenerator()


@chat_router.post("/make", response_model=ChatResponse)
async def chat(request: ChatRequest, user: dict = Depends(verify_token)):
    try:
        try:
            response = client.ask(
                os.getenv("OPENAI_MODEL"),
                system_prompt="Hello",
                user_messages=[{"role": "user", "content": request.message}],
                formatoutput=PlantUmlJsonResponse,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        try:
            diagram_base64 = generator.generate_from_code(response.plantuml_code)
        except Exception as e:
            raise HTTPException(status_code=500, detail=e)

        return ChatResponse(
            message=Message(
                message_type=MessageType.USER,
                message=response.description,
                diagram_base64=diagram_base64,
            ),
            conversation_id=uuid.uuid4().hex,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
