# Risk Agent MVP - CLI Frontend Experience

**Date**: 2025-11-05
**Status**: Completed
**Version**: 1.0

## Overview

The Risk Agent CLI provides a rich, interactive terminal experience using the Rich library for formatted output and the Claude Agent SDK for AI agent orchestration. The implementation is based on the kenneth-liao conversation loop pattern with enhanced message formatting.

## Architecture

```
User Input (Terminal)
    ↓
risk_agent_cli.py (Main CLI Loop)
    ↓
ClaudeSDKClient (Agent SDK)
    ↓
Message Stream (Async Iterator)
    ↓
cli_utils.py (Message Parsing & Formatting)
    ↓
Rich Console (Formatted Terminal Output)
```

## Key Components

### 1. Main CLI (`src/risk_agent_cli.py`)

**Purpose**: Entry point and conversation loop management

**Key Functions**:

#### `show_welcome()`
Displays the welcome banner with:
- Risk Agents branding
- Architecture overview
- Available capabilities
- Coming soon features
- Command hints

#### `get_user_input()`
- Captures user input with Rich prompt styling
- Handles keyboard interrupts (Ctrl+C)
- Returns "exit" on EOF

#### `show_help()`
Displays comprehensive help information:
- Available commands
- Current capabilities (Change-Agent)
- Example queries
- Tips for best results
- Architecture diagram

#### `cli()`
**Synchronous wrapper** for async main function:
- Required for `uv run riskagent` script entry point
- Handles `asyncio.run()` invocation
- Catches KeyboardInterrupt gracefully
- **NEW (2025-01-09)**: Parses `--verbose` / `-v` and `--simple` / `-s` command-line flags

```python
def cli():
    import sys
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    interface = "simple" if ('--simple' in sys.argv or '-s' in sys.argv) else "rich"
    asyncio.run(main(verbose=verbose, interface=interface))
```

#### `async main(verbose: bool = False, interface: str = "rich")`
**Main conversation loop** following kenneth-liao pattern:

```python
async def main(verbose: bool = False, interface: str = "rich"):
    # Show mode status
    if verbose:
        console.print("[dim]Verbose mode enabled[/dim]\n")
    if interface == "simple":
        console.print("[dim]Simple interface mode[/dim]\n")

    # Configure SDK
    options = ClaudeAgentOptions(
        model="claude-sonnet-4-5",
        permission_mode="acceptEdits",
        setting_sources=["project"],
        system_prompt="agents/risk-intelligence-engine"
    )

    # Main loop
    async with ClaudeSDKClient(options=options) as client:
        while True:
            user_input = get_user_input()

            if user_input == 'exit':
                break

            # Toggle verbose at runtime
            if user_input.lower() in ['verbose', 'v']:
                verbose = not verbose
                console.print(f"Verbose mode {'enabled' if verbose else 'disabled'}")
                continue

            # NEW: Toggle interface at runtime
            if user_input.lower() in ['interface', 'i']:
                interface = "simple" if interface == "rich" else "rich"
                console.print(f"Interface mode: {interface}")
                continue

            await client.query(user_input)

            async for message in client.receive_response():
                # Pass both verbose flag and interface mode
                parse_and_print_message(message, console, print_stats=False,
                                       verbose=verbose, interface=interface)
```

**Key Features**:
- Async context manager for SDK client
- Infinite loop for continuous conversation
- Status spinner during processing
- Exception handling with user-friendly errors
- **NEW (2025-01-09)**: Verbose mode support (toggle at runtime or via CLI flag)
- **NEW (2025-01-09)**: Interface mode support (rich panels vs simple text)

### 2. CLI Utilities (`src/cli_utils.py`)

**Purpose**: Message parsing and formatting (adapted from kenneth-liao)

#### Display Mode Implementation

**Added**: 2025-01-09

The `parse_and_print_message()` function now supports both `verbose` and `interface` parameters:

```python
def parse_and_print_message(
    message: Message,
    console: Console,
    print_stats: bool = False,
    verbose: bool = False,      # Controls detail level
    interface: str = "rich"     # Controls formatting style
):
```

