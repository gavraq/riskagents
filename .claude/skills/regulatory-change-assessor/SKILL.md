---
name: regulatory-change-assessor
description: Assesses the impact of new or changed regulations on the Risk Taxonomy framework. Use when user asks to "assess regulatory impact", "what needs to change for [regulation]", "taxonomy impact of [regulation]", "regulatory gap analysis", or "implementation requirements for [regulation]". (project)
---

# Regulatory Change Assessor

## Purpose

This skill takes a new or amended regulation and systematically assesses its impact across all layers of the Risk Taxonomy. It produces:

1. **Gap Analysis**: What's missing or needs updating in current framework
2. **Artefact Impact Matrix**: Which specific documents/artefacts need changes
3. **Implementation Roadmap**: Sequenced actions to achieve compliance
4. **Resource Estimate**: High-level effort and dependencies

---

## When to Use This Skill

**ALWAYS USE THIS SKILL** (do not write custom assessment scripts) when:

- User asks to "assess regulatory impact"
- User asks "what needs to change for [regulation]?"
- User mentions "gap analysis for [regulation]"
- User asks about "implementation requirements"
- User wants to know "what artefacts need updating"
- Following a `regulatory-risk-researcher` output
- Planning a regulatory change project

---

## Input Requirements

This skill requires:

1. **Regulation Details** (required):
   - Regulation name/reference
   - Key requirements (summary or full text)
   - Effective date
   - Scope (which risk domains affected)

2. **Taxonomy Reference** (auto-loaded):
   - Current L1-L7 taxonomy structure from `/docs/risk-taxonomy/`
   - Existing regulatory inventory
   - Current skills mapping

3. **Context** (helpful):
   - Current implementation status
   - Known gaps already identified
   - Resource constraints

---

## Assessment Framework

### Step 1: Requirement Decomposition

Break down the regulation into atomic requirements:

```markdown
| Req ID | Requirement | Category | Mandatory | Timeline |
|--------|-------------|----------|-----------|----------|
| R001 | [Specific requirement] | [Governance/Process/Control/Data] | Yes/No | [Date] |
| R002 | ... | ... | ... | ... |
```

### Step 2: Taxonomy Layer Impact Analysis

For each requirement, assess impact on each taxonomy layer:

```markdown
## Layer Impact Assessment

### L1: Requirements
- [ ] New REQ-L1-xxx node needed: [Yes/No]
- [ ] Existing node update: [Node ID if applicable]
- [ ] Cross-reference needed: [Related nodes]

### L2: Risk Types
- [ ] Risk type definitions affected: [List]
- [ ] New sub-types needed: [List]
- [ ] Materiality reassessment: [Yes/No]

### L3: Governance
- [ ] Policy updates required: [List policies]
- [ ] New policies needed: [List]
- [ ] Committee TOR changes: [List committees]
- [ ] Governance gap: [Description]

### L4: Processes
- [ ] Process changes required: [List processes]
- [ ] New processes needed: [List]
- [ ] BPMN updates required: [Yes/No]
- [ ] Process gap: [Description]

### L5: Controls & Metrics
- [ ] New controls required: [List]
- [ ] Existing controls to modify: [List]
- [ ] New KRIs needed: [List]
- [ ] Limit framework changes: [Description]
- [ ] RCSA update required: [Yes/No]

### L6: Models
- [ ] New models required: [List]
- [ ] Model enhancements needed: [List]
- [ ] Methodology updates: [List]
- [ ] Validation required: [Yes/No]

### L7: Data & Systems
- [ ] New data requirements: [List]
- [ ] Data dictionary updates: [List]
- [ ] System changes: [List]
- [ ] Feed changes: [List]
- [ ] Architecture impact: [Description]
```

### Step 3: Artefact Impact Matrix

Specific artefacts requiring change:

```markdown
## Artefact Impact Matrix

| Artefact | Location | Change Type | Priority | Owner | Effort |
|----------|----------|-------------|----------|-------|--------|
| [Name] | [Path] | New/Update/Retire | High/Med/Low | [Team] | [Days] |
```

Change Types:
- **New**: Artefact doesn't exist, must be created
- **Update**: Artefact exists but requires modification
- **Retire**: Artefact superseded by new requirement
- **Review**: Artefact may need update - review required

### Step 4: Gap Analysis Summary

```markdown
## Gap Analysis Summary

### Critical Gaps (Must address for compliance)
1. [Gap description] - Impacted requirements: R001, R002
2. [Gap description] - Impacted requirements: R003

### High Priority Gaps (Significant risk if not addressed)
1. [Gap description]
2. [Gap description]

### Medium Priority Gaps (Best practice, not strictly required)
1. [Gap description]

### Low Priority Gaps (Nice to have)
1. [Gap description]
```

### Step 5: Implementation Roadmap

