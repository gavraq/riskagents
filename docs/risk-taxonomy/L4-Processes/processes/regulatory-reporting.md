---
# Process Metadata
process_id: MR-L4-009
process_name: Market Risk Regulatory Reporting
version: 1.4
effective_date: 2025-01-15
next_review_date: 2026-01-15
owner: Head of Regulatory Reporting
approving_committee: MLRC

# Taxonomy Linkages
parent_process: MR-L4-001  # Market Risk Process Orchestration
l1_requirements:
  - REQ-L1-001  # CRR (UK)
  - REQ-L1-003  # FRTB
  - REQ-L1-004  # Basel III/IV
  - REQ-L1-022  # BCBS 239
l2_risk_types:
  - MR-L2-001   # Market Risk
l3_governance:
  - MR-L3-001   # Market Risk Policy
l4_processes:
  - MR-L4-006   # Risk Engine Calculation (provides VaR/SVaR/IRC)
  - MR-L4-008   # VaR Backtesting (provides exception data)
l5_controls:
  - MR-L5-004   # Backtesting Exception Limits
l6_models:
  - MR-L6-001   # Historical Simulation VaR
  - MR-L6-002   # Stressed VaR
  - MR-L6-003   # IRC Model
l7_systems:
  - SYS-MR-004  # Risk Reporting DataMart
  - SYS-MR-010  # Regulatory Reporting Platform
---

# Market Risk Regulatory Reporting Process

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Process ID** | MR-L4-009 |
| **Version** | 1.4 |
| **Effective Date** | 15 January 2025 |
| **Parent Process** | Market Risk Process Orchestration (MR-L4-001) |
| **Owner** | Head of Regulatory Reporting |

---

## 1. Purpose

This process defines the requirements, procedures, and controls for submitting market risk regulatory reports to the Prudential Regulation Authority (PRA) and other relevant regulators. It covers:

- **Periodic reporting** (quarterly COREP submissions)
- **Event-driven notifications** (backtesting exceptions, model changes)
- **Ad-hoc requests** (regulatory inquiries, stress test submissions)

Regulatory reporting is a critical control function ensuring Meridian Global Bank maintains its Internal Models Approach (IMA) permission and meets all supervisory requirements.

---

## 2. Regulatory Framework

### 2.1 Primary Legislation and Rules

| Regulation | Jurisdiction | Key Articles | Relevance |
|------------|--------------|--------------|-----------|
| **UK CRR** (as onshored) | UK | Articles 325-377 | Market risk capital requirements |
| **CRR Article 366** | UK | Backtesting and multiplication factors | Exception notification, quarterly assessment |
| **CRR Article 430** | UK | Supervisory reporting | COREP submission requirements |
| **PRA Rulebook** | UK | Reporting (CRR) Part | UK-specific reporting rules |
| **BCBS 239** | International | Principles for risk data aggregation | Data quality standards |

### 2.2 CRR Article 366 - Key Requirements

Article 366 establishes two distinct reporting obligations for backtesting:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     CRR ARTICLE 366 - BACKTESTING REPORTING REQUIREMENTS                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  1. IMMEDIATE NOTIFICATION (Article 366(4))                                             │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  "In order to allow competent authorities to monitor the appropriateness of the         │
│  multiplication factors on an ongoing basis, institutions shall notify promptly,        │
│  and in any case NO LATER THAN WITHIN FIVE WORKING DAYS, the competent authorities      │
│  of overshootings that result from their back-testing programme."                       │
│                                                                                         │
│  Trigger: Each backtesting exception                                                    │
│  Timeline: ≤5 working days from exception date                                          │
│  Method: PRA notification (email/portal)                                                │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  2. QUARTERLY ASSESSMENT (Article 366(3))                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  "For the purpose of determining the addend, the number of overshootings shall be       │
│  assessed AT LEAST QUARTERLY and shall be equal to the higher of the number of          │
│  overshootings under hypothetical and actual changes in the value of the portfolio."    │
│                                                                                         │
│  Frequency: Quarterly (minimum)                                                         │
│  Content: Rolling 250-day exception count, zone status, multiplier                      │
│  Method: COREP template submission                                                      │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.3 Multiplication Factor Framework

| Zone | Exceptions (250 days) | Base Multiplier | Plus-Factor | Total Multiplier |
|------|----------------------|-----------------|-------------|------------------|
| **GREEN** | 0-4 | 3.0 | 0.00 | 3.00 |
| **YELLOW** | 5 | 3.0 | 0.40 | 3.40 |
| **YELLOW** | 6 | 3.0 | 0.50 | 3.50 |
| **YELLOW** | 7 | 3.0 | 0.65 | 3.65 |
| **YELLOW** | 8 | 3.0 | 0.75 | 3.75 |
| **YELLOW** | 9 | 3.0 | 0.85 | 3.85 |
| **RED** | ≥10 | 3.0 | 1.00 | 4.00 |

---

## 3. Reporting Calendar

### 3.1 Quarterly COREP Submissions

| Quarter | Reference Date | Submission Deadline | Remittance Period |
|---------|---------------|---------------------|-------------------|
| Q1 | 31 March | 12 May | 30 business days |
| Q2 | 30 June | 11 August | 30 business days |
| Q3 | 30 September | 11 November | 30 business days |
| Q4 | 31 December | 11 February | 30 business days |

