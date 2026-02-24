# Web UI & Gateway Architecture

> **Document**: 15-web-ui-gateway-architecture.md
> **Created**: 2026-02-24
> **Status**: Current
> **Audience**: Developers, architects, and anyone debugging the web UI flow

## Overview

This document describes the complete end-to-end architecture for how the Risk Agents web UI communicates with the Claude Agent SDK to deliver real-time AI-powered risk management assistance. The system spans three projects:

1. **riskagents-ui** - Next.js frontend (React 19, TypeScript)
2. **unified-gateway** - FastAPI middleware (Python, WebSocket + REST)
3. **riskagents** - Agent definitions, skills, and project configuration

```
                           User's Browser
                               │
                               ▼
┌────────────────────────────────────────────────────────┐
│  riskagents-ui (Next.js, localhost:3002)               │
│  ├── React 19 + TypeScript                             │
│  ├── gateway-client.ts  → HTTP REST calls              │
│  ├── websocket.ts       → Native WebSocket streaming   │
│  └── hooks.ts           → useChat() state management   │
└────────────────┬──────────────────┬────────────────────┘
                 │ HTTP (REST)      │ WebSocket
                 ▼                  ▼
┌────────────────────────────────────────────────────────┐
│  unified-gateway (FastAPI, localhost:8090)             │
│  ├── routes/auth.py       → JWT authentication         │
│  ├── routes/sessions.py   → Session CRUD + history     │
│  ├── routes/websocket.py  → WS streaming endpoint      │
│  ├── services/claude_service.py → SDK wrapper          │
│  └── SQLite              → Sessions, messages, users   │
└────────────────────────────┬───────────────────────────┘
                             │ Subprocess (stdin/stdout)
                             ▼
┌────────────────────────────────────────────────────────┐
│  Claude Agent SDK → Bundled CLI Binary                 │
│  ├── Loads .claude/settings.local.json                 │
│  ├── Loads .claude/agents/*.md (13 agents)             │
│  ├── Loads .claude/skills/*/SKILL.md (11 skills)       │
│  ├── Loads .claude/commands/*.md (slash commands)      │
│  └── Streams events: init → text → tool_use → result   │
└────────────────────────────┬───────────────────────────┘
                             │ Anthropic API
                             ▼
┌────────────────────────────────────────────────────────┐
│  Anthropic Claude API (claude-opus-4-6)                │
│  ├── System prompt from output-style + agents          │
│  ├── Tool definitions from allowed_tools               │
│  └── Prompt caching for repeated context               │
└────────────────────────────────────────────────────────┘
```

---

## 1. Frontend (riskagents-ui)

### Tech Stack

| Technology | Version | Purpose |
|---|---|---|
| Next.js | 15.1.6 | React framework with App Router |
| React | 19 | UI library |
| TypeScript | 5.0 | Type safety |
| Tailwind CSS | 3.4 | Styling |
| Radix UI | Various | Accessible component primitives |
| react-markdown | - | Render streamed markdown responses |
| lucide-react | - | Icons |

### Key Files

| File | Purpose |
|---|---|
| `src/lib/gateway-client.ts` | HTTP API client, token management, URL construction |
| `src/lib/websocket.ts` | WebSocket connection handler with reconnection logic |
| `src/lib/hooks.ts` | `useChat()` hook - main state management for chat |
| `src/lib/auth.tsx` | `AuthProvider` context, login/logout, token persistence |
| `src/app/chat/page.tsx` | Main chat page layout |
| `src/components/chat/message-input.tsx` | User input with auto-resize textarea |
| `src/components/chat/message-list.tsx` | Message rendering with auto-scroll |
| `src/components/chat/streaming-message.tsx` | Markdown renderer for streamed content |
| `src/components/chat/skill-indicator.tsx` | Visual skill execution tracking |
| `src/components/chat/research-agent-cards.tsx` | 5 research agent status cards |
| `.env.local` | `NEXT_PUBLIC_API_URL=http://localhost:8090` |

### Authentication Flow

