# Risk Agent - Observability Integration

**Date**: 2025-11-21
**Status**: Complete

## Overview

This document describes the integration of the riskagent project with Gavin's Multi-Agent Observability system for real-time monitoring of Claude Code agent behavior.

## Architecture

```
Claude Code (riskagent)
    ↓
Hook Scripts (.claude/hooks/)
    ↓ (HTTP POST)
Observability Server (Pi)
    ↓ (WebSocket)
Vue Dashboard (localhost:5173)
```

## Configuration

### Server Details

- **Dashboard**: `https://agentdashboard.gavinslater.co.uk`
- **Server API**: `https://observability.gavinslater.co.uk`
- **Direct IP**: `http://192.168.5.190:4000`
- **WebSocket**: `wss://observability.gavinslater.co.uk/stream`
- **Source App**: `riskagent`

### Configured Event Types

| Event Type | Purpose |
|------------|---------|
| PreToolUse | Before tool execution |
| PostToolUse | After tool completion |
| Notification | User interactions |
| Stop | Response completion |
| UserPromptSubmit | User prompt submission |

## Setup Details

### 1. Hook Files ✅

**Date**: 2025-11-21
**Status**: Complete

Copied from life project to `.claude/hooks/`:
- `send_event.py` - Sends events to observability server
- `pre_tool_use.py` - Tool validation
- `post_tool_use.py` - Result logging
- `notification.py` - Notification handling
- `stop.py` - Session completion
- `user_prompt_submit.py` - Prompt logging
- `utils/` - Helper modules (summarizer, model extractor)

### 2. Settings Configuration ✅

**Date**: 2025-11-21
**Status**: Complete

Added hooks configuration to `.claude/settings.local.json`:

```json
{
  "hooks": {
    "PreToolUse": [{
      "hooks": [{
        "type": "command",
        "command": "uv run /Users/gavinslater/projects/riskagent/.claude/hooks/send_event.py --source-app riskagent --event-type PreToolUse --server-url https://observability.gavinslater.co.uk/events --summarize"
      }]
    }]
  }
}
```

## Usage

### Viewing Events

1. Open the dashboard: `https://agentdashboard.gavinslater.co.uk`

2. Filter by `riskagent` in the source app dropdown

### Server Status Commands

```bash
# Check server health
curl https://observability.gavinslater.co.uk/health

# View recent events
curl https://observability.gavinslater.co.uk/events/recent

# Get filter options
curl https://observability.gavinslater.co.uk/events/filter-options
```

## Troubleshooting

### Events Not Appearing

1. **Check server accessibility**:
   ```bash
   curl https://observability.gavinslater.co.uk/health
   ```

2. **Verify hook paths** in `.claude/settings.local.json` use absolute paths

3. **Check Claude Code** is loading the correct settings file

### Modifying Event Types

Edit `.claude/settings.local.json` to add/remove event types. Available types:
- PreToolUse, PostToolUse
- Notification, Stop, SubagentStop
- UserPromptSubmit
- PreCompact, SessionStart, SessionEnd

## Related Documentation

- **Full System Docs**: `/Users/gavinslater/projects/life/integrations/observability/README.md`
- **Server Implementation**: `/Users/gavinslater/projects/life/integrations/observability/apps/server/`
- **Client Implementation**: `/Users/gavinslater/projects/life/integrations/observability/apps/client/`

## Notes

- Server runs continuously on Raspberry Pi Docker container
- Events include AI-generated summaries via `--summarize` flag
- All events tagged with `source_app: riskagent` for filtering
- Shared infrastructure with `life` project