### 3.2 Annual and Ad-Hoc Submissions

| Report | Frequency | Typical Deadline | Owner |
|--------|-----------|------------------|-------|
| **Pillar 3 Disclosure** | Annual/Semi-annual | 4 months post year-end | Group Risk |
| **ICAAP** | Annual | Per PRA schedule | Capital Management |
| **Stress Test Submissions** | As required | Per PRA schedule | Stress Testing Team |
| **Model Change Notifications** | Event-driven | Prior to implementation | RMA |
| **IMA Re-application** | As required | 12 months before go-live | Market Risk |

### 3.3 Monthly Internal Deadlines

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     QUARTERLY REPORTING TIMELINE (Example: Q4)                          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  Reference Date: 31 December                                                            │
│  Submission Deadline: 11 February (T+30 business days)                                  │
│                                                                                         │
│  Week 1 (T+1 to T+5):                                                                   │
│  ├─ Day 1-2: Data extraction from Risk ODS, P&L ODS                                     │
│  ├─ Day 3-4: Data validation and reconciliation                                         │
│  └─ Day 5: Draft COREP templates populated                                              │
│                                                                                         │
│  Week 2 (T+6 to T+10):                                                                  │
│  ├─ Day 6-7: First-line review (RAV)                                                    │
│  ├─ Day 8-9: Second-line review (Market Risk)                                           │
│  └─ Day 10: Variance analysis vs. prior quarter                                         │
│                                                                                         │
│  Week 3 (T+11 to T+15):                                                                 │
│  ├─ Day 11-12: Finance reconciliation (to GL and capital)                               │
│  ├─ Day 13-14: Issue resolution and adjustments                                         │
│  └─ Day 15: Final templates ready for sign-off                                          │
│                                                                                         │
│  Week 4 (T+16 to T+20):                                                                 │
│  ├─ Day 16-17: Head of Regulatory Reporting sign-off                                    │
│  ├─ Day 18-19: CFO / CRO attestation                                                    │
│  └─ Day 20: Submission to PRA via RegData portal                                        │
│                                                                                         │
│  Buffer (T+21 to T+30):                                                                 │
│  └─ Reserve for queries, resubmissions, technical issues                                │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Own Funds Requirement Calculation

### 4.1 IMA Capital Formula

The market risk Own Funds Requirement (OFR) under the Internal Models Approach is calculated as:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     IMA CAPITAL FORMULA (PRE-BASEL 3.1)                                 │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  MARKET RISK OFR = max(VaRt-1, mc × VaRavg) + max(SVaRt-1, ms × SVaRavg) + IRC          │
│                                                                                         │
│  Where:                                                                                 │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  VaRt-1      = Previous day's VaR (99%, 10-day)                                         │
│  VaRavg      = Average VaR over preceding 60 business days                              │
│  mc          = VaR multiplication factor (3.0 to 4.0, based on backtesting zone)        │
│                                                                                         │
│  SVaRt-1     = Previous day's Stressed VaR (99%, 10-day)                                │
│  SVaRavg     = Average SVaR over preceding 60 business days                             │
│  ms          = SVaR multiplication factor (3.0 minimum)                                 │
│                                                                                         │
│  IRC         = Incremental Risk Charge (99.9%, 1-year, weekly calculation)              │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Multiplication Factor Determination

The VaR multiplication factor (mc) is determined by backtesting performance per CRR Article 366:

| Backtesting Zone | Exception Count (250 days) | Base Factor | Plus-Factor | Total mc |
|------------------|---------------------------|-------------|-------------|----------|
| **GREEN** | 0 | 3.00 | 0.00 | 3.00 |
| **GREEN** | 1 | 3.00 | 0.00 | 3.00 |
| **GREEN** | 2 | 3.00 | 0.00 | 3.00 |
| **GREEN** | 3 | 3.00 | 0.00 | 3.00 |
| **GREEN** | 4 | 3.00 | 0.00 | 3.00 |
| **YELLOW** | 5 | 3.00 | 0.40 | 3.40 |
| **YELLOW** | 6 | 3.00 | 0.50 | 3.50 |
| **YELLOW** | 7 | 3.00 | 0.65 | 3.65 |
| **YELLOW** | 8 | 3.00 | 0.75 | 3.75 |
| **YELLOW** | 9 | 3.00 | 0.85 | 3.85 |
| **RED** | ≥10 | 3.00 | 1.00 | 4.00 |

### 4.3 Daily Capital Calculation Process

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     DAILY OWN FUNDS CALCULATION FLOW                                    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  STEP 1: COLLECT INPUTS (by 09:00)                                                      │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • VaRt-1 from Risk Engine (99%, 10-day holding period)                                 │
│  • VaR 60-day average from Risk ODS                                                     │
│  • SVaRt-1 from Risk Engine (99%, 10-day, stressed period)                              │
│  • SVaR 60-day average from Risk ODS                                                    │
│  • IRC from weekly calculation (most recent)                                            │
│  • Current multiplication factor (from backtesting zone)                                │
│                                                                                         │
│  STEP 2: CALCULATE COMPONENTS                                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • VaR capital = max(VaRt-1, mc × VaRavg)                                               │
│  • SVaR capital = max(SVaRt-1, ms × SVaRavg)                                            │
│  • IRC capital = most recent weekly IRC                                                 │
│                                                                                         │
│  STEP 3: AGGREGATE                                                                      │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Total IMA Capital = VaR capital + SVaR capital + IRC                                 │
│  • Apply any Pillar 2A add-ons (RNIV, RNIME)                                            │
│                                                                                         │
│  STEP 4: RECONCILE                                                                      │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Compare to Finance GL capital requirement                                            │
│  • Investigate any variances > $100k                                                    │
│  • Document reconciliation in daily log                                                 │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.4 Pillar 2A Add-ons

