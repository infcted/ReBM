#!/bin/bash

# ReBM Linux Monitor Installer

echo "Installing ReBM Linux Monitor..."

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

# Create directory
mkdir -p /opt/rebm-linux

# Copy files
cp node_monitor.py /opt/rebm-linux/
cp rebm-linux.service /etc/systemd/system/

# Install requests if not present
python3 -c "import requests" 2>/dev/null || pip3 install requests

# Make executable
chmod +x /opt/rebm-linux/node_monitor.py

# Enable and start service
systemctl daemon-reload
systemctl enable rebm-linux.service
systemctl start rebm-linux.service

echo "Installation complete!"
echo "Service status: $(systemctl is-active rebm-linux.service)"
echo ""
echo "Commands:"
echo "  systemctl status rebm-linux.service"
echo "  systemctl restart rebm-linux.service"
echo "  journalctl -u rebm-linux.service -f" 