#### Interface Mode: Rich vs Simple

Two formatting functions provide different visual styles:

**`print_rich_message()`** - Enhanced visual formatting:
```python
def print_rich_message(
    type: Literal["user", "assistant", "tool_use", "tool_result",
                  "system", "skill_use", "skill_result"],
    message: str,
    console: Console
):
    # Creates colored panels with borders
    # Applies syntax highlighting for JSON
    # Full Rich library features
```

**Output Example**:
```
╭─────────────────────╮
│ 🤖 Risk Agent       │
╰─────────────────────╯
I'll help you with that...
```

**`print_simple_message()`** - Plain text formatting:
```python
def print_simple_message(
    type: Literal["user", "assistant", "tool_use", "tool_result",
                  "system", "skill_use", "skill_result"],
    message: str,
    console: Console
):
    # Emoji prefixes for message types
    # Plain text output (no panels)
    # Same format as Telegram bot
```

**Output Example**:
```
🤖 Risk Agent:
I'll help you with that...
```

**Dynamic Selection**:
```python
# Choose print function based on interface mode
print_fn = print_simple_message if interface == "simple" else print_rich_message

# Use selected function
print_fn("assistant", "I'll help you...", console)
```

#### Verbose Mode: Standard vs Detailed

Controls what content is shown (works with both interface modes):

**Standard Mode (`verbose=False`)**: Only shows skills and assistant responses
  - ✅ `AssistantMessage` with `TextBlock` → Formatted responses
  - ✅ `ToolUseBlock` with `name="Skill"` → Skill invocations
  - ✅ `ToolResultBlock` matching skill IDs → Skill results
  - ❌ Regular tool calls (Read, Write, Bash, etc.) → **Hidden**
  - ❌ Regular tool results → **Hidden**

**Verbose Mode (`verbose=True`)**: Shows all tool activity
  - ✅ All assistant messages
  - ✅ All skill invocations and results
  - ✅ **All tool calls** (Read, Write, Edit, Bash, Grep, Glob, Task)
  - ✅ **All tool results** (file contents, command outputs)
  - ✅ Complete execution trace

**Implementation Highlights**:

```python
elif isinstance(block, ToolUseBlock):
    if block.name == "Skill":
        # Always show skills
        skill_message = f"Skill: {skill_name}\n\nArguments:\n{json.dumps(skill_args, indent=2)}"
        print_rich_message("skill_use", skill_message, console)
    else:
        # Regular tools - only show in verbose mode
        if verbose:
            print_rich_message("tool_use", f"Tool: {block.name}\n\nInput:\n{json.dumps(block.input, indent=2)}", console)
```

```python
if block.tool_use_id in _skill_tool_use_ids:
    # Always show skill results
    print_rich_message("skill_result", f"Skill '{skill_name}' completed\n\n{formatted_content}", console)
else:
    # Regular tool results - only show in verbose mode
    if verbose:
        print_rich_message("tool_result", formatted_content, console)
```

**Benefits**:
- Clean default experience for end users
- Full transparency for developers and debugging
- Runtime toggleable without restart
- Matches Claude Code terminal experience when verbose

#### Message Type Handling

The SDK returns different message types that must be parsed and displayed appropriately:

##### SystemMessage
- **Type**: System-level notifications
- **Subtypes**:
  - `compact_boundary`: Session compaction events
  - Other: General system messages
- **Display**: Cyan panel, compact format

##### AssistantMessage
- **Type**: Main AI responses
- **Content Blocks**:
  - `TextBlock`: Main text response
  - `ToolUseBlock`: Tool invocations (e.g., invoking change-agent)
  - `ThinkingBlock`: Reasoning process
- **Display**: Green panel for Risk Agent responses

##### UserMessage
- **Type**: User inputs and tool results
- **Content Blocks**:
  - `ToolResultBlock`: Results from tool executions
- **Display**: Yellow panel for user, Magenta panel for tool results

