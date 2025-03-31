from google.cloud import firestore


class FirestoreClient:
    _instance = None

    @staticmethod
    def get_client():
        if FirestoreClient._instance is None:
            FirestoreClient._instance = firestore.Client()
        return FirestoreClient._instance
