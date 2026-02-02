---
# Process Metadata
process_id: MR-L4-013
process_name: Market Risk Limits Management
version: 1.1
effective_date: 2025-01-16
next_review_date: 2026-01-16
owner: Head of Market Risk
approving_committee: MLRC

# Taxonomy Linkages
parent_process: MR-L4-001  # Market Risk Process Orchestration
l1_requirements:
  - REQ-L1-001  # CRR
  - REQ-L1-003  # FRTB
l2_risk_types:
  - MR-L2-001   # Market Risk
l3_governance:
  - MR-L3-001   # Market Risk Policy
  - MR-L3-002   # MLRC Terms of Reference
  - MR-L3-003   # VaR Limit Framework
l5_controls:
  - MR-L5-001   # VaR Limits
  - MR-L5-002   # Stress Limits
  - MR-L5-003   # Sensitivity Limits
  - MR-L5-005   # Concentration Limits
  - MR-L5-006   # Stop-Loss Limits
l7_systems:
  - SYS-MR-003  # Risk Engine
  - SYS-MR-004  # Risk Reporting DataMart
  - SYS-MR-008  # Risk ODS
---

# Market Risk Limits Management Process

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Process ID** | MR-L4-013 |
| **Version** | 1.1 |
| **Effective Date** | 16 January 2025 |
| **Parent Process** | Market Risk Process Orchestration (MR-L4-001) |
| **Owner** | Head of Market Risk |

---

## 1. Purpose

The Market Risk Limits Management process governs the **full lifecycle** of market risk limits, from initial setup through daily monitoring and breach management. This process ensures that:

1. **Limits are Established** - Set appropriately to reflect risk appetite and business needs
2. **Limits are Maintained** - Amended through proper governance when required
3. **Limits are Monitored** - Utilisation tracked daily across all hierarchy levels
4. **Breaches are Managed** - Escalated and resolved per the defined framework

This process covers all limit types across the three Risk Engine calculation streams:
- **VaR/SVaR Limits** (from Stream 2)
- **Stress Loss Limits** (from Stream 3)
- **Sensitivity Limits** (from Stream 1)
- **Concentration Limits** (from all streams)
- **Stop-Loss Limits** (from P&L tracking)

---

## 2. Scope

### 2.1 Limit Types

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     MARKET RISK LIMIT TYPES                                             │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐│
│  │                         VaR / SVaR LIMITS (MR-L5-001)                               ││
│  │                                                                                     ││
│  │  • Daily VaR (99%, 1-day)                                                           ││
│  │  • 10-day VaR (99%, 10-day)                                                         ││
│  │  • Stressed VaR (99%, 1-day, stressed period)                                       ││
│  │                                                                                     ││
│  │  Hierarchy: Enterprise → Entity → Division → Business → Desk → Book                 ││
│  │  Source: Risk Engine Stream 2                                                       ││
│  │  Monitoring: Daily                                                                  ││
│  └─────────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐│
│  │                         STRESS LOSS LIMITS (MR-L5-002)                              ││
│  │                                                                                     ││
│  │  • Pillar Scenario Limits (Global Financial Crisis, COVID, Rates shock, etc.)       ││
│  │  • Worst-of Pillar Limit                                                            ││
│  │  • Point of Weakness Limits (portfolio-specific)                                    ││
│  │                                                                                     ││
│  │  Hierarchy: Entity → Division → Business (selected scenarios)                       ││
│  │  Source: Risk Engine Stream 3                                                       ││
│  │  Monitoring: Daily/Weekly                                                           ││
│  └─────────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐│
│  │                         SENSITIVITY LIMITS (MR-L5-003)                              ││
│  │                                                                                     ││
│  │  • DV01 (Interest Rate sensitivity)                                                 ││
│  │  • CS01 (Credit Spread sensitivity)                                                 ││
│  │  • Vega (Volatility sensitivity)                                                    ││
│  │  • FX Delta                                                                         ││
│  │  • Equity Delta                                                                     ││
│  │                                                                                     ││
│  │  Hierarchy: Entity → Division → Business → Desk                                     ││
│  │  Source: Risk Engine Stream 1                                                       ││
│  │  Monitoring: Intraday                                                               ││
│  └─────────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐│
│  │                         CONCENTRATION LIMITS (MR-L5-005)                            ││
│  │                                                                                     ││
│  │  • Single Issuer (% of Trading Book VaR)                                            ││
│  │  • Single Currency (% of FX VaR)                                                    ││
│  │  • Single Curve (% of IR VaR)                                                       ││
│  │  • Sector (% of Credit VaR)                                                         ││
│  │  • Country/EM (% of EM VaR)                                                         ││
│  │  • Position vs ADV (% of 30-day Average Daily Volume)                               ││
│  │                                                                                     ││
│  │  Hierarchy: Entity level (Trading Book wide)                                        ││
│  │  Source: Risk Engine (VaR decomposition)                                            ││
│  │  Monitoring: Daily                                                                  ││
│  └─────────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐│
│  │                         STOP-LOSS LIMITS (MR-L5-006)                                ││
│  │                                                                                     ││
│  │  • Daily Stop-Loss (multiple of VaR limit)                                          ││
│  │  • MTD Stop-Loss (cumulative monthly loss)                                          ││
│  │  • YTD Stop-Loss (entity level only)                                                ││
│  │                                                                                     ││
│  │  Hierarchy: Entity → Division → Business → Desk                                     ││
│  │  Source: P&L ODS (actual P&L)                                                       ││
│  │  Monitoring: Intraday (Daily) / Daily (MTD)                                         ││
│  └─────────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Limit Summary Table

