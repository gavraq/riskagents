---
# Control Metadata
control_id: MR-L5-002
control_name: Scenario Stress Limits Controls
version: 1.1
effective_date: 2025-01-15
next_review_date: 2026-01-15
owner: Head of Market Risk
approving_committee: MLRC

# Taxonomy Linkages
parent_process: MR-L4-011  # Stress Testing
parent_framework: MR-L3-003  # VaR Limit Framework
l1_requirements:
  - REQ-L1-001  # CRR (UK)
  - REQ-L1-003  # FRTB
  - REQ-L1-004  # Basel III/IV
  - REQ-L1-005  # PRA Rulebook
l2_risk_types:
  - MR-L2-001   # Market Risk
l3_governance:
  - MR-L3-001   # Market Risk Policy
  - MR-L3-003   # VaR Limit Framework
l4_processes:
  - MR-L4-011   # Stress Testing
  - MR-L4-013   # Market Risk Limits Management
l6_models:
  - MR-L6-003   # Scenario Stress Testing Model
l7_systems:
  - SYS-MR-001  # Risk Engine (FMDM)
  - SYS-MR-004  # Risk Reporting DataMart
---

# Scenario Stress Limits Controls

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Control ID** | MR-L5-002 |
| **Version** | 1.1 |
| **Effective Date** | 15 January 2025 |
| **Parent Framework** | VaR Limit Framework (MR-L3-003) |
| **Owner** | Head of Market Risk |

---

## 1. Purpose

This document defines the controls for scenario stress testing limits. Unlike VaR/SVaR (which are model-based statistical measures covered in MR-L5-001), scenario stress testing applies defined shocks to risk factors to assess potential losses under specific adverse conditions. These controls ensure stress losses remain within approved appetite and that the scenario library remains relevant.

---

## 2. Scope

### 2.1 Relationship to VaR/SVaR

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  MARKET RISK LIMIT FRAMEWORK                                                            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────────────────┐    ┌─────────────────────────────────────┐ │
│  │     STATISTICAL MEASURES (MR-L5-001)    │    │   SCENARIO MEASURES (MR-L5-002)     │ │
│  │                                         │    │                                     │ │
│  │  VaR: Current market conditions         │    │  Historical Scenarios:              │ │
│  │  • 99%, 1-day, rolling 500 days         │    │  • GFC 2008-09                      │ │
│  │                                         │    │  • COVID-19 2020                    │ │
│  │  SVaR: Stressed market conditions       │    │  • Eurozone Crisis 2011             │ │
│  │  • 99%, 1-day, 2008-09 period           │    │                                     │ │
│  │                                         │    │  Hypothetical Scenarios:            │ │
│  │  Same model, different observation      │    │  • Rates +200bp                     │ │
│  │  periods                                │    │  • Credit spreads +300bp            │ │
│  │                                         │    │  • EM Crisis                        │ │
│  │                                         │    │                                     │ │
│  │  PURPOSE: Day-to-day risk monitoring    │    │  PURPOSE: Tail risk assessment      │ │
│  └─────────────────────────────────────────┘    └─────────────────────────────────────┘ │
│                                                                                         │
│  Note: SVaR/VaR limits are controlled in MR-L5-001                                      │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Scenario Types

| Category | Description | Frequency | Purpose |
|----------|-------------|-----------|---------|
| **Historical** | Replay of actual market events | Weekly | Understand portfolio behavior in past crises |
| **Hypothetical** | Designed shocks to specific factors | Weekly | Test specific vulnerabilities |
| **Pillar/Regulatory** | PRA-mandated macroeconomic scenarios | Annual + Ad-hoc | Capital planning and regulatory stress tests |
| **Reverse** | Find scenarios that would cause specific loss | Quarterly | Identify hidden risks |

### 2.3 Scenario Stress Limits (Entity Level)

| Scenario | Limit ($m) | Warning ($m) |
|----------|------------|--------------|
| **Global Financial Crisis** | 190 | 150 |
| **COVID-19 Shock** | 125 | 100 |
| **Rates +200bp** | 100 | 80 |
| **EM Crisis** | 95 | 75 |
| **Credit Spread +300bp** | 110 | 90 |
| **Worst-of Pillar Scenarios** | 190 | 150 |

