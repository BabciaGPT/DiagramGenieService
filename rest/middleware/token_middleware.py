from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException
from starlette import status

from firebase.auth.verify import verify_id_token_firebase

bearer = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    if not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or missing token."
        )
    check_user = verify_id_token_firebase(credentials.credentials)

    if not check_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or missing token."
        )

    return check_user
