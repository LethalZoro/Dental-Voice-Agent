#!/bin/bash
# build.sh - Custom build script for deployment platforms

# Upgrade pip
pip install --upgrade pip

# Install dependencies excluding PyAudio
pip install -r requirements.txt --no-deps
pip install vapi-python --no-deps
pip install fastapi uvicorn[standard] python-multipart jinja2 python-dotenv pytz typing-extensions requests httpcore httpx