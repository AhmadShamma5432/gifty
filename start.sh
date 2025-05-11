#!/bin/bash

source myenv/bin/activate
export DJANGO_SETTINGS_MODULE=foodordering.settings
uvicorn --host 0.0.0.0 --port 8000 --interface asgi3 foodordering.asgi:application --reload
# daphne -p 8000 -b 0.0.0.0 foodordering.asgi:application
# uvicorn foodordering.asgi:application --host 0.0.0.0 --port 8000 --reload