---

## 3. Scenario Library

### 3.1 Historical Scenarios

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  HISTORICAL SCENARIO LIBRARY                                                            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐   │
│  │  GFC 2008-09 (Global Financial Crisis)                                           │   │
│  │  ────────────────────────────────────────────────────────────────────────────────│   │
│  │  Period: Sep 2008 - Mar 2009                                                     │   │
│  │  Key events: Lehman default, credit freeze, flight to quality                    │   │
│  │  Key shocks:                                                                     │   │
│  │  • Credit spreads: IG +350bp, HY +1500bp                                         │   │
│  │  • Rates: G10 rates -150bp                                                       │   │
│  │  • Equities: -50%                                                                │   │
│  │  • FX: EM currencies -25%                                                        │   │
│  │  • Volatility: VIX +300%                                                         │   │
│  └──────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                         │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐   │
│  │  COVID-19 2020                                                                   │   │
│  │  ────────────────────────────────────────────────────────────────────────────────│   │
│  │  Period: Feb 2020 - Mar 2020                                                     │   │
│  │  Key events: Global pandemic, lockdowns, coordinated policy response             │   │
│  │  Key shocks:                                                                     │   │
│  │  • Equities: -35%                                                                │   │
│  │  • Credit spreads: IG +200bp, HY +700bp                                          │   │
│  │  • Rates: G10 rates -100bp (to floor)                                            │   │
│  │  • Oil: -70%                                                                     │   │
│  │  • Volatility: VIX +400%                                                         │   │
│  └──────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                         │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐   │
│  │  Eurozone Crisis 2011                                                            │   │
│  │  ────────────────────────────────────────────────────────────────────────────────│   │
│  │  Period: Jul 2011 - Nov 2011                                                     │   │
│  │  Key events: Peripheral sovereign stress, bank contagion                         │   │
│  │  Key shocks:                                                                     │   │
│  │  • Peripheral spreads: +500bp                                                    │   │
│  │  • EUR: -15%                                                                     │   │
│  │  • European banks: -40%                                                          │   │
│  │  • European rates: Core -50bp, Periphery +200bp                                  │   │
│  └──────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                         │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐   │
│  │  Taper Tantrum 2013                                                              │   │
│  │  ────────────────────────────────────────────────────────────────────────────────│   │
│  │  Period: May 2013 - Aug 2013                                                     │   │
│  │  Key events: Fed signaling QE tapering, EM outflows                              │   │
│  │  Key shocks:                                                                     │   │
│  │  • US rates: +100bp                                                              │   │
│  │  • EM currencies: -15%                                                           │   │
│  │  • EM rates: +200bp                                                              │   │
│  │  • EM equities: -20%                                                             │   │
│  └──────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Hypothetical Scenarios

| Scenario | Key Shocks | Target Risk |
|----------|------------|-------------|
| **Rates +200bp** | Parallel rate shock across all curves | Duration risk |
| **Rates -100bp** | Parallel rate decline (floored at 0) | Negative convexity |
| **Credit Spread +100bp** | IG spread widening | Credit spread risk |
| **Credit Spread +300bp** | HY spread blowout | Tail credit risk |
| **FX EM Crisis** | 20% depreciation of EM currencies | EM FX exposure |
| **Equity Crash -30%** | Global equity decline | Equity delta |
| **Volatility Spike** | Vol +100% across asset classes | Vega exposure |
| **Curve Steepener** | 2s10s +100bp | Curve risk |
| **Curve Flattener** | 2s10s -100bp | Curve risk |

---

## 4. Control Objectives

| Objective ID | Objective | Risk Mitigated |
|--------------|-----------|----------------|
| **CO-01** | Scenario stress losses are monitored weekly against limits | Undetected tail risk exposure |
| **CO-02** | Scenario breaches are escalated appropriately | Delayed response to excess tail risk |
| **CO-03** | Scenario library remains relevant to current risks | Scenario obsolescence |
| **CO-04** | Pillar stress scenarios inform capital planning | Inadequate capital buffers |
| **CO-05** | Reverse stress testing identifies hidden vulnerabilities | Unknown concentration risk |