In addition to Pillar 1 capital requirements, the PRA may impose Pillar 2A add-ons:

| Add-on Type | Description | Basis | Review Frequency |
|-------------|-------------|-------|------------------|
| **RNIV** (Risks Not In VaR) | Capital for risks not adequately captured in VaR model (e.g., basis risk, gap risk, correlation) | PRA assessment | Annual (ICAAP) |
| **RNIME** (Risks Not In Model Engines) | Capital for risks outside approved IMA scope | PRA assessment | Annual (ICAAP) |
| **Model Limitations** | Add-on for known model weaknesses | PRA assessment | Per supervisory review |

### 4.5 Quarterly Own Funds Reporting

| COREP Template | Content | Timing |
|----------------|---------|--------|
| **C 02.00** | Total Own Funds Requirements (includes Market Risk) | Quarterly |
| **C 24.00** | Market Risk Internal Models - detailed breakdown | Quarterly |
| **C 25.00** | CVA Risk (Credit Valuation Adjustment) | Quarterly |

### 4.6 Reconciliation to Finance

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     OWN FUNDS RECONCILIATION CHECKPOINTS                                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  DAILY RECONCILIATION (RAV → Finance)                                                   │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Risk ODS IMA capital ↔ Finance GL market risk capital                                │
│  • Tolerance: $100k                                                                     │
│  • Break investigation: Same day escalation if > $500k                                  │
│                                                                                         │
│  QUARTERLY RECONCILIATION (Regulatory Reporting → Finance)                              │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • COREP C24.00 total ↔ COREP C02.00 market risk line                                   │
│  • Risk capital ↔ Finance capital adequacy return                                       │
│  • Tolerance: Zero (must match exactly)                                                 │
│  • Full audit trail required for all adjustments                                        │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Pillar 3 Disclosure Requirements

### 5.1 Regulatory Basis

| CRR Article | Requirement | Frequency |
|-------------|-------------|-----------|
| **Article 445** | Market risk exposure disclosure | Annual (minimum) |
| **Article 448** | Interest rate risk in banking book (IRRBB) | Semi-annual |
| **Article 455** | IMA-specific disclosure requirements | Annual |

### 5.2 Pillar 3 Market Risk Templates

| Template | Name | Content | Frequency |
|----------|------|---------|-----------|
| **MR1** | Market Risk under Standardised Approach | SA capital requirements for firms using SA | Annual |
| **MR2-A** | RWA Flow Statements - IMA | Movement in RWA from VaR-based IMA | Annual |
| **MR2-B** | RWA Flow Statements - IMA (Detailed) | Backtesting and P&L attribution detail | Annual |
| **MR3** | IMA Values for Trading Portfolios | VaR, SVaR, IRC statistics | Annual |
| **MR4** | Comparison of VaR Estimates with Gains/Losses | Backtesting results visualisation | Annual |

### 5.3 MR3 Template - IMA Values

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     MR3 - IMA VALUES FOR TRADING PORTFOLIOS                             │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  For each of VaR, SVaR, and IRC, disclose:                                              │
│                                                                                         │
│  │ Measure              │ VaR (99%, 10d) │ SVaR (99%, 10d) │ IRC (99.9%, 1y) │          │
│  ├──────────────────────┼────────────────┼─────────────────┼─────────────────┤          │
│  │ Maximum value        │                │                 │                 │          │
│  │ Minimum value        │                │                 │                 │          │
│  │ Average value        │                │                 │                 │          │
│  │ Period-end value     │                │                 │                 │          │
│                                                                                         │
│  Additional requirements:                                                               │
│  • Narrative on key risk drivers                                                        │
│  • Explanation of material changes from prior year                                      │
│  • Description of methodology and key assumptions                                       │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.4 MR4 Template - Backtesting Visualisation

Per CRR Article 455(e), firms must disclose:

- Daily VaR values (99%, 1-day) over the reporting period
- Corresponding daily P&L outcomes
- Visual representation of exceptions (backtesting breaches)
- Number and explanation of exceptions in the period

### 5.5 Disclosure Calendar

| Report | Frequency | Reference Date | Publication Deadline |
|--------|-----------|----------------|---------------------|
| **Annual Pillar 3** | Annual | 31 December | 4 months post year-end |
| **Semi-annual Pillar 3** (if required) | Semi-annual | 30 June | 3 months post period-end |
| **Quarterly Disclosure** (large institutions) | Quarterly | Quarter-end | Same as COREP |

### 5.6 Governance and Sign-off

| Activity | Owner | Reviewer | Approver |
|----------|-------|----------|----------|
| Data compilation | Regulatory Reporting | RAV / Market Risk | Head of Reg Reporting |
| Narrative drafting | Market Risk | RMA | Head of Market Risk |
| Final publication | Regulatory Reporting | Group Risk | CRO + Board Risk Committee |

