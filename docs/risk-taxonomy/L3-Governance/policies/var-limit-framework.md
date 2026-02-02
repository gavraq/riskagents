---
# Framework Metadata (for policy-updater skill)
framework_id: MR-L3-003
framework_name: VaR Limit Framework
version: 1.1
effective_date: 2025-01-15
next_review_date: 2026-01-15
owner: Head of Market Risk
approving_committee: RMC

# Taxonomy Linkages
parent_policy: MR-L3-001  # Market Risk Policy
l1_requirements:
  - REQ-L1-001  # CRR
  - REQ-L1-003  # FRTB
l2_risk_types:
  - MR-L2-001   # Market Risk
l5_controls:
  - MR-L5-001   # VaR Limits
  - MR-L5-002   # Stress Limits
  - MR-L5-003   # Sensitivity Limits
  - MR-L5-004   # Backtesting Limits
  - MR-L5-005   # Concentration Limits
  - MR-L5-006   # Stop-Loss Limits
l6_models:
  - MR-L6-001   # VaR Model
---

# VaR Limit Framework

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Framework ID** | MR-L3-003 |
| **Version** | 1.1 |
| **Effective Date** | 15 January 2025 |
| **Parent Policy** | Market Risk Policy (MR-L3-001) |
| **Owner** | Head of Market Risk |

---

## 1. Purpose

This Framework establishes the detailed limit structure for Value at Risk (VaR) and related market risk metrics at Meridian Global Bank. It operationalises the risk appetite set out in the Market Risk Policy.

---

## 2. Limit Hierarchy
<!-- L5: MR-L5-001 -->

### 2.1 Structure Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        ENTITY VaR LIMIT                                 │
│                          $25m (99%, 1-day)                              │
│                        Approved by: Board/RMC                           │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│    MARKETS      │      │    TREASURY     │      │    RESERVE      │
│    $19m         │      │    $6m          │      │    $3m          │
│    (RMC)        │      │    (RMC)        │      │    (Unallocated)│
└────────┬────────┘      └────────┬────────┘      └─────────────────┘
         │                        │
    ┌────┴────┬──────┐           │
    │         │      │           │
    ▼         ▼      ▼           ▼
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│ Rates │ │  FX   │ │Credit │ │Treasury│
│ $12m  │ │ $8m   │ │ $6m   │ │ $6m   │
│(MLRC) │ │(MLRC) │ │(MLRC) │ │(MLRC) │
└───┬───┘ └───┬───┘ └───┬───┘ └───────┘
    │         │         │
    ▼         ▼         ▼