---

## 5. Control Inventory

### 5.1 Control Summary

| Control ID | Control Name | Type | Frequency | Owner |
|------------|--------------|------|-----------|-------|
| SS-C01 | Weekly Scenario Stress Run | Detective | Weekly | Market Risk |
| SS-C02 | Scenario Limit Monitoring | Detective | Weekly | Market Risk |
| SS-C03 | Scenario Warning Alert | Detective | On threshold | Market Risk |
| SS-C04 | Scenario Breach Escalation | Responsive | On breach | Market Risk |
| SS-C05 | Scenario Results Analysis | Detective | Weekly | Market Risk |
| SS-C06 | Scenario Library Relevance Review | Detective | Quarterly | Market Risk |
| SS-C07 | New Scenario Proposal Process | Preventive | Ad-hoc | Market Risk |
| SS-C08 | Pillar Stress Scenario Integration | Detective | Annual | Market Risk |
| SS-C09 | Reverse Stress Testing | Detective | Quarterly | Market Risk |
| SS-C10 | MLRC Stress Dashboard Review | Detective | Weekly | MLRC |

---

## 6. Control Details

### 6.1 SS-C01: Weekly Scenario Stress Run

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  CONTROL: SS-C01 - Weekly Scenario Stress Run                                           │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  OBJECTIVE: Calculate P&L impact under defined stress scenarios weekly                  │
│                                                                                         │
│  TYPE: Detective                                                                        │
│  FREQUENCY: Weekly (Friday COB positions, results Monday AM)                            │
│  OWNER: Market Risk                                                                     │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  PROCESS FLOW:                                                                          │
│                                                                                         │
│       Friday COB                    Weekend                     Monday                  │
│       ──────────                    ───────                     ──────                  │
│                                                                                         │
│       ┌────────────┐          ┌────────────┐          ┌────────────┐                    │
│       │  Position  │─────────▶│   Run All  │─────────▶│   QA and   │                    │
│       │  Snapshot  │          │  Scenarios │          │   Publish  │                    │
│       └────────────┘          └────────────┘          └────────────┘                    │
│              │                      │                       │                           │
│              ▼                      ▼                       ▼                           │
│       Extract from           Apply scenario            Review results                   │
│       Trading System         shocks to                 Generate report                  │
│       eg Murex               all positions             by 10:00 Monday                  │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  SCENARIOS RUN:                                                                         │
│  • All Historical Scenarios (4)                                                         │
│  • All Hypothetical Scenarios (9)                                                       │
│  • Current Pillar Scenarios (if active)                                                 │
│                                                                                         │
│  OUTPUT:                                                                                │
│  • P&L impact by scenario at Entity, Division, BU level                                 │
│  • Top 10 contributors to each scenario loss                                            │
│  • Comparison to limits with traffic light status                                       │
│                                                                                         │
│  EVIDENCE:                                                                              │
│  • Weekly Scenario Stress Report                                                        │
│  • Scenario results in Risk DataMart                                                    │
│  • MLRC presentation                                                                    │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 SS-C02: Scenario Limit Monitoring

| Attribute | Value |
|-----------|-------|
| **Control ID** | SS-C02 |
| **Objective** | Compare scenario stress losses against approved limits |
| **Type** | Detective |
| **Frequency** | Weekly |
| **Owner** | Market Risk |

**Control Activities**:
1. Compare each scenario P&L against corresponding limit
2. Calculate utilisation percentage for each scenario
3. Apply traffic light classification:
   - GREEN: 0-79% utilisation
   - AMBER: 80-99% utilisation (Warning)
   - RED: ≥100% utilisation (Breach)
4. Identify "worst-of" scenario (highest utilisation)
5. Flag scenarios approaching limits for MLRC attention

**Evidence**:
- Weekly Scenario Stress Report with scenario utilisation
- Scenario limit dashboard

### 6.3 SS-C03: Scenario Warning Alert

| Attribute | Value |
|-----------|-------|
| **Control ID** | SS-C03 |
| **Objective** | Alert stakeholders when scenario utilisation approaches limit |
| **Type** | Detective |
| **Frequency** | On threshold (≥80%) |
| **Owner** | Market Risk |

