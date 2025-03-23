from fastapi import FastAPI

from rest.routers.chat_routes import chat_router
from rest.routers.conversation_routes import conversation_router

app = FastAPI()

app.include_router(chat_router, prefix="/api/v1")
app.include_router(conversation_router, prefix="/api/v1")
