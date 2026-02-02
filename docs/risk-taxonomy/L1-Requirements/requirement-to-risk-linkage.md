# L1 Requirements to L2 Risk Types Linkage

**Reference Bank**: Meridian Global Bank
**Version**: 1.1
**Last Updated**: 2025-12-11
**Change Summary**: Updated SS3/19→SS5/25, added FCA SDR (REQ-L1-023)

---

## 1. Overview

This document establishes the formal linkage between L1 (Regulatory Requirements) and L2 (Risk Types) in the Risk Taxonomy. This linkage is fundamental to the taxonomy because:

1. **Audit Trail**: Demonstrates which regulations drive which risk management activities
2. **Coverage Check**: Ensures no regulatory requirement is orphaned without risk ownership
3. **Impact Analysis**: When regulations change, identifies affected risk domains
4. **Skills Routing**: Helps AI agents understand which risk context to load for regulatory queries

---

## 2. Linkage Matrix

### 2.1 Primary Linkages

Each regulatory requirement (REQ-L1-xxx) links to one or more risk types (xx-L2-xxx):

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     L1 → L2 REQUIREMENT-RISK LINKAGE                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  REQ-L1-001 ──┬──→ MR-L2-001 (Market Risk)                                  │
│  CRR/CRR III  ├──→ CR-L2-001 (Credit Risk)                                  │
│               ├──→ OR-L2-001 (Operational Risk)                             │
│               └──→ LR-L2-001 (Liquidity Risk)                               │
│                                                                             │
│  REQ-L1-003 ────→ MR-L2-001 (Market Risk) [PRIMARY]                         │
│  FRTB          └─→ CR-L2-002 (Counterparty - CVA) [SECONDARY]               │
│                                                                             │
│  REQ-L1-005 ──┬──→ CR-L2-001 (Credit Risk) [PRIMARY]                        │
│  CRR Credit   ├──→ CR-L2-002 (Counterparty Risk)                            │
│               ├──→ CR-L2-006 (Concentration Risk)                           │
│               └──→ CR-L2-007 (Country Risk)                                 │
│                                                                             │
│  REQ-L1-013 ────→ MDR-L2-001 (Model Risk) [PRIMARY]                         │
│  SS1/23        └─→ All risk domains [SECONDARY - model usage]               │
│                                                                             │
│  REQ-L1-015 ──┬──→ SR-L2-001 (Sustainability Risk) [PRIMARY]                │
│  SS5/25       ├──→ CR-L2-001 (Credit - climate overlay)                     │
│  Climate      ├──→ MR-L2-001 (Market - climate scenarios)                   │
│  (replaces    ├──→ OR-L2-001 (Operational - climate ops resilience)         │
│   SS3/19)     └──→ LR-L2-001 (Liquidity - climate stress)                   │
│                                                                             │
│  REQ-L1-023 ──┬──→ SR-L2-001 (Sustainability Risk) [PRIMARY]                │
│  FCA SDR      ├──→ OR-L2-001 (Operational - product governance)             │
│  (NEW)        └──→ RR-L2-001 (Regulatory Risk)                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Complete Linkage Table