┌───────┐ ┌───────┐ ┌───────┐
│Desk 1 │ │Desk 1 │ │Desk 1 │
│ $6m   │ │ $5m   │ │ $3m   │
└───────┘ └───────┘ └───────┘
┌───────┐ ┌───────┐ ┌───────┐
│Desk 2 │ │Desk 2 │ │Desk 2 │
│ $6m   │ │ $3m   │ │ $3m   │
└───────┘ └───────┘ └───────┘
```

**Note**: Sum of sub-limits exceeds parent due to diversification benefit assumption.

### 2.2 Limit Table

| Level | Entity | VaR Limit ($m) | Approval |
|-------|--------|----------------|----------|
| **Entity** | Meridian Global Bank | 25.0 | Board/RMC |
| **Division** | Markets | 19.0 | RMC |
| | Treasury | 6.0 | RMC |
| | Reserve (unallocated) | 3.0 | RMC |
| **Business Unit** | Rates Trading | 12.0 | MLRC |
| | FX Trading | 8.0 | MLRC |
| | Credit Trading | 6.0 | MLRC |
| | Treasury | 6.0 | MLRC |
| **Desk** | Rates - G10 Swaps | 6.0 | MLRC |
| | Rates - EM Rates | 4.0 | MLRC |
| | Rates - Options | 2.0 | MLRC |
| | FX - G10 Spot | 4.0 | MLRC |
| | FX - EM | 3.0 | MLRC |
| | FX - Options | 1.0 | MLRC |
| | Credit - IG | 3.0 | MLRC |
| | Credit - HY | 2.0 | MLRC |
| | Credit - EM | 1.0 | MLRC |

---

## 3. Limit Types
<!-- L5: MR-L5-001 through MR-L5-006 -->

### 3.1 VaR Limits (MR-L5-001)

| Metric | Parameters | Entity Limit | Warning |
|--------|------------|--------------|---------|
| **Daily VaR** | 99%, 1-day, HS | $25m | $20m (80%) |
| **10-day VaR** | 99%, 10-day, HS | $79m | $63m (80%) |

### 3.2 Stressed VaR Limits (MR-L5-002)

| Metric | Parameters | Entity Limit | Warning |
|--------|------------|--------------|---------|
| **Stressed VaR** | 99%, 1-day, 2008-09 | $50m | $40m (80%) |
| **Stressed VaR 10-day** | 99%, 10-day, 2008-09 | $158m | $125m (80%) |

### 3.3 Stress Loss Limits (MR-L5-002)

| Scenario | Entity Limit | Warning |
|----------|--------------|---------|
| Global Financial Crisis | $190m | $150m |
| COVID-19 Shock | $125m | $100m |
| Rates +200bp | $100m | $80m |
| EM Crisis | $95m | $75m |
| Worst-of Pillar Scenarios | $190m | $150m |

### 3.4 Sensitivity Limits (MR-L5-003)

| Sensitivity | Metric | Entity Limit |
|-------------|--------|--------------|
| **DV01** | $/bp | $625k |
| **CS01** | $/bp | $375k |
| **Vega** | $/%vol | $250k |
| **FX Delta** | $/% | $6m |
| **Equity Delta** | $/% | $2.5m |

### 3.5 Concentration Limits (MR-L5-005)

| Type | Metric | Limit |
|------|--------|-------|
| **Single Issuer** | % of Trading Book VaR | 15% |
| **Single Currency** | % of FX VaR | 30% |
| **Single Curve** | % of IR VaR | 25% |
| **Position vs ADV** | % of 30-day ADV | 10% |

### 3.6 Stop-Loss Limits (MR-L5-006)

| Level | Daily Stop-Loss | MTD Stop-Loss |
|-------|-----------------|---------------|
| Desk | 1.5x VaR limit | 3x VaR limit |
| Business Unit | 2x VaR limit | 4x VaR limit |
| Entity | N/A | $75m |

---

## 4. Limit Monitoring
<!-- L4: MR-L4-005 -->

### 4.1 Monitoring Frequency

| Limit Type | Frequency | Source System |
|------------|-----------|---------------|
| VaR | Daily (T+1) | FMDM |
| Stressed VaR | Daily (T+1) | FMDM |
| Sensitivities | Intraday (hourly) | Murex |
| Stress Limits | Weekly | FMDM |
| Concentration | Daily | FMDM |
| Stop-Loss | Intraday (hourly) | Murex/Finance |

### 4.2 Traffic Light System

| Utilisation | Status | Colour | Action |
|-------------|--------|--------|--------|
| 0-79% | Normal | 🟢 Green | Normal operations |
| 80-99% | Warning | 🟡 Amber | MLRC notification; heightened monitoring |
| 100-109% | Breach | 🔴 Red | Immediate escalation; action plan required |
| ≥110% | Critical | ⚫ Black | CRO escalation; RMC notification |

### 4.3 Dashboard Reporting

Daily VaR Dashboard includes:
- Entity VaR vs limit (with trend)
- Division breakdown with utilisation %
- Desk-level heatmap
- Backtesting P&L vs VaR chart
- Top 5 risk contributors
- Limit breach summary

---

## 5. Limit Breach Management
<!-- L4: MR-L4-006 -->

### 5.1 Breach Classification

| Type | Definition | Response Time |
|------|------------|---------------|
| **Technical Breach** | Data/system error causing apparent breach | Investigate immediately; resolve within 4 hours |
| **Passive Breach** | Market movement caused breach (no new risk) | Action plan within 24 hours |
| **Active Breach** | New position caused breach | Immediate escalation; position reduction required |

### 5.2 Escalation Matrix

| Breach Level | Escalate To | Timeline | Required Action |
|--------------|-------------|----------|-----------------|
| Desk limit | Business Unit Head + Market Risk | Immediate | Reduce risk or request temporary excess |
| BU limit | Trading Head + MLRC Chair | Immediate | MLRC approval for excess or reduction plan |
| Division limit | CRO + MLRC | Immediate | Reduction plan or RMC escalation |
| Entity limit | CRO + RMC Chair + Board Risk | Immediate | Emergency RMC; formal reduction plan |

### 5.3 Temporary Excess Process

| Authority | Max Excess | Max Duration | Conditions |
|-----------|------------|--------------|------------|
| MLRC | 10% | 5 business days | Documented rationale; daily monitoring |
| RMC | 20% | 10 business days | Formal request; reduction trajectory |
| Board | >20% | As approved | Exceptional circumstances only |

### 5.4 Breach Documentation

Each breach must be documented with:
1. Date and time of breach
2. Limit type and level breached
3. Breach amount ($ and %)
4. Cause classification (technical/passive/active)
5. Immediate actions taken
6. Remediation plan with timeline
7. Sign-off by relevant authority

---

## 6. Limit Setting and Review

### 6.1 Annual Limit Review

| Step | Timing | Responsibility |
|------|--------|----------------|
| Trading submit limit requests | November | Trading Heads |
| Market Risk review and challenge | November | Market Risk |
| MLRC review of desk/BU limits | December | MLRC |
| RMC approval of division/entity limits | December | RMC |
| Board approval of entity limit | January | Board |
| Limits effective | 1 January | All |

### 6.2 In-Year Limit Changes

| Change Type | Process | Approval |
|-------------|---------|----------|
| Reallocation within division | Market Risk review | MLRC |
| Increase desk limit (<20%) | Business case required | MLRC |
| Increase BU limit | Formal request with rationale | RMC |
| Increase entity limit | Board paper required | Board |
| Decrease (any level) | Market Risk notification | Relevant committee |

### 6.3 New Desk/Book Limits

For new trading activities:
1. New Product Approval completed
2. Risk assessment including proposed limits
3. Systems configured for limit monitoring
4. MLRC approval of initial limits
5. 3-month review of limit adequacy

---

## 7. Limit Methodology

### 7.1 Entity Limit Calibration

Entity VaR limit is set considering:
- Capital allocated to trading activities
- Risk appetite statement (max loss tolerance)
- Historical VaR usage patterns
- Peer benchmarking
- Strategic growth plans
- Diversification assumptions

### 7.2 Sub-Limit Allocation

Sub-limits allocated based on:
- Historical usage and P&L generation
- Strategic importance of business
- Risk-return efficiency
- Diversification benefit assumptions (typically 20-30%)
- Growth plans and mandates

### 7.3 Diversification Benefit

Sum of sub-limits exceeds parent limit due to assumed diversification:
- Division level: ~25% diversification assumed
- BU level: ~15% diversification assumed
- Desk level: ~10% diversification assumed

Diversification benefits are reviewed annually and may be reduced during stress periods.

---

## 8. Special Situations

### 8.1 Market Stress

During periods of elevated market stress:
- Warning thresholds may be lowered (e.g., 70% instead of 80%)
- Daily MLRC calls may be instituted
- Temporary limit reductions may be imposed
- Diversification assumptions may be reduced

### 8.2 System Outage

If limit monitoring systems are unavailable:
- Manual position limits apply
- No new risk-increasing trades without Market Risk approval
- Estimated VaR calculated manually
- Incident logged and reported to MLRC

### 8.3 Year-End

Additional controls apply at financial year-end:
- Stricter limit utilisation targets (70% max)
- Enhanced P&L monitoring
- Reduced appetite for new positions
- Daily calls with Trading Heads

---

## 9. Related Documents

| Document | Relationship |
|----------|--------------|
| [Market Risk Policy](./market-risk-policy.md) | Parent policy |
| [MLRC Terms of Reference](../committees/mlrc-terms-of-reference.md) | Approval authority |
| [VaR Methodology](../../L6-Models/market-risk/var-svar-methodology.md) | Calculation methodology |
| [Market Risk Process Orchestration Process](../../L4-Processes/processes/market-risk-process-orchestration.md) | Operational process |

---

## 10. Document Control

### 10.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-15 | Initial version | RMC |
| 1.1 | 2025-01-17 | Converted all amounts from GBP to USD for reporting consistency | RMC |

### 10.2 Review Schedule

- Full review: Annually (January)
- Limit amounts: Annually or upon material change
- Methodology: As needed based on market conditions

---

## Appendix A: Limit Summary Table

| Level | Entity | VaR Limit | SVaR Limit | Stress Limit |
|-------|--------|-----------|------------|--------------|
| Entity | MGB | $25m | $50m | $190m |
| Division | Markets | $19m | $38m | $150m |
| Division | Treasury | $6m | $12m | $50m |
| BU | Rates | $12m | $24m | $80m |
| BU | FX | $8m | $16m | $50m |
| BU | Credit | $6m | $12m | $45m |

---

## Appendix B: Sensitivity Limit Details

### Interest Rate Sensitivity (DV01)

| Tenor Bucket | Limit ($k/bp) |
|--------------|---------------|
| 0-3M | 125 |
| 3M-1Y | 185 |
| 1Y-5Y | 185 |
| 5Y-10Y | 95 |
| 10Y+ | 35 |
| **Total** | **625** |

### Credit Spread Sensitivity (CS01)

| Rating Bucket | Limit ($k/bp) |
|---------------|---------------|
| IG (A- and above) | 185 |
| IG (BBB) | 125 |
| HY (BB) | 50 |
| HY (B and below) | 15 |
| **Total** | **375** |

---

*End of Document*