**Control Activities**:
1. Identify scenarios at AMBER status (80-99% utilisation)
2. Generate warning notification to:
   - Division Head
   - CRO
   - MLRC Chair
3. Include in weekly stress report with analysis of:
   - Key drivers
   - Positions contributing most to stress loss
   - Trend vs prior weeks
4. Assess whether limit increase or position reduction warranted

**Evidence**:
- Warning notification emails
- Weekly Stress Report "Watch List" section

### 6.4 SS-C04: Scenario Breach Escalation

| Attribute | Value |
|-----------|-------|
| **Control ID** | SS-C04 |
| **Objective** | Ensure scenario limit breaches are escalated appropriately |
| **Type** | Responsive |
| **Frequency** | On breach |
| **Owner** | Market Risk |

**Escalation Path**:

| Breach Severity | Escalate To | Timeline | Action Required |
|-----------------|-------------|----------|-----------------|
| **Warning (≥80%)** | MLRC | Weekly meeting | Enhanced monitoring; analysis |
| **Breach (≥100%)** | MLRC Chair, CRO | Same day | Present at next MLRC; reduction plan or limit increase request |
| **Severe Breach (≥120%)** | CRO, RMC | Immediate | Ad-hoc MLRC; RMC notification |

**Evidence**:
- Escalation emails
- MLRC minutes with scenario breach discussion

### 6.5 SS-C05: Scenario Results Analysis

| Attribute | Value |
|-----------|-------|
| **Control ID** | SS-C05 |
| **Objective** | Provide insight into stress vulnerabilities |
| **Type** | Detective |
| **Frequency** | Weekly |
| **Owner** | Market Risk |

**Control Activities**:
1. For each scenario, identify:
   - Top 5 desks contributing to loss
   - Top 10 positions by P&L impact
   - Risk factors driving loss (rates, credit, FX, etc.)
2. Compare results to prior week:
   - Identify significant changes
   - Explain drivers of change
3. Assess portfolio hedging effectiveness under stress
4. Identify emerging concentrations
5. Present findings to MLRC

**Evidence**:
- Weekly Scenario Analysis Report
- MLRC presentation

### 6.6 SS-C06: Scenario Library Relevance Review

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  CONTROL: SS-C06 - Scenario Library Relevance Review                                    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  OBJECTIVE: Ensure scenario library reflects current risk landscape                     │
│                                                                                         │
│  TYPE: Detective                                                                        │
│  FREQUENCY: Quarterly                                                                   │
│  OWNER: Market Risk                                                                     │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  REVIEW DIMENSIONS:                                                                     │
│                                                                                         │
│  1. PORTFOLIO COVERAGE                                                                  │
│     • Do scenarios stress all material risk factors in current portfolio?               │
│     • Are new products/exposures adequately captured?                                   │
│     • Have portfolio composition changes affected scenario relevance?                   │
│                                                                                         │
│  2. EMERGING RISKS                                                                      │
│     • Are there emerging risks not captured by current scenarios?                       │
│     • Geopolitical developments (wars, elections, sanctions)                            │
│     • Climate/transition risks                                                          │
│     • Technology/cyber risks                                                            │
│                                                                                         │
│  3. PEER BENCHMARKING                                                                   │
│     • What scenarios are peers running?                                                 │
│     • Regulatory expectations and industry standards                                    │
│                                                                                         │
│  4. SCENARIO EFFECTIVENESS                                                              │
│     • Are scenarios producing differentiated results?                                   │
│     • Are some scenarios no longer relevant?                                            │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  OUTPUT:                                                                                │
│  • Quarterly Scenario Relevance Review memo                                             │
│  • Recommendations for new/retired scenarios                                            │
│  • MLRC presentation and approval                                                       │
│                                                                                         │
│  EVIDENCE:                                                                              │
│  • Scenario Relevance Review memo                                                       │
│  • MLRC minutes with approval                                                           │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.7 SS-C07: New Scenario Proposal Process

| Attribute | Value |
|-----------|-------|
| **Control ID** | SS-C07 |
| **Objective** | Ensure new scenarios are properly designed and approved |
| **Type** | Preventive |
| **Frequency** | Ad-hoc |
| **Owner** | Market Risk |

