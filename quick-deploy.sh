#!/bin/bash
# Quick Docker Deployment Script for Industrial PLC Simulator
# Run this on your server!

echo "=== Industrial PLC Simulator - Quick Docker Deploy ==="
echo "This will have your PLC simulator running in under 5 minutes!"
echo

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker not found. Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    echo "Docker installed! Please log out and back in, then run this script again."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Get the repository
echo "Enter your GitHub username (or press Enter to use DigitalEnergyR):"
read GITHUB_USER
GITHUB_USER=${GITHUB_USER:-DigitalEnergyR}

echo
echo "Cloning repository..."
git clone https://github.com/$GITHUB_USER/industrial-plc-simulator.git 2>/dev/null || {
    echo "Repository not found. Make sure you've pushed to GitHub!"
    echo "Try: https://github.com/$GITHUB_USER/industrial-plc-simulator"
    exit 1
}

cd industrial-plc-simulator

# Start the service
echo "Starting PLC Simulator with Docker..."
docker-compose up -d

# Wait for startup
echo "Waiting for service to start..."
sleep 5

# Check if running
if docker ps | grep industrial-plc-simulator > /dev/null; then
    echo
    echo "✅ SUCCESS! Industrial PLC Simulator is running!"
    echo
    echo "Access your PLC simulator at:"
    echo "  Local: http://localhost:8001"
    echo "  Remote: http://$(curl -s ifconfig.me):8001"
    echo
    echo "Web Interface: http://$(curl -s ifconfig.me):8001/"
    echo
    echo "Useful commands:"
    echo "  View logs: docker logs -f industrial-plc-simulator"
    echo "  Stop: docker-compose down"
    echo "  Restart: docker-compose restart"
    echo "  Update: git pull && docker-compose up -d --build"
else
    echo "❌ Failed to start. Check logs with: docker logs industrial-plc-simulator"
    exit 1
fi