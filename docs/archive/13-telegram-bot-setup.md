# Telegram Bot Setup and Usage

This guide covers setting up and using the Risk Agent Telegram bot for remote access to your AI-powered risk intelligence assistant.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the Bot](#running-the-bot)
- [Usage](#usage)
- [Session Management](#session-management)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)

## Overview

The Risk Agent Telegram bot provides:

- **Remote Access**: Interact with Risk Agent from anywhere via Telegram
- **Session Persistence**: Conversations are saved and resume automatically
- **Multi-User Support**: Each Telegram user gets their own isolated session
- **Working Directory Control**: Set custom working directories per user
- **Verbose Mode**: Toggle detailed output for debugging
- **Full Feature Access**: All CLI capabilities available via Telegram

### Architecture

```
Telegram User → python-telegram-bot → telegram_bot.py
                                            ↓
                                    RiskAgentSession
                                      (per user)
                                            ↓
                                    ClaudeSDKClient
                                      (with resume)
                                            ↓
                                   Risk Intelligence Engine
                                            ↓
                                    Change-Agent → Skills
```

## Prerequisites

1. **Telegram Account**: You need a Telegram account
2. **Bot Token**: Create a bot via [@BotFather](https://t.me/botfather)
3. **Dependencies**: Install with `uv sync` (includes `python-telegram-bot>=20.0`)
4. **API Key**: Anthropic API key (same as CLI)

## Setup

### Step 1: Create Your Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow prompts to choose a name and username
4. **Save the bot token** (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

Example:
```
You: /newbot
BotFather: Alright, a new bot. How are we going to call it?
You: Risk Agent
BotFather: Good. Now let's choose a username for your bot.
You: my_riskagent_bot
BotFather: Done! Here's your token: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

### Step 2: Set Environment Variables

```bash
# Required: Telegram bot token
export TELEGRAM_BOT_TOKEN="your-bot-token-here"

# Required: Anthropic API key (if not already set)
export ANTHROPIC_API_KEY="your-api-key-here"
```

Add to your shell profile for persistence:

```bash
# ~/.zshrc or ~/.bash_profile
export TELEGRAM_BOT_TOKEN="123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Step 3: Install Dependencies

```bash
# Install/update dependencies
uv sync
```

This installs:
- `python-telegram-bot>=20.0` (Telegram API wrapper)
- All other Risk Agent dependencies

## Running the Bot

### Option 1: Using the Command Script

```bash
uv run riskagent-telegram
```

### Option 2: Direct Python Execution

```bash
uv run python -m src.telegram_bot
```

### Option 3: Background Process (Production)

```bash
# Using nohup
nohup uv run riskagent-telegram > telegram_bot.log 2>&1 &

# Using systemd (Linux)
# See "Production Deployment" section below
```

### Verify It's Running

You should see:
```
INFO - Starting Risk Agent Telegram Bot...
INFO - Application started
```

Now open Telegram and search for your bot by username (e.g., `@my_riskagent_bot`).

## Usage

### Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Welcome message | `/start` |
| `/help` | Show help and capabilities | `/help` |
| `/status` | Show session status | `/status` |
| `/setcwd <path>` | Set working directory | `/setcwd /Users/name/projects/myapp` |
| `/verbose` | Toggle verbose mode | `/verbose` |
| `/reset` | Clear conversation history | `/reset` |

### Basic Usage

1. **Start the bot**:
   ```
   You: /start
   Bot: 👋 Welcome to Risk Agent, [Name]!
   ```

2. **Ask a question**:
   ```
   You: Help me plan a Basel IV implementation project
   Bot: 🤖 Risk Agent:
        I'll help you create a comprehensive project plan...
   ```

3. **Check status**:
   ```
   You: /status
   Bot: Session Status
        User ID: 123456789
        Session ID: sess_abc123xyz
        Working Dir: /Users/name/projects/riskagent
        Verbose: Off
   ```

### Working with Files

#### Example: ITC Template Filling

1. **Set working directory** (where your templates/files are):
   ```
   You: /setcwd /Users/name/Documents/templates
   Bot: ✅ Working directory set to: /Users/name/Documents/templates
   ```

2. **Request skill execution**:
   ```
   You: Fill the ITC template using meeting_notes.docx
   Bot: 🔧 Skill: itc-template-filler
        Arguments: {...}
   Bot: ✅ Skill Result: itc-template-filler
        ITC template populated successfully!
        Output: ITC_20250109.xlsx
   ```

3. **Files are saved in your working directory**:
   ```
   /Users/name/Documents/templates/ITC_20250109.xlsx
   ```

### Verbose Mode

Enable verbose mode to see all tool calls (Read, Write, Bash, etc.):

```
You: /verbose
Bot: 🔧 Verbose mode enabled
     All tool calls and results will be shown

You: Read the README.md file
Bot: 🔨 Tool: Read
     Input: {"file_path": "/path/to/README.md"}
Bot: 📋 Result: [file contents]
Bot: 🤖 Risk Agent: Here's what I found in README.md...
```

## Session Management

### How Sessions Work

Each Telegram user gets:

1. **Persistent Session File**: Stored at `~/.riskagent/telegram_sessions/{user_id}.json`
2. **Session ID**: Resumes conversations with Anthropic's servers
3. **Working Directory**: Custom CWD per user
4. **Preferences**: Verbose mode setting

### Session File Format

```json
{
  "session_id": "sess_abc123xyz",
  "cwd": "/Users/name/projects/myproject",
  "verbose": false,
  "last_updated": "2025-01-09T12:00:00Z"
}
```

### Session Lifecycle

```
First Message → Create Session → Save to disk
Next Message  → Load Session   → Resume conversation
Reset Command → Clear session_id → Start fresh (keeps CWD)
```

### Reset vs. New Session

- **`/reset`**: Clears conversation history but keeps your working directory
- **New User**: Creates fresh session with default CWD (bot's current directory)

### Multiple Working Directories

Each user can work on different projects:

```
User A: /setcwd /Users/name/projects/project1
User B: /setcwd /Users/name/projects/project2
User C: /setcwd /Users/name/projects/project3
```

Sessions are completely isolated - User A cannot access User B's files or conversation.

## Security Considerations

### Important: Access Control

⚠️ **The bot has full file system access** within your working directory!

**Recommendations:**

1. **Private Bot**: Don't share your bot token publicly
2. **Restrict Access**: Only share your bot username with trusted users
3. **Path Validation**: The bot validates paths exist before setting CWD
4. **Absolute Paths**: Only absolute paths are accepted for CWD

### User Whitelist (Optional)

Add user ID validation in [telegram_bot.py](../src/telegram_bot.py):

```python
ALLOWED_USERS = [123456789, 987654321]  # Your Telegram user IDs

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("❌ Unauthorized")
        return

    # ... rest of handler
```

### Working Directory Restrictions

Limit allowed directories:

```python
ALLOWED_BASE_DIRS = [
    "/Users/name/projects",
    "/Users/name/Documents/work"
]

def validate_cwd(path: str) -> bool:
    abs_path = os.path.abspath(path)
    return any(abs_path.startswith(base) for base in ALLOWED_BASE_DIRS)
```

### Environment Variables

Never commit tokens to git:

```bash
# .gitignore (already included)
.env
*.log
```

## Troubleshooting

### Bot Not Responding

**Check bot is running:**
```bash
# See if process is active
ps aux | grep telegram_bot
```

**Check logs:**
```bash
# If using nohup
tail -f telegram_bot.log

# If running in terminal, errors appear in console
```

**Common issues:**
- Token not set: `export TELEGRAM_BOT_TOKEN="..."`
- API key not set: `export ANTHROPIC_API_KEY="..."`
- Network issues: Check internet connection

### Session Not Persisting

**Check session directory exists:**
```bash
ls -la ~/.riskagent/telegram_sessions/
```

**Check file permissions:**
```bash
chmod 755 ~/.riskagent/telegram_sessions
```

**Check session file content:**
```bash
cat ~/.riskagent/telegram_sessions/YOUR_USER_ID.json
```

### Working Directory Issues

**Path doesn't exist:**
```
You: /setcwd /invalid/path
Bot: ❌ Directory not found: /invalid/path
```

**Solution:** Use absolute paths and verify directory exists:
```bash
ls -la /Users/name/projects/myproject
```

### Message Too Long Error

If responses exceed Telegram's 4096 character limit, they're automatically split into chunks. If you see errors:

**Reduce verbose mode:**
```
You: /verbose  # Turn off verbose mode
```

**Use file operations instead:**
```
You: Save the analysis to analysis.txt instead of showing it
```

## Production Deployment

### Using systemd (Linux)

Create `/etc/systemd/system/riskagent-telegram.service`:

```ini
[Unit]
Description=Risk Agent Telegram Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/riskagent
Environment="TELEGRAM_BOT_TOKEN=your-token"
Environment="ANTHROPIC_API_KEY=your-key"
ExecStart=/usr/bin/uv run riskagent-telegram
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable riskagent-telegram
sudo systemctl start riskagent-telegram
sudo systemctl status riskagent-telegram
```

### Using Docker (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install uv && uv sync

CMD ["uv", "run", "riskagent-telegram"]
```

Build and run:
```bash
docker build -t riskagent-telegram .
docker run -d \
  -e TELEGRAM_BOT_TOKEN="your-token" \
  -e ANTHROPIC_API_KEY="your-key" \
  -v ~/.riskagent:/root/.riskagent \
  riskagent-telegram
```

## Next Steps

- Read [Architecture Analysis](11-telegram-integration-analysis.md) for implementation details
- Read [Session Management Comparison](12-session-management-comparison.md) for context
- Explore [CLI Documentation](03-cli-implementation.md) for feature parity
- Check main [README](../README.md) for overall project structure

## Support

For issues:
1. Check logs first
2. Verify environment variables
3. Test CLI works: `uv run riskagent`
4. Open GitHub issue with logs and error messages
