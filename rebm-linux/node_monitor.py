"""
ReBM Linux Node Monitor
Copyright (c) 2024 Oscar Baeza
Licensed under the MIT License
"""

import os
import sys
import time
import socket
import requests
from datetime import datetime, timezone

# Configuration
API_URL = os.getenv('REBM_API_URL', 'http://localhost:8000')
NODE_NAME = os.getenv('NODE_NAME', socket.gethostname())
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL_SECONDS', '300'))  # 5 minutes

def get_node_status():
    """Get current node status from API"""
    try:
        response = requests.get(f"{API_URL}/nodes/{NODE_NAME}", timeout=5)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            # Create node if it doesn't exist
            create_node()
            return get_node_status()
        else:
            print(f"API error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Connection error: {e}")
        return None

def create_node():
    """Create node in system if it doesn't exist"""
    try:
        data = {"node": NODE_NAME, "hostname": socket.gethostname()}
        response = requests.post(f"{API_URL}/nodes/", json=data, timeout=5)
        if response.status_code == 200:
            print(f"Created node: {NODE_NAME}")
        else:
            print(f"Failed to create node: {response.status_code}")
    except Exception as e:
        print(f"Error creating node: {e}")

def format_time(time_str):
    """Format time duration"""
    if not time_str:
        return "unknown"
    try:
        start = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        duration = now - start
        
        if duration.days > 0:
            return f"{duration.days}d {duration.seconds // 3600}h"
        elif duration.seconds > 3600:
            return f"{duration.seconds // 3600}h {(duration.seconds % 3600) // 60}m"
        else:
            return f"{duration.seconds // 60}m"
    except:
        return "unknown"

def format_expiry(expires_at):
    """Format expiry time"""
    if not expires_at:
        return ""
    try:
        expiry = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        
        if expiry <= now:
            return "EXPIRED"
        
        time_left = expiry - now
        if time_left.days > 0:
            return f"{time_left.days}d {time_left.seconds // 3600}h left"
        elif time_left.seconds > 3600:
            return f"{time_left.seconds // 3600}h {time_left.seconds % 3600 // 60}m left"
        else:
            return f"{time_left.seconds // 60}m left"
    except:
        return "unknown"

def update_motd(node_data):
    """Update MOTD with node status"""
    try:
        motd = []
        motd.append("=" * 50)
        motd.append(f"ReBM Node: {NODE_NAME}")
        motd.append("=" * 50)
        motd.append("")
        
        if not node_data:
            motd.append("❌ Node not found")
        else:
            status = node_data.get('status', 'unknown')
            if status == 'available':
                motd.append("🟢 AVAILABLE")
                if node_data.get('updated_at'):
                    motd.append(f"   Updated: {format_time(node_data['updated_at'])} ago")
            elif status == 'reserved':
                motd.append("🔴 RESERVED")
                if node_data.get('reserved_by'):
                    motd.append(f"   By: {node_data['reserved_by']}")
                if node_data.get('expires_at'):
                    motd.append(f"   Expires: {format_expiry(node_data['expires_at'])}")
            else:
                motd.append(f"❓ Status: {status}")
        
        motd.append("")
        motd.append("=" * 50)
        motd.append("")
        
        with open('/etc/motd', 'w') as f:
            f.write('\n'.join(motd))
            
        print(f"Updated MOTD - Status: {node_data.get('status') if node_data else 'not found'}")
        
    except PermissionError:
        print("Permission denied writing to MOTD")
    except Exception as e:
        print(f"Error updating MOTD: {e}")

def main():
    """Main function"""
    print(f"Starting monitor for node: {NODE_NAME}")
    print(f"API: {API_URL}")
    print(f"Check interval: {CHECK_INTERVAL}s")
    
    while True:
        try:
            node_data = get_node_status()
            update_motd(node_data)
            time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print("Stopping monitor")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        node_data = get_node_status()
        update_motd(node_data)
    else:
        main() 