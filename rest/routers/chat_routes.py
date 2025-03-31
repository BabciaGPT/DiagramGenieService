import json
import os
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends

from ai.client.OpenAiClient import OpenAIClient
from ai.models.PlantUmlJsonResponse import PlantUmlJsonResponse
from firebase.repositories.ConversationsRepo import ConversationsRepo
from plantuml_generator.core.generator import PlantUMLGenerator
from rest.middleware.token_middleware import verify_token
from rest.models.ChatCreateRequest import ChatCreateRequest
from rest.models.Conversation import Conversation
from rest.models.ConversationResponse import ConversationResponse
from rest.models.Message import Message
from rest.models.MessageType import MessageType

chat_router = APIRouter(prefix="/chat", tags=["Chat"])
client = OpenAIClient()
generator = PlantUMLGenerator()
firebase = ConversationsRepo()


@chat_router.post("/create", response_model=ConversationResponse)
async def chat_create(request: ChatCreateRequest, user: dict = Depends(verify_token)):
    try:

        response = client.ask(
            os.getenv("OPENAI_MODEL"),
            system_prompt="Hello",
            user_messages=[{"role": "user", "content": request.message}],
            formatoutput=PlantUmlJsonResponse,
        )

        ai_response = PlantUmlJsonResponse(**json.loads(response))
        diagram_base64 = None

        if ai_response.plantuml_code:
            try:
                diagram_base64 = generator.generate_from_code(ai_response.plantuml_code)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        saved = firebase.create_conversation(
            [
                {
                    "message": request.message,
                    "diagram_base64": None,
                    "code": None,
                    "message_type": MessageType.USER.value,
                    "timestamp": datetime.now().isoformat(),
                },
                {
                    "message": ai_response.description,
                    "diagram_base64": diagram_base64,
                    "code": ai_response.plantuml_code,
                    "message_type": MessageType.USER.value,
                    "timestamp": datetime.now().isoformat(),
                },
            ],
            user["user_id"],
        )

        return ConversationResponse(
            conversation_id=saved["id"],
            conversation=Conversation(
                title=ai_response.title,
                messages=[
                    Message(
                        message=message["message"],
                        message_type=message["message_type"],
                        timestamp=message["timestamp"],
                        code=message["code"],
                    )
                    for message in saved["messages"]
                ],
            ),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
