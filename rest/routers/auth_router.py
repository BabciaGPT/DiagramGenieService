from fastapi import APIRouter, Depends, HTTPException
from firebase_admin.exceptions import FirebaseError
from starlette import status

from firebase.auth.create_user import create_user_firebase
from firebase.auth.sign_in import sign_in_user_firebase
from rest.middleware.token_middleware import verify_token
from rest.models.LoginRequest import LoginRequest
from rest.models.CreateUserRequest import CreateUserRequest
from rest.models.LoginResponse import LoginResponse
from rest.models.UserCreated import UserCreated
from rest.models.UserInfo import UserInfo

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/createUser", response_model=UserCreated)
async def create_user(create_user_body: CreateUserRequest):
    try:
        user = create_user_firebase(
            email=create_user_body.email,
            password=create_user_body.password,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
            )

        return UserCreated(message="User created successfully", uid=user.uid)

    except FirebaseError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@auth_router.post("/signIn", response_model=LoginResponse)
async def sign_in(login_body: LoginRequest):
    try:
        response = sign_in_user_firebase(
            email=login_body.email, password=login_body.password
        )
        return LoginResponse(token=response["idToken"])
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@auth_router.get("/getUser", response_model=UserInfo)
async def read_current_user(user: dict = Depends(verify_token)):
    return UserInfo(
        username=user["name"],
        email=user["email"],
        user_id=user["user_id"],
    )
