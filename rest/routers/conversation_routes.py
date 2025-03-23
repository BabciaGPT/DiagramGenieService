from fastapi import APIRouter

from rest.models.Conversation import Conversation
from rest.models.ConversationRequest import ConversationRequest
from rest.models.ConversationResponse import ConversationResponse
from rest.models.ConversationsRequest import ConversationsRequest
from rest.models.ConversationsResponse import ConversationsResponse
from rest.models.Message import Message
from rest.models.MessageType import MessageType

conversation_router = APIRouter(prefix="/conversations", tags=["Conversations"])


@conversation_router.post("/fetchAllForUser", response_model=ConversationsResponse)
async def fetch_all_for_user(conversation_request: ConversationsRequest):
    return ConversationsResponse(
        user_id=conversation_request.user_id,
        conversations_titles=["sample 1", "sample 2"],
    )


@conversation_router.post("/fetchConversation", response_model=ConversationResponse)
async def fetch_conversation(conversation_request: ConversationRequest):
    return ConversationResponse(
        conversation_id="test_uuid",
        conversation=Conversation(
            title="sample title",
            messages=[
                Message(
                    message="sample message",
                    message_type=MessageType.USER,
                ),
                Message(
                    message="sample message",
                    message_type=MessageType.SYSTEM,
                ),
            ],
        ),
    )