---

## 6. Model Change Notifications

### 6.1 Regulatory Basis

CRR Article 363 and PRA SS13/13 require notification of model changes:

| Change Type | Notification Requirement | Timing | Approval |
|-------------|-------------------------|--------|----------|
| **Material Change** | Prior PRA approval required | 6+ months before implementation | PRA written approval |
| **Non-Material Change** | PRA notification | 30 days before implementation | Internal governance |
| **Extensions** | PRA approval | 12+ months before go-live | PRA written approval |

### 6.2 Capital Impact Thresholds

Commission Delegated Regulation (EU) 2015/942 and CRR Article 363 define materiality thresholds based on the **relevant risk numbers** per CRR Article 364:

| CRR Reference | Risk Number | Include in Parallel Run? |
|---------------|-------------|--------------------------|
| Article 364(1)(a)(i) | **VaR** (Value-at-Risk) | Yes - if VaR/SVaR model affected |
| Article 364(1)(b)(i) | **SVaR** (Stressed VaR) | Yes - if VaR/SVaR model affected |
| Article 364(2)(b)(i) | **IRC** (Incremental Risk Charge) | Only if IRC model affected |
| Article 364(3)(a) | **CRM** (Comprehensive Risk Measure) | Only if correlation trading affected |

**Key principle**: VaR and SVaR are outputs from the **same model** (using different observation periods), so a methodology change always affects both. The parallel run comparison for a VaR/SVaR model change is based on **VaR + SVaR** at entity level. IRC uses a separate model and should only be included if the change impacts the IRC calculation.

**Materiality Thresholds**:

| Threshold | Measure | Classification | Approval Requirement |
|-----------|---------|----------------|---------------------|
| **<1%** | Any individual risk number | De minimis | Internal governance only |
| **≥1% and <5%** | Any individual risk number | Non-material | PRA pre-notification (10 business day review) |
| **≥5%** | Sum of all affected risk numbers | Material | PRA pre-approval required |
| **≥10%** | Any individual risk number | Material | PRA pre-approval required |

*Note: A change is material if it breaches EITHER the 5% aggregate threshold OR the 10% individual threshold.*

### 6.3 15-Day Parallel Run Requirement

For changes with impact ≥1% on any relevant risk number, a **15-day parallel run** must be conducted before implementation:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     15-DAY PARALLEL RUN PROCESS                                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  RISK NUMBERS TO COMPARE (Entity Level)                                                 │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Include only risk numbers from models AFFECTED by the change:                          │
│                                                                                         │
│  • VaR/SVaR model change → Compare VaR(old) vs VaR(new) AND SVaR(old) vs SVaR(new)      │
│                            (VaR and SVaR are the same model, always both affected)      │
│  • IRC model change      → Compare IRC(old) vs IRC(new)                                 │
│                            (IRC is a separate model)                                    │
│                                                                                         │
│  Calculations performed at ENTITY level; breakdowns at desk level for explanation.      │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  DAY 1: INITIAL IMPACT ASSESSMENT                                                       │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Run both OLD and NEW model configurations                                            │
│  • Calculate impact on each affected risk number:                                       │
│      Individual Impact = |New Risk Number - Old Risk Number| / Old Risk Number          │
│  • Calculate aggregate impact (sum of affected risk numbers):                           │
│      Aggregate Impact = |Sum(New) - Sum(Old)| / Sum(Old)                                │
│  • Record Day 1 percentages                                                             │
│                                                                                         │
│  IF Day 1 Individual Impact < 1% (all risk numbers):                                    │
│  └──▶ STOP: De minimis change → Internal governance only                                │
│                                                                                         │
│  IF Day 1 Individual Impact ≥ 1% AND < 10% (all risk numbers)                           │
│     AND Aggregate Impact < 5%:                                                          │
│  └──▶ CONTINUE parallel run for 14 more days (Days 2-15)                                │
│                                                                                         │
│  IF Day 1 Individual Impact ≥ 10% (any risk number)                                     │
│     OR Aggregate Impact ≥ 5%:                                                           │
│  └──▶ STOP: Material change → Requires PRA PRE-APPROVAL                                 │
│       (Cannot implement without prior PRA written approval)                             │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  DAYS 2-15: PARALLEL RUN MONITORING                                                     │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Continue daily comparison of OLD vs. NEW risk numbers                                │
│  • Monitor for breaches of materiality thresholds                                       │
│                                                                                         │
│  IF any day shows Individual Impact ≥ 10% OR Aggregate Impact ≥ 5%:                     │
│  └──▶ STOP parallel run immediately                                                     │
│       └──▶ Reclassify as MATERIAL change                                                │
│            └──▶ Requires PRA PRE-APPROVAL before implementation                         │
│                                                                                         │
│  IF all 15 days remain below materiality thresholds:                                    │
│  └──▶ COMPLETE parallel run successfully                                                │
│       └──▶ Submit PRA PRE-NOTIFICATION with parallel run results                        │
│            └──▶ Wait 10 business days for PRA review                                    │
│                 └──▶ If no PRA objection → Proceed with implementation                  │
│                 └──▶ If PRA raises questions → Respond and await clearance              │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  PARALLEL RUN DOCUMENTATION                                                             │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Daily log must include:                                                                │
│                                                                                         │
│  │ Date │ VaR   │ VaR   │ VaR  │ SVaR  │ SVaR  │ SVaR │ Agg   │ Agg   │ Agg  │ Notes │  │
│  │      │ (Old) │ (New) │ Δ%   │ (Old) │ (New) │ Δ%   │ (Old) │ (New) │ Δ%   │       │  │
│  ├──────┼───────┼───────┼──────┼───────┼───────┼──────┼───────┼───────┼──────┼───────┤  │
│  │ Day 1│ $10M  │ $10.5M│ 5.0% │ $15M  │ $15.3M│ 2.0% │ $25M  │ $25.8M│ 3.2% │       │  │
│  │ ...  │       │       │      │       │       │      │       │       │      │       │  │
│                                                                                         │
│  Plus desk-level breakdown to explain drivers of change.                                │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.4 Material vs. Non-Material Classification

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     MODEL CHANGE CLASSIFICATION                                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  MATERIAL CHANGES (Require PRA Pre-Approval)                                            │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Change in VaR methodology (e.g., Historical Simulation → Monte Carlo)                │
│  • Significant change to volatility/correlation estimation                              │
│  • Extension of IMA to new trading desks or product classes                             │
│  • Change in stressed period selection methodology                                      │
│  • Change resulting in >10% impact on capital requirement (any day in parallel run)     │
│  • Change in backtesting methodology affecting exception count                          │
│                                                                                         │
│  NON-MATERIAL CHANGES (PRA Pre-Notification with 10 Business Day Review)                │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Changes with 1-10% capital impact (sustained through 15-day parallel run)            │
│  • Parameter recalibration within existing methodology                                  │
│  • Data feed enhancements not affecting methodology                                     │
│  • System upgrades with no methodology change                                           │
│  • Minor scope adjustments (product additions within approved desks)                    │
│                                                                                         │
│  DE MINIMIS CHANGES (Internal Governance Only)                                          │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Changes with <1% capital impact                                                      │
│  • Bug fixes with no capital impact                                                     │
│  • Documentation updates                                                                │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.5 Model Change Notification Process

