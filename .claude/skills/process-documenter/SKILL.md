---
name: process-documenter
description: |
  Creates comprehensive business process and system interaction documentation with professional flow diagrams.

  Use when user wants to:
  - Document a business process, workflow, or operational procedure
  - Create process flow diagrams, BPMN diagrams, or swim lane diagrams
  - Map cross-departmental workflows or approval processes
  - Document system interactions with data flow diagrams
  - Convert meeting minutes or process descriptions into visual diagrams
  - Analyze and improve existing process documentation

  Capabilities:
  - Extracts process information from meeting minutes, documents, or Q&A sessions
  - Recommends optimal diagram format based on process characteristics (BPMN, Mermaid, PlantUML, DFD)
  - Generates professional diagrams with horizontal swim lanes for multi-department processes
  - Supports BPMN message flows, sub-processes, and collapsed activities
  - Creates data flow diagrams for system interactions
  - Produces detailed documentation: step descriptions, decision logic, swim lane responsibilities, data flows
  - Validates critical controls and sequence ordering (e.g., reconciliation before distribution)
  - Supports iterative refinement based on user feedback

  Works with:
  - Input: Meeting minutes, process descriptions, Q&A interviews, existing documentation
  - Output: Multiple diagram formats + comprehensive markdown documentation in ICBC Standard Bank process folder structure

  Best for: Banking operations, governance processes, regulatory workflows, approval chains, system integrations, data flows.

allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Process Documenter Skill

## Overview

The **Process Documenter** skill transforms process descriptions, meeting minutes, or interview responses into professional business process documentation with multiple diagram formats.

## What This Skill Does

### 1. Information Extraction
- Analyzes meeting minutes or process descriptions
- Identifies process steps, decision points, participants, systems
- Detects swim lanes (departments/roles involved)
- Extracts critical controls, data flows, and system interactions

### 2. Intelligent Format Selection
- Recommends diagram format based on:
  - Number of swim lanes (departments)
  - Process complexity (sequential/parallel/loops)
  - Governance requirements (formal BPMN vs agile Mermaid)
  - System interactions (data flow diagrams)
  - Version control needs

### 3. Multi-Format Generation
Generates one or more of:
- **BPMN 2.0**: Industry-standard, horizontal swim lanes, message flows, sub-processes
- **Mermaid LR**: Git-friendly, renders in GitHub, quick iteration
- **PlantUML**: Vertical swim lanes, good for technical docs
- **Data Flow Diagrams**: System interactions, data stores, external entities

### 4. Comprehensive Documentation
Creates markdown documentation including:
- Process overview and trigger events
- Detailed step-by-step descriptions
- Decision point explanations
- Swim lane responsibility matrix
- Data flow analysis
- Critical controls and quality gates
- Inputs/outputs table
- Process timing and frequency

### 5. Quality Assurance
- Validates sequence ordering (critical controls before execution)
- Distinguishes departments vs systems (e.g., "Asset Control" vs "FMDM")
- Checks for missing steps or unclear decision points
- Flags potential issues for user review

## When to Use This Skill

✅ **Use when user says:**
- "Document this process"
- "Create a BPMN diagram for..."
- "Map out our approval workflow"
- "Generate process flow for..."
- "I have meeting minutes about our process, can you diagram it?"
- "Convert this process description into a swim lane diagram"
- "Show data flow between our systems"

✅ **Use when user provides:**
- Meeting minutes discussing a process
- Process description document
- Request for process mapping
- Existing process that needs improvement

❌ **Don't use for:**
- Code documentation (use different skill)
- Data schemas (use ERD tools)
- Project plans (use project management tools)

## Usage Examples

### Example 1: From Meeting Minutes
```
User: "I have meeting minutes from our stress testing parameterisation review.
Can you create process documentation?"

Skill: [Reads meeting minutes, extracts process info, asks clarifying questions if needed]
Output: BPMN diagram + Mermaid LR + comprehensive markdown doc in
/Users/gavinslater/projects/riskagent/data/icbc_standard_bank/Processes/Market_Risk/Stress Testing/docs/
```

### Example 2: Interactive Q&A
```
User: "Document our loan approval process"

Skill: "I'll help you document the loan approval process. Let me ask some questions:
1. How many departments are involved?
2. What triggers the process?
3. What are the major steps?
..." [continues with structured interview]

Output: Multi-format diagrams + documentation
```

### Example 3: System Data Flow
```
User: "Show how data flows between FMDM, Vespa, and Murex GTS"

Skill: [Generates data flow diagram showing systems, data stores, flows]
Output: DFD diagram + data flow documentation
```

## Output Structure

Files are created in:
```
/Users/gavinslater/projects/riskagent/data/icbc_standard_bank/Processes/[Business Area]/[Process Name]/docs/
├── process-analysis-[process-name].md     # Comprehensive documentation
├── [process-name]-bpmn.xml                # BPMN 2.0 diagram (if applicable)
├── [process-name]-mermaid.md              # Mermaid diagrams
├── [process-name]-dfd.md                  # Data flow diagram (if systems involved)
└── [process-name]-plantuml.puml           # PlantUML (optional)
```

## Key Features

### BPMN Support
- ✅ Horizontal swim lanes (multiple departments)
- ✅ Message flows (cross-department communication)
- ✅ Sub-processes (collapsed activities)
- ✅ Gateways (exclusive, parallel, inclusive)
- ✅ Events (start, end, intermediate, timer, error)
- ✅ Tasks, user tasks, service tasks
- ✅ **COMPLETE diagram interchange (DI) for visual layout** - MANDATORY for rendering

**CRITICAL:** All BPMN files MUST include complete BPMNDiagram sections with positioning for every element.
Without complete DI, BPMN files will show empty swim lanes or fail to render in demo.bpmn.io, Camunda, and other tools.

See `bpmn-di-complete-guide.md` for comprehensive positioning algorithms and templates.

### Data Flow Diagrams
- ✅ External entities (departments, users, external systems)
- ✅ Processes (activities that transform data)
- ✅ Data stores (databases, FMDM, Excel golden source)
- ✅ Data flows (with labels and direction)

### Quality Controls
- ✅ Sequence validation (e.g., "reconciliation before distribution")
- ✅ Department vs System distinction
- ✅ Critical control identification
- ✅ Decision point clarity

## Next Steps After Generation

1. **Review**: User reviews generated diagrams and documentation
2. **Refine**: Skill iterates based on feedback (e.g., "move reconciliation earlier")
3. **Validate**: User validates with process owners
4. **Version**: Commit to Git (diagrams are text-based)
5. **Share**: BPMN can be opened in demo.bpmn.io, Mermaid renders in GitHub

## Tips for Best Results

### For Meeting Minutes
- Include: Who is involved, what steps were discussed, decision points, systems mentioned
- The more detail, the better the output
- Skill will ask clarifying questions if information is missing

### For Process Descriptions
- Describe: Trigger, steps, decision points, responsible parties, outputs
- Mention: Any critical controls, reconciliation points, approval gates
- Specify: Systems involved (for data flow diagrams)

### For Iterative Refinement
- Be specific: "The reconciliation should happen before sending to Vespa"
- Mention corrections: "Asset Control is the department, FMDM is the system"
- Request additions: "Add a sub-process for the Top Risk Analysis"

## Version History

- **v1.0** (2025-01): Initial release
  - BPMN 2.0 with swim lanes, message flows, sub-processes
  - Mermaid LR horizontal diagrams
  - PlantUML vertical swim lanes
  - Data flow diagrams
  - Meeting minutes extraction
  - Interactive Q&A mode
  - ICBC Standard Bank folder structure integration
