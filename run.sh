#!/bin/bash
source venv/bin/activate
export PYTHONPATH=$PYTHONPATH:.
export JWT_SECRET_KEY="star-wars-secret-key-123"
functions-framework --target=api_star_wars --debug
