#!/bin/bash
# Deployment script for Industrial PLC Simulator
# Run on Ubuntu/Debian server

set -e

echo "=== Industrial PLC Simulator Deployment Script ==="
echo "Digital Energy Services - www.digitalenergyservices.ca"
echo

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Update system
echo "1. Updating system packages..."
apt-get update
apt-get upgrade -y

# Install dependencies
echo "2. Installing dependencies..."
apt-get install -y python3 python3-pip nginx certbot python3-certbot-nginx git

# Create service user
echo "3. Creating service user..."
useradd -r -s /bin/false plc-service || echo "User already exists"

# Create directories
echo "4. Creating directories..."
mkdir -p /opt/plc-simulator
mkdir -p /opt/plc-simulator/logs
mkdir -p /var/www/plc-simulator/docs

# Clone or update repository
echo "5. Installing PLC Simulator..."
cd /opt/plc-simulator
if [ -d ".git" ]; then
    git pull
else
    git clone https://github.com/Digital-Energy/industrial-plc-simulator.git .
fi

# Set permissions
chown -R plc-service:plc-service /opt/plc-simulator
chmod -R 755 /opt/plc-simulator

# Install systemd service
echo "6. Installing systemd service..."
cp deploy/plc-simulator.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable plc-simulator
systemctl start plc-simulator

# Check service status
sleep 3
if systemctl is-active --quiet plc-simulator; then
    echo "✓ PLC Simulator service is running"
else
    echo "✗ PLC Simulator service failed to start"
    systemctl status plc-simulator
    exit 1
fi

# Install nginx configuration
echo "7. Configuring nginx..."
cp deploy/nginx.conf /etc/nginx/sites-available/plc-simulator
ln -sf /etc/nginx/sites-available/plc-simulator /etc/nginx/sites-enabled/

# Test nginx configuration
nginx -t

# Get SSL certificate (interactive - requires domain to be pointed to this server)
echo "8. Setting up SSL certificate..."
echo "Make sure plc.digitalenergyservices.ca points to this server's IP address"
read -p "Press Enter to continue with SSL setup (or Ctrl+C to skip)..."
certbot --nginx -d plc.digitalenergyservices.ca

# Restart nginx
systemctl restart nginx

echo
echo "=== Deployment Complete ==="
echo "PLC Simulator is now available at:"
echo "  HTTP:  http://plc.digitalenergyservices.ca:8001"
echo "  HTTPS: https://plc.digitalenergyservices.ca"
echo
echo "API Endpoints:"
echo "  GET  https://plc.digitalenergyservices.ca/tags"
echo "  GET  https://plc.digitalenergyservices.ca/read?tags=TAG1,TAG2"
echo "  GET  https://plc.digitalenergyservices.ca/areas"
echo "  GET  https://plc.digitalenergyservices.ca/alarms"
echo "  POST https://plc.digitalenergyservices.ca/write"
echo
echo "To check service status: systemctl status plc-simulator"
echo "To view logs: journalctl -u plc-simulator -f"