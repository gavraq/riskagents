# Policy Updater Skill

**Skill ID**: `policy-updater`
**Version**: 1.0
**Status**: Planned
**Primary Domain**: Cross-Cutting (Governance)
**Taxonomy Layers**: L3 (Policies), with linkages to L1-L7

---

## Overview

The Policy Updater skill automates the annual policy review cycle and regulatory-triggered policy updates. It ensures policies remain aligned with the Risk Taxonomy Framework by systematically checking linkages up (to requirements) and down (to implementation).

## Triggers

Invoke this skill when users say:
- "Update the [X] policy"
- "Annual policy review for [X]"
- "Refresh policy for regulatory changes"
- "What needs to change in [X] policy?"
- "Policy gap analysis"
- "Prepare policy for committee approval"

## Capabilities

### 1. Gap Analysis

Compare current policy against:

| Check | Source | Action |
|-------|--------|--------|
| **L1 Regulatory Changes** | `regulatory-inventory.md`, `regulatory-change-assessor` output | Flag superseded regulations, new requirements |
| **L2 Risk Definitions** | `risk-taxonomy-master.md` | Ensure risk types match current definitions |
| **L4 Process Alignment** | Process documentation in `L4-Processes/` | Verify referenced processes exist and are current |
| **L5 Control Alignment** | Control inventory in `L5-Controls/` | Verify limits and controls referenced are accurate |
| **L6 Model References** | Model registry in `L6-Models/` | Ensure model references are current |
| **L7 System References** | System inventory in `L7-Data-Systems/` | Verify system names and feeds are current |

### 2. Change Identification

For each policy section, identify:

```markdown
## Section Analysis

| Section | Current State | Required Change | Priority | Rationale |
|---------|---------------|-----------------|----------|-----------|
| 1.2 Regulatory Scope | References SS3/19 | Update to SS5/25 | HIGH | SS3/19 superseded Dec 2025 |
| 3.1 VaR Limits | 99% 1-day VaR | No change | - | Still current |
| 4.2 Escalation | Reports to RMC | Add MLRC step | MEDIUM | New committee structure |
```

### 3. Draft Updates

Generate tracked-changes version:

```markdown
## Example Output

**Section 1.2 Regulatory Scope**

~~This policy implements the requirements of PRA SS3/19 (Enhancing banks' and insurers' approaches to managing the financial risks from climate change).~~

This policy implements the requirements of PRA SS5/25 (Climate-related financial risk management), which supersedes SS3/19 effective December 2025.

[CHANGE: Regulatory reference updated - SS3/19 superseded by SS5/25]
```

### 4. Governance Pack Generation

Create approval package containing:

1. **Executive Summary**
   - Number of changes by priority
   - Key regulatory drivers
   - Recommendation

2. **Detailed Change Log**
   - Section-by-section changes
   - Rationale for each
   - Cross-references to taxonomy nodes

3. **Impact Assessment**
   - Processes affected
   - Systems impacted
   - Training requirements
   - Timeline for implementation

4. **Committee Paper**
   - Formatted for approval committee
   - Decision required
   - Appendices with full redline

## Skill Chaining

```
┌─────────────────────────────┐
│ regulatory-risk-researcher  │  ← Identifies new regulations
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ regulatory-change-assessor  │  ← Assesses taxonomy impact
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│     policy-updater          │  ← Updates specific policies
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│     meeting-minutes         │  ← Captures approval decision
└─────────────────────────────┘
```

## Policy Document Requirements

For the skill to work effectively, policies must follow the standard template with:

### Required Metadata Block

```yaml
---
policy_id: MR-L3-001
policy_name: Market Risk Policy
version: 2.1
effective_date: 2025-01-15
next_review_date: 2026-01-15
owner: Chief Risk Officer
approving_committee: RMC
l1_requirements:
  - REQ-L1-001  # CRR
  - REQ-L1-003  # FRTB
  - REQ-L1-004  # SS13/13
l2_risk_types:
  - MR-L2-001   # Market Risk
  - MR-L2-002   # Interest Rate Risk
l4_processes:
  - MR-L4-001   # Daily VaR Production
  - MR-L4-002   # Backtesting
l5_controls:
  - MR-L5-001   # VaR Limits
  - MR-L5-002   # Stress Limits
l6_models:
  - MR-L6-001   # VaR Model
l7_systems:
  - Murex
  - FMDM
---
```

### Section Markers

Each section should include taxonomy linkage comments:

```markdown
## 3. VaR Limit Framework
<!-- L5: MR-L5-001, MR-L5-002 -->
<!-- L1: REQ-L1-003 Art 325bf -->

The Bank maintains VaR limits at the following levels...
```

## Input Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `policy_path` | Yes | Path to policy document |
| `review_type` | No | `annual`, `regulatory`, `ad-hoc` (default: `annual`) |
| `regulatory_changes` | No | List of L1 node IDs with changes |
| `output_format` | No | `summary`, `detailed`, `committee_pack` (default: `detailed`) |

## Output Formats

### Summary Output
- High-level change count
- Key items requiring attention
- Recommended actions

### Detailed Output
- Full gap analysis
- Section-by-section recommendations
- Redlined policy draft

### Committee Pack Output
- Executive summary
- Approval paper
- Full appendices
- Draft board/committee minute

## Example Usage

### Annual Review
```
User: "Run annual review of the Market Risk Policy"

Skill: Reads MR-L3-001, checks all linkages, identifies:
- 3 regulatory reference updates needed
- 1 process reference outdated
- 2 limit values changed
- Generates committee pack for RMC approval
```

### Regulatory-Triggered Update
```
User: "Update Credit Risk Policy for SS5/25 climate requirements"

Skill:
- Loads regulatory-change-assessor output for SS5/25
- Identifies Credit Risk Policy sections impacted
- Drafts new climate risk section
- Flags credit assessment process changes needed
- Generates change summary
```

## Metrics

| Metric | Description |
|--------|-------------|
| Policies reviewed | Count of policies processed |
| Changes identified | Total changes flagged |
| Regulatory gaps | L1 misalignments found |
| Process gaps | L4 misalignments found |
| Time saved | Estimated vs manual review |

## Implementation Notes

### Phase 1 (MVP)
- Gap analysis against L1 regulatory inventory
- Basic change identification
- Summary output format

### Phase 2
- Full taxonomy linkage checking (L1-L7)
- Redline generation
- Committee pack output

### Phase 3
- Integration with document management system
- Automated annual review scheduling
- Approval workflow integration

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `regulatory-risk-researcher` | Upstream - identifies regulatory changes |
| `regulatory-change-assessor` | Upstream - assesses taxonomy impact |
| `meeting-minutes` | Downstream - captures approval |
| `project-planner` | Parallel - plans implementation of changes |
| `process-documenter` | Parallel - updates related processes |

---

*Skill Definition Version: 1.0*
*Created: 2025-12-11*
*Author: Risk Agents Team*
