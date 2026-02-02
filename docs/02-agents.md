# Risk Agent MVP - Agent Architecture

**Date**: 2025-01-24
**Status**: Multi-Domain Production (Change Management + Market Risk)

## Overview

This document describes the agent architecture for the Risk Agent MVP, including the orchestrator and domain specialist patterns.

## Agent Hierarchy

```
┌───────────────────────────────────────────────────────────────┐
│   risk-intelligence-engine.md (Master Orchestrator)          │
│   - Intent classification                                     │
│   - Multi-domain routing                                      │
│   - Coordination                                              │
└───────────────────────────────────────────────────────────────┘
                  ↓ Task tool
    ┌─────────────┴─────────────┐
    ↓                           ↓
┌─────────────────────┐   ┌─────────────────────┐
│  change-agent.md    │   │ market-risk-agent.md│
│  (Domain Specialist)│   │ (Domain Specialist) │
│  - Change mgmt      │   │ - Market risk       │
│  - Governance       │   │ - Stress testing    │
│  - Project delivery │   │ - VaR, limits       │
└─────────────────────┘   └─────────────────────┘
         ↓                         ↓
    Auto-invoked              Auto-invoked
┌─────────────────────┐   ┌─────────────────────┐
│  Change Skills (7)  │   │  Market Risk (2)    │
│  - meeting-minutes  │   │  - pillar-stress-   │
│  - project-planner  │   │    generator        │
│  - status-reporter  │   │  - stress-scenario- │
│  - stakeholder-     │   │    suggester ────┐  │
│    analysis         │   │                  │  │
│  - itc-template-    │   └──────────────────┼──┘
│    filler           │                      │
│  - icc-business-    │         Launches 5 parallel
│    case-filler      │         research agents
│  - process-         │                      ↓
│    documenter       │   ┌──────────────────────────────┐
└─────────────────────┘   │  Research Sub-Agents (5)     │
                          │  - geopolitical-risk-        │
                          │    researcher                │
                          │  - macroeconomic-risk-       │
                          │    researcher                │
                          │  - market-structure-risk-    │
                          │    researcher                │
                          │  - climate-esg-risk-         │
                          │    researcher                │
                          │  - technology-sector-risk-   │
                          │    researcher                │
                          └──────────────────────────────┘
```

## Agent Definitions

### 1. risk-intelligence-engine.md

**Location**: `.claude/agents/risk-intelligence-engine.md`
**Type**: Master Orchestrator
**Purpose**: Route user queries to appropriate domain specialist agents

**Key Responsibilities**:
- Classify user intent based on query analysis
- Route to appropriate domain agent via Task tool
- Handle "coming soon" responses for future domains
- Coordinate multi-domain requests (future)

**Tools**: Task, Read, Write
**Model**: claude-sonnet-4-5

**Current Routing**:
- Change management queries → `change-agent`
- Market risk queries → `market-risk-agent`
- Other domains → "Coming soon" message

**Intent Classification Logic**:
```
Keywords → Domain Mapping:
- project, plan, milestones → Change Management
- meeting, minutes, actions → Change Management
- status, report, progress → Change Management
- stakeholders, engagement → Change Management
- ITC template, ICC business case → Change Management
- process documentation, BPMN → Change Management
- VaR, stress test, limit breach → Market Risk
- back-testing, stop loss, MLRC → Market Risk
- scenario suggestion, emerging risk → Market Risk
- credit, portfolio, IFRS 9 → Credit Risk (future)
- operational, RCSA, loss events → Operational Risk (future)
- etc.
```

### 2. change-agent.md

**Location**: `.claude/agents/change-agent.md`
**Type**: Domain Specialist
**Purpose**: Expert change management consultant for risk/regulatory projects

**Key Responsibilities**:
- Understand user needs in change management context
- Apply banking and risk management domain knowledge
- Invoke appropriate skills (auto-discovered by Claude)
- Add context and expertise around skill outputs
- Provide realistic timelines and assessments

**Tools**: Read, Write
**Model**: claude-sonnet-4-5

**Domain Expertise**:
- **Regulatory**: Basel III/IV, IFRS 9/17, CRR, PRA, MiFID, EMIR
- **Risk Management**: Three lines of defense, risk appetite, ICAAP/ILAAP, stress testing
- **Governance**: Board/committee structures, policies, approvals, audit