1. User enters email + password on login page
2. Frontend calls `POST /api/auth/login` with credentials
3. Gateway returns `{ access_token, refresh_token }`
4. Tokens stored in `localStorage` (`gateway_access_token`, `gateway_refresh_token`)
5. All subsequent HTTP requests include `Authorization: Bearer {token}` header
6. WebSocket connections pass token as query parameter: `?token={token}`

### WebSocket Connection

The frontend uses the **native browser WebSocket API** (no external library). The `ChatWebSocket` class in `websocket.ts` manages:

- **Connection lifecycle**: connect, disconnect, reconnect
- **Auto-reconnection**: Up to 3 attempts with exponential backoff
- **Keep-alive**: Ping every 30 seconds to detect stale connections
- **State tracking**: `connecting` → `connected` → `disconnected` / `error`

```typescript
// URL construction (gateway-client.ts)
export function getWebSocketUrl(sessionId: string): string {
  const token = getAccessToken();
  const wsBase = API_BASE_URL
    .replace("http://", "ws://")
    .replace("https://", "wss://");
  return `${wsBase}/ws/sessions/${sessionId}/stream?token=${token}`;
}
```

### Message Streaming Flow (useChat hook)

```
User types message → sendMessage(content)
    │
    ├── If no active session → createSession() via REST
    ├── If WebSocket not connected → connect()
    │
    └── wsRef.current.sendQuery(content)
            │
            ▼
    Receives events via onMessage callback:
        ├── "chunk"        → Append to current message content
        ├── "skill_start"  → Show skill indicator (blue, spinning)
        ├── "skill_result" → Update skill indicator (green, complete)
        ├── "tool_use"     → Track tool execution, detect research agents
        ├── "tool_result"  → Mark research agents complete
        ├── "done"         → Finalize message, show metadata (cost, duration)
        ├── "error"        → Display error, stop streaming
        └── "cancelled"    → Stop streaming
```

### Research Agent Detection

When the stress-scenario-suggester skill runs, it launches 5 parallel research sub-agents via the `Task` tool. The frontend detects these by inspecting `tool_use` events:

```typescript
// hooks.ts - detecting research agent launches
if (data.tool_name === "Task" && data.tool_input?.subagent_type) {
  // Mark agent as "researching" based on subagent_type
  // e.g., "geopolitical-risk-researcher" → Geopolitical agent active
}
```

The 5 research agents are:
1. Geopolitical Risk Researcher
2. Macroeconomic Risk Researcher
3. Market Structure Risk Researcher
4. Climate & ESG Risk Researcher
5. Technology Sector Risk Researcher

---

## 2. Unified Gateway

### Purpose

The gateway serves as the middleware layer between the web frontend and the Claude Agent SDK. It exists because:

1. **The Claude Agent SDK spawns a local CLI subprocess** that requires filesystem access to the project directory. The gateway runs on the same machine as the project files.
2. **Authentication and session persistence** - JWT auth, SQLite storage for conversation history.
3. **WebSocket-to-SDK bridge** - Translates between WebSocket streaming and the SDK's async event stream.

### Tech Stack

| Technology | Purpose |
|---|---|
| FastAPI | Web framework (async-native) |
| Claude Agent SDK | `claude-agent-sdk>=0.1.41` - Python wrapper for Claude CLI |
| SQLite + aiosqlite | Session and message persistence |
| PyJWT | JWT token creation and verification |
| Pydantic | Request/response validation |
| Uvicorn | ASGI server |

### Key Files

| File | Purpose |
|---|---|
| `src/unified_gateway/main.py` | FastAPI app, CORS, router registration, env cleanup |
| `src/unified_gateway/config.py` | Pydantic settings (host, port, JWT, project paths) |
| `src/unified_gateway/routes/auth.py` | Login, register, refresh, user info |
| `src/unified_gateway/routes/sessions.py` | Session CRUD, message history, CLI session import |
| `src/unified_gateway/routes/websocket.py` | WebSocket streaming endpoint |
| `src/unified_gateway/services/claude_service.py` | Claude SDK wrapper with event parsing |
| `src/unified_gateway/services/session_manager.py` | Session lifecycle management |
| `src/unified_gateway/services/message_store.py` | Message persistence |