**For Material Changes (>10% impact):**

| Phase | Activities | Timeline | Owner |
|-------|------------|----------|-------|
| **Impact Assessment** | Quantify capital impact, classify as material | T-12 months | RMA |
| **Internal Governance** | MLRC review and approval | T-9 months | Market Risk |
| **PRA Pre-Notification** | Informal discussion with supervisor | T-6 months | Regulatory Reporting |
| **Formal Application** | Submit material change application | T-6 months | Regulatory Reporting |
| **PRA Review** | Respond to queries, provide additional analysis | T-6 to T-3 months | RMA |
| **PRA Approval** | Receive written approval from PRA | Before T | Regulatory Reporting |
| **Implementation** | Deploy approved change | T | Risk Technology |
| **Post-Implementation** | Monitor impact, report to PRA | T+3 months | RMA |

**For Non-Material Changes (1-10% impact):**

| Phase | Activities | Timeline | Owner |
|-------|------------|----------|-------|
| **Impact Assessment** | Quantify capital impact, classify as non-material | T-6 weeks | RMA |
| **Internal Governance** | MLRC review and approval | T-5 weeks | Market Risk |
| **Parallel Run** | 15-day parallel run | T-4 weeks to T-3 weeks | RMA / RAV |
| **PRA Pre-Notification** | Submit notification with parallel run results | T-2 weeks | Regulatory Reporting |
| **PRA Review Period** | 10 business day review window | T-2 weeks to T | Regulatory Reporting |
| **Implementation** | Deploy change (if no PRA objection) | T | Risk Technology |
| **Post-Implementation** | Monitor impact | T+1 month | RMA |

### 6.6 PRA Review Period for Non-Material Changes

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     PRA 10 BUSINESS DAY REVIEW PERIOD                                   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  NOTIFICATION SUBMISSION (Day 0)                                                        │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Submit to PRA:                                                                         │
│  • Description of model change                                                          │
│  • 15-day parallel run results (daily impact log)                                       │
│  • Rationale and business justification                                                 │
│  • Internal governance approval evidence                                                │
│  • Proposed implementation date                                                         │
│                                                                                         │
│  REVIEW PERIOD (Days 1-10)                                                              │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • PRA reviews notification                                                             │
│  • PRA may request clarification or additional information                              │
│  • If questions raised → Clock pauses until response provided                           │
│                                                                                         │
│  OUTCOMES                                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  ✓ NO OBJECTION (silence after 10 days):                                                │
│    └──▶ Proceed with implementation on planned date                                     │
│                                                                                         │
│  ? CLARIFICATION REQUESTED:                                                             │
│    └──▶ Respond to PRA queries                                                          │
│         └──▶ Review period restarts from response date                                  │
│                                                                                         │
│  ✗ OBJECTION RAISED:                                                                    │
│    └──▶ Cannot proceed with implementation                                              │
│         └──▶ May need to reclassify as material change                                  │
│              └──▶ Engage in formal approval process                                     │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. COREP Templates - Market Risk

### 7.1 Current IMA Templates (Pre-Basel 3.1)

