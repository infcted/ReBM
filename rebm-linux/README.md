# Simple ReBM Node Monitor

A minimal Linux service that checks node reservation status and updates MOTD.

## What it does

- Checks if the current node exists in ReBM system
- Creates the node if it doesn't exist
- Updates `/etc/motd` with current reservation status
- Runs every 5 minutes

## Quick Install

```bash
sudo chmod +x simple_install.sh
sudo ./simple_install.sh
```

## Manual Install

```bash
# Copy files
sudo mkdir -p /opt/node-monitor
sudo cp simple_monitor.py /opt/node-monitor/
sudo cp simple-monitor.service /etc/systemd/system/

# Install requests
sudo pip3 install requests

# Enable service
sudo systemctl daemon-reload
sudo systemctl enable simple-monitor.service
sudo systemctl start simple-monitor.service
```

## Configuration

Edit `/etc/systemd/system/simple-monitor.service`:

```ini
[Service]
Environment=REBM_API_URL=http://your-api:8000
Environment=NODE_NAME=my-node
Environment=CHECK_INTERVAL_SECONDS=300
```

## Usage

```bash
# Check status
sudo systemctl status simple-monitor.service

# View logs
sudo journalctl -u simple-monitor.service -f

# Test manually
sudo python3 /opt/node-monitor/simple_monitor.py --once
```

## MOTD Output

```
==================================================
ReBM Node: my-node-01
==================================================

🟢 AVAILABLE
   Updated: 2h ago

==================================================
```

Or when reserved:

```
==================================================
ReBM Node: my-node-01
==================================================

🔴 RESERVED
   By: john.doe
   Expires: 1d 3h left

==================================================
```

That's it! Much simpler than the original version. 