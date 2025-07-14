# ReBM Slack Bot

A Slack bot for managing node reservations in the ReBM system.

## Features
- Slash commands for node management
- Socket Mode (no public endpoint required)
- Async, FastAPI-compatible
- User attribution for all actions
- Duration rounding is clearly indicated
- Robust error handling for node existence and duration parsing
- Multi-word node names supported

## Setup

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

## Required Environment Variables
- `SLACK_BOT_TOKEN` (starts with `xoxb-`)
- `SLACK_SIGNING_SECRET`
- `SLACK_APP_TOKEN` (starts with `xapp-`)
- `REBM_API_URL` (default: http://localhost:8000)

## Slash Registration
- **Recommended:** Use the `slack-app-manifest.yaml` file to register all slash commands in your Slack app settings.
