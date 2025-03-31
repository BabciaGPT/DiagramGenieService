from fastapi import APIRouter, Depends

from firebase.repositories.ConversationsRepo import ConversationsRepo
from rest.middleware.token_middleware import verify_token
from rest.models.Conversation import Conversation
from rest.models.ConversationRequest import ConversationRequest
from rest.models.ConversationResponse import ConversationResponse
from rest.models.ConversationsResponse import ConversationsResponse
from rest.models.Message import Message
from rest.models.MessageType import MessageType

conversation_router = APIRouter(prefix="/conversations", tags=["Conversations"])
conversations_repo = ConversationsRepo()


@conversation_router.get("/fetchAllForUser", response_model=ConversationsResponse)
async def fetch_all_for_user(user: dict = Depends(verify_token)):
    conversations = conversations_repo.get_conversations_by_user(
        user["user_id"],
    )
    return ConversationsResponse(conversations=conversations)


@conversation_router.post("/fetchConversation", response_model=ConversationResponse)
async def fetch_conversation(
    conversation_request: ConversationRequest, user: dict = Depends(verify_token)
):
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