**Skills Available** (auto-invoked):
1. `meeting-minutes` - Structure notes, extract actions
2. `project-planner` - Create comprehensive project plans
3. `status-reporter` - Generate progress reports
4. `stakeholder-analysis` - Map and analyze stakeholders
5. `itc-template-filler` - Populate ITC governance templates (first gate)
6. `icc-business-case-filler` - Complete ICC business cases (second gate)
7. `process-documenter` - Create process documentation with flow diagrams

**Approach**:
1. Understand request and context
2. Apply domain knowledge
3. Let skills handle specialized work (auto-invoked)
4. Add banking/risk context to outputs
5. Provide actionable recommendations

### 3. market-risk-agent.md

**Location**: `.claude/agents/market-risk-agent.md`
**Type**: Domain Specialist
**Purpose**: Expert in market risk management including VaR, stress testing, limit monitoring, and regulatory capital

**Key Responsibilities**:
- VaR measurement and interpretation
- Stress testing design and analysis
- Limit framework and breach management
- Back-testing analysis and exceptions
- Market risk capital calculation
- Regulatory reporting requirements
- Risk governance and committee processes

**Tools**: Read, Write, Grep, Glob
**Model**: claude-sonnet-4-5

**Domain Expertise**:
- **Risk Measurement**: VaR, SVaR, IRC, ECAP, sensitivities (DV01, CS01, Greeks)
- **Stress Testing**: Top-down pillar stresses, Point of Weakness (PoW), climate scenarios
- **Key Controls**: Stop losses (Level 1/2/3), back-testing, limit framework, breach escalation
- **Regulatory & Capital**: IMA, FRTB, RWA calculation, PRA requirements
- **Trading Book Coverage**: FX, Rates, Credit, Commodities, Equity

**Skills Available** (auto-invoked):
1. `pillar-stress-generator` - Parameterize stress scenarios with full risk factor shocks
2. `stress-scenario-suggester` - Research emerging risks via 5 parallel research agents

**Approach**:
1. Understand the market risk request (measurement, limits, stress, capital, governance)
2. Apply Market Risk Policy framework and PRA requirements
3. Reference specific controls and escalation paths
4. Let skills handle specialized work (stress scenarios)
5. Provide specific, actionable guidance with governance touchpoints

### 4-8. Research Sub-Agents (5 agents)

**Locations**:
- `.claude/agents/geopolitical-risk-researcher.md`
- `.claude/agents/macroeconomic-risk-researcher.md`
- `.claude/agents/market-structure-risk-researcher.md`
- `.claude/agents/climate-esg-risk-researcher.md`
- `.claude/agents/technology-sector-risk-researcher.md`

**Type**: Research Agents (launched in parallel)
**Purpose**: Specialized research for stress scenario suggestion
**Invoked By**: `stress-scenario-suggester` skill

**Key Responsibilities**:
- Use WebSearch to find current developments (last 3-6 months)
- Analyze domain-specific risks and vulnerabilities
- Suggest 2-3 plausible, material, actionable stress scenarios
- Provide trigger mechanisms, transmission channels, affected assets
- Return findings with sources and confidence levels

**Tools**: WebSearch, Read, Write
**Model**: Inherits from parent agent

**Execution Pattern**:
- All 5 agents launched simultaneously (parallel execution)
- Each operates independently on different risk domain
- Results synthesized by stress-scenario-suggester skill
- Total execution time: ~2-5 minutes for all agents

## Communication Flow

### Example: Project Planning Request

```
User: "Help me plan a Basel IV implementation project"
    ↓
risk-intelligence-engine.md
    ↓ [Classifies as Change Management]
    ↓ Task(subagent_type="change-agent", ...)
    ↓
change-agent.md
    ↓ [Recognizes: Regulatory project, major scale]
    ↓ [project-planner skill auto-invoked]
    ↓ [Adds Basel IV context, regulatory deadlines]
    ↓ [Provides comprehensive project plan]
    ↓
Return to orchestrator → Return to user
```

### Example: Meeting Minutes Request

```
User: "Structure these meeting notes: [notes]"
    ↓
risk-intelligence-engine.md
    ↓ [Classifies as Change Management]
    ↓ Task(subagent_type="change-agent", ...)
    ↓
change-agent.md
    ↓ [Recognizes: Meeting documentation needed]
    ↓ [meeting-minutes skill auto-invoked]
    ↓ [Adds risk management context if applicable]
    ↓ [Provides structured minutes with actions]
    ↓
Return to orchestrator → Return to user
```

### Example: Stress Scenario Research Request

