---
# Process Metadata
process_id: MR-L4-012
process_name: Trading Desk Mandate Management
version: 1.0
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
  - MR-L3-003   # VaR Limit Framework
l5_controls:
  - MR-L5-001   # VaR Limits
  - MR-L5-005   # Concentration Limits
l7_systems:
  - SYS-MR-008  # Risk ODS
  - SYS-MR-011  # Hierarchy ODS
---

# Trading Desk Mandate Management Process

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Process ID** | MR-L4-012 |
| **Version** | 1.0 |
| **Effective Date** | 16 January 2025 |
| **Owner** | Head of Market Risk |

---

## 1. Purpose

The Trading Desk Mandate Management process establishes and maintains the governance framework for trading desks within Meridian Global Bank. This process ensures:

1. **Regulatory Compliance** - Trading desks meet CRR Article 104b requirements for IMA approval
2. **Clear Business Strategy** - Each desk has a defined mandate and permitted activities
3. **Risk Management Structure** - Appropriate risk limits and controls for each desk
4. **Organisational Clarity** - Clear reporting lines and accountability

This process governs the full lifecycle of trading desk mandates from initial setup through annual review and retirement.

---

## 2. Regulatory Context

### 2.1 CRR Article 104b - Trading Desk Requirements

Under CRR Article 104b, institutions using the Internal Models Approach (IMA) must ensure each trading desk:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     CRR ARTICLE 104b - TRADING DESK REQUIREMENTS                        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  (a) CLEAR AND WELL-DOCUMENTED BUSINESS STRATEGY                                        │
│      • Defined scope of activities                                                      │
│      • Permitted product types and markets                                              │
│      • Strategic objectives and risk appetite                                           │
│                                                                                         │
│  (b) CLEAR ORGANISATIONAL STRUCTURE                                                     │
│      • Reporting lines to senior management                                             │
│      • Defined roles and responsibilities                                               │
│      • Independence from control functions                                              │
│                                                                                         │
│  (c) RISK MANAGEMENT STRUCTURE                                                          │
│      • Limits appropriate to the desk's strategy                                        │
│      • Regular limit monitoring and reporting                                           │
│      • Independent risk oversight                                                       │
│                                                                                         │
│  (d) DESIGNATED DEALERS                                                                 │
│      • Named individuals authorised to trade                                            │
│      • Clear authority levels                                                           │
│      • Documented product approval                                                      │
│                                                                                         │
│  (e) PROFIT AND LOSS ATTRIBUTION                                                        │
│      • Daily P&L calculation capability                                                 │
│      • P&L attribution to risk factors                                                  │
│      • Support for P&L attribution test (PLAT)                                          │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Basel MAR 12.4 - Desk Organisation

| Requirement | Basel MAR Reference | Implementation |
|-------------|-------------------|----------------|
| Desk definition | MAR 12.4 | Formal mandate document per desk |
| P&L attribution | MAR 12.4 | Daily P&LA process |
| Backtesting | MAR 12.4 | Desk-level backtesting programme |
| Risk factor mapping | MAR 12.4 | Risk factor inventory per desk |

### 2.3 PRA Expectations

| Expectation | Source | Evidence Required |
|-------------|--------|-------------------|
| Documented desk mandates | SS13/13 | Mandate documents approved by MLRC |
| Independent risk monitoring | SS13/13 | Risk limits and escalation process |
| Trader authorisation | Internal governance | Approved dealer list per desk |
| Annual review | SS13/13 | Documented annual mandate review |

---

## 3. Desk Mandate Framework

### 3.1 Mandate Components

