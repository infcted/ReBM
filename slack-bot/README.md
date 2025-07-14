# ReBM Slack Bot

A Slack bot for managing node reservations in the ReBM system.

## Features
- List all nodes and their status
- Reserve nodes for a specific duration (with flexible time formats)
- Release node reservations
- Create and delete nodes
- Clean up expired reservations
- User attribution for all actions
- Duration rounding is clearly indicated
- Robust error handling for node existence and duration parsing
- Multi-word node names supported
- All messages are public in Slack and sent to the channel where the command is used

## Slash Commands

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

## Slash Commands Registration
- **Recommended:** Use the `slack-app-manifest.yaml` file to register all slash commands in your Slack app settings.
- **Avoid duplicate commands:** Only use the manifest, do not use a registration script.
- **Check your Slack app settings** for duplicate commands and remove extras if needed.

## Security & Release Checklist
- [x] Do **not** commit `.env` or any real secrets. Only include `env.example` with placeholders.
- [x] Do **not** commit your virtual environment (`venv/`, `.venv/`, `env/`, or `slack-bot/`).
- [x] Delete or `.gitignore` any log files (e.g., `slack-bot.log`).
- [x] All code and config is committed, no secrets in git history.
- [x] README is up to date.
- [x] Test all commands in Slack before release.

## .gitignore
A best-practice `.gitignore` is included to ignore venvs, logs, and secrets.

---

**You are ready to release!**