### Configuration

| Setting | Default | Description |
|---|---|---|
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `8090` | Server port |
| `DATABASE_PATH` | `~/.unified-gateway/gateway.db` | SQLite database |
| `JWT_SECRET` | (required) | Token signing key |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Access token lifetime |
| `PROJECTS_BASE_PATH` | `/Volumes/DockSSD/projects` | Root for project directories |
| `DEFAULT_PROJECT` | `riskagents` | Default project name |
| `CORS_ORIGINS` | `localhost:3000,3002` | Allowed origins |

### REST API

| Endpoint | Method | Description |
|---|---|---|
| `/api/auth/register` | POST | Register new user |
| `/api/auth/login` | POST | Login (email + password) → tokens |
| `/api/auth/refresh` | POST | Refresh access token |
| `/api/auth/me` | GET | Current user info |
| `/api/sessions` | GET | List sessions (filterable) |
| `/api/sessions` | POST | Create new session |
| `/api/sessions/{id}` | GET | Session details |
| `/api/sessions/{id}` | PATCH | Update session |
| `/api/sessions/{id}` | DELETE | Delete session |
| `/api/sessions/{id}/reset` | POST | Reset Claude session |
| `/api/sessions/{id}/messages` | GET | Message history |
| `/api/skills` | GET | Available skills list |
| `/api/artifacts` | GET | Generated file artifacts |
| `/health` | GET | Health check |

### WebSocket Protocol

**Endpoint**: `ws://localhost:8090/ws/sessions/{session_id}/stream?token={jwt_token}`

**Client → Server Messages**:
```json
{"type": "query", "content": "User's question here"}
{"type": "cancel"}
{"type": "ping"}
```

**Server → Client Messages**:
```json
{"type": "init", "session_id": "...", "sdk_session_id": "..."}
{"type": "chunk", "content": "...", "is_streaming": true}
{"type": "tool_use", "tool_name": "Read", "tool_input": {"file_path": "..."}}
{"type": "tool_result", "output": "...", "is_error": false}
{"type": "skill_start", "skill_name": "pillar-stress-generator"}
{"type": "skill_result", "skill_name": "...", "output": "..."}
{"type": "done", "duration_ms": 10234, "cost_usd": 0.025, "tokens_input": 3, "tokens_output": 572}
{"type": "error", "error": "Error message with CLI stderr details"}
{"type": "pong"}
{"type": "cancelled"}
```

### WebSocket Query Processing Flow

```python
# Simplified flow from routes/websocket.py

async def process_query(session_id, content, websocket):
    # 1. Store user message in SQLite
    await message_store.add_message(session_id, "user", content)

    # 2. Get SDK session ID for conversation continuity
    sdk_session_id = session.claude_session_id  # None for first message

    # 3. Stream events from Claude SDK
    async for event in claude_service.stream_query(
        message=content,
        project=session.project,        # "riskagents"
        sdk_session_id=sdk_session_id,
    ):
        # 4. Transform event types for frontend
        ws_event = transform_event(event)

        # 5. Send to all connected WebSocket clients
        await websocket.send_json(ws_event)

    # 6. Store assistant response in SQLite
    await message_store.add_message(session_id, "assistant", full_response)
```

---

## 3. Claude Agent SDK Integration

### How the SDK Works

The Claude Agent SDK (`claude-agent-sdk` Python package) is **not** a direct API client. It wraps a **bundled Claude Code CLI binary** that it spawns as a subprocess. The communication happens over stdin/stdout using a JSON streaming protocol.

