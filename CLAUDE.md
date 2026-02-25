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
Terminal CLI / riskagents-ui (localhost:3002) / Telegram Bot
    ↓
Unified Gateway (localhost:8090) → Claude Agent SDK → CLI subprocess
    ↓
Risk Intelligence Engine (Orchestrator)
    ↓ Task tool
Change-Agent / Market-Risk-Agent (Domain Specialists)
    ↓ Auto-invoked
Claude Skills (15 specialized skills)
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
│   ├── skills/                    # Modular capabilities (15 skills)
│   │   ├── climate-scorecard-filler/    # Climate & ESG credit scorecards
│   │   ├── icc-business-case-filler/    # ICC business case templates
│   │   ├── itc-template-filler/         # ITC project templates
│   │   ├── markdown-to-word/            # Markdown to Word conversion
│   │   ├── meeting-minutes/             # Meeting minutes structuring
│   │   ├── pillar-stress-generator/     # Stress scenario parameterization
│   │   ├── policy-updater/              # Policy document updates
│   │   ├── process-documenter/          # Process documentation & flows
│   │   ├── project-planner/             # Project charter creation
│   │   ├── regulatory-change-assessor/  # Regulatory impact assessment
│   │   ├── regulatory-monitor/          # Proactive regulatory scanning
│   │   ├── stakeholder-analysis/        # Stakeholder mapping & RACI
│   │   ├── status-reporter/             # RAG status reports
│   │   ├── stress-scenario-approver/    # Approve scenarios to library
│   │   └── stress-scenario-suggester/   # Emerging risk research
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

## Current Capabilities (15 Skills)

### Change Management (change-agent)
1. **Project Planner** - Create project charters, timelines, resources, risk assessments, governance structures
2. **Meeting Minutes** - Structure meeting notes with action items, decisions, owners, and due dates
3. **Status Reporter** - Generate RAG status reports with progress tracking and milestone management
4. **Stakeholder Analysis** - Map stakeholders with influence/interest matrices, engagement strategies, RACI
5. **ITC Template Filler** - Populate ITC (Investment Technology Committee) governance templates from project data
6. **ICC Business Case Filler** - Complete ICC business cases with interactive clarification for missing fields
7. **Process Documenter** - Create process documentation with flow diagrams and RACI matrices
8. **Markdown to Word** - Convert markdown documents to professionally formatted Word (.docx) files with cover pages and branding

### Market Risk (market-risk-agent)
9. **Pillar Stress Generator** - Parameterize stress scenarios with full risk factor shocks across 7 asset classes (rates, FX, credit, energy, precious metals, base metals, equities)
10. **Stress Scenario Suggester** - Research emerging risks via 5 parallel research sub-agents (geopolitical, macro, market-structure, climate-esg, tech-sector)
11. **Stress Scenario Approver** - Approve scenarios into the official library by updating JSON shocks, UI inventory, and scenario dropdown

### Credit Risk (change-agent)
12. **Climate Scorecard Filler** - Complete Climate & Environmental Risk Scorecards for credit applications, assessing physical and transition risks

### Regulatory (change-agent)
13. **Regulatory Change Assessor** - Assess impact of new/changed regulations on Risk Taxonomy and control frameworks
14. **Regulatory Monitor** - Proactive scanning for new regulatory developments with automated alerts
15. **Policy Updater** - Update policy documents to reflect regulatory and framework changes

## Roadmap

- Additional risk domain agents (Credit, Operational, Liquidity, Model, Climate, Regulatory, Strategic)
- Expand market-risk-agent capabilities (VaR calculation, limit monitoring, back-testing)
- External system integrations (JIRA, SharePoint)
- Multi-language template support

## License

Proprietary - Bright Slate Limited
