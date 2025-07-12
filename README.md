# ReBM - Reserved By Me

A system for managing node reservations with real-time status tracking, web interface, and automated node monitoring.

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