| Template | Name | Content | Frequency |
|----------|------|---------|-----------|
| **C 24.00** | MKR IM | Market Risk Internal Models - capital requirements | Quarterly |
| **C 02.00** | Own Funds Requirements | Summary including market risk | Quarterly |

### 7.2 Basel 3.1 / FRTB Templates

**UK Implementation Timeline** (as of CP17/25, July 2025):

| Component | UK Implementation Date |
|-----------|----------------------|
| FRTB Standardised Approaches (ASA, SSA) | 1 January 2027 |
| Trading Book Boundary | 1 January 2027 |
| FRTB Internal Model Approach (FRTB-IMA) | 1 January 2028 |

*Note: EU implementation of FRTB delayed to 1 January 2027. US timeline remains uncertain.*

| Template | Name | Content | Frequency |
|----------|------|---------|-----------|
| **CAP24.01** | IMA Overview | Summary of IMA capital by trading desk | Quarterly |
| **CAP24.02** | IMA Details | Detailed breakdown by risk class | Quarterly |
| **CAP24.03** | Backtesting and PLAT | Back-testing and P&L Attribution Test results | Quarterly |
| **CAP25.01-10** | ASA Templates | Alternative Standardised Approach (parallel run) | Quarterly |

### 7.3 CAP24.03 - Backtesting Template Structure

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     CAP24.03 - BACKTESTING AND PLAT TEMPLATE                            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  SECTION A: ENTITY-LEVEL BACKTESTING                                                    │
│  ───────────────────────────────────────────────────────────────────────────────────    │
│  • VaR (99%, 1-day) for each of 250 observation dates (T+0 to T+249)                    │
│  • Hypothetical P&L for each observation date                                           │
│  • Actual P&L for each observation date                                                 │
│  • Exception flag (Y/N) for each date                                                   │
│  • Rolling exception count                                                              │
│  • Zone classification (GREEN/YELLOW/RED)                                               │
│  • Capital multiplier applied                                                           │
│                                                                                         │
│  SECTION B: TRADING DESK-LEVEL BACKTESTING                                              │
│  ───────────────────────────────────────────────────────────────────────────────────    │
│  For each trading desk with IMA approval:                                               │
│  • Desk identifier                                                                      │
│  • VaR for each observation date                                                        │
│  • P&L (Hypothetical and Actual)                                                        │
│  • Exception count                                                                      │
│  • P&L Attribution Test results (PLAT)                                                  │
│  • Desk eligibility status                                                              │
│                                                                                         │
│  SECTION C: P&L ATTRIBUTION TEST (PLAT)                                                 │
│  ───────────────────────────────────────────────────────────────────────────────────    │
│  • Risk-theoretical P&L vs. Hypothetical P&L                                            │
│  • Spearman correlation coefficient                                                     │
│  • Kolmogorov-Smirnov test statistic                                                    │
│  • PLAT zone (GREEN/AMBER/RED)                                                          │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 8. Immediate Exception Notification

### 8.1 Notification Process

When a backtesting exception occurs, the following process applies:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     BACKTESTING EXCEPTION NOTIFICATION PROCESS                          │
│                     (CRR Article 366(4) - ≤5 Working Days)                              │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  DAY T: Exception Detected                                                              │
│  ───────────────────────────────────────────────────────────────────────────────────    │
│  • Daily backtesting identifies |P&L| > VaR                                             │
│  • RAV flags exception in daily VaR report                                              │
│  • Exception logged in backtesting register                                             │
│                                                                                         │
│  DAY T+1: Root Cause Analysis Initiated                                                 │
│  ───────────────────────────────────────────────────────────────────────────────────    │
│  • RAV performs initial P&L attribution                                                 │
│  • Price source analysis (genuine vs. noise)                                            │
│  • Market move analysis                                                                 │
│                                                                                         │
│  DAY T+2: Exception Classification                                                      │
│  ───────────────────────────────────────────────────────────────────────────────────    │
│  • Classify as: Genuine / Price Source / Data Error / Exceptional Event                 │
│  • Document root cause findings                                                         │
│  • Head of RAV review and sign-off                                                      │
│                                                                                         │
│  DAY T+3: Notification Preparation                                                      │
│  ───────────────────────────────────────────────────────────────────────────────────    │
│  • Regulatory Reporting prepares PRA notification                                       │
│  • Head of Market Risk review                                                           │
│  • Draft notification includes:                                                         │
│    - Exception date                                                                     │
│    - VaR amount and P&L amount                                                          │
│    - Root cause summary                                                                 │
│    - Updated rolling exception count                                                    │
│    - Zone status and any multiplier change                                              │
│                                                                                         │
│  DAY T+4: Approval and Submission                                                       │
│  ───────────────────────────────────────────────────────────────────────────────────    │
│  • CRO (or delegate) approval                                                           │
│  • Submission to PRA via designated channel                                             │
│  • Confirmation receipt logged                                                          │
│                                                                                         │
│  DAY T+5: DEADLINE                                                                      │
│  ───────────────────────────────────────────────────────────────────────────────────    │
│  • Regulatory deadline for notification                                                 │
│  • Buffer day for any delays                                                            │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 8.2 Notification Content

