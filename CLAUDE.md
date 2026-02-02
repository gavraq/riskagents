# CLAUDE.md - Risk Agents Project

## Project Overview

Risk Agents is an AI-powered Risk Management platform built on the Anthropic Claude Agent SDK. The MVP focuses on Change Management capabilities with a multi-agent architecture.

## Quick Start

```bash
# Install dependencies
uv sync

# Run CLI
uv run riskagent

# Run with verbose mode
uv run riskagent --verbose
```

> **Note**: Telegram access is now via standalone services. See `~/projects/telegram-agent` (Mac) and `~/projects/telegram-gateway` (Docker/Pi).

## Architecture

```
Terminal CLI / Telegram Bot
    ↓
Risk Intelligence Engine (Orchestrator)
    ↓ Task tool
Change-Agent / Market-Risk-Agent (Domain Specialists)
    ↓ Auto-invoked
Claude Skills (8 specialized skills)
    ↓ Parallel research (stress-scenario-suggester)
5 Research Sub-Agents (geopolitical, macro, market-structure, climate-esg, tech-sector)
```

## Project Structure

```
riskagent/
├── .claude/
│   ├── agents/                    # Agent definitions
│   │   ├── risk-intelligence-engine.md          # Orchestrator
│   │   ├── change-agent.md                      # Change management specialist
│   │   ├── market-risk-agent.md                 # Market risk specialist
│   │   ├── geopolitical-risk-researcher.md      # Research sub-agent
│   │   ├── macroeconomic-risk-researcher.md     # Research sub-agent
│   │   ├── market-structure-risk-researcher.md  # Research sub-agent
│   │   ├── climate-esg-risk-researcher.md       # Research sub-agent
│   │   └── technology-sector-risk-researcher.md # Research sub-agent
│   ├── skills/                    # Modular capabilities
│   │   ├── meeting-minutes/
│   │   ├── project-planner/
│   │   ├── status-reporter/
│   │   ├── stakeholder-analysis/
│   │   ├── itc-template-filler/
│   │   ├── icc-business-case-filler/
│   │   ├── process-documenter/
│   │   ├── pillar-stress-generator/
│   │   └── stress-scenario-suggester/
│   ├── hooks/
│   └── output-styles/
├── src/
│   ├── risk_agent_cli.py          # Main CLI entry point
│   ├── cli_utils.py               # CLI formatting utilities
│   └── _deprecated/               # Old telegram code (moved to standalone services)
├── docs/                          # Documentation
├── data/                          # Data files
├── output/                        # Generated outputs
└── test_scenarios/                # Test scenarios
```

## Key Technologies

- **Python 3.11+** with `uv` package manager
- **claude-agent-sdk** - Anthropic's agent orchestration SDK
- **rich** - Terminal formatting and panels
- **openpyxl/python-docx** - Excel and Word file manipulation

## Development Guidelines

### Virtual Environment
- Always use the project's existing `.venv` when running Python scripts
- Use `uv run python script.py` or `source .venv/bin/activate` first
- Never create a new virtual environment - dependencies are already installed via `uv sync`

### Code Style
- Use async/await patterns for agent interactions
- Follow rich library conventions for terminal output
- Keep skills modular and self-contained

### Skills Development
Each skill in `.claude/skills/` should:
- Have a clear, focused purpose
- Include a README.md with usage instructions
- Be auto-invoked based on user intent
- Output structured, actionable results

### Testing
```bash
# Run tests
uv run pytest

# Interactive development
uv run ipython
```

## Common Tasks

### Adding a New Skill
1. Create directory in `.claude/skills/your-skill-name/`
2. Add skill prompt/README.md
3. Implement any supporting Python modules if needed
4. Document in `docs/06-skills-guide.md`

### Modifying Agent Behavior
- Edit `.claude/agents/change-agent.md` for domain-specific behavior
- Edit `.claude/agents/risk-intelligence-engine.md` for orchestration logic

### CLI Modes
- **Standard**: Clean interface with skill results
- **Verbose** (`-v`): Shows all tool calls and results
- **Simple** (`-s`): Plain text output (like Claude Code)

## Important Files

- [src/risk_agent_cli.py](src/risk_agent_cli.py) - Main CLI implementation
- [.claude/agents/change-agent.md](.claude/agents/change-agent.md) - Change agent definition
- [.claude/agents/market-risk-agent.md](.claude/agents/market-risk-agent.md) - Market risk agent
- [.claude/agents/risk-intelligence-engine.md](.claude/agents/risk-intelligence-engine.md) - Orchestrator
- [docs/06-skills-guide.md](docs/06-skills-guide.md) - Complete skills documentation
- [docs/06e-stress-scenario-suggester.md](docs/06e-stress-scenario-suggester.md) - Stress scenario suggester reference

## Environment Variables

- Uses Anthropic Max account authentication (no API key needed)

## Telegram Access (Standalone Services)

Telegram integration has been moved to standalone services for multi-project support:

- **Mac**: `~/projects/telegram-agent` - FastAPI service wrapping Claude SDK
- **Pi/Docker**: `~/projects/telegram-gateway` - Telegram bot container

See those project READMEs for setup instructions.

## Current Capabilities

### Change Management (change-agent)
1. **Project Planning** - Create project charters, timelines, risk assessments
2. **Meeting Minutes** - Structure notes with action items and decisions
3. **Status Reports** - Generate RAG status reports
4. **Stakeholder Analysis** - Map and analyze stakeholders
5. **ITC Template Filler** - Populate ITC governance templates
6. **ICC Business Case Filler** - Complete ICC business cases with interactive mode
7. **Process Documenter** - Create process documentation with flow diagrams

### Market Risk (market-risk-agent)
8. **Pillar Stress Generator** - Parameterize stress scenarios with full risk factor shocks
9. **Stress Scenario Suggester** - Research emerging risks via 5 parallel research agents

## Roadmap

- Additional risk domain agents (Credit, Operational, Liquidity, Model, Climate, Regulatory, Strategic)
- Expand market-risk-agent capabilities (VaR calculation, limit monitoring, back-testing)
- External system integrations (JIRA, SharePoint)
- Multi-language template support

## License

Proprietary - Bright Slate Limited
