#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Starting deployment of WhatsApp SaaS Platform..."

# Update system packages
sudo apt update
sudo apt upgrade -y

# Install Python and pip if not already installed
sudo apt install -y python3.10 python3-pip

# Install MongoDB
sudo apt install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb

# Install Redis
sudo apt install -y redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Navigate to the application directory
cd /home/ubuntu/whatsapp_saas

# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI application using Gunicorn (for production)
# For development, you can use: uvicorn app.main:app --host 0.0.0.0 --port 8000
# We'll use a simple uvicorn command for demonstration, but Gunicorn is recommended for production.
# You might want to use a process manager like systemd or supervisor to keep it running.

echo "Deployment complete. You can now run the applications."

# Example of how to run (for development/testing):
# uvicorn app.main:app --host 0.0.0.0 --port 8000
