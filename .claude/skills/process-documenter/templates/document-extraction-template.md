# Process Information Extraction Template

Use this template to systematically extract process information from meeting minutes, process descriptions, or other documents.

## Extraction Checklist

### ✅ Step 1: Initial Scan
Read the document and identify:
- [ ] Process name
- [ ] Business area / department
- [ ] Purpose / objective
- [ ] Trigger events
- [ ] Main participants (departments/roles)

### ✅ Step 2: Identify Process Structure

#### Participants (Swim Lanes)
Extract:
- [ ] **Departments**: List all departments/roles mentioned (each becomes a swim lane)
  - Look for: "Market Risk", "Front Office", "Asset Control", "IT", "Finance", etc.
  - Note their responsibilities

- [ ] **Systems**: List all systems mentioned (distinguish from departments!)
  - Look for: System names (FMDM, Murex, Vespa, SAP, etc.)
  - Database names, applications, platforms
  - **Watch for**: Phrases like "Asset Control system" → clarify if it's a department or system name

#### Process Flow Markers
Look for:
- [ ] **Sequence indicators**: "first", "then", "next", "after", "before", "finally"
- [ ] **Decision points**: "if", "whether", "decide", "approve", "agree", "check"
- [ ] **Parallel activities**: "while", "simultaneously", "at the same time", "in parallel"
- [ ] **Loops**: "iterate", "repeat", "re-do", "cycle", "until", "revisit"

### ✅ Step 3: Extract Process Steps

For each step found, capture:
```
Step [N]: [Step Name]
Actor: [Who performs this? Department or System]
Action: [What is done? Verb + object]
Input: [What is needed?]
Output: [What is produced?]
Decision: [If applicable: what is being decided?]
Next step: [What happens next? Or branches?]
```

Example:
```
Step 1: Review business mix and portfolios
Actor: Market Risk
Action: Review current portfolio composition and market outlook
Input: Portfolio data, market forecasts
Output: Decision on scenario type (Pillar vs PoW)
Decision: Core scenario or Point of Weakness?
Next step: If Pillar → Step 2A, If PoW → Step 2B
```

### ✅ Step 4: Identify Decision Points

For each decision point, extract:
```
Decision Point: [Name]
Location: [At what step?]
Question: [What is being decided?]
Options: [What are the choices? e.g., Yes/No, Pass/Fail, Option A/B/C]
Criteria: [How is the decision made?]
If [Option 1]: [What happens?]
If [Option 2]: [What happens?]
```

Example:
```
Decision Point: Reconciliation Check
Location: After FMDM upload, before distribution
Question: Does FMDM match Excel golden source?
Options: Yes (OK) / No (mismatch)
Criteria: Compare all parameters field-by-field
If Yes: Proceed to FMDM distribution to Vespa/Murex
If No: Investigate discrepancies, correct FMDM, re-reconcile
```

### ✅ Step 5: Extract Critical Controls

Look for keywords indicating quality controls:
- "reconcile", "validate", "verify", "check", "approve", "sign-off"
- "golden source", "authoritative", "master data"
- "quality gate", "control point", "checkpoint"

For each control, extract:
```
Control: [Name]
Type: [Approval / Reconciliation / Validation / Quality Check]
Sequence: [BEFORE what? AFTER what? This is critical!]
Who performs: [Department/role]
What is checked: [Specific items]
Pass criteria: [What does "pass" mean?]
Fail action: [What happens if it fails?]
```

**CRITICAL**: Pay special attention to sequence. Look for:
- "before sending to..."
- "after receiving from..."
- "must be completed before..."
- "only after approval..."

### ✅ Step 6: Extract Data & Information Flows

#### Inputs to Process
Look for:
- "receives", "provided by", "input from", "requires", "based on"
- Data sources, documents, requests, notifications

For each input:
```
Input: [Name]
Source: [Where from? Who provides?]
Format: [Excel, Word, email, system data, etc.]
Frequency: [When is it provided?]
Used by: [Which step? Which actor?]
```

#### Outputs from Process
Look for:
- "produces", "generates", "creates", "sends to", "delivers", "outputs"
- Documents, reports, data, notifications, approvals

For each output:
```
Output: [Name]
Destination: [Where to? Who receives?]
Format: [File type, system, etc.]
Frequency: [When is it produced?]
Purpose: [Why is it needed?]
```