| Limit Type | Control Ref | Entity Limit | Warning | Monitoring | Approval |
|------------|-------------|--------------|---------|------------|----------|
| **VaR (99%, 1-day)** | MR-L5-001 | $25M | $20M (80%) | Daily | Board/RMC |
| **SVaR (99%, 1-day)** | MR-L5-001 | $50M | $40M (80%) | Daily | RMC |
| **Stress - GFC** | MR-L5-002 | $190M | $150M (80%) | Daily | RMC |
| **Stress - Worst-of** | MR-L5-002 | $190M | $150M (80%) | Daily | RMC |
| **DV01** | MR-L5-003 | $625k/bp | $500k (80%) | Intraday | MLRC |
| **CS01** | MR-L5-003 | $375k/bp | $300k (80%) | Intraday | MLRC |
| **Vega** | MR-L5-003 | $250k/%vol | $200k (80%) | Intraday | MLRC |
| **Single Issuer** | MR-L5-005 | 15% of TB VaR | 12% | Daily | MLRC |
| **Daily Stop-Loss (Desk)** | MR-L5-006 | 1.5x VaR limit | N/A | Intraday | MLRC |

---

## 3. Limit Lifecycle

### 3.1 Lifecycle Overview

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     LIMIT LIFECYCLE                                                     │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐           │
│  │   1. SETUP   │───▶│  2. OPERATE  │───▶│  3. REVIEW   │───▶│  4. AMEND    │──┐        │
│  │              │    │              │    │              │    │              │  │        │
│  │ New desk/    │    │ Daily        │    │ Annual       │    │ In-year      │  │        │
│  │ book/entity  │    │ monitoring   │    │ limit review │    │ changes      │  │        │
│  │ limit setup  │    │ and breach   │    │ process      │    │              │  │        │
│  │              │    │ management   │    │              │    │              │  │        │
│  └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘  │        │
│         ▲                                                                      │        │
│         └──────────────────────────────────────────────────────────────────────┘        │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Limit Setup

### 4.1 New Desk/Book Limit Setup

