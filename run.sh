#!/bin/bash
source venv/bin/activate
export PYTHONPATH=$PYTHONPATH:.
export JWT_SECRET_KEY="star-wars-super-secret-key-that-is-at-least-32-chars-long"
functions-framework --target=api_star_wars --debug