#### Data Transformations
Look for how data changes through the process:
```
Input data → Process step → Output data
```

Example:
```
Economic narrative (Word) → Parameterisation → Shock values (Excel) → FMDM upload → System format → Stress results
```

### ✅ Step 7: Extract Timing Information

Look for:
- Process duration: "takes 2 weeks", "completed within 3 days"
- Step duration: "typically 1 week for..."
- Deadlines: "must be done by month-end", "regulatory deadline Q1"
- Frequency: "monthly", "quarterly", "annual", "ad-hoc"
- SLAs: "within 2 business days", "same-day turnaround"

### ✅ Step 8: Extract Sub-Processes

Look for mentions of complex activities that might be sub-processes:
- "Top Risk Analysis involves..." (then lists multiple sub-steps)
- "The validation process includes..." (then lists checks)
- "Asset Control performs..." (then lists several activities)

Mark these as potential sub-processes or collapsed activities.

### ✅ Step 9: Extract Message Flows (Cross-Department)

Look for communication between departments:
- "Market Risk sends to Front Office"
- "Front Office provides feedback"
- "Asset Control notifies Market Risk"
- "IT sends confirmation to..."

For each message flow:
```
From: [Sender department]
To: [Receiver department]
Content: [What is sent? Document, approval, data, notification]
Trigger: [What prompts this communication?]
Response expected: [Yes/No, and what response?]
```

### ✅ Step 10: Extract Exception Handling

Look for:
- "if [error] occurs, then..."
- "when [problem], escalate to..."
- "in case of [failure], redo..."
- "exception handling", "error recovery"

For each exception:
```
Exception: [What goes wrong?]
Trigger: [What causes it?]
Handler: [Who handles it?]
Action: [What is done?]
Escalation: [When/to whom is it escalated?]
```

### ✅ Step 11: Identify Missing Information

After extraction, check for gaps:
- [ ] Are all process steps clear and sequenced?
- [ ] Are all decision points fully defined?
- [ ] Is the sequence of critical controls clear?
- [ ] Are all swim lane responsibilities identified?
- [ ] Are inputs and outputs complete?
- [ ] Are system vs department names disambiguated?

**Prepare clarifying questions for gaps**, e.g.:
- "The document mentions 'Asset Control system' - is this referring to the Asset Control department, or a specific system like FMDM?"
- "The reconciliation is mentioned, but when exactly does it happen relative to the FMDM distribution step?"
- "What happens if the MLRC defers approval?"

---

## Extraction Output Format

Structure extracted information as follows:

### Process Overview
- **Name**: [Process name]
- **Business Area**: [e.g., Market Risk]
- **Purpose**: [Brief description]
- **Trigger**: [What starts this process?]
- **Frequency**: [How often?]

### Participants
**Departments/Roles** (Swim Lanes):
1. [Department 1]: [Responsibilities]
2. [Department 2]: [Responsibilities]
...

**Systems**:
1. [System 1]: [Role in process]
2. [System 2]: [Role in process]
...

### Process Flow
```
[Step 1] → [Decision Point A?] → [Step 2A / Step 2B] → [Step 3] → ...
```

