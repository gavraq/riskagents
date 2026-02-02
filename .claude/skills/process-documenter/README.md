# Process Documenter Skill

## Overview

The **Process Documenter** skill transforms business process descriptions, meeting minutes, or Q&A sessions into professional documentation with multiple diagram formats (BPMN, Mermaid, PlantUML, Data Flow Diagrams).

## Quick Start

### Option 1: From Meeting Minutes
```
User: "I have meeting minutes about our stress testing process. Can you create process documentation?"
Provide: [Meeting minutes file path or paste content]
```

### Option 2: Interactive Q&A
```
User: "Document our loan approval process"
Skill will ask structured questions to gather information
```

### Option 3: From Process Description
```
User: "Here's our process description: [paste text]. Create BPMN diagram and documentation."
```

## What Gets Created

### Output Files
All files are created in:
```
/Users/gavinslater/projects/riskagent/data/icbc_standard_bank/Processes/
  └── [Business Area]/
      └── [Process Name]/
          └── docs/
              ├── process-analysis-[name].md      # Comprehensive documentation
              ├── [name]-bpmn.xml                 # BPMN 2.0 diagram
              ├── [name]-mermaid.md               # Mermaid diagrams
              ├── [name]-dfd.md                   # Data flow diagram (if systems involved)
              └── [name]-plantuml.puml            # PlantUML (optional)
```

### Documentation Includes
- ✅ Process overview and objectives
- ✅ Trigger events and frequency
- ✅ Detailed step-by-step descriptions
- ✅ Decision point explanations
- ✅ Swim lane responsibility matrix
- ✅ Data flow analysis
- ✅ Critical controls and quality gates
- ✅ Inputs/outputs table
- ✅ Timing and duration estimates
- ✅ Exception handling

### Diagrams Include
- ✅ **BPMN 2.0**: Horizontal swim lanes, message flows, sub-processes, collapsed activities
- ✅ **Mermaid LR**: Git-friendly left-to-right diagrams
- ✅ **PlantUML**: Vertical swim lanes for technical docs
- ✅ **Data Flow Diagrams**: System interactions and data transformations

## Features

### Intelligent Format Selection
The skill recommends diagram formats based on:
- Number of departments involved (swim lanes)
- Process complexity
- Governance requirements
- System interactions
- Version control needs

### Quality Assurance
- ✅ Validates sequence ordering (critical controls before execution)
- ✅ Distinguishes departments vs systems (e.g., "Asset Control" vs "FMDM")
- ✅ Checks for missing steps or unclear decision points
- ✅ Ensures reconciliation happens before distribution

### BPMN 2.0 Support
- ✅ Horizontal swim lanes for cross-departmental processes
- ✅ Message flows showing cross-department communication
- ✅ Sub-processes for complex activities
- ✅ Collapsed activities with links to detailed diagrams
- ✅ Full diagram interchange (DI) for visual layout in BPMN editors

### Data Flow Diagrams
- ✅ External entities (departments, users, external systems)
- ✅ Processes (activities that transform data)
- ✅ Data stores (FMDM, Excel golden source, databases)
- ✅ Data flows with direction and labels

## File Structure

```
.claude/skills/process-documenter/
├── SKILL.md                          # Skill definition (triggers, description)
├── README.md                         # This file
├── reference.md                      # Detailed guide for all diagram formats
├── templates/
│   ├── process-interview-template.md      # Structured Q&A questions
│   └── document-extraction-template.md    # How to extract from documents
└── examples/
    └── stress-testing-example.md          # Full reference example
```

## Usage Examples

### Example 1: Market Risk Stress Testing
**Input:** Meeting minutes discussing stress parameterisation process

**Output:**
- BPMN diagram with 3 swim lanes (Market Risk, Front Office, Asset Control)
- Mermaid LR diagram
- Data flow diagram (FMDM → Vespa/Murex)
- 40-page markdown documentation

**Key Features Used:**
- Pillar vs PoW decision point
- Message flows between departments
- Sub-process for Top Risk Analysis
- Critical control: Reconciliation before distribution

### Example 2: Loan Approval Workflow
**Input:** Interactive Q&A about loan approval process

**Output:**
- BPMN diagram with swim lanes (Origination, Credit Risk, Compliance, Finance)
- Decision points (Credit score check, Compliance review)
- Approval gates
- Exception handling (if declined, notify customer)

### Example 3: System Data Flow
**Input:** "Show how data flows from trading systems through FMDM to calculation engines"

**Output:**
- Data flow diagram showing:
  - External entities (Trading, Market Data)
  - Processes (Validation, Transformation, Distribution)
  - Data stores (FMDM, Vespa DB, Murex DB)
  - Data flows with transformations

## How It Works

### 1. Information Gathering
**From Meeting Minutes:**
- Reads document
- Extracts process steps, decision points, participants, systems
- Identifies swim lanes and data flows

