#!/bin/bash
# build.sh - Custom build script for deployment platforms

# Print environment information for debugging
echo "Python version: $(python --version)"
echo "Working directory: $(pwd)"

# Upgrade pip
pip install --upgrade pip

# Install core dependencies first (without pulling in transitive dependencies)
echo "Installing core dependencies..."
pip install fastapi uvicorn[standard] python-multipart jinja2 python-dotenv pytz typing-extensions requests httpcore httpx --no-deps

# Install vapi-python specifically without its dependencies
echo "Installing vapi-python without dependencies..."
pip install vapi-python --no-deps

# Now install remaining dependencies from requirements.txt
echo "Installing remaining dependencies from requirements.txt..."
pip install -r requirements.txt --no-deps

# Final check to ensure all dependencies are resolved
echo "Finalizing dependency installation..."
pip install fastapi uvicorn[standard] python-multipart jinja2 python-dotenv pytz typing-extensions requests httpcore httpx

# Print installed packages for verification
echo "Installed packages:"
pip list

echo "Build completed successfully!"