```
┌──────────────────────────────────────────────────────┐
│  unified-gateway (Python process)                    │
│                                                      │
│  claude_service.py                                   │
│    └── query(prompt, options) ──┐                    │
│                                 │                    │
│  claude_agent_sdk               │                    │
│    └── SubprocessCLITransport   │                    │
│         └── spawns subprocess ──┘                    │
│              │ stdin (JSON)                          │
│              │ stdout (JSON stream)                  │
│              │ stderr (diagnostics)                  │
│              ▼                                       │
│  ┌────────────────────────────────────────────────┐  │
│  │  Bundled Claude CLI Binary (Node.js)           │  │
│  │  Path: .venv/.../claude_agent_sdk/_bundled/    │  │
│  │                                                │  │
│  │  - Loads project config from cwd               │  │
│  │  - Discovers agents, skills, commands          │  │
│  │  - Calls Anthropic API                         │  │
│  │  - Executes tools (Read, Write, Bash, etc.)    │  │
│  │  - Streams events back via stdout              │  │
│  └────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

### SDK Options (ClaudeAgentOptions)

The gateway configures the SDK with these options:

```python
options = ClaudeAgentOptions(
    cwd="/Volumes/DockSSD/projects/riskagents",  # Project root
    allowed_tools=[
        "Skill",     # Required for skill auto-invocation
        "Read", "Write", "Edit", "MultiEdit",
        "Bash", "Glob", "Grep",
        "WebSearch", "WebFetch",
        "Task",      # Required for sub-agents
        "TodoWrite", "AskUserQuestion",
    ],
    permission_mode="bypassPermissions",  # No user approval needed
    setting_sources=["project"],           # Load .claude/ from project
    stderr=stderr_handler,                 # Capture CLI diagnostics
)

# Resume conversation continuity
if sdk_session_id:
    options.resume = sdk_session_id
```

### What the CLI Discovers at Startup

When the SDK spawns the CLI subprocess with `cwd=/Volumes/DockSSD/projects/riskagents` and `setting_sources=["project"]`, the CLI:

1. **Reads `.claude/settings.local.json`** - Permission mode, output style, allowed tools
2. **Scans `.claude/agents/*.md`** - Loads 13 agent definitions (7 custom + 6 built-in)
3. **Scans `.claude/skills/*/SKILL.md`** - Loads 11 skill definitions from YAML frontmatter
4. **Scans `.claude/commands/*.md`** - Loads slash command definitions
5. **Emits an `init` event** with the full inventory of tools, agents, skills, and slash commands

The `init` event data (from actual gateway logs):
```json
{
  "type": "system",
  "subtype": "init",
  "cwd": "/Volumes/DockSSD/projects/riskagents",
  "session_id": "fb43b976-...",
  "model": "claude-opus-4-6",
  "permissionMode": "bypassPermissions",
  "claude_code_version": "2.1.52",
  "tools": ["Task", "Bash", "Glob", "Grep", "Read", "Edit", "Write", "Skill", ...],
  "agents": [
    "risk-intelligence-engine", "change-agent", "market-risk-agent",
    "geopolitical-risk-researcher", "macroeconomic-risk-researcher",
    "market-structure-risk-researcher", "climate-esg-risk-researcher",
    "technology-sector-risk-researcher", "Bash", "general-purpose",
    "Explore", "Plan", "statusline-setup"
  ],
  "skills": [
    "climate-scorecard-filler", "icc-business-case-filler",
    "itc-template-filler", "markdown-to-word", "meeting-minutes",
    "pillar-stress-generator", "process-documenter",
    "regulatory-change-assessor", "regulatory-monitor",
    "stress-scenario-approver", "stress-scenario-suggester",
    "keybindings-help", "debug"
  ],
  "slash_commands": [
    "climate-scorecard-filler", "icc-business-case-filler", "itc-template-filler",
    "markdown-to-word", "meeting-minutes", "pillar-stress-generator",
    "process-documenter", "regulatory-change-assessor", "regulatory-monitor",
    "stress-scenario-approver", "stress-scenario-suggester",
    "compact", "context", "cost", "debug", "extra-usage", "init",
    "insights", "keybindings-help", "pr-comments", "release-notes",
    "review", "security-review"
  ]
}
```

### SDK Event Types

The SDK emits typed Python objects that the gateway normalizes:

| SDK Class | Gateway Event | Description |
|---|---|---|
| `SystemMessage(subtype="init")` | `init` | Session initialized, returns session_id |
| `AssistantMessage(TextBlock)` | `text`/`chunk` | Model-generated text content |
| `AssistantMessage(ThinkingBlock)` | (skipped) | Extended thinking (not sent to UI) |
| `AssistantMessage(ToolUseBlock)` | `tool_use` | Tool invocation with name + input |
| `UserMessage(ToolResultBlock)` | `tool_result` | Tool execution result |
| `ResultMessage` | `result`/`done` | Final response with cost + usage metadata |

### Event Parsing (claude_service.py)

```python
def _parse_event(self, event):
    class_name = type(event).__name__

    if class_name == "SystemMessage":
        # Extract session_id from init data
        ...

    if class_name == "AssistantMessage":
        for block in event.content:
            if type(block).__name__ == "TextBlock":
                return {"type": "text", "content": block.text}
            elif type(block).__name__ == "ToolUseBlock":
                return {"type": "tool_use", "tool_name": block.name, ...}

    if class_name == "UserMessage":
        # ToolResultBlock from tool execution
        ...

    if class_name == "ResultMessage":
        return {
            "type": "result",
            "content": event.result,
            "session_id": event.session_id,
            "cost_usd": event.total_cost_usd,
            "tokens_input": event.usage.get("input_tokens"),
            "tokens_output": event.usage.get("output_tokens"),
        }
```

### Session Continuity

Each SDK query returns a `session_id` in the `init` and `result` events. The gateway persists this as `claude_session_id` on the session record. On subsequent messages in the same conversation, the gateway passes `options.resume = sdk_session_id`, which tells the CLI to resume the existing Claude conversation (preserving full message history and context).

---

## 4. Skill Discovery and Auto-Invocation

### How Skills Are Discovered

The CLI binary scans `.claude/skills/*/SKILL.md` files and parses their YAML frontmatter:

```yaml
---
name: pillar-stress-generator
description: Generate or review top-down pillar stress scenarios for market risk.
  Use when user asks to create stress scenarios, review scenarios, generate MLRC memos.
  Keywords - pillar stress, macro scenario, stress testing, MLRC.
