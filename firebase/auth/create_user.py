from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError


def create_user_firebase(email: str, password: str, display_name: str):
    try:
        user = auth.create_user(
            email=email, password=password, display_name=display_name
        )
    except FirebaseError as e:
        return None
    return user
