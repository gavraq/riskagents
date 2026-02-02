# Risk Agent - Local Logging System

**Date**: 2025-11-23
**Status**: Active

## Overview

The local logging system captures Claude Code session activity to the `logs/` directory. This is separate from the observability integration which sends events to an external dashboard.

## Architecture

```
Claude Code Session
    ↓
user_prompt_submit.py hook
    ↓
logs/
├── user_prompt_submit.json    (all prompts from session)
└── {session-id}/              (per-session directories)
```

## Log Directory Structure

```
logs/
├── user_prompt_submit.json           # Aggregated log of all prompts
├── 9a8b7093-2ca6-4f1a-b712-eb837937c249/  # Session directory
└── fd6366ec-2270-4952-a6ed-2b0e8275e012/  # Session directory
```

### user_prompt_submit.json

Contains a JSON array of all prompts submitted during the session:

```json
[
  {
    "session_id": "9a8b7093-2ca6-4f1a-b712-eb837937c249",
    "prompt": "Help me plan a Basel IV implementation",
    "timestamp": "2025-11-23T10:30:00Z"
  },
  ...
]
```

### Session Directories

Individual session data is stored in `.claude/data/sessions/{session-id}.json` and may include:
- Prompt history for the session
- Generated agent name (if `--name-agent` flag is used)

## Configuration

The logging is controlled by the `user_prompt_submit.py` hook in `.claude/hooks/`.

### Hook Flags

| Flag | Purpose |
|------|---------|
| `--log-only` | Only log prompts, no validation |
| `--validate` | Enable prompt validation rules |
| `--store-last-prompt` | Store prompt for status line display |
| `--name-agent` | Generate an AI agent name for the session |

### Settings Configuration

The hook is configured in `.claude/settings.local.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "hooks": [{
        "type": "command",
        "command": "uv run .claude/hooks/user_prompt_submit.py --store-last-prompt"
      }]
    }]
  }
}
```

## Use Cases

### Session History
Review what prompts were submitted during a Claude Code session for debugging or auditing.

### Prompt Validation
Block certain patterns or commands by adding rules to the `validate_prompt()` function.

### Agent Naming
Generate creative names for sessions using the `--name-agent` flag (uses Anthropic API or Ollama fallback).

## Differences from Observability

| Feature | Local Logging | Observability |
|---------|---------------|---------------|
| Storage | Local `logs/` directory | External server on Pi |
| Purpose | Session history & audit | Real-time monitoring |
| Events | UserPromptSubmit only | All event types |
| Visualization | JSON files | Vue dashboard |

## Maintenance

### Clearing Old Logs

```bash
# Remove all logs
rm -rf logs/*

# Remove specific session
rm -rf logs/{session-id}
```

### Log Rotation

Logs are not automatically rotated. Consider periodic cleanup for long-running projects.

## Related Files

- **Hook**: [.claude/hooks/user_prompt_submit.py](../.claude/hooks/user_prompt_submit.py)
- **Session Data**: `.claude/data/sessions/`
- **Observability Docs**: [12-observability-integration.md](12-observability-integration.md)
