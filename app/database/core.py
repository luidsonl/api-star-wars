from google.cloud import firestore
import os

# Initialize Firestore client
# In production (Cloud Functions), it uses the default credentials.
# For local development, you can set GOOGLE_APPLICATION_CREDENTIALS
# or use the firestore emulator if configured.
db = firestore.Client()