Each trading desk mandate must include:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     TRADING DESK MANDATE STRUCTURE                                      │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  1. DESK IDENTIFICATION                                                                 │
│     ├── Desk name and ID (unique identifier)                                            │
│     ├── Legal entity                                                                    │
│     ├── Business unit and division                                                      │
│     ├── Location (primary, any satellite)                                               │
│     └── Regulatory treatment (IMA/SA)                                                   │
│                                                                                         │
│  2. BUSINESS STRATEGY                                                                   │
│     ├── Strategic purpose (market making, flow, proprietary)                            │
│     ├── Client types served                                                             │
│     ├── Revenue model                                                                   │
│     └── Growth/wind-down plans                                                          │
│                                                                                         │
│  3. PERMITTED ACTIVITIES                                                                │
│     ├── Permitted asset classes                                                         │
│     ├── Permitted instruments and products                                              │
│     ├── Permitted markets and currencies                                                │
│     ├── Prohibited activities                                                           │
│     └── Tenor/maturity restrictions                                                     │
│                                                                                         │
│  4. RISK LIMITS                                                                         │
│     ├── VaR limit (99%, 1-day)                                                          │
│     ├── Stress limit                                                                    │
│     ├── Sensitivity limits (DV01, CS01, Vega, etc.)                                     │
│     ├── Notional/gross exposure limits                                                  │
│     ├── Concentration limits                                                            │
│     └── Stop-loss trigger                                                               │
│                                                                                         │
│  5. ORGANISATIONAL STRUCTURE                                                            │
│     ├── Desk head (named individual)                                                    │
│     ├── Reporting line                                                                  │
│     ├── Team structure                                                                  │
│     └── Support functions (operations, technology)                                      │
│                                                                                         │
│  6. DESIGNATED DEALERS                                                                  │
│     ├── Authorised traders (by name)                                                    │
│     ├── Authority levels (junior/senior/head)                                           │
│     └── Delegation arrangements                                                         │
│                                                                                         │
│  7. RISK MANAGEMENT                                                                     │
│     ├── Risk oversight (assigned risk manager)                                          │
│     ├── Escalation procedures                                                           │
│     ├── Limit breach protocols                                                          │
│     └── New product approval requirements                                               │
│                                                                                         │
│  8. GOVERNANCE                                                                          │
│     ├── Approval authority (MLRC)                                                       │
│     ├── Review frequency (annual minimum)                                               │
│     └── Amendment process                                                               │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Desk Categories

| Category | Definition | Examples | Typical Limits |
|----------|------------|----------|----------------|
| **Market Making** | Provide liquidity to clients; manage inventory | EUR Rates MM, G10 FX MM | Higher VaR, strict concentration |
| **Flow Trading** | Execute client orders; limited position taking | EM FX Flow, Credit Flow | Lower VaR, higher turnover |
| **Proprietary** | Discretionary position taking | Macro Trading, Relative Value | VaR + stop-loss focused |
| **Treasury** | Manage bank's own liquidity and funding | ALM, Funding Desk | Interest rate and liquidity limits |
| **Structuring** | Create and risk manage structured products | Equity Derivatives, Hybrids | Complex Greeks limits |

---

## 4. Desk Mandate Lifecycle

### 4.1 New Desk Setup Process

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     NEW DESK SETUP PROCESS                                              │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  PHASE 1: BUSINESS CASE (Weeks 1-4)                                                     │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Owner: Business Sponsor                                                                │
│  • Strategic rationale for new desk                                                     │
│  • Revenue and cost projections                                                         │
│  • Proposed activities and products                                                     │
│  • Initial resource requirements                                                        │
│  • Risk appetite and proposed limits                                                    │
│                                                                                         │
│  Approval: Head of Trading                                                              │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  PHASE 2: RISK ASSESSMENT (Weeks 5-8)                                                   │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Owner: Market Risk                                                                     │
│  • Risk factor inventory                                                                │
│  • Proposed VaR and stress limits                                                       │
│  • Concentration limit framework                                                        │
│  • Backtesting requirements                                                             │
│  • P&L attribution capability                                                           │
│  • Limit monitoring requirements                                                        │
│                                                                                         │
│  Review: RMA (methodology review)                                                       │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  PHASE 3: OPERATIONAL SETUP (Weeks 9-12)                                                │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Owners: Operations, Technology, Finance                                                │
│  • System setup (trading, risk, P&L)                                                    │
│  • Book structure in Hierarchy ODS                                                      │
│  • Control framework implementation                                                     │
│  • Operational procedures                                                               │
│  • Finance reporting setup                                                              │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  PHASE 4: MANDATE DOCUMENTATION (Weeks 11-14)                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Owner: Market Risk                                                                     │
│  • Draft mandate document                                                               │
│  • Designated dealer list                                                               │
│  • Risk limit schedule                                                                  │
│  • Escalation procedures                                                                │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  PHASE 5: APPROVAL (Weeks 13-16)                                                        │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Approval Path:                                                                         │
│  1. Head of Market Risk → Risk approval                                                 │
│  2. Head of Trading → Business approval                                                 │
│  3. MLRC → Final approval                                                               │
│                                                                                         │
│  Documentation:                                                                         │
│  • Signed mandate document                                                              │
│  • MLRC minutes                                                                         │
│  • Limit schedule in Risk ODS                                                           │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  PHASE 6: GO-LIVE (Week 16+)                                                            │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Owner: Market Risk                                                                     │
│  • Activate limits in Risk Engine                                                       │
│  • First day validation                                                                 │
│  • 30-day enhanced monitoring                                                           │
│  • Post-implementation review (T+90 days)                                               │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Annual Review Process

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     ANNUAL MANDATE REVIEW PROCESS                                       │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  TIMING: Q4 each year (aligned with budget/planning cycle)                              │
│                                                                                         │
│  STEP 1: DATA GATHERING (October)                                                       │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Prior year VaR utilisation statistics                                                │
│  • Limit breach history                                                                 │
│  • P&L performance                                                                      │
│  • Backtesting results                                                                  │
│  • New product approvals granted                                                        │
│  • Headcount and designated dealer changes                                              │
│                                                                                         │
│  STEP 2: BUSINESS REVIEW (October-November)                                             │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Desk head self-assessment                                                            │
│  • Strategy changes for coming year                                                     │
│  • Limit increase/decrease requests                                                     │
│  • Product scope changes                                                                │
│  • Resource changes                                                                     │
│                                                                                         │
│  STEP 3: RISK ASSESSMENT (November)                                                     │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Market Risk review of performance                                                    │
│  • Limit utilisation analysis                                                           │
│  • Risk factor coverage assessment                                                      │
│  • Backtesting adequacy                                                                 │
│  • Recommendation on limits                                                             │
│                                                                                         │
│  STEP 4: MANDATE UPDATE (November-December)                                             │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Updated mandate document drafted                                                     │
│  • Designated dealer list refreshed                                                     │
│  • Limit schedule updated                                                               │
│  • Changes highlighted                                                                  │
│                                                                                         │
│  STEP 5: APPROVAL (December-January)                                                    │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • MLRC review and approval                                                             │
│  • Updated limits effective 1 January                                                   │
│  • Mandate document version control updated                                             │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Mandate Amendment Process

