import os

import requests


def sign_in_user_firebase(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={os.getenv('GOOGLE_WEB_API_KEY')}"
    payload = {"email": email, "password": password, "returnSecureToken": True}

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise Exception(f"Failed to sign in! {response.text}")
