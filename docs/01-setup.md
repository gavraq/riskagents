# Risk Agent MVP - Setup Documentation

**Date**: 2025-11-05
**Status**: In Progress

## Overview

This document tracks the setup and initialization of the Risk Agent MVP, focusing on the Change-Agent implementation using the Anthropic Claude Agent SDK.

## Architecture

```
Terminal CLI
    ↓
risk-intelligence-engine.md (Orchestrator)
    ↓ (via Task tool)
change-agent.md (Domain Specialist)
    ↓ (auto-invoked)
Claude Skills (meeting-minutes, project-planner, status-reporter, stakeholder-analysis)
```

## Setup Steps

### 1. Project Initialization ✅

**Date**: 2025-11-05
**Status**: Complete

```bash
cd /Users/gavinslater/projects/riskagent
uv init --no-readme
```

**Result**:
- Created `pyproject.toml`
- Created `.python-version` (Python 3.13)
- Created `main.py` (to be replaced)
- Initialized Git repository

### 2. Directory Structure ✅

**Date**: 2025-11-05
**Status**: Complete

Created the following directory structure:

```
riskagent/
├── .claude/
│   ├── agents/              # Agent definitions (markdown)
│   ├── skills/              # Claude Skills
│   │   ├── meeting-minutes/
│   │   ├── project-planner/
│   │   ├── status-reporter/
│   │   └── stakeholder-analysis/
│   └── settings.local.json  # Already exists
├── src/                     # Python source code
├── tests/                   # Test files
├── docs/                    # Documentation
├── pyproject.toml           # uv dependencies
└── .gitignore
```

**Commands used**:
```bash
mkdir -p .claude/agents
mkdir -p .claude/skills/meeting-minutes
mkdir -p .claude/skills/project-planner
mkdir -p .claude/skills/status-reporter
mkdir -p .claude/skills/stakeholder-analysis
mkdir -p src tests docs
```

### 3. Dependencies (In Progress) 🔄

**Target dependencies**:
- `anthropic` - Claude SDK with agent support
- `rich` - Terminal formatting

### 4. Files to Create

**Agents** (`.claude/agents/`):
- [ ] `risk-intelligence-engine.md` - Master orchestrator
- [ ] `change-agent.md` - Change management domain specialist

**Skills** (`.claude/skills/`):
- [ ] `meeting-minutes/SKILL.md`
- [ ] `project-planner/SKILL.md`
- [ ] `status-reporter/SKILL.md`
- [ ] `stakeholder-analysis/SKILL.md`

**Python Code** (`src/`):
- [ ] `risk_agent_cli.py` - Main CLI with conversation loop
- [ ] `cli_utils.py` - Helper functions (optional)

**Configuration**:
- [ ] `.claude/settings.json` - Output styles configuration
- [ ] `README.md` - Setup and usage instructions
- [ ] `.gitignore` - Updated for Python/uv

## Design Decisions

### Authentication
- **Decision**: Use authenticated Anthropic session (no API key)
- **Rationale**: User has Anthropic Max account, can login via terminal
- **Impact**: No need for `.env` file or `python-dotenv` dependency

### Conversation Pattern
- **Decision**: Follow kenneth-liao `4_convo_loop.py` pattern
- **Pattern**: Async with `ClaudeSDKClient`, `while True` loop, `query()` → `receive_response()`
- **Reference**: https://github.com/kenneth-liao/claude-agent-sdk-intro/blob/main/4_convo_loop.py

### Skills vs Sub-Agents
- **Decision**: Use Claude Skills framework (not sub-agents)
- **Rationale**: Official pattern, cleaner, auto-discovery, model-invoked
- **Reference**: https://docs.claude.com/en/docs/claude-code/skills

### Output Formatting
- **Decision**: Use Rich library for terminal formatting
- **Features**: Markdown rendering, panels, status indicators, colored output
- **Reference**: kenneth-liao repo uses Rich

## Next Steps

1. ✅ Complete pyproject.toml with dependencies
2. Create orchestrator agent (`risk-intelligence-engine.md`)
3. Create domain agent (`change-agent.md`)
4. Create 4 skills (SKILL.md files)
5. Implement CLI (`risk_agent_cli.py`)
6. Test end-to-end flow

## Notes

- Existing `.claude/settings.local.json` found - may need to review/update
- Git already initialized
- Python 3.13 set as version
- No frameworks directory for MVP (agents use built-in knowledge)

## References

- [Anthropic Agent SDK](https://github.com/anthropics/anthropic-sdk-python)
- [Claude Skills Documentation](https://docs.claude.com/en/docs/claude-code/skills)
- [kenneth-liao Tutorial](https://github.com/kenneth-liao/claude-agent-sdk-intro)
- [Risk Agent Blueprint](/Users/gavinslater/Library/Mobile Documents/iCloud~md~obsidian/Documents/GavinsiCloudVault/Job & Career/Risk Agents/Risk Agents - Anthropic SDK Implementation Blueprint.md)