| Change Type | Approval Authority | Timeline | Documentation |
|-------------|-------------------|----------|---------------|
| **New Product Addition** | MLRC | 4-6 weeks | Product approval memo + mandate addendum |
| **Limit Increase (≤20%)** | Head of Market Risk | 1-2 weeks | Limit change request |
| **Limit Increase (>20%)** | MLRC | 2-4 weeks | Limit change proposal |
| **Limit Decrease** | Head of Market Risk | Immediate | Notification |
| **Designated Dealer Change** | Desk Head + Market Risk | 1 week | Updated dealer list |
| **Strategy Change** | MLRC | 4-6 weeks | Updated mandate |
| **Desk Closure** | MLRC | Per wind-down plan | Closure plan approval |

---

## 5. Designated Dealer Management

### 5.1 Dealer Authorisation

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     DESIGNATED DEALER FRAMEWORK                                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  AUTHORITY LEVELS                                                                       │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  Level 1: DESK HEAD                                                                     │
│  • Full authority within desk mandate                                                   │
│  • Can approve new traders                                                              │
│  • Responsible for overall desk P&L and risk                                            │
│                                                                                         │
│  Level 2: SENIOR TRADER                                                                 │
│  • Authority up to defined notional/risk thresholds                                     │
│  • Can trade all permitted products                                                     │
│  • May deputise for desk head (if designated)                                           │
│                                                                                         │
│  Level 3: TRADER                                                                        │
│  • Limited authority (lower thresholds)                                                 │
│  • May have product restrictions                                                        │
│  • Escalation to senior trader for large trades                                         │
│                                                                                         │
│  Level 4: JUNIOR TRADER / ASSISTANT                                                     │
│  • Execution only (no new risk)                                                         │
│  • Under supervision of senior trader                                                   │
│  • Training towards higher authority                                                    │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  AUTHORITY THRESHOLDS (Example)                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  │ Level        │ Single Trade  │ Daily DV01    │ Product Scope                │        │
│  ├──────────────┼───────────────┼───────────────┼──────────────────────────────┤        │
│  │ Desk Head    │ Unlimited     │ Unlimited     │ All permitted                │        │
│  │ Senior Trader│ $50M notional │ $200k DV01    │ All permitted                │        │
│  │ Trader       │ $10M notional │ $50k DV01     │ Vanilla products             │        │
│  │ Junior       │ Execution only│ N/A           │ Vanilla execution only       │        │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Dealer List Maintenance