**Detailed Steps**:
1. **[Step Name]** ([Actor])
   - Action: [What is done]
   - Input: [What is needed]
   - Output: [What is produced]
   - Next: [What's next]

2. **[Decision Point Name]** ([Actor])
   - Question: [What is decided?]
   - Options: [Choices]
   - If [X]: [Path]
   - If [Y]: [Path]

...

### Critical Controls
1. **[Control Name]**
   - Type: [Approval/Reconciliation/Validation]
   - Sequence: [Before/After what step]
   - Performer: [Who]
   - Criteria: [Pass/Fail definition]

### Data Flows
**Inputs**:
- [Input 1]: From [source], Format [type]
- [Input 2]: From [source], Format [type]

**Outputs**:
- [Output 1]: To [destination], Format [type]
- [Output 2]: To [destination], Format [type]

### Message Flows
- [Dept A] → [Dept B]: [Message content]
- [Dept B] → [Dept A]: [Response]

### Timing
- Total duration: [X weeks]
- Key phase durations: [X days for Y phase]
- Deadlines: [Any regulatory/business deadlines]

### Sub-Processes
- [Sub-process 1]: [Brief description or note that it's complex]
- [Sub-process 2]: [Brief description]

### Exception Handling
- If [exception X]: [Handler does Y]
- Escalation: [To whom, when]

### Missing Information (Questions for User)
1. [Question 1]
2. [Question 2]
...

---

## Example: Extraction from Meeting Minutes

### Input Document:
```
Meeting Minutes: Market Risk Stress Parameterisation Review
Date: 15 Jan 2025
Attendees: Market Risk (Sarah), Front Office (John), Asset Control (Mike)

Discussion:
- Reviewed the process for creating pillar stress scenarios
- Market Risk explained they start by reviewing the portfolio mix and market outlook
- Two types of scenarios: regular pillar stresses and Point of Weakness (PoW) stresses
- For PoW, they do a Top Risk Analysis first to identify risks like concentrations or basis risk
- After parameterisation, they consult with Front Office desk heads
- Mike from Asset Control noted that after MLRC approval, they upload parameters to FMDM
- Important: FMDM must be reconciled against the Excel golden source BEFORE sending to Vespa and Murex
- John asked about timing - Sarah said typically 2-3 weeks for scenario design, 1 week for FO consultation
...
```

### Extraction Output:
```
Process Overview:
- Name: Market Risk Stress Parameterisation
- Business Area: Market Risk / Stress Testing
- Purpose: Create and approve stress test scenarios for regulatory and risk appetite purposes
- Trigger: Annual review cycle, ad-hoc market events, Top Risk Analysis
- Frequency: Annual (pillar stresses), ad-hoc (PoW stresses)

Participants:
Departments (Swim Lanes):
1. Market Risk: Scenario design, parameterisation, governance
2. Front Office (Global Markets): Consultation, validation
3. Asset Control (RAV): System implementation, reconciliation

Systems:
1. FMDM: Central parameter repository
2. Vespa: Stress calculation engine
3. Murex GTS: Trading system stress calculation
4. Excel: Golden source (MLRC-approved parameters)

Process Flow:
[Review portfolio] → [Scenario type decision: Pillar vs PoW?] →
  If Pillar: [Parameterise from historic data] → [Document] → [FO Consult] → [MLRC] → [FMDM Upload] → ...
  If PoW: [Top Risk Analysis] → [Determine PoW scenarios] → [Discuss with desk heads] → [Document] → [FO Consult] → [MLRC] → [FMDM Upload] → ...
→ [Reconcile FMDM vs Excel] → [FMDM distributes to Vespa/Murex] → [Calculations]

Critical Controls:
1. FMDM Reconciliation
   - Type: Reconciliation
   - Sequence: AFTER FMDM upload, BEFORE distribution to Vespa/Murex
   - Performer: Asset Control
   - Criteria: FMDM parameters must match Excel golden source exactly
   - If fail: Investigate, correct FMDM, re-reconcile

Timing:
- Scenario design: 2-3 weeks
- FO consultation: 1 week
- Total: ~4-5 weeks (excluding MLRC meeting wait)

Missing Information (Questions):
1. What exactly triggers a PoW stress vs a pillar stress?
2. What happens if Front Office disagrees during consultation?
3. What systems does FMDM send data to besides Vespa and Murex?
4. How long does Asset Control need for FMDM upload and reconciliation?
```

---

## Tips for Effective Extraction

1. **Read the full document first** before extracting - get the big picture
2. **Look for sequence keywords** (before, after, then, next) to establish flow
3. **Disambiguate names**: "Asset Control" = department? Or "Asset Control system" = FMDM?
4. **Probe on critical controls**: Where exactly does reconciliation happen?
5. **Note what's missing**: Prepare clarifying questions
6. **Cross-reference**: If document mentions "Step 3" but you only see 2 steps, ask
7. **Watch for loops**: "iterate until approved" = loop back
8. **Identify sub-processes**: Complex activities that might need separate diagrams
9. **Extract message flows**: Cross-department communications for BPMN
10. **Be skeptical of sequence**: Validate that critical controls happen in the right order

---

## After Extraction

1. **Review extracted information** for completeness
2. **Prepare clarifying questions** for missing information
3. **Recommend diagram format** based on:
   - Number of swim lanes (3+ → BPMN recommended)
   - System interactions (Yes → add DFD)
   - Complexity (High → BPMN with sub-processes)
   - Governance (Formal → BPMN)
4. **Generate diagrams and documentation**
5. **Iterate with user** based on feedback