```
User: "Suggest stress scenarios based on current market developments"
    ↓
risk-intelligence-engine.md
    ↓ [Classifies as Market Risk - scenario suggestion]
    ↓ Task(subagent_type="market-risk-agent", ...)
    ↓
market-risk-agent.md
    ↓ [Recognizes: Emerging risk research needed]
    ↓ [stress-scenario-suggester skill auto-invoked]
    ↓
stress-scenario-suggester skill
    ↓ [Launches 5 research agents IN PARALLEL via Task tool]
    ↓
    ├─ geopolitical-risk-researcher → WebSearch → Returns findings
    ├─ macroeconomic-risk-researcher → WebSearch → Returns findings
    ├─ market-structure-risk-researcher → WebSearch → Returns findings
    ├─ climate-esg-risk-researcher → WebSearch → Returns findings
    └─ technology-sector-risk-researcher → WebSearch → Returns findings
    ↓ [All agents complete]
    ↓
stress-scenario-suggester skill
    ↓ [Synthesizes 10-15 scenario suggestions]
    ↓ [Prioritizes by urgency/severity]
    ↓ [Returns comprehensive report]
    ↓
market-risk-agent.md
    ↓ [Adds market risk context and governance notes]
    ↓ [Suggests next steps: use pillar-stress-generator for Priority 1]
    ↓
Return to orchestrator → Return to user
```

## Agent Design Principles

### 1. Separation of Concerns
- **Orchestrator**: Routing and coordination only
- **Domain Agent**: Context and expertise
- **Skills**: Specialized structured output
- **Research Sub-Agents**: Parallel research for specific skills

### 2. Context Management
- Orchestrator has minimal context (classification only)
- Domain agent loads relevant domain knowledge
- Skills have focused, clean context for specific tasks
- Research agents receive domain-specific research prompts

### 3. Extensibility
- Easy to add new domain agents (just update orchestrator routing)
- Each domain agent operates independently
- Skills can be shared across domain agents
- Research sub-agents can be reused by multiple skills

### 4. Parallel Execution
- Research agents launched simultaneously (not sequentially)
- Reduces total execution time from ~10-15 min to ~2-5 min
- Each agent operates on different WebSearch queries
- Results synthesized after all agents complete

### 5. Human-in-the-Loop
- Agents flag decisions requiring approval
- Confidence scoring on recommendations
- Clear distinction between analysis and decision
- Research findings require expert validation before action

## Current Status (January 2025)

### ✅ Production Domains
1. **Change Management** (change-agent) + 7 skills
2. **Market Risk** (market-risk-agent) + 2 skills + 5 research agents

### 🔄 In Development
- Expanding market-risk-agent capabilities (VaR calculation, limit monitoring)
- Additional research agent use cases

### ⏳ Planned Domains
- Credit Risk
- Operational Risk
- Liquidity Risk
- Model Risk
- Climate Risk
- Regulatory Risk
- Strategic Risk

## Future Extensions

### Phase 3: Add More Risk Domains

When adding new domain agents (e.g., `credit-risk-agent`):

1. **Update Orchestrator** (`risk-intelligence-engine.md`):
   - Add credit-risk indicators to classification logic
   - Add routing rule: credit queries → `credit-risk-agent`
   - Update "Available Agents" list

2. **Create Domain Agent** (`.claude/agents/credit-risk-agent.md`):
   - Define credit risk expertise (IFRS 9, concentration, ratings)
   - Reference credit risk frameworks (PRA, BCBS)
   - List credit-specific skills
   - Follow same pattern as market-risk-agent

3. **Create Domain Skills** (`.claude/skills/...`):
   - Concentration analysis
   - IFRS 9 ECL calculation
   - Portfolio analysis
   - Credit stress scenarios

4. **Optional**: Create research sub-agents if needed
   - Follow pattern from stress-scenario-suggester
   - Launch in parallel for efficiency

5. **No changes needed** to:
   - CLI code
   - Other domain agents
   - Existing skills

### Phase 4: Multi-Domain Coordination

For queries spanning multiple domains:

```
User: "Plan IFRS 9 implementation including data, systems, and process changes"

Orchestrator:
1. Recognize: Multi-domain (Change + Credit + Operational)
2. Invoke change-agent for project planning
3. Invoke credit-risk-agent for IFRS 9 methodology
4. Invoke operational-risk-agent for process design
5. Synthesize responses
6. Return coordinated plan
```

**Current Implementation**: Single-domain routing only
**Future Enhancement**: Multi-domain coordination with Task tool parallelization

## Files Created

