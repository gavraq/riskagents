# Risk Agent MVP - CLI Implementation

**Date**: 2025-11-05
**Status**: Implemented - Ready for Testing

## Overview

The CLI (`src/risk_agent_cli.py`) implements the kenneth-liao conversation loop pattern using the Claude Agent SDK to invoke the orchestrator agent.

## Architecture

```
User → CLI → ClaudeSDKClient → risk-intelligence-engine.md → change-agent.md → Skills
```

## Implementation Details

### Dependencies

**Added**: `claude-agent-sdk>=0.1.6`

```bash
uv add claude-agent-sdk
```

### Key Components

#### 1. Agent SDK Configuration

```python
options = ClaudeAgentOptions(
    agent_name="risk-intelligence-engine",  # Orchestrator agent
    model="claude-sonnet-4-5",
    permission_mode="acceptEdits",
    setting_sources=["project"]  # Load from .claude/
)
```

**Key Options**:
- `agent_name`: Specifies which agent in `.claude/agents/` to invoke
- `model`: Claude model to use
- `permission_mode`: How to handle tool executions ("acceptEdits" auto-accepts)
- `setting_sources`: Where to load settings from (["project"] uses `.claude/settings.json`)

#### 2. Conversation Loop Pattern

Following kenneth-liao `4_convo_loop.py`:

```python
async with ClaudeSDKClient(options=options) as client:
    while True:
        user_input = get_user_input()

        if user_input.lower() == 'exit':
            break

        await client.query(user_input)  # Send query

        async for message in client.receive_response():  # Receive responses
            parse_and_print_message(message)
```

#### 3. Agent Discovery

The SDK automatically discovers:
- **Agents**: `.claude/agents/*.md` files
- **Skills**: `.claude/skills/*/SKILL.md` files
- **Settings**: `.claude/settings.json` or `.claude/settings.local.json`

No explicit configuration needed - just place files in correct locations!

### Flow Diagram

```
User types: "Help me plan a Basel IV project"
    ↓
CLI sends query via client.query()
    ↓
SDK invokes: risk-intelligence-engine.md
    ↓
Orchestrator classifies: "Change Management"
    ↓
Orchestrator uses Task tool: invoke change-agent
    ↓
change-agent.md receives query
    ↓
change-agent recognizes: "Project planning needed"
    ↓
SDK auto-invokes: project-planner skill
    ↓
Skill generates: Comprehensive project plan
    ↓
Response flows back: skill → agent → orchestrator → client → CLI
    ↓
CLI displays: Formatted project plan
```

## Commands

| Command | Action |
|---------|--------|
| `help` | Show available capabilities |
| `clear` | Clear screen (conversation maintained) |
| `verbose`, `v` | Toggle verbose mode (show all tool calls/results) |
| `interface`, `i` | Toggle interface mode (rich panels vs simple text) |
| `exit`, `quit`, `q` | Exit application |

## Running the CLI

```bash
cd /Users/gavinslater/projects/riskagent

# Run the CLI (standard mode - rich interface)
uv run riskagent

# Run with verbose mode (shows all tool calls and results)
uv run riskagent --verbose
# or
uv run riskagent -v

# Run with simple interface (plain text, no panels)
uv run riskagent --simple
# or
uv run riskagent -s

# Combine modes (simple interface + verbose output)
uv run riskagent --simple --verbose

# Alternative (direct Python execution)
uv run python src/risk_agent_cli.py
```

**Prerequisites**:
- Logged in to Anthropic (authenticated session)
- OR Anthropic API key in environment

## Display Modes

**Added**: 2025-01-09

The CLI supports two orthogonal display settings that can be combined:

### Interface Mode

Controls the visual formatting of messages.

#### Rich Mode (Default)
Enhanced terminal interface with visual formatting:
- 🎨 Colored panels with borders
- 🔍 Syntax highlighting for JSON/code
- 📦 Visual separation between message types
- ✨ Full Rich library formatting

**Use when**: Working in a terminal that supports colors and formatting (most modern terminals).

#### Simple Mode
Plain text interface without Rich formatting:
- 📝 Clean text output with emoji prefixes
- 🚫 No panels or borders
- 🔤 No syntax highlighting
- 📊 Same format as Telegram bot

**Use when**:
- Working in limited terminals (no color support)
- Logging output to files
- Matching Telegram bot output format
- Preference for minimalist interface

**Enable simple mode**:
- At launch: `uv run riskagent --simple` or `uv run riskagent -s`
- At runtime: Type `interface` or `i` to toggle

### Verbose Mode

Controls the level of detail shown (works with both interface modes).

#### Standard Detail (Default)
Shows a clean, focused interface:
- ✅ Assistant text responses
- ✅ Skill invocations
- ✅ Skill results
- ❌ Individual tool calls hidden
- ❌ Tool results hidden

