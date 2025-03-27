import os

import firebase_admin
from firebase_admin import credentials


def init_firebase():
    service_account_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    cred = credentials.Certificate(service_account_path)
    firebase_admin.initialize_app(cred)