| Requirement ID | Regulation | Primary Risk Type(s) | Secondary Risk Type(s) |
|---------------|------------|---------------------|----------------------|
| REQ-L1-001 | CRR/CRR III | MR-L2-001, CR-L2-001, OR-L2-001 | LR-L2-001, STR-L2-002 |
| REQ-L1-002 | CRD VI | All L2 risk types | - |
| REQ-L1-003 | FRTB | MR-L2-001 | CR-L2-002 (CVA) |
| REQ-L1-004 | SS13/13 Market Risk | MR-L2-001 | MDR-L2-001 |
| REQ-L1-005 | CRR Credit | CR-L2-001, CR-L2-002 | CR-L2-006, CR-L2-007 |
| REQ-L1-006 | IFRS 9 | CR-L2-001 | MDR-L2-001 |
| REQ-L1-007 | Large Exposures | CR-L2-006 | CR-L2-001 |
| REQ-L1-008 | SMA Op Risk | OR-L2-001 | - |
| REQ-L1-009 | SS1/21 Op Res | OR-L2-001 | LR-L2-001 |
| REQ-L1-010 | SS2/21 Outsourcing | OR-L2-001 | - |
| REQ-L1-011 | LCR | LR-L2-001, LR-L2-002 | - |
| REQ-L1-012 | NSFR | LR-L2-001, LR-L2-002 | - |
| REQ-L1-013 | SS1/23 MRM | MDR-L2-001 | All (via model usage) |
| REQ-L1-014 | SR 11-7 | MDR-L2-001 | All (via model usage) |
| REQ-L1-015 | **SS5/25 Climate** (replaces SS3/19) | SR-L2-001, SR-L2-002 | CR-L2-001, MR-L2-001, OR-L2-001, LR-L2-001 |
| REQ-L1-016 | TCFD | SR-L2-001 | All (disclosure) |
| REQ-L1-023 | **FCA SDR** (NEW) | SR-L2-001 | OR-L2-001, RR-L2-001 |
| REQ-L1-017 | MiFID II | MR-L2-001, OR-L2-001 | - |
| REQ-L1-018 | MAR | MR-L2-001, OR-L2-001 | - |
| REQ-L1-019 | MLR | OR-L2-001 (Financial Crime) | CR-L2-001 |
| REQ-L1-020 | Sanctions | OR-L2-001 (Financial Crime) | CR-L2-001 |
| REQ-L1-021 | BRRD II | All | - |
| REQ-L1-022 | BCBS 239 | All (data governance) | - |

---

## 3. Risk Type to Requirement Reverse Lookup

### 3.1 Market Risk (MR-L2-001)

| Requirement | Description | Materiality |
|-------------|-------------|-------------|
| REQ-L1-001 | CRR - Market Risk Capital | CRITICAL |
| REQ-L1-003 | FRTB | CRITICAL |
| REQ-L1-004 | SS13/13 Market Risk | HIGH |
| REQ-L1-017 | MiFID II - Best Execution | HIGH |
| REQ-L1-018 | MAR - Market Abuse | HIGH |
| REQ-L1-015 | SS3/19 - Climate Scenarios | MEDIUM |
| REQ-L1-022 | BCBS 239 - Data | HIGH |

**Total Requirements**: 7 primary, multiple secondary

---

### 3.2 Credit Risk (CR-L2-001)

| Requirement | Description | Materiality |
|-------------|-------------|-------------|
| REQ-L1-001 | CRR - Credit Risk Capital | CRITICAL |
| REQ-L1-005 | CRR Part 3 - Credit Risk | CRITICAL |
| REQ-L1-006 | IFRS 9 - ECL | CRITICAL |
| REQ-L1-007 | Large Exposures | HIGH |
| REQ-L1-015 | SS3/19 - Climate Overlay | MEDIUM |
| REQ-L1-019 | MLR - CDD | HIGH |
| REQ-L1-020 | Sanctions - Screening | HIGH |
| REQ-L1-022 | BCBS 239 - Data | HIGH |

**Total Requirements**: 8 primary, multiple secondary

---

### 3.3 Operational Risk (OR-L2-001)

| Requirement | Description | Materiality |
|-------------|-------------|-------------|
| REQ-L1-001 | CRR - Op Risk Capital | CRITICAL |
| REQ-L1-008 | SMA | CRITICAL |
| REQ-L1-009 | SS1/21 Operational Resilience | CRITICAL |
| REQ-L1-010 | SS2/21 Outsourcing | HIGH |
| REQ-L1-017 | MiFID II - Conduct | HIGH |
| REQ-L1-018 | MAR - Surveillance | HIGH |
| REQ-L1-019 | MLR - AML Controls | CRITICAL |
| REQ-L1-020 | Sanctions - Compliance | CRITICAL |
| REQ-L1-022 | BCBS 239 - Data | HIGH |

**Total Requirements**: 9 primary

---

### 3.4 Liquidity Risk (LR-L2-001)

| Requirement | Description | Materiality |
|-------------|-------------|-------------|
| REQ-L1-001 | CRR - Liquidity | CRITICAL |
| REQ-L1-011 | LCR | CRITICAL |
| REQ-L1-012 | NSFR | CRITICAL |
| REQ-L1-009 | SS1/21 - Payment Continuity | HIGH |
| REQ-L1-022 | BCBS 239 - Data | HIGH |

