from typing import Dict

from google.cloud import firestore

from firebase.client.FirestoreClient import FirestoreClient


class ConversationsRepo:
    def __init__(self):
        self.db = FirestoreClient.get_client()
        self.collection = self.db.collection("conversations")

    def create_conversation(self, messages, user_id, title):
        _, document_ref = self.collection.add(
            {"user_id": user_id, "title": title, "messages": messages}
        )
        document_snapshot = document_ref.get()

        if document_snapshot.exists:
            return {"id": document_ref.id, **document_snapshot.to_dict()}
        else:
            return None

    def update_with_messages(self, conversation_id, pair_messages):
        doc_ref = self.db.collection("conversations").document(conversation_id)
        doc = doc_ref.get()

        if not doc.exists:
            return None

        return doc_ref.update({"messages": firestore.ArrayUnion(pair_messages)})

    def fetch_user_conversation(self, conversation_id):
        doc_ref = self.db.collection("conversations").document(conversation_id)
        doc = doc_ref.get()

        if not doc.exists:
            return None

        return doc.to_dict()

    def get_conversations_by_user(self, user_id):
        query = self.collection.where(
            filter=firestore.FieldFilter("user_id", "==", user_id)
        )
        docs = query.stream()

        conversations = []
        for doc in docs:
            doc_data = doc.to_dict()
            conversations.append(
                {"id": doc.id, "title": doc_data.get("title", "Untitled")}
            )

        return conversations
