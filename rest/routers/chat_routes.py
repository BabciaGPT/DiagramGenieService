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
from rest.models.ChatRequest import ChatRequest
from rest.models.Conversation import Conversation
from rest.models.ConversationResponse import ConversationResponse
from rest.models.Message import Message
from rest.models.MessageType import MessageType
from rest.util.check_code_base64 import check_code_base64

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
        diagram = check_code_base64(ai_response, generator)

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
                    "diagram_base64": diagram,
                    "code": ai_response.plantuml_code,
                    "message_type": MessageType.SYSTEM.value,
                    "timestamp": datetime.now().isoformat(),
                },
            ],
            user["user_id"],
            ai_response.title,
        )

        return ConversationResponse(
            conversation_id=saved["id"],
            conversation=Conversation(
                title=ai_response.title,
                messages=[
                    Message(
                        message=message["message"],
                        message_type=message["message_type"],
                        diagram_base64=message["diagram_base64"],
                        timestamp=message["timestamp"],
                        code=message["code"],
                    )
                    for message in saved["messages"]
                ],
            ),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@chat_router.put("/put", response_model=Message, dependencies=[Depends(verify_token)])
async def chat_put(request: ChatRequest):
    try:
        _, conversation = firebase.fetch_user_conversation(request.conversation_id)
        past_messages = [
            {
                "role": message["message_type"],
                "content": f"PlantUML code: {message['code']}"
                f"\nMessage: {message['message']}",
            }
            for message in conversation["messages"]
        ]

        response = client.ask(
            os.getenv("OPENAI_MODEL"),
            system_prompt="Hello",
            user_messages=past_messages
            + [{"role": "user", "content": request.message}],
            formatoutput=PlantUmlJsonResponse,
        )

        ai_response = PlantUmlJsonResponse(**json.loads(response))
        diagram = check_code_base64(ai_response, generator)

        user_msg = {
            "message": request.message,
            "diagram_base64": None,
            "code": None,
            "message_type": MessageType.USER.value,
            "timestamp": datetime.now().isoformat(),
        }

        system_msg = {
            "message": ai_response.description,
            "diagram_base64": diagram,
            "code": ai_response.plantuml_code,
            "message_type": MessageType.SYSTEM.value,
            "timestamp": datetime.now().isoformat(),
        }

        updated = firebase.update_with_messages(
            request.conversation_id,
            [user_msg, system_msg],
        )
        if updated:
            return Message(**system_msg)
        else:
            raise HTTPException(status_code=500, detail="Error while saving")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
