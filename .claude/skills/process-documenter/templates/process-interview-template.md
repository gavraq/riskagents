# Process Documentation Interview Template

Use this template to gather information for comprehensive process documentation through Q&A with the user.

## Section 1: Process Overview

### 1.1 Basic Information
**Q**: What is the name of this process?
**Q**: What business area does this belong to? (e.g., Market Risk, Credit Risk, Operations)
**Q**: What triggers this process? (e.g., monthly cycle, ad-hoc request, regulatory requirement)
**Q**: What is the primary purpose/objective of this process?

### 1.2 Scope & Context
**Q**: Is this a:
- [ ] Operational process (day-to-day activities)
- [ ] Governance process (approvals, committees)
- [ ] System process (automated/technical)
- [ ] Cross-functional process (multiple departments)

**Q**: How often does this process run?
- [ ] Daily
- [ ] Weekly
- [ ] Monthly
- [ ] Quarterly
- [ ] Annually
- [ ] Ad-hoc/Event-driven

**Q**: What regulatory or policy requirements apply to this process? (if any)

---

## Section 2: Participants & Swim Lanes

### 2.1 Departments/Roles Involved
**Q**: Which departments or roles are involved in this process?
(List all, as each may become a swim lane)

Examples:
- Market Risk
- Front Office (Trading)
- Asset Control / RAV
- Compliance
- IT / Systems
- Finance

**For each department, ask:**
- What are their key responsibilities in this process?
- Do they make decisions, execute tasks, or provide input?

### 2.2 Systems Involved
**Q**: What systems are involved in this process?
(Important: Distinguish between departments and systems)

Examples:
- FMDM (system), not "Asset Control" (department)
- Murex GTS
- Vespa
- Excel (Golden Source)
- SharePoint
- Email

**For each system, ask:**
- What role does it play? (storage, calculation, approval, distribution)
- What data does it receive/send?

---

## Section 3: Process Flow

