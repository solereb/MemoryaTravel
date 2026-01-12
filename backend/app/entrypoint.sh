#!/bin/bash

source /app/venv/bin/activate

python country_adding.py
python regions_adding.py

exec uvicorn src.main:app --host 0.0.0.0 --port 8000