##### ResultMessage
- **Type**: Session statistics and metadata
- **Content**: Token usage, cost, duration, session ID
- **Display**: Optional Rich table (controlled by `print_stats` flag)

#### Key Functions

##### `is_json_string(text: str) -> bool`
```python
def is_json_string(text: str) -> bool:
    """Check if a string is valid JSON"""
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError:
        return False
```

**Purpose**: Determine if text should be syntax-highlighted as JSON

##### `format_tool_result(content) -> str`
```python
def format_tool_result(content) -> str:
    """Format tool result content, handling nested JSON strings"""
    # Handles str, list, dict with JSON parsing
    # Returns formatted JSON or plain text
```

**Purpose**: Pretty-print tool results with proper indentation and formatting

**Features**:
- Detects and parses nested JSON
- Handles list of content blocks
- Pretty-prints with 2-space indentation
- Falls back to plain text if not JSON

##### `print_rich_message(type, message, console)`
```python
def print_rich_message(
    type: Literal["user", "assistant", "tool_use", "tool_result", "system"],
    message: str,
    console: Console
):
    """Prints message in styled panel with color-coded borders"""
```

**Style Configuration**:

| Message Type | Color | Border Style | Panel Title |
|--------------|-------|--------------|-------------|
| user | Yellow | yellow | User Prompt |
| assistant | Green | green | Risk Agent |
| tool_use | Blue | blue | Tool Use |
| tool_result | Magenta | magenta | Tool Result |
| system | Cyan | cyan | System Message |

**Special Handling**:
- **Tool Results**: JSON syntax highlighting with Monokai theme
- **All Panels**: Full-width (`expand=True`) for consistent sizing
- **Double line breaks**: `end="\n\n"` for readability

##### `parse_and_print_message(message, console, print_stats)`
```python
def parse_and_print_message(
    message: Message,
    console: Console,
    print_stats: bool = False
):
    """Main message dispatcher - routes to appropriate formatter"""
```

**Flow**:
1. Check message type with `isinstance()`
2. Handle message-specific logic
3. Iterate through content blocks
4. Call `print_rich_message()` with appropriate styling

## Message Flow Example

### Example: Project Planning Query

**User Input**:
```
You: Help me plan a Basel IV implementation project
```

**Message Stream**:

1. **SystemMessage** (Session Init)
   ```
   ┌─ System Message ─────────────────────────────────────┐
   │ Session initialized                                  │
   └──────────────────────────────────────────────────────┘
   ```

2. **AssistantMessage with ToolUseBlock** (Orchestrator → Change-Agent)
   ```
   ┌─ Tool Use ───────────────────────────────────────────┐
   │ Tool: <Task>                                         │
   │                                                      │
   │ {                                                    │
   │   "subagent_type": "change-agent",                   │
   │   "description": "Plan Basel IV project",            │
   │   "prompt": "Help me plan a Basel IV implementation" │
   │ }                                                    │
   └──────────────────────────────────────────────────────┘
   ```

3. **UserMessage with ToolResultBlock** (Change-Agent Response)
   ```
   ┌─ Tool Result ────────────────────────────────────────┐
   │ {                                                    │
   │   "content": [                                       │
   │     {                                                │
   │       "type": "text",                                │
   │       "text": "[Project plan content...]"            │
   │     }                                                │
   │   ]                                                  │
   │ }                                                    │
   └──────────────────────────────────────────────────────┘
   ```

4. **AssistantMessage with TextBlock** (Final Response)
   ```
   ┌─ Risk Agent ─────────────────────────────────────────┐
   │                                                      │
   │ # Project Plan: Basel IV Implementation              │
   │                                                      │
   │ ## Executive Summary                                 │
   │ - Implement standardized approach for credit risk    │
   │ - 12-month timeline with 4 phases                    │
   │ - Key risks: data quality, system changes            │
   │                                                      │
   │ [Full plan continues...]                             │
   │                                                      │
   └──────────────────────────────────────────────────────┘
   ```

## User Interface Features

### Commands

