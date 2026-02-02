# Skills Guide - Risk Agent Framework

**Purpose**: Complete guide to understanding, using, and developing skills in the Risk Agent framework
**Audience**: Users and developers
**Last Updated**: 2025-11-12

---

## Table of Contents

1. [What Are Skills?](#what-are-skills)
2. [Available Skills](#available-skills)
3. [How Skills Work](#how-skills-work)
4. [Using Skills](#using-skills)
5. [Developing Skills](#developing-skills)
6. [Troubleshooting](#troubleshooting)

---

## What Are Skills?

Skills are specialized capabilities that the Risk Agent can invoke to handle complex, domain-specific tasks. They follow the [Claude Agent SDK skills framework](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills).

### Key Characteristics

- **Reusable**: Skills can be invoked multiple times across sessions
- **Self-contained**: Each skill bundles its own documentation and executables
- **Discoverable**: Skills are automatically detected from `.claude/skills/` directory
- **Visible**: Skill invocations appear with distinct visual styling (bright magenta border)

### Skill vs Tool vs Direct Implementation

| Approach | When to Use | Example |
|----------|-------------|---------|
| **Skill** | Complex, repeatable domain tasks | "Create meeting minutes from transcript" |
| **Tool** | Single-purpose operations | "Read file", "Run bash command" |
| **Direct** | One-off custom logic | "Write a quick script to parse this CSV" |

---

## Available Skills

The Risk Agent framework includes 9 skills:

### 1. meeting-minutes
**Purpose**: Extract structured meeting minutes from transcripts
**Trigger**: "create meeting minutes", "structure these notes"
**Output**: Formatted markdown with attendees, decisions, action items

### 2. project-planner
**Purpose**: Generate comprehensive project plans
**Trigger**: "create project plan", "plan this initiative"
**Output**: Markdown with scope, timeline, resources, risks

### 3. status-reporter
**Purpose**: Generate project status reports
**Trigger**: "create status report", "generate project update"
**Output**: Executive summary with RAG status, accomplishments, risks

### 4. stakeholder-analysis
**Purpose**: Analyze stakeholder relationships and influence
**Trigger**: "analyze stakeholders", "map stakeholder landscape"
**Output**: Stakeholder matrix with power/interest analysis

### 5. itc-template-filler
**Purpose**: Populate ITC (Investment Technology Committee) governance templates - **first governance gate**
**Trigger**: "complete ITC template", "fill ITC proposal", "prepare for ITC"
**Output**: Populated Excel template + gap analysis report

**Special Features**:
- Handles merged cells in Excel templates
- Multi-source data extraction with confidence scoring
- Bundled executable Python modules
- Command-line interface available

See: [ITC Template Filler Reference](06b-itc-template-filler-reference.md) for detailed documentation

### 6. icc-business-case-filler
**Purpose**: Populate ICC (Investment & Change Committee) business case templates - **second governance gate**
**Trigger**: "complete ICC template", "fill ICC business case", "prepare ICC approval"
**Output**: Populated Excel template + interactive clarification report

**Special Features**:
- **Interactive clarification mode** - identifies missing critical fields and generates targeted questions
- Pre-populates from ITC template (30-40 fields automatically)
- Handles 17-sheet template with ~2000 fields
- Priority-based gap analysis (CRITICAL → HIGH → MEDIUM → LOW)
- Iterative completion workflow for complex business cases
- Bundled executable Python modules
- Command-line interface available

**Governance Flow**: ITC (strategic alignment) → ICC (detailed business case)

See: `.claude/skills/icc-business-case-filler/README.md` for detailed documentation

### 7. pillar-stress-generator
**Purpose**: Create and review top-down "pillar stress" scenarios for market risk management
**Trigger**: "create stress scenario", "review stress scenario", "generate MLRC stress document"
**Output**: Complete scenario parameterization + MLRC Word document + validation report

**Special Features**:
- **Comprehensive risk factor library** - 473 rate curves, 271 FX pairs, Credit, Energy, Precious/Base Metals
- **Historical crisis calibration** - Parameterization based on 5 major historical crises (2008, 2011, 2020, 2022, 2015)
- **10 scenario types** - Recession, inflation shock, supply disruption, financial crisis, policy error, and more
- **Validation framework** - Correlation consistency, magnitude limits, tenor structure logic
- **Annual review workflow** - Assess relevance, detect changes, propose updates
- **MLRC document generation** - Word docs matching governance format
- **Confidence scoring** - 60-80% confidence on test scenarios with zero validation errors
- Bundled executable Python modules (3,200+ lines)

**Workflow**: Scenario design → Parameterization → Validation → Front Office consultation → MLRC approval

See: [Pillar Stress Generator Reference](06c-pillar-stress-generator.md) for detailed documentation

### 8. process-documenter
**Purpose**: Create comprehensive business process and workflow documentation with professional flow diagrams
**Trigger**: "document process", "create BPMN diagram", "create process flow", "process documentation"
**Output**: Process analysis document + BPMN 2.0 XML + Mermaid diagrams + Data Flow Diagrams (if applicable)

**Special Features**:
- **Multiple diagram formats** - BPMN 2.0, Mermaid (LR and TB), PlantUML, Data Flow Diagrams
- **BPMN 2.0 support** - Horizontal swim lanes, message flows, sub-processes, collapsed activities, full DI (diagram interchange)
- **Intelligent format selection** - Recommends best format based on process characteristics
- **3 input modes** - Interactive Q&A, meeting minutes extraction, process description
- **Quality assurance** - Validates sequence ordering, distinguishes departments vs systems, checks for missing steps
- **Critical control sequencing** - Ensures reconciliation, approvals, and quality gates happen in correct order
- **Swim lane analysis** - Identifies cross-departmental workflows and communication
- **Data flow diagrams** - External entities, processes, data stores, transformations
- **Git-friendly** - Mermaid and PlantUML diagrams render in markdown

**Workflow**: Gather information (Q&A or document extraction) → Analyze process → Recommend formats → Generate diagrams + documentation → Iterate on feedback

**Use Cases**:
- Operational processes (stress testing, month-end close, data quality)
- Governance processes (committee approvals, policy reviews, regulatory reporting)
- System processes (ETL, data flows, integrations)
- Cross-functional workflows (new product approval, incident management)

See: [Process Documenter Reference](06d-process-documenter.md) for detailed documentation

### 9. stress-scenario-suggester
**Purpose**: Research current financial market developments and suggest stress scenarios for market risk testing
**Trigger**: "suggest stress scenarios", "identify emerging risks", "what scenarios should we test", "research market developments"
**Output**: Comprehensive research report with prioritized scenario recommendations

**Special Features**:
- **Parallel research architecture** - Launches 5 specialized research agents simultaneously
- **5 research domains** - Geopolitical, Macroeconomic, Market Structure, Climate & ESG, Technology & Sector risks
- **Web search powered** - Each agent uses WebSearch to find current developments (last 3-6 months)
- **Prioritization matrix** - Ranks scenarios by urgency vs severity
- **Plausibility assessment** - Filters for realistic, material, actionable scenarios
- **Integration with pillar-stress-generator** - Outputs can be directly fed into scenario parameterization
- **Confidence scoring** - Based on source quality and consistency across agents

**Research Agents**:
1. **Geopolitical Risk Researcher** - Conflicts, sanctions, trade wars, political instability
2. **Macroeconomic Risk Researcher** - Monetary policy, inflation, recession, sovereign debt
3. **Market Structure Risk Researcher** - Leverage, liquidity, concentration, systemic risks
4. **Climate & ESG Risk Researcher** - Physical risks, transition risks, regulatory changes
5. **Technology & Sector Risk Researcher** - AI disruption, cyber threats, sector vulnerabilities

**Workflow**: Launch parallel research → WebSearch for current developments → Each agent suggests 2-3 scenarios → Synthesize findings → Prioritize by urgency/severity → Recommend next steps

**Use Cases**:
- Quarterly stress scenario library review
- Risk appetite framework updates
- ICAAP/ILAAP emerging risk identification
- MLRC scenario portfolio planning
- Forward-looking risk radar updates

**Example Output**:
- **Priority 1**: US Commercial Real Estate Collapse (High urgency, not currently tested)
- **Priority 2**: AI Disruption to Financial Services (Medium urgency, novel scenario)
- **Priority 3**: China Property Contagion (High urgency, update existing scenario)

See: [Stress Scenario Suggester Reference](06e-stress-scenario-suggester.md) for detailed documentation

---

## How Skills Work

### Architecture

```
User Query
    ↓
Risk Agent (change-agent)
    ↓
Model evaluates: Should I use a Skill?
    ↓
[YES] → Invokes Skill tool with skill name + args
    ↓
SDK loads skill from .claude/skills/{name}/SKILL.md
    ↓
Skill executes (may use bundled Python modules)
    ↓
Returns result to agent
    ↓
Agent continues with result
```

### Skill Detection

The SDK automatically detects skills by:
1. Looking in `.claude/skills/` directory
2. Finding subdirectories with `SKILL.md` files
3. Parsing YAML frontmatter for metadata:
   ```yaml
   ---
   name: skill-name
   description: Short description for model to understand when to use this skill
   ---
   ```

### Skill Invocation in CLI

When a skill is invoked, you'll see:

```
╭────────────────────── Skill: meeting-minutes ──────────────────────╮
│                                                                     │
│ Arguments:                                                          │
│ {                                                                   │
│   "transcript": "...",                                             │
│   "meeting_date": "2025-01-08"                                     │
│ }                                                                   │
╰─────────────────────────────────────────────────────────────────────╯
```

### Technical Implementation

**Detection in CLI** (`src/cli_utils.py`):
```python
if block.name == "Skill":
    skill_name = block.input.get("skill", "unknown")  # SDK uses "skill" key
    skill_args = block.input.get("args", {})
    _skill_tool_use_ids[block.id] = skill_name
    # Display with bright magenta border
```

**SDK Structure** (what the model sends):
```python
ToolUseBlock(
    name="Skill",
    input={
        "skill": "meeting-minutes",  # Skill name
        "args": {                     # Skill arguments
            "transcript": "...",
            "meeting_date": "..."
        }
    }
)
```

---

## Using Skills

### For Users

#### Invoke by Natural Language

Simply describe what you want in natural language. The agent will choose the appropriate skill:

```
Create meeting minutes from the transcript in data/meeting.txt
```

The agent recognizes keywords and invokes the `meeting-minutes` skill automatically.

#### Explicit Invocation

You can explicitly request a skill:

```
Use the itc-template-filler skill to complete the ITC template
```

#### Check What Skills Are Available

```
What skills do you have available?
```

The agent will list all detected skills with descriptions.

### For Developers

#### Skill Invocation Triggers

Each skill has trigger keywords in its description. For example:

**meeting-minutes**:
```yaml
description: Creates structured meeting minutes from transcripts. Use when user asks to "create meeting minutes", "structure notes", or "format meeting transcript"
```

Keywords: "create meeting minutes", "structure notes", "format meeting transcript"

**itc-template-filler**:
```yaml
description: Automatically fills out ITC Project Template Excel files. Use when user asks to "complete ITC template", "fill template", "populate template"
```

Keywords: "complete ITC template", "fill template", "populate template"

#### Skill Preferences in change-agent

The change agent is configured to **prefer skills over custom implementations**:

From `.claude/agents/change-agent.md`:
```markdown
### 3. Let Skills Handle Specialized Work

**IMPORTANT**: Always use skills for specialized tasks - DO NOT write custom Python scripts when a skill exists.

When user asks to:
- "Complete ITC template" → Use itc-template-filler skill (don't write custom Excel scripts)
- "Create meeting minutes" → Use meeting-minutes skill (don't write custom parsing code)
```

---

## Developing Skills

### Skill Structure

Following [Anthropic's best practices](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills):

```
.claude/skills/your-skill-name/
├── SKILL.md           # Skill definition (required)
├── README.md          # User documentation (recommended)
├── helper_module.py   # Python modules (optional)
└── executable.py      # Standalone scripts (optional)
```

### SKILL.md Format

```markdown
---
name: your-skill-name
description: Short description. Use when user asks to "trigger phrase", "another trigger"
---

# Skill Name

## Purpose
What this skill does...

## When to Use
**ALWAYS USE THIS SKILL** when:
- User asks to "trigger phrase"
- User mentions "specific keywords"

## What This Skill Provides
Detailed description...

## Input Parameters
- `param1`: Description
- `param2`: Description

## Output Format
What the skill returns...

## Examples
Concrete examples...
```

### Progressive Disclosure Principle

1. **Minimal metadata** in YAML frontmatter (name + short description)
2. **Detailed context** in SKILL.md body (when to use, parameters, examples)
3. **Implementation details** in bundled Python modules (if needed)

The SDK only loads what's needed when the skill becomes relevant.

### Bundling Executable Modules

For complex skills (like `itc-template-filler`), bundle Python modules:

**Benefits**:
- Reusable code (don't recreate scripts each time)
- Handle technical complexity (e.g., merged cells in Excel)
- Serve as both executables AND reference documentation
- Can be used programmatically or via CLI

**Example**: itc-template-filler includes:
- `excel_helpers.py` - Safe Excel manipulation
- `extraction_helpers.py` - Multi-source data extraction
- `populate_template.py` - Main population engine

The SKILL.md references these modules with usage examples.

### Best Practices

1. **Clear Trigger Keywords**: Make description match common user queries
2. **Explicit Directives**: Use "ALWAYS USE THIS SKILL (do not write custom scripts)"
3. **Concrete Examples**: Show real inputs and outputs
4. **Error Handling**: Document common errors and solutions
5. **Modular Code**: Separate concerns into focused modules
6. **Dual-Purpose Scripts**: Modules should be usable standalone or imported

---

## Troubleshooting

### Issue: Skill Not Invoked

**Symptom**: Agent creates custom scripts instead of using skill

**Possible Causes**:
1. ❌ Skill description doesn't match query keywords
2. ❌ Model prefers direct implementation over skill
3. ❌ Skill not detected (SKILL.md missing or malformed)

**Solutions**:

**Check Skill Detection**:
```bash
# List all skills
ls .claude/skills/
```

Each should have `SKILL.md` file.

**Verify Description Keywords**:
Open `.claude/skills/your-skill/SKILL.md` and check if trigger keywords match your query.

**Add Explicit Directive**:
In SKILL.md, add:
```markdown
## When to Use
**ALWAYS USE THIS SKILL** (do not write custom Python scripts) when:
- User asks to "exact phrase from your query"
```

**Update change-agent**:
In `.claude/agents/change-agent.md`, add skill reference:
```markdown
### your-skill-name
Use when user asks to "trigger phrase". DO NOT write custom scripts for this task.
```

### Issue: Skill Name Shows as "unknown"

**Symptom**: CLI displays `Skill: unknown` instead of actual skill name

**Cause**: Code looking for wrong key in skill invocation

**Solution**: Fixed in v1.1. Code now uses correct key:
```python
# Correct (SDK uses "skill" key):
skill_name = block.input.get("skill", "unknown")

# Wrong (doesn't exist):
skill_name = block.input.get("skill_name", "unknown")
```

### Issue: Merged Cell Error in Excel

**Symptom**: `AttributeError: 'MergedCell' object attribute 'value' is read-only`

**Cause**: Direct assignment to merged cell in Excel

**Solution**: Use `itc-template-filler` skill which includes merged cell handling:
```python
from excel_helpers import set_cell_value
set_cell_value(sheet, 'E11', value)  # Works for merged or regular cells
```

### Issue: Low Confidence Extractions

**Symptom**: Gap analysis shows many low-confidence fields

**Cause**: Insufficient or ambiguous source documentation

**Solutions**:
1. Provide multiple source types (meeting minutes + technical spec + business case)
2. Ensure source documents have clear section headers
3. Use explicit field labels in source docs (e.g., "Business Sponsor: John Doe")
4. Review gap analysis to see what's missing, then update source docs

---

## Additional Resources

### Documentation
- [ITC Template Filler Reference](06b-itc-template-filler-reference.md) - Detailed guide for itc-template-filler skill
- [Pillar Stress Generator Reference](06c-pillar-stress-generator.md) - Detailed guide for pillar-stress-generator skill
- [Process Documenter Reference](06d-process-documenter.md) - Detailed guide for process-documenter skill
- [itc-template-filler README](../.claude/skills/itc-template-filler/README.md) - Quick start and module documentation
- [pillar-stress-generator README](../.claude/skills/pillar-stress-generator/README.md) - Quick start and module documentation
- [process-documenter README](../.claude/skills/process-documenter/README.md) - Quick start and usage guide

### External Links
- [Claude Agent SDK Documentation](https://github.com/anthropics/claude-agent-sdk)
- [Anthropic: Equipping Agents for the Real World with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

### Source Code
- Skill definitions: `.claude/skills/*/SKILL.md`
- Change agent configuration: `.claude/agents/change-agent.md`
- CLI skill detection: `src/cli_utils.py`

---

**Document Version**: 1.1
**Consolidated From**: 06-skill-detection-implementation.md, 09-skill-invocation-troubleshooting.md
**Status**: Active Reference