**From Q&A:**
- Asks structured questions:
  - Process overview
  - Participants (departments/systems)
  - Steps and decision points
  - Critical controls
  - Data flows
  - Timing

### 2. Analysis
- Counts swim lanes (determines if BPMN recommended)
- Identifies system interactions (determines if DFD needed)
- Assesses complexity (sub-processes needed?)
- Checks for critical controls (reconciliation, approvals)

### 3. Format Recommendation
Recommends diagram format(s) based on analysis:
- **BPMN**: If 2+ swim lanes + formal governance
- **DFD**: If system interactions are primary focus
- **Mermaid**: If simple process + version control important
- **PlantUML**: If technical audience + vertical flow preferred

### 4. Generation
- Creates diagram(s) in recommended format(s)
- Generates comprehensive markdown documentation
- Validates sequence ordering
- Saves to ICBC Standard Bank folder structure

### 5. Iteration
- User reviews output
- Provides feedback (e.g., "reconciliation should happen earlier")
- Skill refines diagrams and documentation
- Repeat until approved

## Tips for Best Results

### When Providing Meeting Minutes
**Include:**
- Who is involved (departments, roles)
- What steps were discussed
- Decision points and criteria
- Systems mentioned
- Critical controls (reconciliation, approvals)
- Timing estimates

**Example:**
```
"Mike from Asset Control noted that after MLRC approval, they upload parameters
to FMDM. Important: FMDM must be reconciled against the Excel golden source
BEFORE sending to Vespa and Murex."
```

### When Doing Q&A
**Be specific:**
- "3 departments: Market Risk, Front Office, Asset Control"
- "Decision point: Is the scenario a Pillar stress or Point of Weakness stress?"
- "Critical control: Reconcile FMDM vs Excel golden source BEFORE distribution"

**Mention corrections:**
- "Asset Control is the department name, FMDM is the system name"
- "The reconciliation should happen after FMDM upload but before sending to calculation systems"

### When Requesting Refinements
**Be explicit:**
- ✅ "Move the reconciliation step to before the distribution step"
- ✅ "Add a sub-process for Top Risk Analysis with these steps: [...]"
- ✅ "Change 'Asset Control system' to 'FMDM (Financial Market Data Management)'"
- ❌ "Fix the flow" (too vague)

## Common Use Cases

### ✅ Operational Processes
- Trading book approval
- Month-end close procedures
- Data quality checks
- Report generation workflows

### ✅ Governance Processes
- Committee approval workflows
- Policy review cycles
- Regulatory reporting submission
- Audit processes

### ✅ System Processes
- Data flows between systems
- ETL (Extract, Transform, Load) processes
- System integrations
- Automated calculations

### ✅ Cross-Functional Processes
- Stress testing parameterisation
- New product approval
- Incident management
- Change management

## Limitations

### ❌ Not For
- Code documentation (use code documentation tools)
- Data schemas (use ERD tools)
- Project plans (use project management tools)
- Organization charts (use org chart tools)

### ⚠️ Mermaid Limitations
- Swim lanes are stacked vertically, not truly horizontal
- No message flows between lanes
- Limited to basic elements (tasks, decisions)
- Best for simple processes (1-2 swim lanes)

### ⚠️ PlantUML Limitations
- Swim lanes are vertical only
- No horizontal layout for cross-functional processes
- Better suited for technical diagrams

## Troubleshooting

### Issue: "I can't see the BPMN diagram"
**Solution:** BPMN XML files need a BPMN editor:
- Go to https://demo.bpmn.io/
- Click "Open File"
- Select the generated `[name]-bpmn.xml` file

### Issue: "Mermaid diagram doesn't render in my editor"
**Solution:**
- GitHub/GitLab: Should render automatically
- VSCode: Install "Markdown Preview Mermaid Support" extension
- Online: Use https://mermaid.live/

### Issue: "The reconciliation is in the wrong place"
**Solution:** Tell the skill explicitly:
- "The reconciliation should happen after FMDM upload but before distribution to Vespa/Murex"
- Skill will regenerate diagrams with correct sequence

### Issue: "Department names vs system names are confusing"
**Solution:** Clarify:
- "Asset Control is the department (swim lane)"
- "FMDM is the system (not a swim lane)"
- Skill will update diagrams and documentation

## Version History

### v1.0 (January 2025)
**Initial Release:**
- BPMN 2.0 with horizontal swim lanes, message flows, sub-processes
- Mermaid LR diagrams
- PlantUML vertical swim lanes
- Data flow diagrams
- Meeting minutes extraction
- Interactive Q&A mode
- ICBC Standard Bank folder structure integration
- Comprehensive documentation generation
- Sequence validation for critical controls

## Support

For questions or issues:
1. Check the [reference.md](reference.md) for detailed diagram guides
2. Review [examples/stress-testing-example.md](examples/stress-testing-example.md) for a complete example
3. Use the interview template in [templates/process-interview-template.md](templates/process-interview-template.md)

## License

This skill is part of the Risk Agent project for ICBC Standard Bank.