When a new trading desk or book is established (following desk mandate approval per MR-L4-012):

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     NEW LIMIT SETUP PROCESS                                             │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  STEP 1: LIMIT REQUEST (Trading)                                                        │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Trading submits limit request for new desk/book                                      │
│  • Request includes: Business rationale, expected activity, proposed limits             │
│  • Must reference approved desk mandate (MR-L4-012)                                     │
│                                                                                         │
│  STEP 2: MARKET RISK REVIEW                                                             │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Market Risk reviews proposed limits against:                                         │
│    - Available headroom at parent level (division/entity)                               │
│    - Consistency with similar desks                                                     │
│    - Risk/return expectations                                                           │
│    - Diversification assumptions                                                        │
│  • Market Risk prepares recommendation                                                  │
│                                                                                         │
│  STEP 3: APPROVAL                                                                       │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Desk/Book limits: MLRC approval                                                      │
│  • Business Unit limits: MLRC approval                                                  │
│  • Division/Entity limits: RMC approval (Board for entity)                              │
│                                                                                         │
│  STEP 4: SYSTEM CONFIGURATION                                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Limits entered into Risk Engine / Limit Management System                            │
│  • Hierarchy mapping updated (Hierarchy ODS)                                            │
│  • Alerts configured for new limit                                                      │
│  • Reporting templates updated                                                          │
│                                                                                         │
│  STEP 5: CONFIRMATION AND MONITORING                                                    │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Limits effective from agreed date                                                    │
│  • Initial monitoring period (enhanced scrutiny for 3 months)                           │
│  • Review of limit adequacy at 3-month mark                                             │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Limit Setup Documentation

| Document | Content | Prepared By | Approved By |
|----------|---------|-------------|-------------|
| **Limit Request Form** | Proposed limits, rationale, expected usage | Trading | Business Head |
| **Market Risk Assessment** | Review, recommendation, conditions | Market Risk | Head of Market Risk |
| **Approval Paper** | Summary for committee | Market Risk | MLRC/RMC |
| **System Change Request** | Technical implementation | Market Risk | Risk Engine Ops |

---

## 5. Limit Hierarchy and Structure

### 5.1 VaR Limit Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        VaR LIMIT HIERARCHY                                              │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  HIERARCHY LEVEL        LIMIT TYPE           APPROVING AUTHORITY                        │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  Enterprise             Appetite Limit       Board (via Risk Appetite Statement)        │
│  │                      $25M (illustrative)                                             │
│  │                                                                                      │
│  └─ Legal Entity        Entity Limit         RMC (Board endorsement)                    │
│     │                   Meridian UK: $20M                                               │
│     │                                                                                   │
│     └─ Division         Division Limit       RMC                                        │
│        │                Global Markets: $15M                                            │
│        │                Treasury: $5M                                                   │
│        │                                                                                │
│        └─ Business      Business Limit       MLRC                                       │
│           │             Rates Trading: $8M                                              │
│           │             FX Trading: $5M                                                 │
│           │             Credit Trading: $4M                                             │
│           │                                                                             │
│           └─ Desk       Desk Limit           MLRC (Market Risk delegated)               │
│              │          EUR Rates London: $4M                                           │
│              │          USD Rates NY: $3M                                               │
│              │                                                                          │
│              └─ Book    Book Limit           Desk Head (within desk allocation)         │
│                         EUR-RATES-LON-01: $2M                                           │
│                                                                                         │
│  Note: Limits at higher levels are less than sum of children (diversification)          │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Diversification Assumptions

Sum of sub-limits exceeds parent limit due to assumed diversification:

| Level | Diversification Assumption | Example |
|-------|---------------------------|---------|
| **Division** | ~25% | Divisions sum to $22M, Entity limit $20M |
| **Business Unit** | ~20% | BUs sum to $19M, Division limit $15M |
| **Desk** | ~15% | Desks sum to $9M, BU limit $8M |
| **Book** | ~10% | Books sum to $4.4M, Desk limit $4M |

> **Note**: Diversification benefits are reviewed annually and may be reduced during stress periods.

---

## 6. Daily Limit Monitoring

