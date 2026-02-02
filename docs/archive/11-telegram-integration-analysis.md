# Telegram Integration Analysis for Risk Agent

**Date**: 2025-01-09
**Comparing**: Risk Agent vs Cole Medin's Ottomator Implementation

---

## Executive Summary

Cole Medin's Telegram bot implementation provides a solid foundation for adding Telegram support to the Risk Agent. The architectures are highly compatible, with both using the Claude Agent SDK's session management and async patterns. Key integration opportunities include per-user session management, working directory configuration, and streaming responses.

---

## 1. CLI Implementation Comparison

### Architecture Similarities

Both implementations follow the **same core pattern**:

| Aspect | Risk Agent (`risk_agent_cli.py`) | Cole Medin (`simple_cli.py`) |
|--------|----------------------------------|------------------------------|
| **Framework** | ClaudeSDKClient + Rich | ClaudeSDKClient + Colorama |
| **Pattern** | Async conversation loop | Async conversation loop |
| **Session** | Not explicitly managed | Saved to `sessions/` JSON |
| **Message Loop** | `client.receive_response()` | `client.receive_response()` |
| **Streaming** | Via Rich panels | Via colored text |
| **Tool Handling** | Distinguishes Skills vs Tools | Shows all tools uniformly |

### Key Architectural Differences

#### 1. Session Management

**Cole Medin's Approach:**
```python
# Explicit session persistence
def save_session(session_id: str):
    SESSIONS_DIR.mkdir(exist_ok=True)
    with open(CURRENT_SESSION_FILE, "w") as f:
        json.dump({"session_id": session_id}, f)

# Resume support built-in
options_dict = {
    "cwd": os.getcwd(),
    "system_prompt": "You are a helpful AI assistant.",
    "allowed_tools": ["Read", "Write", "Bash"],
}
if session_id:
    options_dict["resume"] = session_id  # KEY: Resume parameter

options = ClaudeAgentOptions(**options_dict)
```

**Risk Agent's Approach:**
```python
# No explicit session persistence (relies on SDK internal state)
options = ClaudeAgentOptions(
    model="claude-sonnet-4-5",
    permission_mode="acceptEdits",
    setting_sources=["project"],  # Load from .claude/
    system_prompt="agents/risk-intelligence-engine",  # Orchestrator
    allowed_tools=['Skill', 'Read', 'Write', 'Edit', ...]
)
```

**Implication**: Risk Agent would need to add session persistence for Telegram multi-user support.

#### 2. Agent Configuration

**Cole Medin:**
- Simple system prompt string
- Direct tool configuration
- Single agent (no orchestrator)

**Risk Agent:**
- Agent orchestration (`risk-intelligence-engine` → `change-agent`)
- Skill system integration
- Project-specific settings from `.claude/` directory

**Implication**: Risk Agent's architecture is more sophisticated but requires careful mapping to Telegram user contexts.

#### 3. Output Handling

**Cole Medin:**
```python
# Simple streaming with color codes
async for message in client.receive_response():
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                print(f"{Fore.GREEN}{block.text}{Style.RESET_ALL}", end="", flush=True)
            elif isinstance(block, ToolUseBlock):
                print(f"\n{Back.MAGENTA}{Fore.WHITE} 🔧 {block.name.upper()} {Style.RESET_ALL}")
```

**Risk Agent:**
```python
# Structured message parsing with Rich panels
async for message in client.receive_response():
    parse_and_print_message(message, console, print_stats=False, verbose=verbose)
    # Handles Skills specially, distinguishes from regular tools
```

**Implication**: For Telegram, we'll need simpler text formatting (no Rich panels, limited Markdown).

---

## 2. Telegram Bot Architecture Analysis

### Cole Medin's Telegram Bot Structure