**Proposal Requirements**:
1. Scenario name and description
2. Rationale (why is this scenario needed?)
3. Risk factors affected and calibration
4. Historical basis or hypothetical design
5. Expected portfolio impact (indicative)
6. Proposed limit (if applicable)
7. Run frequency

**Approval Path**:
- New historical/hypothetical scenario: MLRC
- New pillar scenario: RMC
- Retirement of existing scenario: MLRC

**Evidence**:
- New Scenario Proposal form
- MLRC/RMC approval minutes

### 6.8 SS-C08: Pillar Stress Scenario Integration

| Attribute | Value |
|-----------|-------|
| **Control ID** | SS-C08 |
| **Objective** | Integrate PRA pillar stress scenarios into market risk monitoring |
| **Type** | Detective |
| **Frequency** | Annual (aligned to ICAAP/stress testing cycle) |
| **Owner** | Market Risk |

**Control Activities**:
1. Receive updated pillar stress scenarios from Enterprise Risk
2. Translate macro scenarios to market risk factor shocks:
   - Interest rates (by curve and tenor)
   - Credit spreads (by rating and sector)
   - FX rates
   - Equity indices
   - Commodity prices
   - Volatilities
3. Calculate trading book P&L under pillar scenarios
4. Compare results to scenario stress limits
5. Feed results into ICAAP capital planning
6. Present to RMC as part of annual stress testing

**Evidence**:
- Pillar stress scenario calibration document
- Trading book stress results
- ICAAP contribution

### 6.9 SS-C09: Reverse Stress Testing

| Attribute | Value |
|-----------|-------|
| **Control ID** | SS-C09 |
| **Objective** | Identify scenarios that could cause severe losses |
| **Type** | Detective |
| **Frequency** | Quarterly |
| **Owner** | Market Risk |

**Control Activities**:
1. Define "breaking point" thresholds:
   - Entity P&L loss of $150m (3× VaR limit)
   - Capital depletion >25% of trading book capital
2. Work backwards to identify scenarios that would cause such losses:
   - What combination of market moves?
   - What concentrations would need to exist?
   - What correlations would need to break down?
3. Assess plausibility of identified scenarios
4. Identify risk mitigations if plausible
5. Present to MLRC and RMC

**Evidence**:
- Quarterly Reverse Stress Test Report
- MLRC/RMC presentation

### 6.10 SS-C10: MLRC Stress Dashboard Review

| Attribute | Value |
|-----------|-------|
| **Control ID** | SS-C10 |
| **Objective** | Governance oversight of scenario stress framework |
| **Type** | Detective |
| **Frequency** | Weekly |
| **Owner** | MLRC |

**Control Activities**:
1. Market Risk presents stress dashboard to MLRC
2. Review includes:
   - Scenario stress results vs limits (all scenarios)
   - Week-on-week changes and drivers
   - Worst-of scenario analysis
   - Emerging risk assessment
   - Scenario library status
3. MLRC challenges assumptions and approves actions
4. Decisions minuted

**Evidence**:
- MLRC agenda and pack
- MLRC minutes

---