### 6.1 Monitoring Process

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     DAILY LIMIT MONITORING PROCESS                                      │
│                     (From 07:30 GMT+1 onwards)                                          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  [After Market Risk Report Sign-off (MR-L4-007)]                                        │
│              │                                                                          │
│              ▼                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐│
│  │  STEP 1: UTILISATION CALCULATION                                                    ││
│  │                                                                                     ││
│  │  For each hierarchy level and limit type:                                           ││
│  │                                                                                     ││
│  │  Utilisation % = (Risk Metric ÷ Limit) × 100%                                       ││
│  │                                                                                     ││
│  │  EXAMPLES:                                                                          ││
│  │  • VaR Utilisation = ($3.2M VaR ÷ $4.0M Limit) = 80%                                ││
│  │  • Stress Utilisation = ($120M Stress P&L ÷ $150M Limit) = 80%                      ││
│  │  • DV01 Utilisation = ($400k/bp ÷ $500k/bp Limit) = 80%                             ││
│  │                                                                                     ││
│  └─────────────────────────────────────────────────────────────────────────────────────┘│
│              │                                                                          │
│              ▼                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐│
│  │  STEP 2: STATUS CLASSIFICATION                                                      ││
│  │                                                                                     ││
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐    ││
│  │  │  Utilisation    │  Status    │  Indicator │  Action Required                │    ││
│  │  │  ─────────────────────────────────────────────────────────────────────────  │    ││
│  │  │  0% - 80%       │  GREEN     │  🟢        │  Normal operations              │    ││
│  │  │  80% - 90%      │  AMBER     │  🟡        │  Alert desk head; monitor       │    ││
│  │  │  90% - 100%     │  RED       │  🔴        │  Warning; prepare for breach    │    ││
│  │  │  >100%          │  BREACH    │  ⚫        │  Immediate escalation           │    ││
│  │  └─────────────────────────────────────────────────────────────────────────────┘    ││
│  │                                                                                     ││
│  └─────────────────────────────────────────────────────────────────────────────────────┘│
│              │                                                                          │
│              ▼                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐│
│  │  STEP 3: NOTIFICATION AND ESCALATION                                                ││
│  │                                                                                     ││
│  │  GREEN:  No action required                                                         ││
│  │  AMBER:  Automated email to Desk Head + Market Risk                                 ││
│  │  RED:    Automated email + phone call to Business Head                              ││
│  │  BREACH: Immediate escalation per Section 7                                         ││
│  │                                                                                     ││
│  └─────────────────────────────────────────────────────────────────────────────────────┘│
│              │                                                                          │
│              ▼                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐│
│  │  STEP 4: DASHBOARD UPDATE                                                           ││
│  │                                                                                     ││
│  │  • Risk Portal updated with current utilisation                                     ││
│  │  • Traffic light status by hierarchy                                                ││
│  │  • Breach history and trend                                                         ││
│  │  • Top consumers by limit type                                                      ││
│  │                                                                                     ││
│  └─────────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Monitoring Frequency by Limit Type

| Limit Type | Monitoring Frequency | Source System | Alert Mechanism |
|------------|---------------------|---------------|-----------------|
| **VaR** | Daily (T+1) | Risk Engine | Dashboard + Email |
| **SVaR** | Daily (T+1) | Risk Engine | Dashboard + Email |
| **Stress Limits** | Daily/Weekly | Risk Engine | Dashboard + Email |
| **Sensitivities (DV01, CS01, Vega)** | Intraday (hourly) | Risk Engine | Real-time Dashboard |
| **Concentration** | Daily | Risk Engine | Dashboard + Email |
| **Stop-Loss (Daily)** | Intraday (hourly) | P&L System | Real-time Alert |
| **Stop-Loss (MTD)** | Daily | P&L System | Dashboard + Email |

---

## 7. Breach Management

### 7.1 Breach Classification

| Type | Definition | Response Time |
|------|------------|---------------|
| **Technical Breach** | Data/system error causing apparent breach | Investigate immediately; resolve within 4 hours |
| **Passive Breach** | Market movement caused breach (no new risk) | Action plan within 24 hours |
| **Active Breach** | New position caused breach | Immediate escalation; position reduction required |

### 7.2 Escalation Matrix

