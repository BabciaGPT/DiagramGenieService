from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from firebase.util.init import init_firebase
from rest.routers.auth_router import auth_router

from rest.routers.chat_routes import chat_router
from rest.routers.code_router import plantuml_router
from rest.routers.conversation_routes import conversation_router
from rest.routers.project_routes import project_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        content={"error": str(exc)},
        status_code=500,
        headers={"Access-Control-Allow-Origin": "*"},  # Ensure CORS in error responses
    )


load_dotenv()
init_firebase()
app.include_router(auth_router)

app.include_router(chat_router)
app.include_router(conversation_router)
app.include_router(project_router)
app.include_router(plantuml_router)