**Total Requirements**: 5 primary

---

### 3.5 Model Risk (MDR-L2-001)

| Requirement | Description | Materiality |
|-------------|-------------|-------------|
| REQ-L1-013 | SS1/23 MRM | CRITICAL |
| REQ-L1-014 | SR 11-7 | HIGH |
| REQ-L1-004 | SS13/13 - VaR Models | HIGH |
| REQ-L1-006 | IFRS 9 - ECL Models | HIGH |
| REQ-L1-003 | FRTB - IMA Models | HIGH |

**Total Requirements**: 5 primary

---

### 3.6 Sustainability Risk (SR-L2-001)

| Requirement | Description | Materiality |
|-------------|-------------|-------------|
| REQ-L1-015 | **SS5/25 Climate** (replaces SS3/19) | **CRITICAL** |
| REQ-L1-023 | **FCA SDR** (NEW) | HIGH |
| REQ-L1-016 | TCFD | HIGH |
| REQ-L1-001 | CRR - ESG Considerations | MEDIUM |

**Total Requirements**: 4 primary

**Note on SS5/25**: Published 3 December 2025, supersedes SS3/19 entirely. Key deadline: **3 June 2026** for board-approved action plan. See REQ-L1-015 in regulatory-inventory.md for full requirements.

---

### 3.7 Regulatory Risk (RR-L2-001)

| Requirement | Description | Materiality |
|-------------|-------------|-------------|
| All REQ-L1-xxx | All regulations | CRITICAL |

**Note**: Regulatory Risk is unique in that ALL L1 requirements feed into it. The regulatory-risk-researcher agent and regulatory-change-assessor skill operate at this level.

---

## 4. Cross-Cutting Requirements

Some requirements affect multiple risk types simultaneously:

### 4.1 CRR/CRR III (REQ-L1-001)

```
REQ-L1-001: CRR/CRR III
│
├─→ MR-L2-001: Market Risk
│   └── Part 3 Title III: Trading book capital
│
├─→ CR-L2-001: Credit Risk
│   └── Part 3 Title I-II: Credit risk capital
│
├─→ OR-L2-001: Operational Risk
│   └── Part 3 Title IV: Op risk capital
│
├─→ LR-L2-001: Liquidity Risk
│   └── Part 6: Liquidity requirements
│
└─→ STR-L2-002: Business Risk (via capital buffers)
    └── Part 2: Own funds requirements
```

### 4.2 SS1/23 Model Risk (REQ-L1-013)

```
REQ-L1-013: SS1/23 Model Risk Management
│
├─→ MDR-L2-001: Model Risk [PRIMARY]
│   └── MRM framework, inventory, validation
│
├─→ MR-L2-001: Market Risk [SECONDARY]
│   └── VaR, SVaR, ES models
│
├─→ CR-L2-001: Credit Risk [SECONDARY]
│   └── PD, LGD, EAD, ECL models
│
├─→ LR-L2-001: Liquidity Risk [SECONDARY]
│   └── LCR, NSFR models
│
└─→ OR-L2-001: Operational Risk [SECONDARY]
    └── SMA, scenario models
```

### 4.3 BCBS 239 (REQ-L1-022)

```
REQ-L1-022: BCBS 239 Risk Data Aggregation
│
├─→ ALL Risk Types [DATA GOVERNANCE]
│   └── Data quality, timeliness, accuracy
│
├─→ L7 Data & Systems [IMPLEMENTATION]
│   └── Data architecture, lineage, controls
│
└─→ L5 Controls [MEASUREMENT]
    └── DQ metrics, reporting controls
```

---

## 5. Linkage Maintenance

### 5.1 When to Update Linkages

| Trigger | Action |
|---------|--------|
| New regulation added to L1 | Map to all affected L2 risk types |
| Regulation amended | Review and update affected linkages |
| New risk type added to L2 | Back-map to all applicable L1 requirements |
| Regulation repealed | Mark linkages as deprecated (maintain for audit) |

### 5.2 Validation Rules

1. **No orphan requirements**: Every REQ-L1-xxx must link to at least one L2 risk type
2. **No orphan risk types**: Every xx-L2-xxx must link to at least one L1 requirement
3. **Primary designation**: Each linkage must specify if primary or secondary
4. **Materiality assessment**: Each linkage should have materiality (Critical/High/Medium/Low)

