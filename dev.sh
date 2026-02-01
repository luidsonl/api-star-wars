#!/bin/bash
source venv/bin/activate

export PYTHONPATH=$PYTHONPATH:.
export JWT_SECRET_KEY="star-wars-super-secret-key-that-is-at-least-32-chars-long"

# Local Emulator
export FIRESTORE_EMULATOR_HOST="[::1]:8480"

# Cloud Project
export GOOGLE_CLOUD_PROJECT="star-wars-api-test"

python app/main.py