| Breach Level | Escalate To | Timeline | Required Action |
|--------------|-------------|----------|-----------------|
| **Book** | Desk Head + Market Risk | Immediate | Reallocate within desk or reduce |
| **Desk** | Business Head + Market Risk Manager | Within 1 hour | MLRC notification; temp excess or reduction |
| **Business** | Trading Head + MLRC Chair | Within 2 hours | MLRC decision required |
| **Division** | CRO + MLRC | Immediate | Reduction plan or RMC escalation |
| **Entity** | CRO + RMC Chair + Board Risk | Immediate | Emergency RMC; formal reduction plan |

### 7.3 Breach Response Framework

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     BREACH RESPONSE FRAMEWORK                                           │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  STEP 1: IMMEDIATE NOTIFICATION (Within 30 minutes of breach identification)            │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • RAV/Market Risk notifies relevant parties per escalation matrix                      │
│  • Breach logged in exception tracking system                                           │
│  • Initial assessment: Technical, Passive, or Active breach?                            │
│                                                                                         │
│  STEP 2: ROOT CAUSE ANALYSIS (Within 2 hours)                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Identify driver of breach:                                                           │
│    - New trade / position change?                                                       │
│    - Market movement?                                                                   │
│    - Methodology / parameter change?                                                    │
│    - Data / system error?                                                               │
│  • Assess if breach is temporary or structural                                          │
│  • Prepare options for remediation                                                      │
│                                                                                         │
│  STEP 3: REMEDIATION DECISION (Per escalation authority)                                │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  OPTION A: TEMPORARY EXCESS APPROVAL                                                    │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐  │
│  │  Authority      │ Max Excess │ Max Duration │ Conditions                          │  │
│  │  ─────────────────────────────────────────────────────────────────────────────────│  │
│  │  MLRC           │ 10%        │ 5 days       │ Documented rationale; daily monitor │  │
│  │  RMC            │ 20%        │ 10 days      │ Formal request; reduction trajectory│  │
│  │  Board          │ >20%       │ As approved  │ Exceptional circumstances only      │  │
│  └───────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                         │
│  OPTION B: RISK REDUCTION                                                               │
│  • Desk instructed to reduce risk to within limit                                       │
│  • Timeline specified (intraday, EOD, T+1)                                              │
│  • Progress monitored by Market Risk                                                    │
│                                                                                         │
│  OPTION C: LIMIT INCREASE REQUEST                                                       │
│  • If breach reflects legitimate business need                                          │
│  • Requires formal MLRC/RMC approval                                                    │
│  • Supported by business case and headroom analysis                                     │
│                                                                                         │
│  STEP 4: DOCUMENTATION AND FOLLOW-UP                                                    │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Breach recorded in exception log with full details                                   │
│  • Daily monitoring until resolved                                                      │
│  • Post-incident review if material or repeated                                         │
│  • MLRC reporting of all breaches                                                       │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 7.4 Breach Documentation Requirements

Each breach must be documented with:

1. Date and time of breach
2. Limit type and level breached
3. Breach amount (absolute and %)
4. Cause classification (technical/passive/active)
5. Root cause analysis
6. Immediate actions taken
7. Remediation plan with timeline
8. Sign-off by relevant authority
9. Resolution date and confirmation

---

## 8. Annual Limit Review

### 8.1 Annual Review Process

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     ANNUAL LIMIT REVIEW PROCESS                                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  TIMELINE                                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  NOVEMBER                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  Week 1-2: Trading submits limit requests for following year                    │    │
│  │  • Review of current utilisation patterns                                       │    │
│  │  • Business growth plans and strategy                                           │    │
│  │  • Proposed limit changes with rationale                                        │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  Week 3-4: Market Risk review and challenge                                     │    │
│  │  • Analysis of historical usage vs. limits                                      │    │
│  │  • Risk/return assessment                                                       │    │
│  │  • Peer comparison                                                              │    │
│  │  • Headroom analysis at entity level                                            │    │
│  │  • Recommendation prepared                                                      │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                         │
│  DECEMBER                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  Week 1-2: MLRC review of desk/BU limits                                        │    │
│  │  • Challenge and approval of desk and business unit limits                      │    │
│  │  • Conditions attached as needed                                                │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  Week 3: RMC approval of division/entity limits                                 │    │
│  │  • Division and entity limits approved                                          │    │
│  │  • Alignment with Risk Appetite confirmed                                       │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                         │
│  JANUARY                                                                                │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  Week 1: Board approval of entity limit                                         │    │
│  │  • Board Risk Committee endorsement                                             │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  Week 2: Limits effective                                                       │    │
│  │  • New limits entered into systems                                              │    │
│  │  • Communication to all stakeholders                                            │    │
│  │  • Effective from 15 January                                                    │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 8.2 Limit Review Criteria

