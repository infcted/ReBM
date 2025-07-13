# ReBM Slack Bot

A Slack bot for managing node reservations in the ReBM system.

## Features
- Slash commands for node management
- Socket Mode (no public endpoint required)
- Async, FastAPI-compatible

## Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
2. **Create a `.env` file** (copy from `env.example` and fill in your real tokens)
3. **Run the bot**
   ```bash
   python main.py
   ```

## Required Environment Variables
- `SLACK_BOT_TOKEN` (starts with `xoxb-`)
- `SLACK_SIGNING_SECRET`
- `SLACK_APP_TOKEN` (starts with `xapp-`)
- `REBM_API_URL` (default: http://localhost:8000)

## Slash Commands
- `/rebm-help`
- `/rebm-list`
- `/rebm-status <node>`
- `/rebm-reserve <node> [hours]`
- `/rebm-release <node>`
- `/rebm-create <node> [desc]`
- `/rebm-delete <node>`
- `/rebm-cleanup` 