from dotenv import load_dotenv
from fastapi import FastAPI

from firebase.util.init import init_firebase
from rest.routers.auth_router import auth_router

app = FastAPI()
load_dotenv()
init_firebase()
app.include_router(auth_router)
