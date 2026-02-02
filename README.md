# Risk Agents - Change Agent MVP

AI-powered Risk Management Agents focusing on Change Management, Project Planning, and Risk Consulting.

## Overview

This MVP implements a Change-Agent using the Anthropic Claude Agent SDK with the following architecture:

```
Terminal CLI
    ↓
Risk Intelligence Engine (Orchestrator)
    ↓ Task tool
Change-Agent / Market-Risk-Agent (Domain Specialists)
    ↓ Auto-invoked
Claude Skills (8 specialized skills)
    ↓ Parallel research (stress-scenario-suggester)
5 Research Sub-Agents
```

## Features

- **Project Planning**: Create comprehensive project charters, timelines, and risk assessments
- **Meeting Minutes**: Structure meeting notes with action items and decisions
- **Status Reports**: Generate progress reports with RAG status and risk tracking
- **Stakeholder Analysis**: Map and analyze stakeholders with engagement strategies
- **ITC Template Population**: Automatically populate ITC governance templates from project documents (first governance gate)
- **ICC Business Case Population**: Complete ICC business cases with interactive clarification mode (second governance gate, Excel with merged cell handling)
- **Process Documentation**: Create comprehensive process and workflow documentation with professional flow diagrams (BPMN, Mermaid, PlantUML, Data Flow)
- **Pillar Stress Generator**: Parameterize market risk stress scenarios with full risk factor shocks across all asset classes
- **Stress Scenario Suggester**: Research current market developments via 5 parallel research agents to suggest emerging stress scenarios

## Setup

### Prerequisites