| Activity | Frequency | Owner | Deliverable |
|----------|-----------|-------|-------------|
| New dealer onboarding | As needed | Desk Head + HR | Completed onboarding checklist |
| Authority level change | As needed | Desk Head + Market Risk | Updated dealer list |
| Dealer offboarding | As needed | Desk Head + HR | Exit checklist; dealer removed from list |
| Full dealer list review | Annual | Market Risk | Validated dealer list in mandate |
| System access reconciliation | Monthly | Operations | System access = authorised dealers |

---

## 6. Risk Limit Framework

### 6.1 Limit Types by Desk

Each desk mandate includes the following limit types:

| Limit Type | Definition | Monitoring | Escalation |
|------------|------------|------------|------------|
| **VaR Limit** | 99%, 1-day VaR maximum | Daily | Soft (warning), Hard (stop trading) |
| **Stress Limit** | Maximum stress P&L | Daily | Warning to MLRC |
| **Sensitivity Limits** | DV01, CS01, Vega per bucket | Intraday | Trading alert |
| **Notional Limit** | Gross notional exposure | Intraday | Trading alert |
| **Concentration Limit** | Single name, curve, currency | Daily | Warning/Hard |
| **Stop-Loss Trigger** | Cumulative loss threshold | Daily | Management review |

### 6.2 Limit Utilisation Monitoring

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     LIMIT UTILISATION THRESHOLDS                                        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  UTILISATION ZONES                                                                      │
│                                                                                         │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                                                                                    │ │
│  │  0%                    75%            90%          95%         100%                │ │
│  │  ├────────────────────┼──────────────┼────────────┼───────────┤                    │ │
│  │  │       GREEN        │    AMBER     │   AMBER+   │    RED    │                    │ │
│  │  │                    │              │            │           │                    │ │
│  │  │   Normal trading   │   Warning    │  Enhanced  │   Hard    │                    │ │
│  │  │   operations       │   issued     │  monitoring│   breach  │                    │ │
│  │  │                    │              │            │           │                    │ │
│  │  └────────────────────┴──────────────┴────────────┴───────────┘                    │ │
│  │                                                                                    │ │
│  └────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                         │
│  ESCALATION BY ZONE                                                                     │
│                                                                                         │
│  GREEN (0-75%):    No escalation required                                               │
│  AMBER (75-90%):   Warning to desk head; Market Risk notified                           │
│  AMBER+ (90-95%):  Daily reporting to Head of Market Risk; reduction plan required      │
│  RED (≥95%):       Immediate notification to Head of Trading; new risk prohibited       │
│  BREACH (≥100%):   MLRC notification; position reduction required; investigation        │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Governance

### 7.1 Approval Authorities

| Decision | Approval Authority | Escalation |
|----------|-------------------|------------|
| New desk creation | MLRC | Board Risk Committee (if >$10M VaR) |
| Desk closure | MLRC | Board Risk Committee |
| Mandate approval | MLRC | - |
| Limit changes (>20%) | MLRC | - |
| Limit changes (≤20%) | Head of Market Risk | MLRC (if disputed) |
| Dealer authorisation | Desk Head + Market Risk | - |
| Product scope expansion | MLRC | - |

### 7.2 MLRC Oversight

| Activity | Frequency | Documentation |
|----------|-----------|---------------|
| New desk approval | As needed | Full mandate document |
| Annual mandate review | Annual (Q4) | Updated mandates for all desks |
| Limit breach review | Each MLRC | Breach log and resolution |
| Desk performance review | Quarterly | KRI dashboard by desk |

### 7.3 Documentation Requirements

| Document | Owner | Storage | Retention |
|----------|-------|---------|-----------|
| Mandate Document | Market Risk | Document Management System | Current + 7 years |
| Designated Dealer List | Market Risk | Risk ODS | Current + 7 years |
| Limit Schedule | Market Risk | Risk Engine / Risk ODS | Current + 7 years |
| MLRC Approvals | MLRC Secretary | Committee Records | Permanent |
| Amendment History | Market Risk | Document Management System | Current + 7 years |

---

## 8. Controls

| Control ID | Control | Type | Owner |
|------------|---------|------|-------|
| DM-C01 | All trading desks have approved mandate documents | Preventive | Market Risk |
| DM-C02 | Designated dealer list maintained and current | Preventive | Market Risk |
| DM-C03 | Annual mandate review completed | Detective | Market Risk |
| DM-C04 | System access matches authorised dealer list | Detective | Operations |
| DM-C05 | Trading activity within permitted products | Detective | Market Risk |
| DM-C06 | Limits aligned with desk mandate | Preventive | Market Risk |
| DM-C07 | New desks approved by MLRC before trading | Preventive | Market Risk |
| DM-C08 | Desk closure follows wind-down process | Preventive | Market Risk |