### 3.1 Major Steps
**Q**: What are the major steps in this process, from start to finish?
(List in order, we'll add detail later)

Example:
1. Review business mix and portfolio
2. Select appropriate stress scenarios
3. Parameterise scenarios
4. Consult with Front Office
5. Submit to MLRC
6. Upload to FMDM
7. Execute stress calculations

### 3.2 Decision Points
**Q**: Are there any decision points where the process branches?

For each decision point, ask:
- What is the question being asked? (e.g., "Core scenario?" "Reconciliation OK?")
- What are the possible outcomes? (e.g., Yes/No, Pass/Fail, Pillar/PoW)
- What happens in each branch?

### 3.3 Parallel Activities
**Q**: Are there any steps that happen in parallel (at the same time)?

Example:
- While Market Risk parameterises scenarios, Front Office reviews portfolio positions
- Top Risk Analysis happens alongside Core scenario parameterisation

### 3.4 Loops & Iterations
**Q**: Are there any steps that repeat or loop back?

Examples:
- If Front Office disagrees, iterate on parameterisation
- If reconciliation fails, correct FMDM and re-reconcile

---

## Section 4: Critical Controls & Quality Gates

### 4.1 Approval Gates
**Q**: What are the formal approval points in this process?

Examples:
- MLRC approval of parameterisation
- Front Office agreement on scenarios
- Asset Control sign-off on reconciliation

**For each approval, ask:**
- Who approves?
- What happens if approval is denied?
- Is this a hard gate (process stops) or soft gate (escalation)?

### 4.2 Reconciliation & Validation
**Q**: Are there any reconciliation or validation steps?
**CRITICAL**: Where exactly do they occur in the sequence?

Examples:
- Reconcile FMDM vs Excel golden source
- Validate parameter completeness
- Cross-check calculations

**For each reconciliation, ask:**
- What is being compared?
- What is the "golden source" or authoritative source?
- What happens if reconciliation fails?
- **Does this happen BEFORE or AFTER subsequent steps?** (sequence is critical!)

### 4.3 Quality Checks
**Q**: What quality checks or control points exist?

Examples:
- Parameter magnitude limits
- Correlation consistency checks
- Historical calibration validation

---

## Section 5: Data & Information Flow

### 5.1 Inputs
**Q**: What are the inputs to this process?

For each input, ask:
- What is it? (document, data, request)
- Where does it come from?
- In what format? (Excel, Word, email, system data)
- Who provides it?

Examples:
- Portfolio composition data (from trading systems)
- Historical crisis data (from market data vendors)
- Regulatory scenario guidance (from PRA)
- Excel parameter template (from previous MLRC)

### 5.2 Outputs
**Q**: What are the outputs of this process?

For each output, ask:
- What is it?
- Who receives it?
- In what format?
- What happens with it next?

Examples:
- MLRC paper (Word document, to Risk Committee)
- Excel parameter file (golden source, to Asset Control)
- FMDM upload (system, to calculation engines)
- Monthly stress reports (Excel/PDF, to senior management)

### 5.3 Data Transformations
**Q**: How does data change as it flows through the process?

Example:
- Economic narrative → Parameter shocks → System-ready format → Calculation results

---

## Section 6: Timing & Duration

### 6.1 Process Duration
**Q**: How long does this process typically take, end-to-end?

**Q**: What are the typical durations for each major phase?

Examples:
- Scenario design: 2-3 weeks
- Front Office consultation: 1 week
- MLRC approval: 1 meeting cycle (monthly)
- System implementation: 1-2 weeks

### 6.2 Deadlines & SLAs
**Q**: Are there any deadlines or service level agreements?

Examples:
- Must be completed before month-end
- Regulatory deadline (e.g., annual stress review by Q1)
- Internal SLA (respond within 2 business days)

---

## Section 7: Sub-Processes & Collapsed Activities

### 7.1 Complex Activities
**Q**: Are there any steps that are themselves complex processes?
(These can be modeled as sub-processes or collapsed activities in BPMN)

Examples:
- "Top Risk Analysis" might be a sub-process with its own steps:
  1. Analyze portfolio exposures
  2. Identify concentration risks
  3. Assess illiquidity
  4. Rank risks by severity
  5. Select top 3-5 risks for PoW stress

**For each sub-process, ask:**
- Do you want to show the detailed steps, or collapse it as a single box?
- If collapsed, should we create a separate diagram for the sub-process?

---

## Section 8: Message Flows (Cross-Department Communication)

### 8.1 Information Exchange
**Q**: How do departments communicate during this process?

Examples:
- Market Risk sends parameters to Front Office (for consultation)
- Front Office sends feedback back to Market Risk (if they disagree)
- Market Risk sends approved parameters to Asset Control (for FMDM upload)

**For each message flow, ask:**
- Who sends?
- Who receives?
- What is sent? (document, approval, data, notification)
- Is there a response expected?

---

## Section 9: Exceptions & Edge Cases

### 9.1 Error Handling
**Q**: What happens when something goes wrong?

Examples:
- Reconciliation fails → Investigate discrepancies → Correct FMDM → Re-reconcile
- MLRC defers approval → Market Risk revises → Re-submit next month
- System error in Vespa → Asset Control investigates → Re-run calculation

### 9.2 Escalation Paths
**Q**: When does escalation occur, and to whom?

Examples:
- If Front Office and Market Risk cannot agree → Escalate to CRO
- If reconciliation fails repeatedly → Escalate to Head of Asset Control

---

## Section 10: Documentation & Artifacts

### 10.1 Process Documents
**Q**: What documents are created during this process?

Examples:
- Scenario narrative (Word)
- Parameter tables (Excel golden source)
- MLRC paper (Word)
- Consultation email to desks
- Meeting minutes from Front Office discussion

### 10.2 Governance Records
**Q**: What needs to be retained for audit/compliance?

Examples:
- MLRC approval minutes
- Excel golden source (signed off version)
- Reconciliation report
- Annual review memo

---

## Section 11: Improvement Opportunities

### 11.1 Pain Points
**Q**: What are the current challenges or pain points in this process?

Examples:
- Manual Excel → FMDM upload (error-prone)
- Lengthy Front Office consultation (delays MLRC submission)
- Reconciliation done manually (time-consuming)

### 11.2 Automation Potential
**Q**: What steps could be automated or improved?

Examples:
- Automated Excel → FMDM upload with validation
- Collaborative platform for Front Office feedback
- Automated reconciliation with alerts for mismatches

---

## Section 12: Diagram Preferences

### 12.1 Format Selection
**Q**: Do you have a preference for diagram format?
- [ ] BPMN 2.0 (industry standard, horizontal swim lanes, good for governance)
- [ ] Mermaid (Git-friendly, renders in markdown)
- [ ] PlantUML (technical, vertical swim lanes)
- [ ] Data Flow Diagram (for system interactions)
- [ ] Multiple formats (I'll recommend based on process characteristics)

### 12.2 Level of Detail
**Q**: How detailed should the diagram be?
- [ ] High-level (major steps only, 5-10 boxes)
- [ ] Medium (show key decision points and sub-processes, 10-20 boxes)
- [ ] Detailed (show all steps, validations, error handling, 20+ boxes)

---

## After Interview: Next Steps

1. **Analysis**: Analyze answers to determine:
   - Number of swim lanes
   - Process complexity (sequential/parallel/loops)
   - System interactions (need DFD?)
   - Governance formality (BPMN recommended?)

2. **Format Recommendation**: Recommend diagram format(s) with rationale

3. **Generation**: Create diagram(s) and documentation

4. **Review**: User reviews and provides feedback

5. **Iteration**: Refine based on feedback (e.g., "reconciliation should happen earlier")

---

## Template Usage Notes

- Not all questions are relevant for every process - skip sections that don't apply
- Ask follow-up questions based on user responses
- Clarify ambiguities (e.g., "Is Asset Control a department or a system?" → "Department. System is FMDM.")
- Probe on sequence ordering for critical controls (reconciliation, approvals)
- If user provides a document, extract as much as possible and ask only clarifying questions