- Python 3.11+
- `uv` package manager ([installation](https://github.com/astral-sh/uv))
- Anthropic Max account (authenticated session, no API key needed)

### Installation

```bash
# Clone or navigate to project
cd /path/to/riskagent

# Install dependencies
uv sync

# Run the CLI
uv run riskagent
```

## Usage

### CLI Interface

```bash
# Standard mode (clean interface)
$ uv run riskagent

# Verbose mode (full detail, shows all tool calls/results)
$ uv run riskagent --verbose
# or
$ uv run riskagent -v

# Simple interface (plain text, like Claude Code)
$ uv run riskagent --simple
# or
$ uv run riskagent -s

# Combine modes
$ uv run riskagent --simple --verbose

# Start chatting with the Change-Agent
You: Help me plan a Basel IV implementation project

# Commands:
# - 'help' : Show available capabilities
# - 'verbose' or 'v' : Toggle verbose mode at runtime
# - 'interface' or 'i' : Toggle interface mode (rich/simple)
# - 'clear' : Clear screen
# - 'exit' : Quit
```

### Telegram Bot (Remote Access)

Access Risk Agent remotely via Telegram:

```bash
# Set up your bot token (one-time)
export TELEGRAM_BOT_TOKEN="your-bot-token-here"

# Run the Telegram bot
$ uv run riskagent-telegram
```

Features:
- **Remote Access**: Use Risk Agent from anywhere via Telegram
- **Session Persistence**: Conversations resume automatically
- **Working Directory Control**: Set custom CWD per user
- **Full Capabilities**: All CLI features available

See [Telegram Bot Setup Guide](./docs/13-telegram-bot-setup.md) for complete instructions.

### Display Modes

The CLI supports two interface modes:

**Rich Mode** (default): Enhanced terminal interface
- Colored panels with borders
- Syntax highlighting for code/JSON
- Visual separation of messages
- Ideal for terminal usage

**Simple Mode**: Plain text interface
- Clean text output (like standard Claude Code)
- No panels or colors
- Same format as Telegram bot
- Perfect for logging or simple terminals

**Verbose Mode**: Toggle detail level
- **Off** (default): Shows assistant responses and skill results only
- **On**: Shows every tool call (Read, Write, Bash, etc.) and results
- Perfect for debugging and learning

Toggle modes at runtime with `interface` and `verbose` commands, or use launch flags.

## Project Structure

```
riskagent/
├── .claude/
│   ├── agents/
│   │   ├── risk-intelligence-engine.md       # Orchestrator
│   │   ├── change-agent.md                   # Change management specialist
│   │   ├── market-risk-agent.md              # Market risk specialist
│   │   ├── geopolitical-risk-researcher.md   # Research agent
│   │   ├── macroeconomic-risk-researcher.md  # Research agent
│   │   ├── market-structure-risk-researcher.md # Research agent
│   │   ├── climate-esg-risk-researcher.md    # Research agent
│   │   └── technology-sector-risk-researcher.md # Research agent
│   └── skills/
│       ├── meeting-minutes/
│       ├── project-planner/
│       ├── status-reporter/
│       ├── stakeholder-analysis/
│       ├── itc-template-filler/         # ITC governance templates (first gate)
│       ├── icc-business-case-filler/    # ICC business cases (second gate)
│       ├── process-documenter/          # Process flow documentation
│       ├── pillar-stress-generator/     # Market risk stress parameterization
│       └── stress-scenario-suggester/   # Parallel research for emerging risks
├── src/
│   ├── risk_agent_cli.py                # Main CLI
│   ├── cli_utils.py                     # CLI formatting utilities
│   ├── telegram_bot.py                  # Telegram bot interface
│   └── telegram_utils.py                # Telegram message handling
├── docs/                                 # Documentation
├── tests/                                # Tests
└── pyproject.toml                       # Dependencies
```

## Documentation

### User Guides
- **[Skills Guide](./docs/06-skills-guide.md)** - Complete guide to using and developing skills (includes all 8 skills)
- **[ITC Template Filler Reference](./docs/06b-itc-template-filler-reference.md)** - Detailed reference for itc-template-filler skill
- **[ICC Business Case Filler](./.claude/skills/icc-business-case-filler/README.md)** - Detailed reference for icc-business-case-filler skill with interactive clarification mode
- **[Process Documenter](./docs/06d-process-documenter.md)** - Detailed reference for process-documenter skill with BPMN/Mermaid/PlantUML/DFD support
- **[Stress Scenario Suggester](./docs/06e-stress-scenario-suggester.md)** - Research emerging risks via 5 parallel research agents for market risk stress testing
- **[Telegram Bot Setup](./docs/13-telegram-bot-setup.md)** - Complete guide to setting up and using the Telegram bot

### Implementation Documentation
- [01-architecture.md](./docs/01-architecture.md) - Overall system architecture
- [02-agent-system.md](./docs/02-agent-system.md) - Multi-agent orchestration design
- [03-cli-implementation.md](./docs/03-cli-implementation.md) - Terminal interface implementation
- [04-cli-frontend-experience.md](./docs/04-cli-frontend-experience.md) - CLI frontend with verbose mode
- [10-itc-template-filler-enhancements.md](./docs/10-itc-template-filler-enhancements.md) - v1.0 → v1.1 enhancement history
- [11-telegram-integration-analysis.md](./docs/11-telegram-integration-analysis.md) - Telegram integration analysis and architecture
- [12-session-management-comparison.md](./docs/12-session-management-comparison.md) - Session management comparison across implementations
- [14-observability-integration.md](./docs/14-observability-integration.md) - Real-time agent monitoring via observability dashboard

See [docs/archive/](./docs/archive/) for historical documentation from development sessions.

## Development Status

**Current Phase**: MVP Production Ready
**Status**: Core Features Complete

### Completed
- ✅ Project structure and dependencies
- ✅ Multi-agent orchestration (orchestrator → change-agent → market-risk-agent)
- ✅ CLI with rich formatting and output styles
- ✅ 8 production skills (meeting-minutes, project-planner, status-reporter, stakeholder-analysis, itc-template-filler, icc-business-case-filler, process-documenter, pillar-stress-generator, stress-scenario-suggester)
- ✅ Parallel research agent architecture (5 specialized research agents)
- ✅ Skill detection and invocation with visual indicators
- ✅ Executable skill modules with Python libraries (itc-template-filler, icc-business-case-filler)
- ✅ Interactive clarification mode for complex business cases (icc-business-case-filler)
- ✅ Verbose mode and simple interface mode for CLI
- ✅ Telegram bot integration with session persistence
- ✅ Per-user session management and working directory control

### In Progress
- 🔄 Real-world testing and refinement
- 🔄 Telegram bot production deployment

### Planned
- ⏳ Additional skills for other governance processes
- ⏳ More risk domains (Credit Risk, Market Risk, Operational Risk)
- ⏳ Integration with external systems (JIRA, SharePoint, etc.)
- ⏳ Multi-language support for templates

## Architecture

This MVP follows the architecture outlined in the Risk Agents Blueprint, using:
- **Anthropic Claude Agent SDK** for agent orchestration
- **Claude Skills** for modular capabilities
- **Rich** library for terminal formatting
- **Async conversation loop** pattern from kenneth-liao tutorial

## Contributing

This is currently a solo MVP development project. Documentation will be expanded as the project matures.

## License

Proprietary - Bright Slate Limited

## Author

Gavin Slater
