from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from firebase.util.init import init_firebase
from rest.routers.auth_router import auth_router

from rest.routers.chat_routes import chat_router
from rest.routers.conversation_routes import conversation_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
init_firebase()
app.include_router(auth_router)

app.include_router(chat_router)
app.include_router(conversation_router)