### Agent Files
- ✅ `.claude/agents/risk-intelligence-engine.md` - Master orchestrator
- ✅ `.claude/agents/change-agent.md` - Change management specialist
- ✅ `.claude/agents/market-risk-agent.md` - Market risk specialist
- ✅ `.claude/agents/geopolitical-risk-researcher.md` - Research sub-agent
- ✅ `.claude/agents/macroeconomic-risk-researcher.md` - Research sub-agent
- ✅ `.claude/agents/market-structure-risk-researcher.md` - Research sub-agent
- ✅ `.claude/agents/climate-esg-risk-researcher.md` - Research sub-agent
- ✅ `.claude/agents/technology-sector-risk-researcher.md` - Research sub-agent

### Skills (9 total)
**Change Management (7)**:
- ✅ `meeting-minutes` - Meeting documentation
- ✅ `project-planner` - Project planning
- ✅ `status-reporter` - Status reporting
- ✅ `stakeholder-analysis` - Stakeholder mapping
- ✅ `itc-template-filler` - ITC governance templates
- ✅ `icc-business-case-filler` - ICC business cases
- ✅ `process-documenter` - Process flow documentation

**Market Risk (2)**:
- ✅ `pillar-stress-generator` - Stress scenario parameterization
- ✅ `stress-scenario-suggester` - Parallel research for emerging risks

### Implementation
- ✅ `src/risk_agent_cli.py` - Main CLI
- ✅ `src/cli_utils.py` - Rich formatting
- ✅ Multi-agent orchestration via Task tool
- ✅ Parallel sub-agent execution

### Documentation
- ✅ `README.md` - Project overview
- ✅ `CLAUDE.md` - Developer guide
- ✅ `docs/02-agents.md` - This file (agent architecture)
- ✅ `docs/06-skills-guide.md` - Skills overview
- ✅ `docs/06e-stress-scenario-suggester.md` - Detailed skill reference

## Testing Strategy

### Unit Testing (Future)
- Test orchestrator classification logic
- Test domain agent context application
- Test skill invocation patterns

### Integration Testing
- Test complete flow: User → Orchestrator → Domain Agent → Skill → Response
- Test routing to correct domain agent
- Test skill auto-invocation
- Test "coming soon" handling

### Manual Testing Scenarios

**Change Management**:
1. **Project Planning**: "Plan a Basel IV project"
2. **Meeting Minutes**: "Structure these notes: [notes]"
3. **Status Report**: "Generate status for IFRS 9"
4. **Stakeholder Analysis**: "Who should be involved in risk appetite review?"
5. **ITC Template**: "Fill this ITC template with project info"
6. **ICC Business Case**: "Complete ICC business case template"
7. **Process Documentation**: "Document the stress testing process"

**Market Risk**:
8. **Stress Scenario Suggestion**: "Suggest stress scenarios based on current developments"
9. **Stress Scenario Parameterization**: "Create a US Recession scenario"
10. **VaR Breach**: "We have a Level 2 VaR limit breach, what should we do?"
11. **Back-Testing Exception**: "Explain back-testing exceptions at Global Markets level"

**Future Domains**:
12. **Credit Risk**: "Calculate IFRS 9 ECL for loan portfolio" (should get "coming soon")

## Key Architectural Patterns

### 1. Markdown-Based Agent Definitions
- Agents defined in `.md` files with YAML frontmatter
- Anthropic SDK discovers and invokes agents automatically
- No Python classes or explicit registration needed

### 2. Model-Invoked Skills
- Skills auto-discovered from `.claude/skills/` directory
- Model decides when to invoke based on description
- No explicit skill calling in agent code

### 3. Task Tool for Orchestration
- Orchestrator uses Task tool to invoke domain agents
- Domain agents can use Task tool to invoke research sub-agents
- Enables multi-level agent hierarchies

### 4. Parallel Execution Pattern
- Multiple agents launched simultaneously via single Task tool call
- Example: 5 research agents in stress-scenario-suggester
- Reduces total execution time significantly

### 5. Domain Separation
- Each domain agent operates independently
- Skills can be domain-specific or shared
- Easy to add new domains without touching existing code

## Summary

The Risk Agent architecture demonstrates:
- ✅ **Multi-level orchestration** (orchestrator → domain → research)
- ✅ **Parallel execution** (5 research agents simultaneously)
- ✅ **Model-invoked skills** (auto-detection and invocation)
- ✅ **Domain expertise** (banking, risk, regulatory frameworks)
- ✅ **Extensibility** (easy to add new domains and skills)
- ✅ **Production-ready** (9 skills, 2 domains, 5 research agents)