**Use when**: You want a clean, distraction-free experience focused on outcomes.

#### Verbose Detail
Shows complete execution details like Claude Code terminal:
- ✅ Assistant text responses
- ✅ Skill invocations and results
- ✅ **Every tool call** (Read, Write, Edit, Bash, Grep, Glob, etc.)
- ✅ **All tool results** (file contents, command outputs)
- ✅ Complete execution trace

**Use when**:
- Debugging skill execution issues
- Learning how the agent works internally
- Verifying data extraction and file operations
- Tracking the agent's decision-making process

**Enable verbose mode**:
- At launch: `uv run riskagent --verbose` or `uv run riskagent -v`
- At runtime: Type `verbose` or `v` to toggle

### Combining Modes

You can combine interface mode and verbose mode:

```bash
# Rich interface + standard detail (default)
uv run riskagent

# Rich interface + verbose detail
uv run riskagent --verbose

# Simple interface + standard detail
uv run riskagent --simple

# Simple interface + verbose detail (like Claude Code terminal with plain text)
uv run riskagent --simple --verbose
```

**Example Output Comparison**:

**Rich Mode**:
```
╭──────────────────╮
│ 🤖 Risk Agent    │
╰──────────────────╯
I'll help you with that project plan...
```

**Simple Mode**:
```
🤖 Risk Agent:
I'll help you with that project plan...
```

**Implementation**:
- Interface mode: [src/cli_utils.py:134-154](../src/cli_utils.py#L134-L154)
- Verbose mode: [src/cli_utils.py:157-226](../src/cli_utils.py#L157-L226)

## Testing Checklist

### Basic Tests
- [  ] CLI starts without errors
- [  ] Welcome banner displays
- [  ] `help` command works
- [  ] `clear` command works
- [  ] `exit` command works

### Agent Tests
- [  ] Orchestrator loads and responds
- [  ] Query routes to change-agent
- [  ] Skills are invoked (check for project-planner, etc.)

### Functional Tests
1. **Project Planning**:
   - Input: `"Help me plan a Basel IV implementation project"`
   - Expected: Comprehensive project plan with phases, timeline, risks

2. **Meeting Minutes**:
   - Input: `"Structure these notes: Met with team about Basel IV..."`
   - Expected: Structured minutes with actions, decisions

3. **Future Domain**:
   - Input: `"Calculate VaR for my portfolio"`
   - Expected: "Coming soon" message with alternatives

### Error Handling
- [  ] Invalid input handled gracefully
- [  ] Network errors caught and displayed
- [  ] Authentication errors clear

## Files Structure

```
src/
├── __init__.py
└── risk_agent_cli.py    # Main CLI (✅ Implemented)

.claude/
├── agents/
│   ├── risk-intelligence-engine.md  # ✅ Created
│   └── change-agent.md              # ✅ Created
│
└── skills/
    ├── meeting-minutes/
    │   └── SKILL.md                 # ✅ Created
    ├── project-planner/
    │   └── SKILL.md                 # ⏳ Pending
    ├── status-reporter/
    │   └── SKILL.md                 # ⏳ Pending
    └── stakeholder-analysis/
        └── SKILL.md                 # ⏳ Pending
```

## Known Limitations (MVP)

1. **Message Parsing**: Simplified - just prints messages
   - Can enhance to handle TextBlock, ToolUseBlock, ThinkingBlock separately
   - Can add Rich formatting for different message types

2. **Settings**: Using defaults
   - Can add `.claude/settings.json` for output styles
   - Can customize system prompts

3. **Error Recovery**: Basic
   - Can add retry logic
   - Can add better error messages

4. **Only 1 Skill**: meeting-minutes created
   - Need 3 more skills for full MVP

## Enhancement Opportunities

### Short Term
1. Create remaining 3 skills
2. Add `.claude/settings.json` for output styles
3. Improve message parsing and formatting
4. Add conversation export feature

### Medium Term
1. Add more sophisticated error handling
2. Implement conversation history save/load
3. Add metrics tracking (tokens, cost, time)
4. Create test suite

### Long Term
1. Add second domain agent (Credit Risk)
2. Implement multi-domain coordination
3. Add voice input capability
4. Build web UI wrapper

## Next Steps

1. **Test Current Implementation**:
   ```bash
   uv run python src/risk_agent_cli.py
   ```

2. **If Working**:
   - Create remaining 3 skills
   - Test end-to-end flows
   - Document any issues

3. **If Not Working**:
   - Check error messages
   - Verify authentication
   - Check agent/skill file locations
   - Review SDK documentation

## References

- [Claude Agent SDK Python Docs](https://docs.claude.com/en/api/agent-sdk/python)
- [kenneth-liao Tutorial](https://github.com/kenneth-liao/claude-agent-sdk-intro)
- [Claude Skills Documentation](https://docs.claude.com/en/docs/claude-code/skills)