| Field | Description | Example |
|-------|-------------|---------|
| **Entity** | Legal entity name | Meridian Bank UK |
| **Exception Date** | Date of the exception | 14 January 2025 |
| **VaR (T-1)** | Predicted VaR | $8.5M |
| **Hypothetical P&L** | Clean P&L | -$10.2M |
| **Actual P&L** | Dirty P&L | -$12.5M |
| **Exception Type** | Classification | Genuine / Price Source / Other |
| **Root Cause Summary** | Brief explanation | Emerging market FX moves exceeded historical scenarios |
| **Rolling Exception Count** | Updated count | 4 (Hypothetical), 5 (Actual) |
| **Zone Status** | Current zone | GREEN (Hypothetical), YELLOW (Actual) |
| **Multiplier Impact** | If zone changes | No change / Increased to 3.40x |

### 8.3 Escalation for Zone Changes

| Scenario | Escalation | Timeline |
|----------|------------|----------|
| Exception within GREEN zone | Standard notification | ≤5 working days |
| Exception moving to YELLOW zone | CRO notification; enhanced analysis | ≤3 working days |
| Exception moving to RED zone | CRO + Board notification; PRA call | Immediate (same day) |

---

## 9. Quarterly Submission Process

### 9.1 Data Sources and Reconciliation

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     QUARTERLY COREP DATA FLOW                                           │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  SOURCE SYSTEMS                    RECONCILIATION                    COREP TEMPLATES    │
│                                                                                         │
│  ┌─────────────────┐                                                                    │
│  │   RISK ODS      │─────┐                                                              │
│  │  • VaR          │     │                                                              │
│  │  • SVaR         │     │       ┌─────────────────────────┐       ┌─────────────────┐  │
│  │  • IRC          │     ├──────▶│  RECONCILIATION LAYER   │──────▶│  C 24.00        │  │
│  └─────────────────┘     │       │                         │       │  MKR IM         │  │
│                          │       │  • Risk vs. Finance     │       └─────────────────┘  │
│  ┌─────────────────┐     │       │  • VaR vs. Capital      │                            │
│  │   P&L ODS       │─────┤       │  • Exception count      │       ┌─────────────────┐  │
│  │  • Hypo P&L     │     │       │    reconciliation       │──────▶│  CAP24.03       │  │
│  │  • Actual P&L   │     │       │  • Data quality checks  │       │  Backtesting    │  │
│  └─────────────────┘     │       │                         │       └─────────────────┘  │
│                          │       │                         │                            │
│  ┌─────────────────┐     │       │                         │       ┌─────────────────┐  │
│  │  BACKTESTING    │─────┤       │                         │──────▶│  C 02.00        │  │
│  │  REGISTER       │     │       │                         │       │  Own Funds Req  │  │
│  │  • Exceptions   │     │       └─────────────────────────┘       └─────────────────┘  │
│  │  • Zone status  │     │                                                              │
│  └─────────────────┘     │                                                              │
│                          │                                                              │
│  ┌─────────────────┐     │                                                              │
│  │  FINANCE GL     │─────┘                                                              │
│  │  • Capital      │                                                                    │
│  │  • RWA          │                                                                    │
│  └─────────────────┘                                                                    │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Key Reconciliation Points

| Reconciliation | Source 1 | Source 2 | Tolerance | Owner |
|----------------|----------|----------|-----------|-------|
| VaR to Capital | Risk ODS | Finance GL | $100k | RAV |
| Exception count | Backtesting Register | Daily Reports | Zero | RAV |
| SVaR to VaR ratio | Risk ODS | Prior quarter | ±20% | RMA |
| Trading desk count | Risk Engine | COREP prior | Explain changes | Regulatory Reporting |

### 9.3 Quality Assurance Checks

| Check | Description | Owner | Timing |
|-------|-------------|-------|--------|
| **Completeness** | All desks/entities included | Regulatory Reporting | Week 1 |
| **Accuracy** | Values match source systems | RAV | Week 2 |
| **Consistency** | Quarter-on-quarter trends logical | Market Risk | Week 2 |
| **Timeliness** | Submitted before deadline | Regulatory Reporting | Week 4 |
| **Reconciliation** | Ties to Finance capital numbers | Finance | Week 3 |

---

## 10. Roles and Responsibilities

### 10.1 RACI Matrix

| Activity | RAV | Reg Reporting | Market Risk | Finance | CRO |
|----------|:---:|:-------------:|:-----------:|:-------:|:---:|
| Daily backtesting | R/A | I | I | - | I |
| Exception root cause | R | I | C | - | I |
| Immediate notification | C | R | C | - | A |
| COREP data extraction | R | C | I | I | - |
| COREP reconciliation | C | R | C | R | I |
| COREP template completion | I | R/A | C | C | I |
| Quarterly sign-off | I | R | C | C | A |
| PRA submission | I | R/A | I | I | I |
| Regulatory queries | C | R | C | C | A |

**R** = Responsible, **A** = Accountable, **C** = Consulted, **I** = Informed

### 10.2 Sign-off Authority

| Report Type | Preparer | Reviewer | Approver |
|-------------|----------|----------|----------|
| Daily exception notification | RAV Analyst | Head of RAV | CRO (delegate) |
| Quarterly COREP | Reg Reporting Analyst | Head of Reg Reporting | CFO / CRO |
| Annual Pillar 3 | Reg Reporting | Head of Market Risk | CRO + Board Risk Committee |