### 5.3 Quality Checks

Run periodically:
- [ ] All L1 nodes have at least one L2 linkage
- [ ] All L2 nodes have at least one L1 linkage
- [ ] No circular references
- [ ] Materiality assessments are current
- [ ] Deprecated linkages are flagged

---

## 6. Skills Integration

### 6.1 How Skills Use Linkages

| Skill | How It Uses L1→L2 Linkage |
|-------|---------------------------|
| `regulatory-risk-researcher` | When identifying new regulations, determines affected risk domains |
| `regulatory-change-assessor` | When assessing impact, follows linkages to identify all affected L2 types |
| `pillar-stress-generator` | Loads regulatory context from linked L1 nodes for stress scenarios |
| `stress-scenario-suggester` | Uses linkages to identify which risk domains need scenario coverage |

### 6.2 Query Routing Example

```
User Query: "What are the model risk implications of FRTB?"
                │
                ▼
Step 1: Identify regulation → REQ-L1-003 (FRTB)
                │
                ▼
Step 2: Follow linkages → MR-L2-001 (primary), CR-L2-002 (secondary)
                │
                ▼
Step 3: Identify model risk intersection → MDR-L2-001
                │
                ▼
Step 4: Load context from:
        - REQ-L1-003 (FRTB requirements)
        - REQ-L1-013 (SS1/23 MRM)
        - MR-L2-001 (Market Risk definition)
        - MDR-L2-001 (Model Risk definition)
                │
                ▼
Step 5: Generate response with full regulatory and risk context
```

---

## 7. Document Control

| Attribute | Value |
|-----------|-------|
| **Owner** | Risk Taxonomy Team |
| **Review Cycle** | Quarterly |
| **Last Review** | 2025-12-11 |
| **Next Review** | 2026-03-11 |

---

## Appendix A: Node ID Reference

### L1 Requirement Nodes

| Node ID | Regulation | Status |
|---------|------------|--------|
| REQ-L1-001 | CRR/CRR III | Active |
| REQ-L1-002 | CRD VI | Active |
| REQ-L1-003 | FRTB | Active |
| REQ-L1-004 | SS13/13 Market Risk | Active |
| REQ-L1-005 | CRR Credit | Active |
| REQ-L1-006 | IFRS 9 | Active |
| REQ-L1-007 | Large Exposures | Active |
| REQ-L1-008 | SMA Op Risk | Active |
| REQ-L1-009 | SS1/21 Op Res | Active |
| REQ-L1-010 | SS2/21 Outsourcing | Active |
| REQ-L1-011 | LCR | Active |
| REQ-L1-012 | NSFR | Active |
| REQ-L1-013 | SS1/23 MRM | Active |
| REQ-L1-014 | SR 11-7 | Active |
| REQ-L1-015 | **SS5/25 Climate** (replaces SS3/19) | **NEW** |
| REQ-L1-016 | TCFD | Active |
| REQ-L1-017 | MiFID II | Active |
| REQ-L1-018 | MAR | Active |
| REQ-L1-019 | MLR | Active |
| REQ-L1-020 | Sanctions | Active |
| REQ-L1-021 | BRRD II | Active |
| REQ-L1-022 | BCBS 239 | Active |
| REQ-L1-023 | **FCA SDR** | **NEW** |

### L2 Risk Type Nodes

| Node ID | Risk Type |
|---------|-----------|
| MR-L2-001 | Market Risk |
| CR-L2-001 | Credit Risk |
| CR-L2-002 | Counterparty Risk |
| CR-L2-006 | Concentration Risk |
| CR-L2-007 | Country Risk |
| OR-L2-001 | Operational Risk |
| LR-L2-001 | Liquidity Risk |
| LR-L2-002 | Funding Liquidity Risk |
| MDR-L2-001 | Model Risk |
| SR-L2-001 | Sustainability Risk |
| SR-L2-002 | Environmental Risk |
| RR-L2-001 | Regulatory Risk |
| STR-L2-001 | Strategic Risk |
| STR-L2-002 | Business Risk |
| CM-L2-001 | Change Risk |

---

*This document is the property of Meridian Global Bank and is intended for internal use only.*