---
```

### Skills vs Slash Commands

The CLI maintains two separate lists:

- **Skills** (auto-invocable): The model can automatically invoke these via the `Skill` tool based on user intent. Filtered by the `AER` function which requires `hasUserSpecifiedDescription || whenToUse`.
- **Slash Commands** (user-invocable): Available as `/command-name` for explicit invocation. All skills appear here plus built-in commands like `/compact`, `/review`, `/cost`.

### YAML Frontmatter Gotcha

**Critical**: The YAML `description` value must not contain unquoted colons that look like YAML keys. The CLI uses a JavaScript YAML parser that interprets `Keywords:` (with colon) as a mapping key, breaking the description parsing.

**Broken** (description parsed as object, not string):
```yaml
description: Some text. Keywords: keyword1, keyword2.
```

**Working** (description parsed as string):
```yaml
description: Some text. Keywords - keyword1, keyword2.
```

This was the root cause of 4 skills not being auto-invocable until fixed (2026-02-24). See the skills that were affected: `markdown-to-word`, `pillar-stress-generator`, `regulatory-monitor`, `stress-scenario-suggester`.

### How the Skill Tool Works

When the model determines a user's intent matches a skill's description, it calls:

```json
{
  "tool": "Skill",
  "input": {
    "skill": "pillar-stress-generator"
  }
}
```

The CLI then loads the full SKILL.md content as instructions and the model follows them to complete the task, using other tools (Read, Write, Bash, Task, etc.) as needed.

---

## 5. Agent Routing

### Risk Intelligence Engine (Orchestrator)

The orchestrator agent (`.claude/agents/risk-intelligence-engine.md`) receives all user queries first and routes to domain specialists:

```
User Query
    │
    ▼
Risk Intelligence Engine
    ├── Change management queries → Task(change-agent)
    ├── Market risk queries       → Task(market-risk-agent)
    ├── Stress research queries   → Task(market-risk-agent) → 5 research sub-agents
    └── General questions         → Responds directly
```

### Sub-Agent Communication

Agents communicate via the `Task` tool, which spawns a new Claude subprocess:

```python
# The orchestrator calls:
Task(
    subagent_type="change-agent",
    prompt="Create meeting minutes from the following notes...",
)