---

## 11. Controls

| Control ID | Control | Type | Owner |
|------------|---------|------|-------|
| RR-C01 | Backtesting exceptions notified to PRA within 5 working days | Preventive | Regulatory Reporting |
| RR-C02 | Quarterly COREP submitted within 30 business days | Preventive | Regulatory Reporting |
| RR-C03 | Four-eyes review of all regulatory submissions | Detective | Regulatory Reporting |
| RR-C04 | Reconciliation to Finance GL before submission | Detective | Finance |
| RR-C05 | Variance analysis vs. prior quarter documented | Detective | Market Risk |
| RR-C06 | Audit trail maintained for all submissions | Detective | Regulatory Reporting |
| RR-C07 | Submission confirmation receipt logged | Detective | Regulatory Reporting |
| RR-C08 | Regulatory query response within SLA | Preventive | Regulatory Reporting |
| RR-C09 | Annual attestation of reporting accuracy | Preventive | CRO |
| RR-C10 | Regulatory reporting calendar maintained and monitored | Preventive | Regulatory Reporting |

---

## 12. Service Levels

| Metric | Target | Threshold | Escalation |
|--------|--------|-----------|------------|
| Exception notification | ≤4 working days | 5 working days (regulatory limit) | Head of Reg Reporting |
| COREP submission | T+25 business days | T+30 (regulatory limit) | CFO |
| Reconciliation completion | T+15 business days | T+20 | Head of RAV |
| Regulatory query response | 5 business days | 10 business days | CRO |
| Resubmission (if required) | 3 business days | 5 business days | Head of Reg Reporting |

---

## 13. Exception Handling

### 13.1 Submission Delays

| Scenario | Action | Authority | Notification |
|----------|--------|-----------|--------------|
| Data quality issue | Fix and resubmit | Head of Reg Reporting | PRA if deadline at risk |
| System failure | BCP procedures; manual submission | Head of Reg Reporting | PRA proactive notification |
| Deadline miss | Immediate PRA notification; remediation plan | CRO | PRA same day |

### 13.2 Resubmission Triggers

| Trigger | Threshold | Action |
|---------|-----------|--------|
| Material error discovered | >$1M impact on capital | Resubmit with explanation |
| PRA query identifies issue | Any material finding | Resubmit within agreed timeframe |
| Reconciliation break | >$500k unexplained | Investigate; resubmit if required |

---

## 14. Regulatory Engagement

### 14.1 Routine Engagement

| Activity | Frequency | Participants | Purpose |
|----------|-----------|--------------|---------|
| PRA supervisory meeting | Quarterly | CRO, Head of Market Risk, Reg Reporting | Discuss risk profile, upcoming changes |
| Model change notifications | As required | RMA, Reg Reporting | Pre-notification of material changes |
| Annual IMA review | Annual | Market Risk, RMA, PRA | Assess ongoing IMA eligibility |

### 14.2 Ad-Hoc Requests

| Request Type | Typical Turnaround | Owner |
|--------------|-------------------|-------|
| Data request | 5-10 business days | Regulatory Reporting |
| Methodology query | 5-10 business days | RMA |
| Stress test submission | Per PRA schedule | Stress Testing Team |
| Thematic review | As specified | Relevant team |

---

## 15. Systems and Tools

### 15.1 Regulatory Reporting Platform

| System | Function | Owner |
|--------|----------|-------|
| **RegData** | PRA submission portal | PRA (external) |
| **Axiom** (or similar) | COREP template preparation and validation | Regulatory Reporting |
| **Risk Reporting DataMart** | Source data for reports | Risk Technology |
| **Backtesting Register** | Exception tracking and history | RAV |

### 15.2 Data Quality Controls

| Check | System | Frequency |
|-------|--------|-----------|
| Schema validation | Axiom | Each submission |
| Business rule validation | Axiom | Each submission |
| Cross-template consistency | Axiom | Each submission |
| Historical trend analysis | DataMart | Quarterly |

---

## 16. Related Documents

| Document | Relationship |
|----------|--------------|
| [Market Risk Process Orchestration](./market-risk-process-orchestration.md) | Parent orchestration |
| [VaR Backtesting](./backtesting.md) | Source of exception data |
| [Risk Engine Calculation](./risk-engine-calculation.md) | Source of VaR/SVaR/IRC |
| [VaR Limit Framework](../L3-Governance/policies/var-limit-framework.md) | Limit structure context |
| [Market Risk Policy](../L3-Governance/policies/market-risk-policy.md) | Governance framework |

---

## 17. Document Control

### 17.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-15 | Initial version | MLRC |
| 1.1 | 2025-01-15 | Added Own Funds Calculation, Pillar 3 Disclosure, Model Change Notification sections | MLRC |
| 1.2 | 2025-01-15 | Updated Basel 3.1/FRTB dates (2027/2028); added 15-day parallel run requirement for model changes; fixed diagram | MLRC |
| 1.3 | 2025-01-15 | Corrected non-material change process: PRA pre-notification with 10 business day review period (not post-implementation) | MLRC |
| 1.4 | 2025-01-15 | Clarified parallel run risk numbers (VaR/SVaR same model; IRC separate model, only if affected); added 5% aggregate threshold; added CRR Article 364 references | MLRC |

---

*End of Document*