```markdown
## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-4)
| Activity | Deliverable | Dependencies | Owner |
|----------|-------------|--------------|-------|
| [Activity] | [Deliverable] | [Deps] | [Owner] |

### Phase 2: Core Implementation (Weeks 5-12)
| Activity | Deliverable | Dependencies | Owner |
|----------|-------------|--------------|-------|

### Phase 3: Testing & Validation (Weeks 13-16)
| Activity | Deliverable | Dependencies | Owner |
|----------|-------------|--------------|-------|

### Phase 4: Go-Live & Embedding (Weeks 17-20)
| Activity | Deliverable | Dependencies | Owner |
|----------|-------------|--------------|-------|
```

### Step 6: Skills Integration

```markdown
## Skills to Support Implementation

| Implementation Activity | Applicable Skill | How It Helps |
|------------------------|------------------|--------------|
| [Activity] | [Skill name] | [Description] |
```

---

## Output Format

The complete assessment should be structured as:

```markdown
# Regulatory Change Impact Assessment

**Regulation**: [Name and reference]
**Assessment Date**: [Date]
**Assessor**: Risk Agents - regulatory-change-assessor
**Status**: [Draft/Final]

---

## Executive Summary

[2-3 paragraph overview of:
- What the regulation requires
- Scale of impact on taxonomy
- Key implementation challenges
- Recommended approach]

---

## 1. Regulation Overview

### 1.1 Key Requirements
[Summary table of requirements]

### 1.2 Effective Dates
[Timeline of implementation milestones]

### 1.3 Scope
[Which parts of the business/risk framework affected]

---

## 2. Taxonomy Impact Assessment

### 2.1 Layer-by-Layer Analysis
[Detailed L1-L7 impact]

### 2.2 Cross-Cutting Impacts
[Impacts spanning multiple layers]

---

## 3. Gap Analysis

### 3.1 Gap Summary
[Prioritized list of gaps]

### 3.2 Gap Details
[Detailed description of each significant gap]

---

## 4. Artefact Impact Matrix

[Full matrix of artefacts requiring change]

---

## 5. Implementation Roadmap

### 5.1 Phased Approach
[Phase breakdown with activities]

### 5.2 Resource Requirements
[Estimated effort and skills needed]

### 5.3 Dependencies & Risks
[Key dependencies and risks]

---

## 6. Skills Integration

[How Risk Agent skills can support implementation]

---

## 7. Recommended Next Steps

1. [Specific action with owner and date]
2. [Specific action with owner and date]
3. [Specific action with owner and date]

---

## Appendices

### A. Requirement Traceability Matrix
### B. Detailed Artefact Specifications
### C. Supporting Analysis
```

---

## Integration with Other Skills/Agents

### Inputs From
- `regulatory-risk-researcher` agent: Provides regulation details
- User: Direct regulation input

### Outputs To
- `project-planner` skill: Creates detailed project plan from roadmap
- `process-documenter` skill: Documents new/changed processes
- `itc-template-filler` / `icc-business-case-filler`: Governance documentation
- `status-reporter` skill: Tracks implementation progress

### Workflow Integration

```
regulatory-risk-researcher
        │
        │ New regulation identified
        ▼
regulatory-change-assessor (this skill)
        │
        │ Impact assessment complete
        ▼
project-planner
        │
        │ Implementation project created
        ▼
[Implementation Skills]
        │
        │ project-planner, status-reporter,
        │ process-documenter, etc.
        ▼
status-reporter
        │
        │ Track to completion
        ▼
Compliance Achieved
```

---

## Example Usage

### Example 1: FRTB Assessment

**User Input**: "Assess the impact of FRTB implementation on our risk taxonomy"

**Skill Actions**:
1. Load FRTB requirements from REQ-L1-003
2. Decompose into specific requirements (SbM, DRC, RRAO, IMA, PLA, Backtesting)
3. Assess L1-L7 impact for each requirement
4. Identify gaps in current framework
5. Create artefact impact matrix
6. Propose implementation roadmap

---

### Example 2: New Regulation (SS1/23 Model Risk)

**User Input**: "We need to comply with SS1/23 by May 2025. What needs to change?"

**Skill Actions**:
1. Parse SS1/23 principles and expectations
2. Map to current Model Risk framework
3. Identify gaps in model inventory, validation, governance
4. Assess L3 policy changes needed
5. Identify L4 process changes
6. Flag L6 methodology updates
7. Create prioritized implementation plan

---

## Quality Checks

Before finalizing assessment:

1. ✅ All regulation requirements traced to taxonomy impacts
2. ✅ Every gap has a proposed resolution
3. ✅ Artefact owners identified (or flagged as TBD)
4. ✅ Timeline aligned with regulatory deadline
5. ✅ Dependencies clearly stated
6. ✅ Skills integration identified
7. ✅ Executive summary accurately reflects detail

---

## Error Handling

| Scenario | Response |
|----------|----------|
| Regulation not in inventory | Create provisional REQ-L1-xxx node |
| Taxonomy incomplete | Note gaps, proceed with available layers |
| Ambiguous requirement | Flag for human interpretation |
| Timeline impossible | Flag risk, propose phased approach |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-11 | Initial specification |

---

*This skill is part of the Risk Agents regulatory intelligence capability.*