| Command | Action | Example |
|---------|--------|---------|
| `help` | Display help information | Type `help` and press Enter |
| `clear` | Clear screen (maintains context) | Type `clear` and press Enter |
| `exit`, `quit`, `q` | Exit application | Type `exit` and press Enter |

### Status Indicators

**Processing**:
```
⠋ Risk Intelligence Engine analyzing query...
```
- Animated spinner during agent processing
- Cyan colored text
- Automatically dismissed when response arrives

### Error Handling

**Display Format**:
```
Error: [error message]
Please check your setup and try again
```
- Red bold text for error labels
- Dimmed troubleshooting hints
- Maintains conversation context

## Rich Library Features Used

### Panels
- **Purpose**: Bordered containers for messages
- **Features**:
  - Title bars
  - Color-coded borders
  - Full-width or fit-to-content sizing
  - Padding and alignment

### Syntax Highlighting
- **Purpose**: JSON formatting in tool results
- **Theme**: Monokai
- **Features**:
  - Color-coded JSON keys/values
  - Indentation preservation
  - Automatic line wrapping

### Console
- **Purpose**: Core output management
- **Features**:
  - Styled text (bold, dim, italic, colors)
  - Status spinners
  - Clear screen
  - Prompt styling

### Markdown Rendering
- **Purpose**: Format text responses
- **Features**:
  - Headers (# ## ###)
  - Lists (bullet, numbered)
  - Code blocks
  - Bold/italic
  - Links

### Tables
- **Purpose**: Session statistics (optional)
- **Features**:
  - Column alignment
  - Header styling
  - Border styles
  - Title bars

## Configuration

### SDK Options

Configured in `risk_agent_cli.py`:

```python
options = ClaudeAgentOptions(
    model="claude-sonnet-4-5",              # Claude model
    permission_mode="acceptEdits",           # Auto-accept tool edits
    setting_sources=["project"],             # Load from .claude/
    system_prompt="agents/risk-intelligence-engine"  # Orchestrator
)
```

### Console Setup

```python
console = Console()  # Default Rich console with auto-detection
```

**Auto-detection includes**:
- Terminal width
- Color support (true color, 256, 16, or monochrome)
- Unicode support
- Interactive vs. non-interactive (pipes)

## Running the CLI

### Standard Usage

```bash
cd /Users/gavinslater/projects/riskagent

# Standard mode (rich interface, standard detail)
uv run riskagent

# Verbose mode (rich interface, full detail)
uv run riskagent --verbose
# or
uv run riskagent -v

# Simple interface (plain text, standard detail)
uv run riskagent --simple
# or
uv run riskagent -s

# Combine modes (simple interface + verbose detail)
uv run riskagent --simple --verbose
```

### Development Mode

```bash
# Run directly with Python
uv run python src/risk_agent_cli.py

# With full options
uv run python src/risk_agent_cli.py --simple --verbose
```

## Testing the Frontend

### Visual Tests

1. **Welcome Banner**:
   ```bash
   uv run riskagent
   # Check: Formatted panel with branding and commands
   ```

2. **User Input Styling**:
   ```
   You: [text appears in yellow]
   ```

3. **Assistant Response**:
   ```
   # Should see green panel with "Risk Agent" title
   ```

4. **Tool Invocation**:
   ```bash
   You: Help me plan a project
   # Should see blue "Tool Use" panel when orchestrator invokes change-agent
   ```

5. **Help Command**:
   ```bash
   You: help
   # Should see formatted markdown help with sections
   ```

6. **Error Handling**:
   ```bash
   # Disconnect internet and try a query
   # Should see red error message with helpful text
   ```

### Functional Tests

**Test Checklist**:
- [ ] Welcome banner displays correctly
- [ ] User prompt is yellow and bold
- [ ] Assistant responses in green panels
- [ ] Tool use shows in blue panels
- [ ] Tool results in magenta with JSON highlighting
- [ ] System messages in cyan panels
- [ ] All panels same width
- [ ] Help command works
- [ ] Clear command works
- [ ] Exit command works
- [ ] Ctrl+C handled gracefully
- [ ] Markdown rendering works (headers, lists, bold)
- [ ] Status spinner shows during processing
- [ ] Errors display in red with hints

## Known Limitations

### Current Version (MVP)

1. **No Session Persistence**:
   - Conversation history lost on exit
   - No save/load functionality

2. **Limited Statistics**:
   - `print_stats=False` by default
   - Can enable for debugging

3. **No Color Customization**:
   - Hardcoded color scheme
   - Future: user preferences

4. **No Output Export**:
   - Terminal only
   - Future: save to file, copy to clipboard

## Enhancement Opportunities

### Short Term
1. **Session Management**:
   - Save conversation history
   - Resume previous sessions
   - Export conversations to markdown

2. **Better Error Messages**:
   - Specific troubleshooting for common errors
   - Links to documentation
   - Retry logic

3. **Statistics Display**:
   - Optional stats table at end of session
   - Token usage tracking
   - Cost estimation

### Medium Term
1. **Custom Themes**:
   - User-configurable color schemes
   - Light/dark mode toggle
   - Accessibility options (high contrast)

2. **Rich History**:
   - Navigate previous queries with arrow keys
   - Search conversation history
   - Conversation branching

3. **Output Formats**:
   - Export to PDF
   - Generate HTML reports
   - Copy formatted responses

### Long Term
1. **TUI (Text User Interface)**:
   - Split panes for input/output
   - Sidebar with conversation history
   - Tool invocation visualization

2. **Streaming Improvements**:
   - Live typing effect for responses
   - Progress bars for long operations
   - Real-time token counting

3. **Multi-Session Support**:
   - Multiple conversation tabs
   - Session comparison
   - Collaborative sessions

## Troubleshooting

### Common Issues

**Issue**: Panels different widths
**Solution**: Ensure `expand=True` in `cli_utils.py` line 116

**Issue**: Colors not showing
**Solution**: Check terminal supports colors (most modern terminals do)

**Issue**: Markdown not rendering
**Solution**: Verify Rich library installed: `uv pip list | grep rich`

**Issue**: JSON not syntax highlighted
**Solution**: Check `is_json_string()` function in `cli_utils.py`

**Issue**: Status spinner freezes
**Solution**: Ensure async loop is running properly, check for blocking calls

## File Structure

```
src/
├── risk_agent_cli.py          # Main CLI entry point
│   ├── cli()                  # Sync wrapper for script execution
│   ├── main()                 # Async conversation loop (with verbose & interface params)
│   ├── show_welcome()         # Welcome banner
│   ├── show_help()            # Help display
│   └── get_user_input()       # User prompt
│
├── cli_utils.py               # Message formatting utilities
│   ├── parse_and_print_message()   # Main dispatcher (supports interface mode)
│   ├── print_rich_message()        # Rich panel formatting
│   ├── print_simple_message()      # Simple text formatting (NEW v1.1)
│   ├── format_tool_result()        # JSON formatter
│   └── is_json_string()            # JSON validator
│
├── telegram_bot.py            # Telegram bot interface (NEW v1.1)
│   ├── RiskAgentSession        # Per-user session management
│   ├── Command handlers        # /start, /help, /status, /setcwd, /verbose, /reset
│   └── handle_message()        # Main message handler
│
└── telegram_utils.py          # Telegram message utilities (NEW v1.1)
    ├── extract_message_text()      # Convert SDK messages to text
    ├── split_long_message()        # Handle 4096 char limit
    └── format_telegram_code_block() # Telegram markdown
```

## Dependencies

```toml
[project.dependencies]
anthropic = ">=0.40.0"              # Claude API
claude-agent-sdk = ">=0.1.6"        # Agent orchestration
rich = ">=13.0.0"                   # Terminal formatting
python-telegram-bot = ">=20.0"      # Telegram bot (NEW v1.1)
python-docx = ">=1.1.0"             # Word document processing (skills)
openpyxl = ">=3.1.0"                # Excel processing (skills)
pandas = ">=2.0.0"                  # Data manipulation (skills)
```

## References

- [Rich Documentation](https://rich.readthedocs.io/)
- [Claude Agent SDK Python Docs](https://docs.claude.com/en/api/agent-sdk/python)
- [kenneth-liao Tutorial](https://github.com/kenneth-liao/claude-agent-sdk-intro)
- [Rich API Reference](https://rich.readthedocs.io/en/stable/reference.html)
- [Telegram Bot Setup Guide](./13-telegram-bot-setup.md) - Remote access via Telegram
- [Telegram Integration Analysis](./11-telegram-integration-analysis.md) - Architecture and design
- [Session Management Comparison](./12-session-management-comparison.md) - Session persistence patterns

## Interface Mode Deep Dive

**Added**: 2025-01-09
**Version**: 1.1

### Feature Overview

Interface mode controls the visual formatting of CLI output. Two modes are available:
- **Rich Mode** (default): Enhanced terminal interface with colored panels and syntax highlighting
- **Simple Mode**: Plain text output with emoji prefixes (same format as Telegram bot)

### Comparison

| Feature | Rich Mode | Simple Mode |
|---------|-----------|-------------|
| Panels with borders | ✅ Yes | ❌ No |
| Color formatting | ✅ Yes | ✅ Yes (limited) |
| Syntax highlighting | ✅ Yes (JSON) | ❌ No |
| Message prefixes | ❌ No (in title) | ✅ Emoji prefixes |
| Visual separation | ✅ Panels | 📝 Whitespace |
| Use case | Terminal usage | Logging, Telegram |

### Rich Mode Output Example

```
╭──────────────────────────────────╮
│ 🤖 Risk Agent                    │
╰──────────────────────────────────╯
I'll help you plan that Basel IV
implementation project.

╭─────────────────────────────────────────╮
│ 🔧 Skill Invocation                     │
╰─────────────────────────────────────────╯
Skill: project-planner

Arguments:
{
  "project_name": "Basel IV Implementation",
  "scope": "regulatory compliance"
}

╭─────────────────────────────────────────╮
│ ✅ Skill Output                          │
╰─────────────────────────────────────────╯
Skill 'project-planner' completed

{
  "success": true,
  "charter_created": true,
  "timeline_months": 18
}
```

### Simple Mode Output Example

```
🤖 Risk Agent:
I'll help you plan that Basel IV
implementation project.

🔧 Skill: project-planner

Arguments:
{
  "project_name": "Basel IV Implementation",
  "scope": "regulatory compliance"
}

✅ Skill Result: project-planner

{
  "success": true,
  "charter_created": true,
  "timeline_months": 18
}
```

### When to Use Each Mode

**Rich Mode (Default)**:
- ✅ Working in modern terminal with color support
- ✅ Want visual clarity and separation
- ✅ Prefer structured, formatted output
- ✅ Using terminal for extended sessions
- ✅ Presenting output to others

**Simple Mode**:
- ✅ Logging output to files (`uv run riskagent --simple > log.txt`)
- ✅ Limited terminal (no color support)
- ✅ Matching Telegram bot output format for consistency
- ✅ Minimalist preference
- ✅ Piping output to other tools
- ✅ Screen readers / accessibility tools

### Combining with Verbose Mode

Interface mode and verbose mode are **orthogonal** - they can be combined:

```bash
# Rich + Standard: Default experience
uv run riskagent

# Rich + Verbose: Detailed output with panels
uv run riskagent --verbose

# Simple + Standard: Plain text, outcomes only
uv run riskagent --simple

# Simple + Verbose: Plain text with full detail (like Claude Code)
uv run riskagent --simple --verbose
```

**Example: Simple + Verbose** (closest to Claude Code terminal):
```
🤖 Risk Agent:
I'll populate the ICC template.

🔨 Tool: Read
Input:
{
  "file_path": "/path/to/template.xlsm"
}

📋 Result:
File loaded successfully. 17 sheets detected.

🔨 Tool: Bash
Input:
{
  "command": "python .claude/skills/icc-business-case-filler/..."
}

📋 Result:
====================
ICC TEMPLATE POPULATION
====================
Step 1: Pre-populating from ITC...
  ✓ Project Name: Energy VaR
  ✓ Sponsor: John Smith
[... detailed progress ...]

🔧 Skill: icc-business-case-filler
Arguments: {...}

✅ Skill Result: icc-business-case-filler
{
  "success": true,
  "populated_fields": 47
}
```

### Runtime Toggle

Switch interface modes without restarting:

```bash
$ uv run riskagent

You: interface
Interface mode: simple
Plain text output (like Claude Code)

You: [query - see simple format]

You: i  # shortcut
Interface mode: rich
Rich formatted output with panels and colors

You: [query - see rich format]
```

### Telegram Bot Consistency

Simple mode uses **exactly the same formatting** as the Telegram bot:
- Same emoji prefixes (🤖, 🔧, ✅, 🔨, 📋)
- Same text structure
- Same message types

This means:
- Test Telegram bot output in CLI with `--simple`
- Debug message formatting in terminal before deploying to Telegram
- Consistent experience across CLI and Telegram interfaces

### Implementation

Both formatting functions share the same signature:

```python
# Rich formatting
def print_rich_message(type, message, console):
    # Create Panel with borders and colors
    panel = Panel(content, title=..., border_style=...)
    console.print(panel)

# Simple formatting
def print_simple_message(type, message, console):
    # Emoji prefix + plain text
    prefix = prefixes.get(type, "")
    console.print(f"\n{prefix}\n{message}\n")

# Dynamic selection in parse_and_print_message()
print_fn = print_simple_message if interface == "simple" else print_rich_message
print_fn("assistant", "I'll help you...", console)
```

## Verbose Mode Deep Dive

**Added**: 2025-01-09
**Version**: 1.1

### Feature Overview

Verbose mode provides full transparency into agent execution, showing every tool call and result. This matches the detail level of the Claude Code terminal experience.

### Use Cases

**1. Debugging Skill Execution**
```bash
# Enable verbose to see what files skills are reading/writing
uv run riskagent --verbose

You: Complete the ICC template for Energy VaR project

# In verbose mode, you'll see:
╭─── Tool Use ───╮
│ Tool: Read     │
│ Input: {       │
│   "file_path": │
│   "/path/to/   │
│   template.xlsm│
│ }              │
╰────────────────╯

╭─── Tool Result ───╮
│ [Excel template   │
│  metadata...]     │
╰───────────────────╯

[... many more tool calls showing exactly what's happening ...]
```

**2. Learning Agent Internals**
See how skills break down complex tasks into individual operations:
- Which files are read
- What bash commands execute
- How data flows between tools
- Where errors occur in the pipeline

**3. Verifying Data Extraction**
When skills extract information from documents:
```
╭─── Tool Use ───╮
│ Tool: Grep     │
│ Pattern: "Project Name:.*" │
╰────────────────╯

╭─── Tool Result ───╮
│ Found in line 42: │
│ "Project Name: Energy VaR Migration" │
╰───────────────────╯
```

**4. Monitoring File Operations**
Track exactly what files are modified:
```
╭─── Tool Use ───╮
│ Tool: Write    │
│ file_path: output/populated_template.xlsm │
╰────────────────╯
```

### Runtime Toggle

You can enable/disable verbose mode without restarting:

```bash
$ uv run riskagent

You: verbose
Verbose mode enabled
All tool calls and results will be shown

You: [run complex task - see all details]

You: v   # shortcut to toggle
Verbose mode disabled
Only showing skill invocations and assistant responses
```

### Output Comparison

#### Standard Mode Output
```
╭─────────── Risk Agent ───────────╮
│ I'll populate the ICC template   │
│ using the ITC template you       │
│ provided.                        │
╰──────────────────────────────────╯

╭───── Skill: icc-business-case-filler ─────╮
│ Arguments: {                               │
│   "template_path": "...",                  │
│   "itc_template_path": "..."               │
│ }                                          │
╰────────────────────────────────────────────╯

╭───── Skill 'icc-business-case-filler' completed ─────╮
│ {                                                     │
│   "success": true,                                    │
│   "populated_fields": 47,                             │
│   "pre_populated_from_itc": 35                        │
│ }                                                     │
╰───────────────────────────────────────────────────────╯

╭─────────── Risk Agent ───────────╮
│ Successfully populated 47 fields │
│ [clarification questions...]     │
╰──────────────────────────────────╯
```

#### Verbose Mode Output
```
╭─────────── Risk Agent ───────────╮
│ I'll populate the ICC template   │
│ using the ITC template you       │
│ provided.                        │
╰──────────────────────────────────╯

╭───── Tool Use ─────╮
│ Tool: Read         │
│ Input: {           │
│   "file_path":     │
│   "/path/template" │
│ }                  │
╰────────────────────╯

╭───── Tool Result ─────╮
│ File metadata:        │
│ Size: 301KB           │
│ Format: .xlsm         │
│ Sheets: 17            │
╰───────────────────────╯

╭───── Tool Use ─────╮
│ Tool: Bash         │
│ Command: python... │
╰────────────────────╯

╭───── Tool Result ─────╮
│ ==================== │
│ ICC TEMPLATE POPULATION │
│ ==================== │
│ Step 1: Pre-populating from ITC... │
│   ✓ Project Name: Energy VaR       │
│   ✓ Sponsor: John Smith            │
│ [... detailed progress output ...] │
╰───────────────────────╯

╭───── Skill: icc-business-case-filler ─────╮
│ [Same as standard mode]                    │
╰────────────────────────────────────────────╯

[... more tool calls and results ...]

╭───── Skill 'icc-business-case-filler' completed ─────╮
│ [Same as standard mode]                               │
╰───────────────────────────────────────────────────────╯

╭─────────── Risk Agent ───────────╮
│ Successfully populated 47 fields │
│ [clarification questions...]     │
╰──────────────────────────────────╯
```

### Performance Considerations

**Console Output Volume**:
- Standard mode: ~3-5 panels per query
- Verbose mode: ~20-50+ panels for complex operations (like ICC template population)

**When to Use Each**:
- **Standard**: Daily usage, clean experience, focus on outcomes
- **Verbose**: Development, debugging, learning, error investigation

### Implementation Notes

The verbose flag is passed through the entire message processing pipeline:

```
cli() [parses --verbose flag]
  ↓
main(verbose=True)
  ↓
parse_and_print_message(message, console, verbose=True)
  ↓
[Conditional rendering based on verbose flag]
```

No performance overhead when verbose is disabled - tool calls and results are simply not rendered to console.

## Changelog

### Version 1.1 (2025-01-09)
- ✅ **Interface mode** - Toggle between rich panels and simple text
  - Command-line flags: `--simple` / `-s`
  - Runtime toggle command: `interface` or `i`
  - Rich mode: Enhanced panels with colors and syntax highlighting (default)
  - Simple mode: Plain text with emoji prefixes (matches Telegram bot)
  - Both modes combinable with verbose mode
- ✅ **Verbose mode** - Toggle between clean and detailed output
  - Command-line flags: `--verbose` / `-v`
  - Runtime toggle command: `verbose` or `v`
  - Shows all tool calls and results when enabled
  - Matches Claude Code terminal experience
- ✅ **Telegram integration** - Remote access via Telegram bot
  - Uses simple interface mode for consistent formatting
  - Per-user session management
  - Working directory control
- ✅ Enhanced help text with all mode documentation
- ✅ Updated welcome banner with new commands

### Version 1.0 (2025-11-05)
- ✅ Initial CLI implementation
- ✅ Proper message parsing from kenneth-liao pattern
- ✅ Rich formatting with panels
- ✅ JSON syntax highlighting
- ✅ Consistent panel widths
- ✅ Welcome banner and help system
- ✅ Error handling and status indicators
- ✅ Command system (help, clear, exit)

### Planned for Version 1.2
- Session persistence for CLI (already in Telegram bot)
- Statistics display
- Output export
- Custom themes
- Configurable verbose level (minimal, standard, full)
- History navigation with arrow keys
