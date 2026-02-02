# Risk Taxonomy Framework

**Reference Bank**: Meridian Global Bank
**Status**: Phase 1 - Foundation (L1 Complete, L2 Complete)
**Last Updated**: 2025-12-11
**Skills**: 13 (10 existing + 2 regulatory + 1 policy-updater)
**Architecture**: Apache Iceberg Data Lakehouse (adapted from Nordea T&R)
**Data Sources**: ICBCS Bank reference data

---

## Quick Start

The Risk Taxonomy is a hierarchical knowledge structure that serves as the foundation for the Risk Agents platform. It provides:

- **For Humans**: A knowledge management platform for onboarding, cross-training, and regulatory communication
- **For AI Agents**: Efficient context retrieval without loading all documents
- **For Skills**: Coverage mapping showing which capabilities exist across risk domains

---

## Directory Structure

```
risk-taxonomy/
├── README.md                           # This file
├── 00-Risk-Taxonomy-Implementation-Plan.md   # Master implementation plan
├── 01-Taxonomy-Schema.md               # Node structure definition
├── 05-Skills-Mapping-Framework.md      # Skills-to-taxonomy mapping
│
├── L1-Requirements/                    # Regulatory & business drivers
│   └── (coming soon)
│
├── L2-Risk-Types/                      # Risk classification & definitions
│   └── risk-taxonomy-master.md         # ✅ Complete risk type definitions
│
├── L3-Governance/                      # Policies, committees, mandates
│   ├── policies/
│   └── committees/
│
├── L4-Processes/                       # Business processes & procedures
│   └── processes/
│
├── L5-Controls/                        # KRIs, limits, RCSA controls
│
├── L6-Models/                          # Risk models & methodologies
│   └── methodologies/
│
└── L7-Data-Systems/                    # Data, systems, feeds
    ├── systems/
    ├── feeds/
    └── architecture/
```

---

## The Seven-Layer Pyramid

