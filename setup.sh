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

echo "[3/4] Installing Docker CLI plugins (compose + buildx)..."
# Amazon Linux 2023 ships Docker without the compose and buildx plugins, so fetch them directly.
PLUGIN_DIR=/usr/local/lib/docker/cli-plugins
sudo mkdir -p "$PLUGIN_DIR"

case "$(uname -m)" in
    x86_64)  BUILDX_ARCH=amd64 ;;
    aarch64) BUILDX_ARCH=arm64 ;;
    *) echo "Unsupported architecture: $(uname -m)"; exit 1 ;;
esac

if ! sudo docker compose version &> /dev/null; then
    sudo curl -fsSL \
        "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-$(uname -m)" \
        -o "$PLUGIN_DIR/docker-compose"
    sudo chmod +x "$PLUGIN_DIR/docker-compose"
fi

# "compose build" delegates to buildx and rejects anything older than 0.17.0.
BUILDX_HAVE=$(sudo docker buildx version 2>/dev/null | awk '{print $2}' | tr -d 'v')
if [ -z "$BUILDX_HAVE" ] || [ "$(printf '%s\n0.17.0\n' "$BUILDX_HAVE" | sort -V | head -1)" != "0.17.0" ]; then
    # The API is unauthenticated here and can be rate-limited, so fall back to a known-good tag.
    BUILDX_TAG=$(curl -fsSL https://api.github.com/repos/docker/buildx/releases/latest 2>/dev/null \
        | grep -m1 '"tag_name"' | cut -d'"' -f4)
    BUILDX_TAG=${BUILDX_TAG:-v0.36.1}
    sudo curl -fsSL \
        "https://github.com/docker/buildx/releases/download/${BUILDX_TAG}/buildx-${BUILDX_TAG}.linux-${BUILDX_ARCH}" \
        -o "$PLUGIN_DIR/docker-buildx"
    sudo chmod +x "$PLUGIN_DIR/docker-buildx"
fi

echo "[4/4] Building and starting backend + frontend..."
sudo docker rm -f ai-workbench 2>/dev/null || true
sudo docker compose up -d --build

PUBLIC_IP=$(curl -fsS --max-time 3 http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo "<YOUR-EC2-PUBLIC-IP>")

echo ""
echo "=== Setup Complete ==="
echo "API      : http://${PUBLIC_IP}:8000"
echo "Frontend : http://${PUBLIC_IP}:8501"
echo ""
echo "Test the API locally:"
echo "  curl http://localhost:8000/health"
echo ""
echo "Make sure your Security Group allows inbound TCP on ports 8000 and 8501."