| Criterion | Analysis | Data Source |
|-----------|----------|-------------|
| **Historical Utilisation** | Average, peak, volatility of utilisation | Risk Engine |
| **Breach History** | Number and nature of breaches | Exception Log |
| **P&L Performance** | Risk-adjusted returns | Finance |
| **Business Strategy** | Growth plans, new products | Trading |
| **Market Conditions** | Expected volatility regime | Market Risk |
| **Diversification Benefits** | Correlation analysis | Risk Engine |
| **Peer Comparison** | Benchmark vs. similar desks | Market Risk |

---

## 9. In-Year Limit Changes

### 9.1 Change Types and Approval

| Change Type | Process | Approval | Documentation |
|-------------|---------|----------|---------------|
| **Reallocation within division** | Market Risk review | MLRC | Email confirmation |
| **Desk limit increase (<20%)** | Business case required | MLRC | Formal paper |
| **BU limit increase** | Formal request + rationale | RMC | Committee paper |
| **Entity limit increase** | Board paper required | Board | Full submission |
| **Decrease (any level)** | Market Risk notification | Relevant committee | Email notification |
| **New limit type** | Full assessment | MLRC/RMC | Policy paper |

### 9.2 Emergency Limit Changes

In exceptional circumstances (e.g., market crisis, significant loss event):

| Authority | Scope | Conditions |
|-----------|-------|------------|
| **Head of Market Risk** | Temporary reduction (up to 20%) | Must report to MLRC within 24 hours |
| **CRO** | Any temporary change | Must report to RMC within 48 hours |
| **CEO + CRO** | Emergency suspension | Board notification immediate |

---

## 10. Controls

| Control ID | Control | Type | Owner |
|------------|---------|------|-------|
| LIM-C01 | All new limits approved through governance before system entry | Preventive | Market Risk |
| LIM-C02 | Limit utilisation calculated for all hierarchy levels daily | Detective | RAV |
| LIM-C03 | Breaches escalated within defined timelines | Detective | Market Risk |
| LIM-C04 | Breach documentation complete with root cause | Detective | Market Risk |
| LIM-C05 | Temporary excess approvals time-limited and monitored | Detective | Market Risk |
| LIM-C06 | Annual limit review completed per schedule | Detective | Market Risk |
| LIM-C07 | System limits reconciled to approved limits quarterly | Detective | Risk Engine Ops |
| LIM-C08 | MLRC receives weekly breach summary | Detective | Market Risk |
| LIM-C09 | Diversification assumptions reviewed annually | Detective | RMA |

---

## 11. Service Levels

| Metric | Target | Threshold | Escalation |
|--------|--------|-----------|------------|
| Limit utilisation calculation | 07:30 GMT+1 | 08:00 GMT+1 | RAV Manager |
| Breach notification | Within 30 mins | Within 1 hour | Head of Market Risk |
| Root cause analysis | Within 2 hours | Within 4 hours | Head of Market Risk |
| Temporary excess decision | Within 4 hours | Same day | MLRC Chair |
| New limit setup (after approval) | Within 2 days | Within 5 days | Risk Engine Ops |
| Annual review completion | January 15 | January 31 | Head of Market Risk |

---

## 12. Reporting

### 12.1 Limit Reporting Schedule

