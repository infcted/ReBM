# ReBM - Reserved By Me

A system for managing node reservations with real-time status tracking, web interface, and automated node monitoring.

---

## Chat Bot Interface

ReBM includes a pluggable chat bot interface for managing node reservations directly from your team’s chat platform. The current implementation is for Slack, but the architecture allows for future support of other platforms (e.g., Microsoft Teams, Discord).

### Features
- List all nodes and their status
- Reserve nodes for a specific duration (with flexible time formats)
- Release node reservations
- Create and delete nodes
- Clean up expired reservations
- User attribution for all actions
- Duration rounding is clearly indicated
- Robust error handling for node existence and duration parsing
- Multi-word node names supported
- All messages are public in the chat channel where the command is used

### Supported Platforms
- **Slack** (current)
- _Pluggable: Teams, Discord, etc. (future)_

### Slash Commands (Slack Example)
| Command                              | Description                        |
|---------------------------------------|------------------------------------|
| `/rebm-help`                         | Show help and usage                |
| `/rebm-list`                         | List all nodes                     |
| `/rebm-status <node>`                | Show status of a node              |
| `/rebm-reserve <node> [duration]`    | Reserve a node (e.g. `1h`, `2 days`, `90m`) |
| `/rebm-release <node>`               | Release a node                     |
| `/rebm-create <node> [desc]`         | Create a new node                  |
| `/rebm-delete <node>`                | Delete a node                      |
| `/rebm-cleanup`                      | Clean up expired reservations      |

**Duration formats:**  
- Single word: `1w`, `2d`, `12h`, `90m`, `24`  
- Two words: `1 week`, `2 days`, `12 hours`, `90 minutes`  
- Plain number: `24` (assumes hours)

### Setup (Slack)
1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
2. **Create a `.env` file** (copy from `env.example` and fill in your real tokens)
3. **(Recommended) Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```
4. **Run the bot**
   ```bash
   python main.py
   ```

### Required Environment Variables (Slack)
- `SLACK_BOT_TOKEN` (starts with `xoxb-`)
- `SLACK_SIGNING_SECRET`
- `SLACK_APP_TOKEN` (starts with `xapp-`)
- `REBM_API_URL` (default: http://localhost:8000)

### Slash Commands Registration (Slack)
- **Recommended:** Use the `slack-app-manifest.yaml` file to register all slash commands in your Slack app settings.
- **Avoid duplicate commands:** Only use the manifest, do not use a registration script.
- **Check your Slack app settings** for duplicate commands and remove extras if needed.

### Security & Release Checklist
- [x] Do **not** commit `.env` or any real secrets. Only include `env.example` with placeholders.
- [x] Do **not** commit your virtual environment (`venv/`, `.venv/`, `env/`, or `slack-bot/`).
- [x] Delete or `.gitignore` any log files (e.g., `slack-bot.log`).
- [x] All code and config is committed, no secrets in git history.
- [x] README is up to date.
- [x] Test all commands in Slack before release.

---

## System Overview

ReBM consists of three main components:

- **API Server** (`api/`) - FastAPI backend with DynamoDB storage
- **Web UI** (`web-ui/`) - React/TypeScript frontend for node management
- **ReBM Linux** (`rebm-linux/`) - Linux service for node status monitoring

## Quick Start

### Prerequisites

- **For API**: Python 3.8+, AWS credentials (for DynamoDB)
- **For Web UI**: Node.js 16+, npm
- **For ReBM Linux**: Python 3.6+, systemd (Linux)

### 1. Start the API Server

```bash
cd api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 2. Start the Web UI

```bash
cd web-ui
npm install
npm start
```

The web interface will be available at `http://localhost:3000`

### 3. Install ReBM Linux (Optional)

For each node you want to monitor:

```bash
cd rebm-linux
sudo chmod +x install.sh
sudo ./install.sh
```

## Features

### Core Functionality
- **Node Management**: Create, view, reserve, release, and delete nodes
- **Real-time Status**: Live status indicators and automatic updates
- **Expiration Tracking**: Automatic cleanup of expired reservations
- **Web Interface**: Modern, responsive UI built with React and Tailwind CSS
- **RESTful API**: FastAPI backend with comprehensive endpoints
- **Persistent Storage**: DynamoDB backend for reliable data storage

### Node Monitoring
- **MOTD Updates**: Automatic `/etc/motd` updates with reservation status
- **Health Checks**: Periodic node status verification
- **Auto-registration**: Nodes automatically register themselves
- **Service Management**: Systemd services for reliable operation

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/nodes/` | List all nodes |
| `GET` | `/nodes/{node}` | Get specific node |
| `POST` | `/nodes/` | Create new node |
| `DELETE` | `/nodes/{node}` | Delete node |
| `POST` | `/nodes/{node}/reserve` | Reserve node |
| `POST` | `/nodes/{node}/release` | Release node |
| `POST` | `/nodes/cleanup/expired` | Cleanup expired nodes |
| `GET` | `/health` | Health check |

## Configuration

### Environment Variables

**API Server**:
```bash
NODE_STORE_BACKEND=dynamodb  # Storage backend
NODE_STORE_TABLE_NAME=ReBM-dev  # DynamoDB table name
```

**Web UI**:
```bash
REACT_APP_API_URL=http://localhost:8000  # API endpoint
```

**ReBM Linux**:
```bash
REBM_API_URL=http://your-api:8000  # API endpoint
NODE_NAME=my-node  # Node identifier
CHECK_INTERVAL_SECONDS=300  # Check interval (5 minutes)
```

## Monitoring and Logs

### API Server
```bash
# View API logs
tail -f api.log

# Health check
curl http://localhost:8000/health
```

### ReBM Linux
```bash
# Check service status
sudo systemctl status rebm-linux.service

# View logs
sudo journalctl -u rebm-linux.service -f
```

## Development

### API Development
```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload
```

### Web UI Development
```bash
cd web-ui
npm install
npm start
```

### Testing
```bash
# API tests
cd api
pytest

# Web UI tests
cd web-ui
npm test
```
