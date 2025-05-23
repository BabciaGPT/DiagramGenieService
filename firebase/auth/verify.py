from firebase_admin import auth


def verify_id_token_firebase(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        return None