```
telegram_bot.py
├── Session Management (Per-User)
│   ├── save_user_session(user_id, session_id, cwd)
│   ├── load_user_session(user_id) → (session_id, cwd)
│   ├── set_user_cwd(user_id, cwd)
│   ├── get_user_cwd(user_id)
│   └── clear_user_session(user_id)
│
├── Command Handlers
│   ├── /start - Welcome message
│   ├── /help - Show commands
│   ├── /setcwd <path> - Set working directory
│   ├── /getcwd - Show current directory
│   ├── /searchcwd <query> - Find directories
│   └── /reset - Clear conversation
│
├── Message Handler
│   ├── Load user session & cwd
│   ├── Configure ClaudeAgentOptions with user context
│   ├── Send query to Claude SDK
│   ├── Stream response back to Telegram
│   └── Save updated session
│
└── Utility Functions
    └── send_long_message() - Handle 4096 char limit
```

### Key Features

#### 1. Per-User Session Isolation

**Storage Pattern:**
```
telegram_sessions/
├── 123456789.json   # User 1's session
├── 987654321.json   # User 2's session
└── ...

# Session file structure:
{
  "session_id": "sdk_generated_session_id",
  "cwd": "/path/to/user/workspace",
  "created_at": "2025-01-09T10:00:00Z",
  "last_updated": "2025-01-09T10:30:00Z"
}
```

**Benefits:**
- Each user has independent conversation context
- Working directory is user-specific
- Sessions persist across bot restarts
- Privacy: users can't see each other's conversations

#### 2. Working Directory Management

**Critical for File Operations:**
```python
# Each user configures their own workspace
/setcwd /Users/gavin/projects/myproject

# Claude Code then operates in that directory
"Read the README.md"  # Reads from user's configured cwd
"List Python files"   # Lists from user's cwd
```

**Why This Matters:**
- Without per-user cwd, all users would share the same filesystem context
- Risk Agent skills (like `itc-template-filler`) need to read/write project files
- Each user might be working on different projects

#### 3. Streaming Response Handling

**Challenge:**
```python
# Claude SDK streams tokens in real-time
async for message in client.receive_response():
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                response_parts.append(block.text)  # Collect

# But Telegram doesn't support streaming well
# So we collect all parts, then send complete message
full_response = "".join(response_parts)
await update.message.reply_text(full_response)
```

