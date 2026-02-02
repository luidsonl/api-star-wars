from google.cloud import firestore
import os


class FirestoreProxy:
    def __init__(self):
        self._db = None

    @property
    def db(self):
        if self._db is None:
            project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
            database_id = os.environ.get("FIRESTORE_DATABASE", "(default)")
            self._db = firestore.Client(project=project_id, database=database_id)
        return self._db

    def __getattr__(self, name):
        return getattr(self.db, name)

db = FirestoreProxy()