```
                    ┌─────────────────────┐
                    │   L1: REQUIREMENTS  │  ← Regulatory & Business Drivers
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   L2: RISK TYPES    │  ← Risk Classification & Definitions
                    └──────────┬──────────┘
                               │
              ┌────────────────▼────────────────┐
              │       L3: GOVERNANCE            │  ← Policies, Committees, Mandates
              └────────────────┬────────────────┘
                               │
         ┌─────────────────────▼─────────────────────┐
         │           L4: PROCESSES                   │  ← Business Processes
         └─────────────────────┬─────────────────────┘
                               │
    ┌──────────────────────────▼──────────────────────────┐
    │              L5: CONTROLS & METRICS                 │  ← KRIs, Limits, RCSA
    └──────────────────────────┬──────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                  L6: MODELS & METHODOLOGIES                 │  ← Calculations
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                 L7: DATA, SYSTEMS & FEEDS                       │  ← Infrastructure
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Documents

| Document | Purpose | Status |
|----------|---------|--------|
| [Implementation Plan](00-Risk-Taxonomy-Implementation-Plan.md) | Master plan v2.0 with Iceberg architecture | ✅ Complete |
| [Taxonomy Schema](01-Taxonomy-Schema.md) | YAML schema for node definitions | ✅ Complete |
| [Regulatory Inventory](L1-Requirements/regulatory-inventory.md) | 22 regulations mapped to risk domains | ✅ Complete |
| [Requirement-Risk Linkage](L1-Requirements/requirement-to-risk-linkage.md) | L1→L2 traceability | ✅ Complete |
| [Risk Types Master](L2-Risk-Types/risk-taxonomy-master.md) | All 9 risk domains (v2.0 expanded) | ✅ Complete |
| [Skills Mapping](05-Skills-Mapping-Framework.md) | Skills-to-taxonomy mapping | ✅ Complete |

### Key Architecture Documents

| Document | Location | Purpose |
|----------|----------|---------|
| Nordea T&R Executive Summary | `/data/Nordea Bank/Reference Architecture/` | Reference ODS architecture |
| ICBCS Feed Documentation | `/data/ICBCS Bank/Feeds/Feed Documentation/` | Real sensitivity/VaR docs |
| ICBCS Metrics | `/data/ICBCS Bank/metrics/` | Product/metrics definitions |

---

## Current Phase: Foundation

### Completed
- [x] Taxonomy pyramid architecture defined (7 layers)
- [x] Schema for taxonomy nodes (YAML structure)
- [x] **L1 Requirements - Regulatory Inventory** (22 regulations)
- [x] **L1→L2 Requirement-Risk Linkage** (full traceability)
- [x] L2 Risk Types - all 9 domains defined
- [x] Skills mapping framework with gap analysis
- [x] Directory structure created
- [x] **NEW: regulatory-risk-researcher agent** (regulatory monitoring)
- [x] **NEW: regulatory-change-assessor skill** (impact assessment)

### In Progress
- [ ] First vertical slice: Market Risk - VaR Production
- [ ] Reference bank data generation

### Next Up
- [ ] L3 Governance - Market Risk Policy
- [ ] L4 Process - Daily VaR Production (BPMN)
- [ ] L5 Controls - VaR Limits Framework

---

## Risk Domains

| # | Domain | L1 Reqs | L2 Defined | Skills | Coverage |
|---|--------|:-------:|:----------:|:------:|----------|
| 1 | Market Risk | 7 | ✅ | 2 | Partial |
| 2 | Credit Risk | 8 | ✅ | 1 | Low |
| 3 | Operational Risk | 9 | ✅ | 2 | Partial |
| 4 | Liquidity Risk | 5 | ✅ | 0 | None |
| 5 | Model Risk | 5 | ✅ | 0 | None |
| 6 | Sustainability Risk | 3 | ✅ | 1 | Partial |
| 7 | Regulatory Risk | 22 | ✅ | 2 | **NEW** |
| 8 | Strategic Risk | 2 | ✅ | 0 | None |
| 9 | Change Management | 2 | ✅ | 7 | Strong |

---

## Skills Integration

Current skills mapped to taxonomy (12 total):

| Skill | Primary Domain | Layers |
|-------|----------------|--------|
| pillar-stress-generator | Market Risk | L5, L6, L7 |
| stress-scenario-suggester | Market Risk | L2, L5 |
| climate-scorecard-filler | Sustainability | L2, L5 |
| meeting-minutes | Cross-Cutting | L3 |
| project-planner | Change Mgmt | L4, L5 |
| status-reporter | Change Mgmt | L5 |
| stakeholder-analysis | Change Mgmt | L3, L4 |
| itc-template-filler | Change Mgmt | L3, L4 |
| icc-business-case-filler | Change Mgmt | L3, L4, L5 |
| process-documenter | Cross-Cutting | L4 |
| **regulatory-risk-researcher** (NEW) | Regulatory Risk | L1 |
| **regulatory-change-assessor** (NEW) | Regulatory Risk | L1, L3-L7 |

See [Skills Mapping Framework](05-Skills-Mapping-Framework.md) for full analysis.

### Regulatory Intelligence Workflow

```
┌─────────────────────────────────┐
│ regulatory-risk-researcher      │  ← Monitors PRA, FCA, EBA, BCBS
│ (Agent)                         │  ← Identifies new regulations
└───────────────┬─────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│ regulatory-change-assessor      │  ← Assesses taxonomy impact
│ (Skill)                         │  ← Creates gap analysis
└───────────────┬─────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│ project-planner                 │  ← Creates implementation plan
│ (Skill)                         │
└─────────────────────────────────┘
```

---

## Reference Bank

The taxonomy uses a fictional **Meridian Global Bank** as the reference implementation:

- **Type**: Universal bank with trading operations
- **Size**: Mid-tier GSIB (~$75bn assets)
- **Geography**: UK-headquartered, global operations
- **Regulator**: PRA/FCA

Synthetic data will be created in `/data/reference-bank/` for:
- Market data (curves, prices)
- Positions (500 trades)
- Counterparties (100 entities)
- Sample reports

---

## Contributing

To add content to the taxonomy:

1. **Identify the layer** (L1-L7) for your content
2. **Create a node** following the [schema](01-Taxonomy-Schema.md)
3. **Link to parent/children** using node IDs
4. **Map skills** that apply to the node
5. **Add artefacts** (process maps, policies, etc.)

---

## Contact

**Project Owner**: Risk Agents Team
**Repository**: `/Users/gavinslater/projects/riskagent`