**Options:**
1. **Collect & Send Once** (Cole's approach): Wait for complete response, send as one message
2. **Progressive Updates**: Send message, edit it as more content arrives (complex, rate-limited)
3. **Chunked Delivery**: Send logical chunks (paragraphs) as they complete

#### 4. Message Length Handling

**Telegram Limit:** 4096 characters per message

**Cole's Solution:**
```python
async def send_long_message(chat_id: int, text: str, context):
    """Split long messages intelligently"""
    if len(text) <= 4096:
        await context.bot.send_message(chat_id=chat_id, text=text)
    else:
        # Split by lines to avoid breaking mid-sentence
        chunks = []
        for line in text.split("\n"):
            # Build chunks respecting 4096 limit
            # Add "(continued N/M)" indicators

        for chunk in chunks:
            await context.bot.send_message(chat_id=chat_id, text=chunk)
```

**Risk Agent Consideration:**
- Status reports can be long (especially with verbose risk analysis)
- ICC clarification questions can exceed 4096 chars
- Need intelligent splitting that preserves markdown formatting

---

## 3. Integration Strategy for Risk Agent

### Option A: Direct Telegram Bot (Recommended)

**Architecture:**
```
Telegram User
    ↓
telegram_bot.py (new)
    ↓
risk_agent_core.py (extract shared logic from risk_agent_cli.py)
    ↓
ClaudeSDKClient
    ↓
risk-intelligence-engine → change-agent → Skills
```

**Benefits:**
- Full control over Telegram-specific features
- Can optimize for mobile experience
- Direct integration with Risk Agent's orchestrator

**Implementation Plan:**

1. **Extract Core Logic** (refactor `risk_agent_cli.py`)
   ```python
   # New: src/risk_agent_core.py
   class RiskAgentSession:
       """Encapsulates a Risk Agent session"""
       def __init__(self, session_id=None, cwd=None, verbose=False):
           self.session_id = session_id
           self.cwd = cwd
           self.verbose = verbose

       async def query(self, message: str) -> AsyncIterator[Message]:
           """Send query and yield streaming responses"""
           options = self._build_options()
           async with ClaudeSDKClient(options=options) as client:
               await client.query(message)
               async for message in client.receive_response():
                   yield message

       def _build_options(self) -> ClaudeAgentOptions:
           """Build options with session resume support"""
           options_dict = {
               "model": "claude-sonnet-4-5",
               "permission_mode": "acceptEdits",
               "setting_sources": ["project"],
               "system_prompt": "agents/risk-intelligence-engine",
               "allowed_tools": ['Skill', 'Read', 'Write', ...],
               "cwd": self.cwd or os.getcwd()
           }
           if self.session_id:
               options_dict["resume"] = self.session_id
           return ClaudeAgentOptions(**options_dict)
   ```

2. **Create Telegram Bot** (adapting Cole's pattern)
   ```python
   # New: src/telegram_bot.py
   from src.risk_agent_core import RiskAgentSession

   async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
       user_id = update.effective_user.id
       user_message = update.message.text

       # Load user's Risk Agent session
       session_data = load_user_session(user_id)
       session_id, cwd = session_data if session_data else (None, None)

       # Create Risk Agent session
       agent = RiskAgentSession(session_id=session_id, cwd=cwd)

       # Stream response from Risk Agent
       response_parts = []
       new_session_id = None

       async for message in agent.query(user_message):
           if isinstance(message, AssistantMessage):
               for block in message.content:
                   if isinstance(block, TextBlock):
                       response_parts.append(block.text)
           elif isinstance(message, ResultMessage):
               new_session_id = message.session_id

       # Send formatted response to Telegram
       full_response = format_for_telegram("".join(response_parts))
       await send_long_message(update.message.chat_id, full_response, context)

       # Save session
       if new_session_id:
           save_user_session(user_id, new_session_id, cwd)
   ```

3. **Telegram-Specific Commands**
   ```python
   /start - Welcome to Risk Agents
   /help - Show capabilities
   /setcwd <path> - Set project directory
   /skills - List available skills
   /verbose - Toggle verbose mode (show tool calls)
   /reset - Clear conversation history

   # Risk Agent specific:
   /itc - Show ITC template filler help
   /icc - Show ICC business case help
   ```

4. **Format Responses for Telegram**
   ```python
   def format_for_telegram(text: str) -> str:
       """
       Convert Risk Agent output to Telegram-friendly format
       - Replace Rich panels with simple markdown
       - Convert emoji indicators
       - Handle skill invocation formatting
       """
       # Example transformations:
       # Rich panel → **Title**\n`content`
       # Skill invocation → 🤖 **Skill: skill-name**
       # Tool use → 🔧 Tool: Read
       return formatted_text
   ```

### Option B: Telegram as Interface to Existing CLI

**Architecture:**
```
Telegram User
    ↓
telegram_bot.py
    ↓
risk_agent_cli.py (subprocess)
    ↓
ClaudeSDKClient → Agents → Skills
```

**Benefits:**
- Minimal refactoring
- Reuses existing CLI logic

**Drawbacks:**
- Less efficient (subprocess overhead)
- Harder to capture streaming responses
- Session management more complex
- Not recommended

---

## 4. Telegram-Specific Considerations

### Mobile-Friendly Features

**1. Shorter Responses**
```python
# CLI: Can display multi-page panels
# Telegram: Need concise, mobile-readable text

# Example: Status Report
# CLI version: 500+ lines with tables, diagrams
# Telegram version: Executive summary + "Show details?" inline button
```

**2. Inline Keyboards**
```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# After showing clarification questions:
keyboard = [
    [InlineKeyboardButton("Answer Questions", callback_data='answer_questions')],
    [InlineKeyboardButton("Show Full Report", callback_data='full_report')],
    [InlineKeyboardButton("Export PDF", callback_data='export_pdf')]
]
reply_markup = InlineKeyboardMarkup(keyboard)
await update.message.reply_text("ICC template 40% complete", reply_markup=reply_markup)
```

**3. File Attachments**
```python
# When skills generate Excel templates, send as files
with open(output_path, 'rb') as f:
    await context.bot.send_document(
        chat_id=chat_id,
        document=f,
        filename="ICC_BusinessCase_Populated.xlsm",
        caption="✅ Your populated ICC template is ready!"
    )
```

### Security Considerations

**1. User Authentication**
```python
# Option 1: Whitelist allowed Telegram user IDs
ALLOWED_USER_IDS = os.getenv("TELEGRAM_ALLOWED_USERS", "").split(",")

async def authorize_user(update: Update):
    user_id = update.effective_user.id
    if str(user_id) not in ALLOWED_USER_IDS:
        await update.message.reply_text("⛔ Unauthorized. Contact admin.")
        return False
    return True
```

**2. Working Directory Restrictions**
```python
# Validate cwd is within allowed paths
ALLOWED_BASE_PATHS = [
    "/Users/gavin/projects/",
    "/home/gavin/work/"
]

def validate_cwd(path: str) -> bool:
    abs_path = os.path.abspath(path)
    return any(abs_path.startswith(base) for base in ALLOWED_BASE_PATHS)
```

**3. Sensitive Data Handling**
```python
# Never send session files or credentials via Telegram
# Store sessions on server only
# Use encryption for session storage if needed
```

### Rate Limiting

**Telegram Limits:**
- 30 messages/second per bot
- 20 messages/minute to same user
- File uploads: 50MB max

**Mitigation:**
```python
import asyncio
from collections import deque
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_per_minute=15):
        self.max_per_minute = max_per_minute
        self.requests = deque()

    async def acquire(self):
        now = datetime.now()
        # Remove requests older than 1 minute
        while self.requests and self.requests[0] < now - timedelta(minutes=1):
            self.requests.popleft()

        if len(self.requests) >= self.max_per_minute:
            wait_time = 60 - (now - self.requests[0]).seconds
            await asyncio.sleep(wait_time)

        self.requests.append(now)
```

---

## 5. Implementation Roadmap

### Phase 1: Foundation (Week 1)

**Goal**: Basic Telegram bot with simple Q&A

**Tasks:**
1. ✅ Extract `RiskAgentSession` class from `risk_agent_cli.py`
2. ✅ Create `telegram_bot.py` adapting Cole's structure
3. ✅ Implement per-user session management
4. ✅ Add basic commands (`/start`, `/help`, `/reset`)
5. ✅ Test with simple queries (no skills yet)

**Deliverable**: Working Telegram bot that answers questions

### Phase 2: Working Directory & Skills (Week 2)

**Goal**: Enable file operations and skill invocation

**Tasks:**
1. ✅ Add `/setcwd` and `/getcwd` commands
2. ✅ Test file reading/writing with per-user context
3. ✅ Verify skill invocation works (test with `meeting-minutes`)
4. ✅ Add skill-specific help commands (`/skills`, `/itc`, `/icc`)
5. ✅ Format skill outputs for Telegram (markdown conversion)

**Deliverable**: Users can invoke Risk Agent skills via Telegram

### Phase 3: Template Skills Integration (Week 3)

**Goal**: Full ITC/ICC template population via Telegram

**Tasks:**
1. ✅ Test ITC template filler via Telegram
2. ✅ Test ICC template filler with clarification mode
3. ✅ Implement file attachment sending for populated templates
4. ✅ Add inline keyboards for clarification question workflows
5. ✅ Handle long clarification reports (4096 char limit)

**Deliverable**: Complete template population workflow on Telegram

### Phase 4: Polish & Security (Week 4)

**Goal**: Production-ready Telegram bot

**Tasks:**
1. ✅ Add user authentication/authorization
2. ✅ Implement rate limiting
3. ✅ Add error handling and graceful degradation
4. ✅ Create comprehensive user guide
5. ✅ Set up logging and monitoring
6. ✅ Deploy to server with systemd service

**Deliverable**: Production deployment

---

## 6. Code Examples

### Example 1: Extracted Core Session Logic

```python
# src/risk_agent_core.py
from typing import AsyncIterator, Optional
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, Message

class RiskAgentSession:
    """
    Encapsulates a Risk Agent conversation session.
    Can be used by CLI, Telegram, or other interfaces.
    """

    def __init__(
        self,
        session_id: Optional[str] = None,
        cwd: Optional[str] = None,
        verbose: bool = False,
        user_context: Optional[dict] = None
    ):
        self.session_id = session_id
        self.cwd = cwd or os.getcwd()
        self.verbose = verbose
        self.user_context = user_context or {}

    async def query(self, message: str) -> AsyncIterator[Message]:
        """
        Send a query to the Risk Agent and yield streaming responses.

        Yields:
            Message objects from Claude SDK (AssistantMessage, ResultMessage, etc.)
        """
        options = self._build_options()

        async with ClaudeSDKClient(options=options) as client:
            await client.query(message)

            async for response_message in client.receive_response():
                # Update session ID if we get a new one
                if isinstance(response_message, ResultMessage):
                    self.session_id = response_message.session_id

                yield response_message

    def _build_options(self) -> ClaudeAgentOptions:
        """Build Claude Agent SDK options with session resume support."""
        options_dict = {
            "model": "claude-sonnet-4-5",
            "permission_mode": "acceptEdits",
            "setting_sources": ["project"],
            "system_prompt": "agents/risk-intelligence-engine",
            "allowed_tools": [
                'Skill', 'Read', 'Write', 'Edit', 'MultiEdit',
                'Grep', 'Glob', 'Task', 'TodoWrite',
                'WebSearch', 'WebFetch', 'Bash'
            ],
            "cwd": self.cwd
        }

        # Add session resume if we have a session ID
        if self.session_id:
            options_dict["resume"] = self.session_id

        return ClaudeAgentOptions(**options_dict)

    def to_dict(self) -> dict:
        """Serialize session for persistence."""
        return {
            "session_id": self.session_id,
            "cwd": self.cwd,
            "verbose": self.verbose,
            "user_context": self.user_context
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'RiskAgentSession':
        """Deserialize session from persistence."""
        return cls(
            session_id=data.get("session_id"),
            cwd=data.get("cwd"),
            verbose=data.get("verbose", False),
            user_context=data.get("user_context", {})
        )
```

### Example 2: Telegram Message Handler with Risk Agent

```python
# src/telegram_bot.py
from src.risk_agent_core import RiskAgentSession
from telegram import Update
from telegram.ext import ContextTypes

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages from Telegram users."""
    user = update.effective_user
    user_id = user.id
    user_message = update.message.text

    logger.info(f"User {user_id} ({user.username}): {user_message[:50]}...")

    try:
        # Load user's session from storage
        session_data = load_user_session(user_id)

        # Create or restore Risk Agent session
        if session_data:
            agent = RiskAgentSession.from_dict(session_data)
            logger.info(f"Resumed session for user {user_id}")
        else:
            # New session - use default working directory
            agent = RiskAgentSession(cwd=get_user_cwd(user_id))
            logger.info(f"New session for user {user_id}")

        # Send "typing" indicator
        await update.message.chat.send_action("typing")

        # Collect response from Risk Agent
        response_collector = TelegramResponseCollector()

        async for message in agent.query(user_message):
            response_collector.process_message(message)

        # Format and send response
        formatted_response = response_collector.get_formatted_response()

        await send_long_message(
            chat_id=update.message.chat_id,
            text=formatted_response,
            context=context
        )

        # Save updated session
        save_user_session(user_id, agent.to_dict())
        logger.info(f"Saved session for user {user_id}")

    except Exception as e:
        logger.error(f"Error handling message from user {user_id}: {e}", exc_info=True)
        await update.message.reply_text(
            "⚠️ Sorry, I encountered an error.\n"
            f"Error: {str(e)}\n\n"
            "Use /reset to start fresh or try again."
        )


class TelegramResponseCollector:
    """Collects and formats streaming responses for Telegram."""

    def __init__(self):
        self.text_parts = []
        self.tool_uses = []
        self.skill_uses = []

    def process_message(self, message: Message):
        """Process a message from the Claude SDK stream."""
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    self.text_parts.append(block.text)
                elif isinstance(block, ToolUseBlock):
                    if block.name == "Skill":
                        skill_name = block.input.get("skill", "unknown")
                        self.skill_uses.append(skill_name)
                    else:
                        self.tool_uses.append(block.name)

    def get_formatted_response(self) -> str:
        """Get the complete formatted response for Telegram."""
        # Join text parts
        text = "".join(self.text_parts)

        # Add tool usage indicators at the end
        if self.skill_uses:
            text += "\n\n🤖 **Skills Used:** " + ", ".join(self.skill_uses)

        if self.tool_uses:
            text += "\n🔧 **Tools:** " + ", ".join(set(self.tool_uses))

        return text or "I processed your request."
```

---

## 7. Comparison Summary

### What Risk Agent Has (Advantages)

1. ✅ **Multi-Agent Orchestration**: Sophisticated routing via orchestrator
2. ✅ **Skills System**: Reusable, complex capabilities (template filling, planning)
3. ✅ **Domain Expertise**: Banking/risk management context baked in
4. ✅ **Rich Output Formatting**: Beautiful CLI with verbose mode
5. ✅ **Comprehensive Documentation**: Well-documented architecture

### What Cole's Implementation Has (Learn From)

1. ✅ **Session Persistence**: Explicit save/resume logic
2. ✅ **Per-User Context**: Well-designed multi-user session management
3. ✅ **Working Directory Management**: Per-user cwd configuration
4. ✅ **Telegram Integration**: Production-ready bot with all commands
5. ✅ **Message Length Handling**: Smart text splitting

### What Risk Agent Needs to Add

1. ❌ **Session Persistence Layer** - Extract from SDK, save to JSON
2. ❌ **Per-User Session Management** - Adapt Cole's pattern for Telegram
3. ❌ **Core Logic Extraction** - Create `RiskAgentSession` class
4. ❌ **Telegram Output Formatting** - Convert Rich panels to Markdown
5. ❌ **File Attachment Sending** - For Excel templates

---

## 8. Recommendations

### Immediate Next Steps

1. **Refactor CLI** to extract `RiskAgentSession` class
   - This makes the core logic reusable
   - CLI becomes a thin wrapper around `RiskAgentSession`
   - Telegram bot can then use the same core

2. **Adapt Cole's Telegram Structure** with Risk Agent specifics
   - Copy session management functions
   - Modify message handler to use `RiskAgentSession`
   - Add Risk Agent-specific commands

3. **Start Simple, Add Complexity**
   - Phase 1: Basic Q&A (no skills)
   - Phase 2: File operations
   - Phase 3: Skill invocation
   - Phase 4: Template workflows with file attachments

### Long-Term Considerations

1. **Multi-Interface Design**: Design for CLI + Telegram + (future Web UI)
2. **Shared Session Store**: Consider database for session management
3. **Webhook vs Polling**: For production, use webhooks not polling
4. **Monitoring**: Add Sentry or similar (Cole has `telegram_bot_sentry.py`)

---

## 9. Conclusion

Cole Medin's Telegram implementation provides an excellent blueprint for adding Telegram support to Risk Agent. The key is to:

1. Extract Risk Agent's core session logic into a reusable `RiskAgentSession` class
2. Adapt Cole's per-user session management and Telegram command structure
3. Bridge Risk Agent's sophisticated orchestrator/skills architecture with Telegram's simpler text-based interface
4. Implement phased rollout starting with basic features

The architectures are highly compatible - both use the Claude Agent SDK's async patterns and session management. The main work is in creating the abstraction layer (`RiskAgentSession`) that can be used by both CLI and Telegram interfaces.

**Estimated Effort**: 2-4 weeks for production-ready Telegram bot with full Risk Agent capabilities.

**Biggest Challenges**:
1. Converting Rich panel formatting to Telegram markdown
2. Handling 4096 character limit for verbose outputs
3. File attachment workflow for template skills

**Biggest Opportunities**:
1. Mobile access to Risk Agent's powerful skills
2. Async collaboration (multiple users working with same agent)
3. File sharing for populated templates
4. Inline keyboards for interactive workflows (clarification questions)
