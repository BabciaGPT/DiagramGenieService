from typing import Dict

from google.cloud import firestore

from firebase.client.FirestoreClient import FirestoreClient


class ProjectsRepo:
    def __init__(self):
        self.db = FirestoreClient.get_client()
        self.collection = self.db.collection("projects")

    def create_project(self, user_id, title, description):
        _, document_ref = self.collection.add(
            {
                "user_id": user_id,
                "title": title,
                "description": description,
                "diagrams": [],
            }
        )
        document_snapshot = document_ref.get()

        if document_snapshot.exists:
            return {"id": document_ref.id, **document_snapshot.to_dict()}
        else:
            return None

    def append_message_to_diagrams(self, project_id, message: dict):
        doc_ref = self.collection.document(project_id)
        doc = doc_ref.get()

        if not doc.exists:
            return None

        try:
            doc_ref.update({"diagrams": firestore.ArrayUnion([message])})
            return True
        except Exception:
            return False

    def fetch_user_project(self, project_id):
        doc_ref = self.db.collection("projects").document(project_id)
        doc = doc_ref.get()

        if not doc.exists:
            return None

        return doc.id, doc.to_dict()

    def get_projects_by_user(self, user_id):
        query = self.collection.where(
            filter=firestore.FieldFilter("user_id", "==", user_id)
        )
        docs = query.stream()

        projects = []
        for doc in docs:
            doc_data = doc.to_dict()
            projects.append({"id": doc.id, "project": doc_data})

        return projects

    def delete_project(self, project_id):
        try:
            doc_ref = self.collection.document(project_id)
            doc_ref.delete()
            return True
        except Exception:
            return False