# The change-agent may then auto-invoke a skill:
Skill(skill="meeting-minutes")
```

---

## 6. Environment and Deployment

### Local Development

```
┌─────────────────────────────────────────────────────┐
│  Mac (localhost)                                    │
│                                                     │
│  riskagents-ui    → localhost:3002 (npm run dev)    │
│  unified-gateway  → localhost:8090 (uv run)         │
│  riskagents/      → /Volumes/DockSSD/projects/      │
└─────────────────────────────────────────────────────┘
```

### Production (External Access)

```
┌─────────────────────────────────────────────────────┐
│  Internet → agent-web-ui.gavinslater.co.uk          │
└──────────────────────┬──────────────────────────────┘
                       │ HTTPS
                       ▼
┌─────────────────────────────────────────────────────┐
│  Raspberry Pi (nginx proxy manager)                 │
│  - SSL termination (Let's Encrypt)                  │
│  - /api/*, /ws/* → Mac:8090 (gateway)               │
│  - /*           → localhost:3002 (web UI)           │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP / WebSocket
                       ▼
┌─────────────────────────────────────────────────────┐
│  Mac (192.168.5.192)                                │
│  - unified-gateway on port 8090                     │
│  - launchd service for auto-start                   │
│  - Filesystem access to project files               │
└─────────────────────────────────────────────────────┘
```

### Important: Environment Variable Cleanup

When the gateway is started from within a Claude Code terminal session, it inherits environment variables like `CLAUDECODE`, `CLAUDE_CODE_ENTRYPOINT`, etc. The CLI subprocess detects these and refuses to start ("Claude Code cannot be launched inside another Claude Code session").

The gateway's `main.py` strips these on startup:

```python
_CLAUDE_ENV_VARS_TO_STRIP = [
    "CLAUDECODE",
    "CLAUDE_CODE_ENTRYPOINT",
    "CLAUDE_CODE_ENTRY_POINT",
    "CLAUDE_CODE_SESSION_ID",
]
for _var in _CLAUDE_ENV_VARS_TO_STRIP:
    if _var in os.environ:
        del os.environ[_var]
```

When running via `launchd`, this is not an issue since the service starts with a clean environment.

---

## 7. Logging and Diagnostics

### Gateway Logs

| Log File | Content |
|---|---|
| `~/.unified-gateway/logs/gateway.log` | Application logs (rotating, 5MB, 3 backups) |
| `~/.unified-gateway/logs/stdout.log` | Uvicorn access logs (when run as daemon) |

### CLI Stderr Capture

The gateway captures stderr from the CLI subprocess via a per-query buffer. If the CLI fails (exit code 1), the stderr content is:
1. Logged to `gateway.log` at ERROR level
2. Included in the error event sent to the frontend
3. Available for post-mortem debugging

Example error with full diagnostics:
```
[ERROR] Claude SDK error: Command failed with exit code 1
CLI stderr output:
Error: Claude Code cannot be launched inside another Claude Code session.
Nested sessions share runtime resources and will crash all active sessions.
To bypass this check, unset the CLAUDECODE environment variable.
```

### SDK Event Logging

All SDK events are logged at INFO level with their full content:
```
SDK Event: type=None, event=SystemMessage(subtype='init', data={...})
SDK Event: type=None, event=AssistantMessage(content=[TextBlock(...)])
SDK Event: type=None, event=ResultMessage(subtype='success', cost=0.025, ...)
```

---

## 8. Cost and Performance

### Typical Query Costs (Max Plan)

The `total_cost_usd` in SDK responses is an **informational estimate** of API-equivalent pricing. On the Anthropic Max subscription plan, there is no per-query charge - the flat monthly fee covers all usage.

| Query Type | Typical Cost Estimate | Response Time |
|---|---|---|
| Simple greeting/overview | ~$0.025 | ~10 seconds |
| Skill invocation (e.g., meeting minutes) | ~$0.05-0.15 | 30-120 seconds |
| Multi-agent research (5 parallel agents) | ~$0.50-1.50 | 2-5 minutes |
| Complex stress scenario generation | ~$0.10-0.30 | 60-180 seconds |

### Prompt Caching

The SDK leverages Anthropic's prompt caching. The first query in a session pays the cache creation cost, while subsequent queries benefit from cached context:

```json
{
  "cache_creation_input_tokens": 3934,   // First query: populates cache
  "cache_read_input_tokens": 16464       // Reads from cache
}
```

---

## 9. Troubleshooting

### Common Issues

| Symptom | Cause | Fix |
|---|---|---|
| "Exit code 1" on all queries | `CLAUDECODE` env var inherited | Restart gateway (env cleanup in main.py) or use launchd |
| Skills not auto-invoked | `Keywords:` (colon) in YAML description | Change to `Keywords -` (dash) in SKILL.md frontmatter |
| WebSocket disconnects immediately | JWT token expired | Frontend auto-refreshes; check token expiry setting |
| "Command failed with exit code 1" | Various CLI errors | Check `~/.unified-gateway/logs/gateway.log` for stderr capture |
| Slow first query | Cache creation | Normal - subsequent queries are faster |
| Skills visible in UI admin but not used by model | Skill not in CLI `skills` list | Check SKILL.md frontmatter parsing (description must be a string) |

### Diagnostic Commands

```bash
# Check gateway health
curl http://localhost:8090/health

# View gateway logs
tail -f ~/.unified-gateway/logs/gateway.log

# Check available skills via API
curl -H "Authorization: Bearer TOKEN" http://localhost:8090/api/skills

# Test SDK directly (from unified-gateway project)
cd /Volumes/DockSSD/projects/unified-gateway
env -u CLAUDECODE .venv/bin/python -c "
import asyncio
from claude_agent_sdk import ClaudeAgentOptions, query

async def test():
    options = ClaudeAgentOptions(
        cwd='/Volumes/DockSSD/projects/riskagents',
        allowed_tools=['Skill', 'Read'],
        permission_mode='bypassPermissions',
        setting_sources=['project'],
    )
    async for event in query(prompt='Say hello', options=options):
        print(type(event).__name__, getattr(event, 'subtype', ''))
        if type(event).__name__ == 'ResultMessage':
            break

asyncio.run(test())
"
```

---

## 10. CLI Session Management

### Overview

The gateway can discover, import, and display CLI sessions created directly in the terminal using `claude` or `claude-code`. This allows users to review past CLI conversations in the web UI and maintain a unified session history across both interfaces.

### CLI Session Storage

Claude Code stores sessions as JSONL files:

```
~/.claude/projects/{encoded-project-path}/
    ├── {session-id}.jsonl           # Raw conversation data
    ├── {session-id}/                # Session artifacts
    │   ├── subagents/               # Sub-agent transcripts
    │   └── tool-results/            # Large tool outputs
    ├── sessions-index.json          # Summary metadata (Claude-maintained)
    └── memory/                      # Long-term memory
```

The encoded project path uses dashes for path separators, e.g., `-Volumes-DockSSD-projects-riskagents`.

### JSONL File Format

Each line is a JSON object with a `type` field:

| Entry Type | Frequency | Description |
|---|---|---|
| `user` | ~5% | User-typed messages (string content) or tool_result relays (list content) |
| `assistant` | ~19% | Text, thinking, and tool_use blocks |
| `progress` | ~63% | Streaming progress events (skip during import) |
| `system` | ~2% | System messages (skip) |
| `file-history-snapshot` | ~3% | File state snapshots (skip) |
| `queue-operation` | ~2% | Internal queue ops (skip) |
| `custom-title` | rare | Session rename via `/rename` command |

A typical session with 24 user-typed messages has ~3,000 raw JSONL entries.

### Session Discovery

**Endpoint**: `GET /api/sessions/cli/discover`

Scans `~/.claude/projects/` to find all JSONL session files and enriches them with metadata:

| Source | Data Retrieved |
|---|---|
| JSONL file | Slug (auto-generated session name, e.g., `squishy-hugging-tome`) |
| JSONL file | Custom title (from `type: "custom-title"` entries set via `/rename`) |
| `sessions-index.json` | Summary, first prompt, message count |
| `~/.claude/history.jsonl` | Custom display names (older `/rename` pattern) |
| File system | Size, modification date |
| Gateway DB | Whether already imported |

**Session name priority**: custom-title from JSONL > display name from history.jsonl > auto-generated slug.

### Session Import with Message Backfill

**Endpoint**: `POST /api/sessions/cli/import`

Import creates a gateway session and parses the JSONL file to extract and store the full conversation history.

#### Import Flow

```
POST /api/sessions/cli/import
  {"cli_session_id": "d2a964f0-...", "project": "riskagents"}
    │
    ├── 1. Locate JSONL file in ~/.claude/projects/
    ├── 2. Parse JSONL → extract conversation turns
    │       ├── Filter: only user-typed messages + assistant text blocks
    │       ├── Skip: progress, system, file-history-snapshot, tool_result relays
    │       └── Group: user message + all assistant responses = 1 turn
    ├── 3. Extract custom title (from custom-title entry or first prompt)
    ├── 4. Create Gateway session record
    ├── 5. Bulk insert messages with original timestamps preserved
    └── 6. Return ImportCLISessionResponse with messages_imported count
```

#### Turn Identification Logic

A "turn" starts with a **user-typed message** (where `type == "user"` and `message.content` is a plain string). Everything between two consecutive user-typed messages belongs to one turn.

- **User-typed messages**: `type == "user"` with `message.content` as a string
- **Tool result relays**: `type == "user"` with `message.content` as a list (skipped - these are tool responses, not user input)
- **Assistant text**: `type == "assistant"` with `text` blocks in `message.content` (extracted, thinking blocks skipped)
- **Tool usage**: Collected from `tool_use` blocks for metadata

#### Title Resolution

The import endpoint resolves the session title using this priority chain:

1. Explicit `title` from the import request body
2. `customTitle` from `type: "custom-title"` entries in the JSONL file (set via `/rename`)
3. Custom display name from `~/.claude/history.jsonl` (older `/rename` pattern)
4. First user prompt content (truncated to 80 chars, markdown headers stripped)
5. Session slug from JSONL (e.g., `CLI: squishy-hugging-tome`)
6. Truncated session ID (e.g., `Imported: d2a964f0...`)

#### Key Files

| File | Purpose |
|---|---|
| `unified-gateway/services/cli_session_parser.py` | JSONL parser - extracts `ConversationTurn` objects |
| `unified-gateway/services/message_store.py` | `bulk_add_messages()` - batch insert with preserved timestamps |
| `unified-gateway/routes/sessions.py` | Discovery, import endpoints, title resolution |

#### Response Model

```json
{
  "id": "fe7f7ab8-...",
  "title": "import-cli-sessions-bulk-insert",
  "channel": "cli",
  "message_count": 38,
  "messages_imported": 38,
  "last_active_at": "2026-02-24T14:55:00Z",
  "claude_session_id": "d2a964f0-..."
}
```

#### Error Handling

If JSONL parsing fails (corrupt file), the session is still created but with 0 messages. The error is stored in `extra_data`:

```json
{"import_error": "Failed to parse JSONL: ..."}
```

### Re-importing Sessions

To re-import a session (e.g., after code updates), delete the existing gateway session first via the UI or API, then import again. Previously imported sessions show a checkmark in the discovery dialog.

---

## 11. Related Documentation

| Document | Location |
|---|---|
| Unified Gateway README | `/Volumes/DockSSD/projects/unified-gateway/README.md` |
| Agent Architecture | `docs/02-agents.md` |
| Skills Guide | `docs/06-skills-guide.md` |
| Pillar Stress Generator | `docs/06c-pillar-stress-generator.md` |
| Stress Scenario Suggester | `docs/06e-stress-scenario-suggester.md` |
| Telegram Standalone Architecture | `docs/11-telegram-standalone-architecture.md` |
| Observability Integration | `docs/12-observability-integration.md` |
| Local Logging System | `docs/13-local-logging-system.md` |
| Regulatory Monitor | `docs/14-proactive-regulatory-monitor.md` |
