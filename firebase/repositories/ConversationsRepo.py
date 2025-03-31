from typing import Dict

from firebase.client.FirestoreClient import FirestoreClient


class ConversationsRepo:
    def __init__(self):
        self.db = FirestoreClient.get_client()
        self.collection = self.db.collection("conversations")

    def create_conversation(self, messages, user_id):
        _, document_ref = self.collection.add(
            {"user_id": user_id, "messages": messages}
        )
        document_snapshot = document_ref.get()

        if document_snapshot.exists:
            return {"id": document_ref.id, **document_snapshot.to_dict()}
        else:
            return None
