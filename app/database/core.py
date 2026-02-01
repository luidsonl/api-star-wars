from google.cloud import firestore
import os

# Initialize Firestore client lazily
# In production (Cloud Functions), it uses the default credentials.
# For local development, you can set GOOGLE_APPLICATION_CREDENTIALS
# or use the firestore emulator if configured.

class FirestoreProxy:
    def __init__(self):
        self._db = None

    @property
    def db(self):
        if self._db is None:
            # This only fails if we actually try to use it without project ID
            self._db = firestore.Client()
        return self._db

    def __getattr__(self, name):
        return getattr(self.db, name)

db = FirestoreProxy()
