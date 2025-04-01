from firebase_admin import auth


def create_user_firebase(email: str, password: str):
    user = auth.create_user(email=email, password=password, display_name=email)
    return user
