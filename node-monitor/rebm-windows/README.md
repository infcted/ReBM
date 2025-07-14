# Simple ReBM Node Monitor (Windows)

A minimal Windows service that checks node reservation status and updates a status file.

## What it does

- Checks if the current node exists in ReBM system
- Creates the node if it doesn't exist
- Updates `C:\ReBM\motd.txt` with current reservation status
- Runs every 5 minutes as a Windows service

## Quick Install

```powershell
# Run as Administrator
powershell -ExecutionPolicy Bypass -File install.ps1
```

## Manual Install

1. Install Python 3 (if not already installed)
2. Install dependencies:
   ```powershell
   pip install requests
   ```
3. Copy files to `C:\ReBM`:
   - `node_monitor.py`
   - `install.ps1`
4. Run `install.ps1` as Administrator to set up the service

## Configuration

Edit environment variables in the Windows service (via `services.msc` or the install script):
- `REBM_API_URL` (default: http://localhost:8000)
- `NODE_NAME` (default: computer hostname)
- `CHECK_INTERVAL_SECONDS` (default: 300)

## Usage

- The service will write status to `C:\ReBM\motd.txt`
- Optionally, add the following to your PowerShell profile to display the status on session start:
  ```powershell
  if (Test-Path 'C:\ReBM\motd.txt') { Get-Content 'C:\ReBM\motd.txt' }
  ```
- To check service status:
  - Open `services.msc` and look for `ReBM Windows Monitor`
  - Or use PowerShell: `Get-Service -Name 'ReBMWindowsMonitor'`

## Example Output

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