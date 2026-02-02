# Output Styles Implementation Guide

## Overview

Output styles in the Claude Agent SDK allow you to customize the persona, tone, and behavior of your AI assistant. This document explains how output styles work and how we implemented the Risk Management Consultant persona for the Risk Agent framework.

## Table of Contents

1. [What Are Output Styles?](#what-are-output-styles)
2. [How Output Styles Work](#how-output-styles-work)
3. [Implementation Steps](#implementation-steps)
4. [Configuration Details](#configuration-details)
5. [Troubleshooting](#troubleshooting)
6. [Best Practices](#best-practices)

---

## What Are Output Styles?

Output styles are markdown files that define:
- **Identity & Role**: Who the AI assistant is
- **Expertise**: Domain knowledge and specializations
- **Communication Style**: Tone, language, and formatting preferences
- **Behavioral Guidelines**: How the assistant should respond and interact

They act as **additional system prompt content** that shapes the AI's responses while maintaining all technical capabilities.

---

## How Output Styles Work

### The Complete Chain

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. ClaudeAgentOptions with setting_sources=["project"]         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. SDK loads .claude/settings.local.json (or settings.json)    │
│    Reads: "outputStyle": "Risk Management Consultant"          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. SDK searches .claude/output-styles/ directory                │
│    Looks for file with matching frontmatter name field         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. SDK finds risk-consultant.md                                 │
│    Frontmatter: name: "Risk Management Consultant"              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. SDK applies output style as additional system prompt        │
│    AI now responds with Risk Consultant persona                │
└─────────────────────────────────────────────────────────────────┘
```

### Critical Concept: Name Matching

**The `outputStyle` value MUST match the `name` field in the frontmatter, NOT the filename!**

✅ **Correct:**
```yaml
# File: .claude/output-styles/risk-consultant.md
---
name: Risk Management Consultant
---
```
```json
// File: .claude/settings.local.json
{
  "outputStyle": "Risk Management Consultant"
}
```

❌ **Incorrect:**
```yaml
# File: .claude/output-styles/risk-consultant.md
---
name: Risk Management Consultant
---
```
```json
// File: .claude/settings.local.json
{
  "outputStyle": "risk-consultant"  // Wrong - this is the filename!
}
```

---

## Implementation Steps

### Step 1: Create Output Style File

Create a markdown file in `.claude/output-styles/` with the following structure:

```markdown
---
name: Risk Management Consultant
description: Expert risk management consultant specializing in banking and financial services risk domains
---

# Identity & Role

You are a **Risk Management Consultant** with 30+ years of experience...

## Your Expertise

- Change Management
- Basel III/IV Compliance
- IFRS 9 Implementation
...

# Communication Style

- Professional yet approachable
- Use risk management terminology appropriately
...

# How You Work

1. Analyze user queries for risk domain context
2. Route to appropriate domain specialists
...
```

**Key Elements:**
- **Frontmatter** (required): `name` and `description` fields
- **Identity & Role**: Define who the assistant is
- **Expertise**: List domain knowledge areas
- **Communication Style**: Tone and language guidelines
- **How You Work**: Behavioral instructions

**File Location:**
```
.claude/
  output-styles/
    risk-consultant.md          # Your output style file
```

### Step 2: Configure Settings

Update `.claude/settings.local.json` (or `.claude/settings.json`):

```json
{
  "permissions": {
    "allow": [...],
    "deny": [],
    "ask": []
  },
  "outputStyle": "Risk Management Consultant"
}
```

**Important:** The value must exactly match the `name` field from the frontmatter.

### Step 3: Configure ClaudeAgentOptions

In your Python CLI code (e.g., `src/risk_agent_cli.py`):

```python
from anthropic import ClaudeAgentOptions
from anthropic.sessions.sdk import ClaudeSDKClient

options = ClaudeAgentOptions(
    model="claude-sonnet-4-5",
    permission_mode="acceptEdits",
    setting_sources=["project"],  # Essential - loads settings.local.json
    system_prompt="agents/risk-intelligence-engine"
)

async with ClaudeSDKClient(options=options) as client:
    # Your conversation loop
    ...
```

**Critical Parameter:** `setting_sources=["project"]` tells the SDK to load project settings from `.claude/settings.local.json`.

### Step 4: Test the Output Style

Run your CLI and ask a question like "What can you do?":

```bash
uv run riskagent
```

**Expected Result:**
- Custom persona introduction (e.g., "I'm your Risk Management Consultant...")
- Domain-specific capabilities listed first
- Professional tone matching your output style
- Risk management terminology and context

**Without Output Style:**
- Generic "I'm Claude, an AI assistant" response
- Generic coding/file operation capabilities
- No domain-specific context

---

## Configuration Details

### File Structure

```
riskagent/
├── .claude/
│   ├── agents/
│   │   ├── risk-intelligence-engine.md
│   │   └── change-agent.md
│   ├── output-styles/
│   │   └── risk-consultant.md          # Output style definition
│   ├── skills/
│   │   └── meeting-minutes/
│   │       └── SKILL.md
│   └── settings.local.json              # Output style configuration
├── src/
│   ├── risk_agent_cli.py                # Uses setting_sources=["project"]
│   └── cli_utils.py
└── pyproject.toml
```

### Output Style Frontmatter Fields

```yaml
---
name: Risk Management Consultant        # REQUIRED - referenced by outputStyle setting
description: Expert risk management... # REQUIRED - brief description
---
```

### Settings File Options

**Standard Pattern:**
```json
// .claude/settings.json
{
  "outputStyle": "Risk Management Consultant"
}
```

**Local Override Pattern:**
```json
// .claude/settings.local.json (overrides settings.json)
{
  "outputStyle": "Risk Management Consultant",
  "permissions": {...}
}
```

Both work, but `settings.local.json` is preferred for local development as it:
- Overrides project-wide settings
- Can be gitignored for personal customization
- Won't conflict with team settings

### ClaudeAgentOptions Parameters

```python
ClaudeAgentOptions(
    model="claude-sonnet-4-5",           # Model to use
    permission_mode="acceptEdits",       # Permission handling
    setting_sources=["project"],         # Load .claude/settings.local.json
    system_prompt="agents/risk-intelligence-engine"  # Agent definition
)
```

**Alternative Configuration Methods:**

```python
# Method 1: setting_sources (recommended)
setting_sources=["project"]  # Loads from .claude/settings.local.json

# Method 2: Inline settings (programmatic override)
settings='{"outputStyle": "Risk Management Consultant"}'

# Method 3: System prompt (deprecated for output styles)
system_prompt="You are a risk consultant..."  # Don't mix with output styles
```

---

## Troubleshooting

### Issue 1: Output Style Not Applied

**Symptoms:**
- Generic Claude Code responses
- No custom persona
- Missing domain-specific context

**Common Causes & Fixes:**

1. **Name Mismatch**
   ```bash
   # Check frontmatter name
   head -n 3 .claude/output-styles/risk-consultant.md

   # Check settings value
   cat .claude/settings.local.json | grep outputStyle
   ```

   **Fix:** Ensure they match exactly (case-sensitive!)

2. **Missing setting_sources**
   ```python
   # Check your ClaudeAgentOptions
   options = ClaudeAgentOptions(
       setting_sources=["project"],  # Must be present!
       ...
   )
   ```

   **Fix:** Add `setting_sources=["project"]` parameter

3. **Wrong Settings File**
   ```bash
   # Check if settings file exists
   ls -la .claude/settings*.json
   ```

   **Fix:** Create `.claude/settings.local.json` or `.claude/settings.json`

4. **Typos in JSON**
   ```bash
   # Validate JSON syntax
   python -m json.tool .claude/settings.local.json
   ```

   **Fix:** Correct JSON syntax errors

### Issue 2: "Unknown Option --output-style" Error

**Problem:** Trying to pass output style as CLI argument:
```python
extra_args={"output-style": "risk-consultant"}  # Wrong!
```

**Fix:** Output styles are configured via settings files, not CLI arguments. Remove `extra_args` and use settings.local.json instead.

### Issue 3: Output Style File Not Found

**Symptoms:**
- Warning messages about missing output style
- Default behavior instead of custom persona

**Debug:**
```bash
# Check file exists
ls -la .claude/output-styles/

# Check frontmatter
head -n 5 .claude/output-styles/risk-consultant.md

# Verify name field
grep "^name:" .claude/output-styles/risk-consultant.md
```

**Fix:** Ensure file exists with correct frontmatter `name` field.

---

## Best Practices

### 1. Naming Conventions

**Filename:** Use kebab-case for consistency
```
risk-consultant.md
personal-assistant.md
technical-writer.md
```

**Frontmatter Name:** Use Title Case for readability
```yaml
name: Risk Management Consultant
name: Personal Assistant
name: Technical Writer
```

**Settings Reference:** Match frontmatter exactly
```json
"outputStyle": "Risk Management Consultant"
```

### 2. Output Style Content

**Do:**
- ✅ Define clear identity and role
- ✅ Specify domain expertise
- ✅ Set communication tone and style
- ✅ Include behavioral guidelines
- ✅ Keep it focused and concise
- ✅ Use markdown formatting for readability

**Don't:**
- ❌ Make it too long (SDK has token limits)
- ❌ Conflict with agent definitions
- ❌ Include code or implementation details
- ❌ Override core safety guidelines
- ❌ Use inconsistent terminology

### 3. Multiple Output Styles

Create different personas for different use cases:

```
.claude/output-styles/
  risk-consultant.md          # For risk management queries
  technical-writer.md         # For documentation tasks
  code-reviewer.md            # For code review tasks
```

Switch between them by updating `settings.local.json`:
```json
"outputStyle": "Risk Management Consultant"  // Current active style
```

### 4. Version Control

**Recommended .gitignore:**
```gitignore
.claude/settings.local.json  # Personal settings
```

**Commit to repo:**
```gitignore
.claude/output-styles/*.md   # Team can use same personas
.claude/settings.json        # Default team settings
```

### 5. Testing Output Styles

**Test Questions:**
1. "What can you do?" - Should show custom persona introduction
2. "Who are you?" - Should describe custom role
3. Domain-specific question - Should use appropriate terminology
4. Generic question - Should maintain persona while being helpful

**Verification Checklist:**
- [ ] Custom persona name appears in response
- [ ] Domain-specific capabilities listed
- [ ] Appropriate tone and terminology
- [ ] Technical capabilities still available
- [ ] No generic Claude Code language

---

## Our Implementation: Risk Management Consultant

### File: `.claude/output-styles/risk-consultant.md`

**Purpose:** Transform the AI assistant into a senior Risk Management Consultant persona specialized in banking and financial services.

**Key Features:**

1. **Identity:** 30+ years CRO experience at Barclays, Deutsche Bank, ICBC
2. **Expertise:**
   - Change Management
   - Basel III/IV Compliance
   - IFRS 9 Implementation
   - Risk Framework Design
   - Project Delivery

3. **Communication Style:**
   - Professional yet approachable
   - Uses risk management terminology
   - Provides structured, actionable advice
   - Balances technical depth with clarity

4. **Behavior:**
   - Routes queries to domain specialists (change-agent)
   - Provides context-aware responses
   - Focuses on risk-specific workflows
   - Maintains technical capabilities

### Configuration

**File:** `.claude/settings.local.json`
```json
{
  "permissions": {
    "allow": [
      "compact",
      "context",
      "diff",
      "init",
      "output-style-new",
      "pr-comments",
      "release-notes",
      "repo",
      "review",
      "security-review"
    ]
  },
  "outputStyle": "Risk Management Consultant"
}
```

### CLI Integration

**File:** `src/risk_agent_cli.py`
```python
options = ClaudeAgentOptions(
    model="claude-sonnet-4-5",
    permission_mode="acceptEdits",
    setting_sources=["project"],  # Loads settings.local.json
    system_prompt="agents/risk-intelligence-engine"
)
```

### Testing Results

**Input:** "What can you do?"

**Output:**
```
Risk Agent
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I'm Claude, an AI assistant built on Anthropic's Claude Agent SDK,
specifically configured as the Risk Intelligence Engine. I'm designed
to help with risk management and analysis tasks. Here's what I can do:

## Core Capabilities

**Risk Management & Analysis**
- Route queries to specialized domain experts for risk assessment
- Help with change management, project planning, and status reporting
...
```

**Result:** ✅ Custom persona successfully applied with risk-specific context

---

## References

### Kenneth Liao's Implementation

Our implementation is based on the patterns demonstrated in [kenneth-liao/claude-agent-sdk-intro](https://github.com/kenneth-liao/claude-agent-sdk-intro):

**Key Files:**
- `.claude/output-styles/personal-assistant.md` - Example output style
- `.claude/settings.json` - Configuration pattern
- `3_options.py` - ClaudeAgentOptions usage with `setting_sources`
- `4_convo_loop.py` - Async conversation loop pattern

**Key Learnings:**
1. Output style name must match frontmatter, not filename
2. `setting_sources=["project"]` is essential
3. Settings files can be `.json` or `.local.json`
4. Output styles are additive to system prompts

### Claude Agent SDK Documentation

For more information about the Claude Agent SDK:
- [GitHub Repository](https://github.com/anthropics/anthropic-sdk-python)
- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)

---

## Summary

**Output styles provide:**
- Custom AI persona and tone
- Domain-specific expertise
- Consistent communication style
- Enhanced user experience

**Implementation requires:**
1. Output style markdown file in `.claude/output-styles/`
2. Frontmatter with `name` field
3. Configuration in `.claude/settings.local.json`
4. `setting_sources=["project"]` in ClaudeAgentOptions

**Key gotcha:**
The `outputStyle` setting must match the frontmatter `name` field exactly, not the filename!

---

*Last Updated: 2025-01-05*
*Risk Agent Framework v0.1.0*