## 7. Scenario Stress Dashboard

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                    MERIDIAN GLOBAL BANK - SCENARIO STRESS DASHBOARD                     │
│                                   Week Ending: [Date]                                   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  HISTORICAL SCENARIOS (Entity Level)                                                    │
│  ────────────────────────────────────                                                   │
│  │  Scenario              │   Loss ($m)  │   Limit  │   Util   │  Status │  WoW       │ │
│  ├────────────────────────┼──────────────┼──────────┼──────────┼─────────┼────────────│ │
│  │  GFC 2008-09           │    142.5     │   190    │   75%    │   🟢    │   +2.3%    │ │
│  │  COVID-19 2020         │     98.2     │   125    │   79%    │   🟢    │   -1.5%    │ │
│  │  Eurozone Crisis 2011  │     65.1     │   N/A    │   N/A    │   🟢    │   +0.8%    │ │
│  │  Taper Tantrum 2013    │     48.3     │   N/A    │   N/A    │   🟢    │   -2.1%    │ │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  HYPOTHETICAL SCENARIOS (Entity Level)                                                  │
│  ──────────────────────────────────────                                                 │
│  │  Scenario              │   Loss ($m)  │   Limit  │   Util   │  Status │  WoW       │ │
│  ├────────────────────────┼──────────────┼──────────┼──────────┼─────────┼────────────│ │
│  │  Rates +200bp          │     82.5     │   100    │   83%    │   🟡    │   +5.2%    │ │
│  │  Rates -100bp          │     35.2     │   N/A    │   N/A    │   🟢    │   -1.8%    │ │
│  │  Credit Spread +100bp  │     42.1     │   N/A    │   N/A    │   🟢    │   +0.5%    │ │
│  │  Credit Spread +300bp  │     95.3     │   110    │   87%    │   🟡    │   +3.2%    │ │
│  │  FX EM Crisis          │     71.8     │    95    │   76%    │   🟢    │   +1.1%    │ │
│  │  Equity Crash -30%     │     28.5     │   N/A    │   N/A    │   🟢    │   -0.3%    │ │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  WATCH LIST (Scenarios at >80% utilisation)                                             │
│  ──────────────────────────────────────────                                             │
│  • Rates +200bp: 83% - Driven by increased duration in Rates Trading desk               │
│  • Credit Spread +300bp: 87% - HY portfolio growth over past month                      │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  WORST-OF ANALYSIS                                                                      │
│  ─────────────────                                                                      │
│  Worst-of scenario: GFC 2008-09 at $142.5m loss (75% of $190m limit)                    │
│                                                                                         │
│  Key drivers of GFC scenario loss:                                                      │
│  1. Credit Trading desk: $58m (41%)                                                     │
│  2. Rates Trading desk: $42m (29%)                                                      │
│  3. FX Trading desk: $28m (20%)                                                         │
│  4. Treasury: $14.5m (10%)                                                              │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 8. Control Testing Schedule

| Control | Test Frequency | Test Type | Tester |
|---------|---------------|-----------|--------|
| SS-C01 | Quarterly | Process review | Internal Audit |
| SS-C02 | Quarterly | Sample testing | Internal Audit |
| SS-C03 | Semi-annually | Alert test | Market Risk |
| SS-C04 | Semi-annually | Scenario test | Operational Risk |
| SS-C05 | Quarterly | Sample review | Internal Audit |
| SS-C06 | Annually | Full review | Model Risk |
| SS-C07 | As needed | Process review | Internal Audit |
| SS-C08 | Annually | Process review | Enterprise Risk |
| SS-C09 | Semi-annually | Methodology review | Model Risk |
| SS-C10 | Ongoing | Attendance/minutes | MLRC Secretary |

---

## 9. Key Risk Indicators (KRIs)

| KRI ID | Indicator | Threshold | Escalation |
|--------|-----------|-----------|------------|
| KRI-SS-01 | Scenario limit breaches per quarter | >2 | RMC |
| KRI-SS-02 | Scenarios at >80% utilisation | >3 | MLRC |
| KRI-SS-03 | Worst-of scenario utilisation | >90% | CRO |
| KRI-SS-04 | Scenario library unchanged | >12 months | MLRC |
| KRI-SS-05 | Reverse stress test findings unaddressed | >90 days | RMC |

---

## 10. Related Controls

| Control ID | Control Name | Relationship |
|------------|--------------|--------------|
| MR-L5-001 | VaR and SVaR Limits Controls | Complementary - statistical risk measures |
| MR-L5-003 | Sensitivity Limit Controls | Related - factor-level limits |
| MR-L5-005 | Concentration Limits Controls | Related - concentration may drive stress losses |
| MR-L5-006 | Stop-Loss Controls | Complementary - P&L-based limits |

---

## 11. Document Control

### 11.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-15 | Initial version | MLRC |
| 1.1 | 2025-01-15 | Refocused on scenario stress only (SVaR moved to MR-L5-001); updated currency to USD | MLRC |

### 11.2 Review Schedule

- Full review: Annually (January)
- Scenario library: Quarterly
- Post-incident: Following any stress event

---

*End of Document*
