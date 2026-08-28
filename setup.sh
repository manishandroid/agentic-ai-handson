#!/bin/bash
# AI Workbench — EC2 Bootstrap Script
# Run this on a fresh Amazon Linux 2023 / Ubuntu EC2 instance.
# Usage: chmod +x setup.sh && ./setup.sh

set -e

cd "$(dirname "$0")"

echo "=== AI Workbench EC2 Setup ==="
echo ""

if [ ! -f .env ]; then
    echo "Missing .env — copy .env.example to .env and fill in OPENAI_API_KEY."
    exit 1
fi

# Detect OS and install Docker
if command -v dnf &> /dev/null; then
    echo "[1/4] Installing Docker (Amazon Linux)..."
    sudo dnf update -y -q
    sudo dnf install -y docker
elif command -v apt-get &> /dev/null; then
    echo "[1/4] Installing Docker (Ubuntu)..."
    sudo apt-get update -qq
    sudo apt-get install -y docker.io
else
    echo "Unsupported OS. Install Docker manually."
    exit 1
fi

echo "[2/4] Starting Docker service..."
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

echo "[3/4] Building the AI Workbench container..."
# Context is the project root because the Dockerfile copies the shared requirements.txt.
sudo docker build -f week3/backend/Dockerfile -t ai-workbench-api .

echo "[4/4] Running the container..."
sudo docker rm -f ai-workbench 2>/dev/null || true
sudo docker run -d \
    --name ai-workbench \
    --restart unless-stopped \
    -p 8000:8000 \
    --env-file .env \
    ai-workbench-api

echo ""
echo "=== Setup Complete ==="
echo "Your AI Workbench API is running on port 8000."
echo ""
echo "Test it:"
echo "  curl http://localhost:8000/health"
echo ""
echo "From outside (use your EC2 public IP):"
echo "  curl http://<YOUR-EC2-PUBLIC-IP>:8000/health"
echo ""
echo "Make sure your Security Group allows inbound TCP on port 8000."
