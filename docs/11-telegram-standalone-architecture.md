# Telegram Standalone Architecture

**Date**: 2025-11-23 (Updated: 2025-12-27)
**Status**: Implemented

---

## Overview

Telegram access to Risk Agent (and other Claude Agent projects) is now provided via standalone services rather than being embedded in the riskagent project. This enables multi-project support from a single Telegram bot.

**Consolidated Repository**: `~/projects/telegram`

For complete documentation, see: [Telegram System README](../../telegram/README.md)

## Architecture

```
┌─────────────────┐
│  Telegram User  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   Raspberry Pi (Docker)             │
│   telegram-gateway                  │
│                                     │
│   - Telegram bot handlers           │
│   - SQLite session management       │
│   - HTTP client to Mac              │
└────────┬────────────────────────────┘
         │ HTTPS via Nginx Proxy Manager
         │ telegram.gavinslater.co.uk
         ▼
┌─────────────────────────────────────┐
│   Mac                               │
│   ~/projects/telegram/agent         │
│                                     │
│   FastAPI service (port 8095)       │
│   - POST /query                     │
│   - Runs Claude SDK in any cwd      │
│   - Project autodiscovery           │
└─────────────────────────────────────┘
```

## Project Structure

The Telegram system is now consolidated in a single repository:

```
~/projects/telegram/
├── README.md                 # Complete documentation
├── agent/                    # Mac service (FastAPI + Claude SDK)
│   ├── pyproject.toml
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── .env.example
│   ├── com.gavinslater.telegram-agent.plist  # launchd config
│   └── src/telegram_agent/
│       ├── main.py          # FastAPI application
│       ├── runner.py        # Claude SDK execution
│       └── project.py       # Project autodiscovery
└── gateway/                  # Pi/Docker service (Telegram bot)
    ├── pyproject.toml
    ├── Dockerfile
    ├── docker-compose.yml
    ├── .env.example
    └── src/telegram_gateway/
        ├── bot.py           # Telegram bot
        ├── session.py       # SQLite sessions
        └── client.py        # HTTP client
```

## Quick Reference

### Start Agent Service (Mac)
```bash
cd ~/projects/telegram/agent
uv sync
uv run telegram-agent
```

### Deploy Gateway (Pi)
```bash
cd ~/docker/telegram-gateway
docker-compose up -d
```

### Bot Commands
| Command | Description |
|---------|-------------|
| `/start` | Welcome message |
| `/help` | Show help |
| `/status` | Session info |
| `/setcwd <path>` | Set working directory |
| `/reset` | Clear conversation |
| `/health` | Check Mac service |

### Switch Projects
```
/setcwd /Users/gavinslater/projects/riskagent
/setcwd /Users/gavinslater/projects/life
```

## Deprecated Code

The previous embedded implementation has been moved to `src/_deprecated/`:
- `telegram_bot.py` - Original Telegram bot
- `telegram_utils.py` - Message formatting utilities

This code is kept for reference but is no longer used.

## Full Documentation

See the consolidated README for complete details:
- [~/projects/telegram/README.md](../../telegram/README.md)

---

## Archived Documentation

Previous Telegram implementation docs moved to `docs/archive/`:
- `11-telegram-integration-analysis.md`
- `12-session-management-comparison.md`
- `13-telegram-bot-setup.md`