| Report | Content | Frequency | Audience |
|--------|---------|-----------|----------|
| **Limit Dashboard** | Real-time utilisation by hierarchy | Continuous | FO, Market Risk |
| **Daily Limit Report** | VaR, Stress, Sensitivity utilisation | Daily | Market Risk, Trading |
| **Breach Summary** | All breaches with status | Daily | Market Risk |
| **MLRC Limit Pack** | Utilisation trends, breaches, analysis | Weekly | MLRC |
| **Board Limit Report** | Entity utilisation, breach summary | Monthly | Board Risk |
| **Annual Limit Review** | Proposed limits, analysis, recommendations | Annual | RMC, Board |

### 12.2 Limit Dashboard Contents

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     LIMIT DASHBOARD - ENTITY VIEW                                       │
│                     Meridian Bank UK | 16-Jan-2025 07:30 GMT+1                          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  VaR LIMITS                                                                             │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Limit Type        │  Current  │  Limit    │  Util %  │  Status  │  Trend (5d)          │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  VaR (99%, 1-day)  │  $16.5M   │  $20.0M   │   83%    │  🟡      │  ↑ +5%               │
│  SVaR              │  $35.2M   │  $40.0M   │   88%    │  🟡      │  ↑ +8%               │
│                                                                                         │
│  STRESS LIMITS                                                                          │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Scenario          │  Stress P&L │  Limit   │  Util %  │  Status  │  Trend (5d)         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  GFC               │  -$125M     │  $150M   │   83%    │  🟡      │  ↑ +6%              │
│  COVID             │  -$88M      │  $100M   │   88%    │  🟡      │  ↓ -4%              │
│  Rates +200bp      │  -$65M      │  $80M    │   81%    │  🟡      │  ↑ +5%              │
│  Worst-of          │  -$125M     │  $150M   │   83%    │  🟡      │  ↑ +6%              │
│                                                                                         │
│  SENSITIVITY LIMITS                                                                     │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Sensitivity       │  Current    │  Limit   │  Util %  │  Status  │  Trend (5d)         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  DV01              │  $420k/bp   │  $500k   │   84%    │  🟡      │  → 0%               │
│  CS01              │  $180k/bp   │  $300k   │   60%    │  🟢      │  ↓ -5%              │
│  Vega              │  $145k/%    │  $200k   │   73%    │  🟢      │  ↑ +3%              │ 
│                                                                                         │
│  BREACHES (Last 30 days): 2                                                             │
│  • 10-Jan: EUR Rates London - VaR breach (103%, resolved same day)                      │
│  • 05-Jan: Credit Trading - Stop-loss breach (technical, resolved 4 hours)              │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 13. Related Documents

| Document | Relationship |
|----------|--------------|
| [Market Risk Process Orchestration](./market-risk-process-orchestration.md) | Parent orchestration |
| [Market Risk Reporting and Sign-off](./market-risk-reporting-signoff.md) | Upstream - provides metrics |
| [Risk Engine Calculation](./risk-engine-calculation.md) | Upstream - calculates VaR/Stress |
| [Aged Inventory Monitoring](./aged-inventory-monitoring.md) | Related - quarterly inventory review |
| [Desk Mandate Management](./desk-mandate-management.md) | Related - desk setup prerequisite |
| [VaR Limit Framework](../L3-Governance/policies/var-limit-framework.md) | Governance - limit definitions |
| [VaR Limits Controls](../../L5-Controls/var-limits.md) | Control definitions |
| [Stress Limits Controls](../../L5-Controls/stress-limits.md) | Control definitions |
| [MLRC Terms of Reference](../L3-Governance/committees/mlrc-terms-of-reference.md) | Governance - approval authority |

---

## 14. Document Control

### 14.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-16 | Initial version - extracted from VaR Reporting process and expanded to cover full limit lifecycle including setup, monitoring, breach management, and annual review | MLRC |
| 1.1 | 2025-01-16 | Removed Aged Inventory section - now standalone document MR-L4-014 Aged Inventory Monitoring | MLRC |

---

*End of Document*