---

## 9. Service Levels

| Activity | Target | Threshold | Escalation |
|----------|--------|-----------|------------|
| New desk setup (end-to-end) | 12 weeks | 16 weeks | Head of Market Risk |
| Annual review completion | 31 December | 15 January | Head of Market Risk |
| Dealer onboarding | 5 business days | 10 business days | Desk Head |
| Limit change (minor) | 2 business days | 5 business days | Market Risk Manager |
| Limit change (MLRC) | Next MLRC | MLRC+1 | Head of Market Risk |
| Mandate amendment | 4 weeks | 6 weeks | Head of Market Risk |

---

## 10. Related Documents

| Document | Relationship |
|----------|--------------|
| [Market Risk Process Orchestration](./market-risk-process-orchestration.md) | Parent orchestration |
| [VaR Limit Framework](../L3-Governance/policies/var-limit-framework.md) | Limit governance |
| [Market Risk Policy](../L3-Governance/policies/market-risk-policy.md) | Policy framework |
| [MLRC Terms of Reference](../L3-Governance/committees/mlrc-terms-of-reference.md) | Approval authority |
| [VaR Limits Controls](../L5-Controls/market-risk/var-limits-controls.md) | Limit monitoring |
| [Hierarchy Management](./hierarchy-management.md) | Book structure management |
| [New Product Approval](./new-product-approval.md) | Product governance |

---

## 11. Appendix: Mandate Template

### 11.1 Mandate Document Template

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     TRADING DESK MANDATE                                                │
│                     [DESK NAME]                                                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  DOCUMENT CONTROL                                                                       │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Desk ID:           [XXX-DESK-YYY]                                                      │
│  Version:           [X.X]                                                               │
│  Effective Date:    [DD/MM/YYYY]                                                        │
│  Last Review:       [DD/MM/YYYY]                                                        │
│  Next Review:       [DD/MM/YYYY]                                                        │
│  Owner:             [Desk Head Name]                                                    │
│  Approved By:       [MLRC Date]                                                         │
│                                                                                         │
│  SECTION 1: DESK IDENTIFICATION                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Legal Entity:      [Entity Name]                                                       │
│  Division:          [Division]                                                          │
│  Business Unit:     [Business Unit]                                                     │
│  Location:          [Primary Location]                                                  │
│  Regulatory Status: [IMA / SA]                                                          │
│                                                                                         │
│  SECTION 2: BUSINESS STRATEGY                                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  [Description of desk purpose, client base, revenue model, strategic objectives]        │
│                                                                                         │
│  SECTION 3: PERMITTED ACTIVITIES                                                        │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Asset Classes:     [List]                                                              │
│  Instruments:       [List]                                                              │
│  Markets:           [List]                                                              │
│  Currencies:        [List]                                                              │
│  Tenors:            [Restrictions]                                                      │
│  Prohibited:        [List]                                                              │
│                                                                                         │
│  SECTION 4: RISK LIMITS                                                                 │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  VaR Limit (99%, 1-day):     $[X]M                                                      │
│  Stress Limit:               $[X]M                                                      │
│  DV01 Limit:                 $[X]k per bucket                                           │
│  CS01 Limit:                 $[X]k                                                      │
│  Vega Limit:                 $[X]k per bucket                                           │
│  Notional Limit:             $[X]Bn                                                     │
│  Stop-Loss Trigger:          $[X]M (MTD / YTD)                                          │
│                                                                                         │
│  SECTION 5: ORGANISATION                                                                │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Desk Head:         [Name]                                                              │
│  Reports To:        [Name, Title]                                                       │
│  Risk Manager:      [Name]                                                              │
│  Headcount:         [Number]                                                            │
│                                                                                         │
│  SECTION 6: DESIGNATED DEALERS                                                          │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  [Table of authorised traders with authority levels]                                    │
│                                                                                         │
│  SECTION 7: APPROVALS                                                                   │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  _______________________    _______________________    _______________________          │
│  Desk Head                  Head of Market Risk        MLRC Chair                       │
│  Date:                      Date:                      Date:                            │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 12. Document Control

### 12.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-16 | Initial version | MLRC |

---

*End of Document*
