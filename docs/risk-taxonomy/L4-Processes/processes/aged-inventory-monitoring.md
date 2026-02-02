---
# Process Metadata
process_id: MR-L4-014
process_name: Aged Inventory Monitoring
version: 1.0
effective_date: 2025-01-16
next_review_date: 2026-01-16
owner: Head of Market Risk
approving_committee: MLRC

# Taxonomy Linkages
parent_process: MR-L4-001  # Market Risk Process Orchestration
l1_requirements:
  - REQ-L1-001  # CRR
  - REQ-L1-004  # PRA SS13/13
  - REQ-L1-022  # BCBS 239
l2_risk_types:
  - MR-L2-001   # Market Risk
l3_governance:
  - MR-L3-001   # Market Risk Policy (Section 10.6)
  - MR-L3-002   # MLRC Terms of Reference
l5_controls:
  - MR-L5-005   # Concentration Limits
l7_systems:
  - SYS-MR-003  # Risk Engine
  - SYS-MR-008  # Risk ODS
---

# Aged Inventory Monitoring Process

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Process ID** | MR-L4-014 |
| **Version** | 1.0 |
| **Effective Date** | 16 January 2025 |
| **Parent Process** | Market Risk Process Orchestration (MR-L4-001) |
| **Owner** | Head of Market Risk |

---

## 1. Purpose

The Aged Inventory Monitoring process ensures that trading book positions align with trading intent requirements and identifies potential illiquidity, concentration, and fair value concerns. This quarterly review process:

1. **Identifies** positions held beyond expected timeframes
2. **Validates** ongoing trading intent through desk attestation
3. **Assesses** liquidity and exit strategy for aged positions
4. **Reports** findings to MLRC and feeds into ICAAP illiquidity assessments

This process supports the Bank's compliance with trading book boundary requirements and informs capital adequacy assessments for market risk.

> **Regulatory Drivers**: For aged inventory regulatory requirements (CRR Art 325, PRA SS13/13, CRD VI Art 79, BCBS 239), see [Market Risk Policy Section 10.6.1](../../L3-Governance/policies/market-risk-policy.md#1061-aged-inventory-regulatory-drivers).

---

## 2. Scope

### 2.1 Definition

**Aged Inventory** refers to trading book positions that have been held for an extended period without significant turnover, potentially indicating:
- Reduced liquidity or marketability
- Positions outside trading intent
- Potential fair value concerns
- Concentration risk build-up

### 2.2 Aged Inventory Criteria

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     AGED INVENTORY CLASSIFICATION                                       │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  A position is classified as AGED INVENTORY if:                                         │
│                                                                                         │
│  1. HOLDING PERIOD:                                                                     │
│     • Position held for >6 months with minimal turnover (<10% of position traded)       │
│     • OR held outside agreed expectations at time of trade                              │
│                                                                                         │
│  2. MATERIALITY THRESHOLD:                                                              │
│     • Issuer risk positions (bonds, credit) >$5M equivalent                             │
│     • Single-name equity positions >$2M equivalent                                      │
│     • Derivatives with notional >$25M equivalent                                        │
│                                                                                         │
│  3. EXCLUSIONS:                                                                         │
│     • Hedging positions (documented hedge relationship)                                 │
│     • Market-making inventory within normal bands                                       │
│     • Client facilitation with documented exit strategy                                 │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.3 Asset Classes in Scope

| Asset Class | Materiality Threshold | Typical Concerns |
|-------------|----------------------|------------------|
| **Corporate Bonds** | >$5M | Credit deterioration, illiquid secondary market |
| **Emerging Market Debt** | >$5M | Currency risk, political risk, limited liquidity |
| **Structured Products** | >$5M | Model risk, no secondary market |
| **Single-Name Equities** | >$2M | Concentration, activist situations |
| **FX Options (Long-dated)** | >$25M notional | Illiquid tenors, model dependency |
| **Exotic Derivatives** | >$25M notional | Fair value uncertainty, exit difficulty |

---

## 3. Quarterly Review Process

### 3.1 Process Overview

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     AGED INVENTORY QUARTERLY REVIEW                                     │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  TIMING: Quarterly (January, April, July, October - aligned with ICAAP)                 │
│  OWNER: Market Risk (RAV Team)                                                          │
│  GOVERNANCE: Results reported to MLRC                                                   │
│                                                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐               │
│  │   STEP 1    │───▶│   STEP 2    │───▶│   STEP 3    │───▶│   STEP 4    │               │
│  │ IDENTIFY    │    │   ENGAGE    │    │  ANALYSE    │    │   REPORT    │               │
│  │             │    │             │    │             │    │             │               │
│  │ Week 1-2    │    │  Week 2-3   │    │  Week 3-4   │    │   Week 4    │               │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘               │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Step 1: Identification (Week 1-2)

**Owner**: RAV Team

**Activities**:
- Extract positions meeting aged criteria from Risk Engine
- Data includes: trade date, current value, P&L since inception, turnover history
- Cross-reference with Concentration VaR report (MR-L4-006, Section 6.6)
- Flag positions exceeding materiality thresholds

**Data Sources**:

| Source | Data Elements |
|--------|---------------|
| **Risk ODS** | Positions, sensitivities, VaR contribution |
| **Trade Repository** | Trade date, original intent, expected holding period |
| **P&L ODS** | MTM, inception-to-date P&L, turnover metrics |
| **Hierarchy ODS** | Desk, book, trader ownership |

**Output**: Preliminary aged inventory list with position details

### 3.3 Step 2: Desk Engagement (Week 2-3)

**Owner**: RAV Team (coordination), Trading Desks (attestation)

**Activities**:
- Send aged inventory list to Desk Heads
- Request attestation for each position covering:

| Attestation Question | Purpose |
|---------------------|---------|
| Is trading intent still valid? | Regulatory requirement (CRR Art 325) |
| What is the expected exit timeline? | Liquidity assessment |
| Are there any liquidity concerns? | ICAAP input |
| Is fair value supportable? | Valuation integrity |
| Has the position been actively marketed? | Evidence of exit effort |

**Output**: Completed attestation forms from each desk

### 3.4 Step 3: Market Risk Analysis (Week 3-4)

**Owner**: RAV Team, with Product Control input

**Activities**:
- Review desk attestations for completeness and reasonableness
- Challenge positions with unclear exit strategy
- Assess fair value concerns (coordinate with Product Control)
- Identify positions for enhanced monitoring or remediation
- Calculate aged inventory contribution to concentration risk
- Categorise positions by risk level

**Risk Categorisation**:

| Category | Criteria | Action |
|----------|----------|--------|
| **Low Risk** | Clear exit strategy, liquid market, stable value | Monitor quarterly |
| **Medium Risk** | Extended holding, limited liquidity, stable value | Enhanced monitoring, monthly review |
| **High Risk** | No clear exit, illiquid, fair value concerns | Remediation plan required, MLRC escalation |

**Output**: Analysed aged inventory with risk categorisation and recommendations

### 3.5 Step 4: Reporting and Governance (Week 4)

**Owner**: Head of Market Risk

**Activities**:
- Prepare aged inventory report for MLRC
- Feed results into ICAAP illiquidity assessment
- Track remediation actions from prior quarters
- Update concentration risk analysis

**Governance**:

| Forum | Content | Frequency |
|-------|---------|-----------|
| **MLRC** | Full aged inventory report, risk categorisation, remediation tracker | Quarterly |
| **RMC** | Summary of high-risk positions, ICAAP implications | Quarterly (as needed) |
| **Capital Planning** | ICAAP illiquidity inputs | Quarterly |

---

## 4. Aged Inventory Report

### 4.1 Report Template

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     AGED INVENTORY REPORT - Q1 2025                                     │
│                     Date: 31-Jan-2025                                                   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  SUMMARY                                                                                │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Total Aged Positions: 15                                                               │
│  Total Market Value: $185M                                                              │
│  % of Trading Book: 3.2%                                                                │
│  Change vs. Prior Quarter: +2 positions (+$25M)                                         │
│                                                                                         │
│  BY ASSET CLASS                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Asset Class          │ Positions │ Value    │ Avg Age │ Key Issues                     │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Corporate Bonds      │    8      │  $120M   │ 9 mo    │ EM credit - exit in progress   │
│  Structured Products  │    3      │   $45M   │ 14 mo   │ Limited secondary market       │
│  Equity (Single Name) │    2      │   $12M   │ 7 mo    │ Activist situations            │
│  FX Options           │    2      │    $8M   │ 8 mo    │ Long-dated exotics             │
│                                                                                         │
│  BY RISK CATEGORY                                                                       │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Category     │ Positions │ Value    │ Action                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Low Risk     │    9      │  $95M    │ Continue quarterly monitoring                    │
│  Medium Risk  │    4      │  $65M    │ Monthly review, enhanced monitoring              │
│  High Risk    │    2      │  $25M    │ Remediation plan in progress                     │
│                                                                                         │
│  CONCENTRATION IMPACT                                                                   │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Aged positions contribute 18% of Single Issuer concentration                         │
│  • 3 issuers appear on both aged and concentration watch lists                          │
│  • Top aged position = 4.5% of Trading Book VaR (within 15% limit)                      │
│                                                                                         │
│  REMEDIATION TRACKER                                                                    │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Positions from Q4 2024: 13                                                             │
│  Resolved: 5 (sold: 3, matured: 2)                                                      │
│  Ongoing: 8                                                                             │
│  New this quarter: 7                                                                    │
│                                                                                         │
│  ACTION ITEMS                                                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  1. Credit Trading to provide exit plan for EM bond positions (Due: 15-Feb)             │
│  2. Product Control to review fair value for structured products (Due: 28-Feb)          │
│  3. ICAAP team to incorporate aged inventory in illiquidity add-on (Due: Q1 ICAAP)      │
│                                                                                         │
│  Prepared by: RAV Team                                                                  │
│  Reviewed by: Head of Market Risk                                                       │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Report Distribution

| Recipient | Content | Timing |
|-----------|---------|--------|
| **MLRC** | Full report | Quarterly MLRC meeting |
| **Trading Desks** | Desk-specific extract | Within 5 days of MLRC |
| **Product Control** | Positions flagged for fair value review | Week 3 |
| **Capital Planning** | ICAAP inputs | Quarterly |

---

## 5. ICAAP Integration

Aged inventory analysis feeds directly into the Bank's Internal Capital Adequacy Assessment Process (ICAAP):

### 5.1 ICAAP Inputs

| ICAAP Component | Aged Inventory Input |
|-----------------|---------------------|
| **Pillar 2A - Market Risk** | Illiquidity add-on calibrated using aged inventory analysis |
| **Concentration Risk** | Aged positions with single-name exposure flagged |
| **Stressed Capital** | Liquidation assumptions incorporate aged inventory haircuts |
| **Capital Planning** | Expected P&L impact of aged position exit strategies |

### 5.2 Illiquidity Add-on Calculation

The aged inventory analysis informs the ICAAP illiquidity add-on:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     ILLIQUIDITY ADD-ON METHODOLOGY                                      │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  For each aged position:                                                                │
│                                                                                         │
│  Illiquidity Add-on = Position Value × Liquidity Haircut × √(Extended Holding Period)   │
│                                                                                         │
│  Where:                                                                                 │
│  • Liquidity Haircut = Asset-class specific (see table below)                           │
│  • Extended Holding Period = Days beyond standard 10-day VaR horizon                    │
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  Asset Class          │ Base Haircut │ Stressed Haircut │ Holding Assumption    │    │
│  ├───────────────────────┼──────────────┼──────────────────┼───────────────────────┤    │
│  │  Corporate Bonds (IG) │     2%       │       5%         │      20 days          │    │
│  │  Corporate Bonds (HY) │     5%       │      15%         │      40 days          │    │
│  │  EM Debt              │     5%       │      20%         │      40 days          │    │
│  │  Structured Products  │    10%       │      30%         │      60 days          │    │
│  │  Illiquid Derivatives │     8%       │      25%         │      40 days          │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                         │
│  Total Illiquidity Add-on = Σ (Position Add-ons) × Diversification Factor (0.7)         │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Controls

| Control ID | Control | Type | Owner |
|------------|---------|------|-------|
| AGE-C01 | Quarterly aged inventory review completed per schedule | Detective | RAV |
| AGE-C02 | Desk attestations obtained for all aged positions | Detective | RAV |
| AGE-C03 | High-risk positions have documented remediation plans | Detective | Market Risk |
| AGE-C04 | Aged inventory report presented to MLRC quarterly | Detective | Head of Market Risk |
| AGE-C05 | ICAAP illiquidity inputs updated quarterly | Detective | Capital Planning |
| AGE-C06 | Remediation actions tracked to completion | Detective | RAV |

---

## 7. Service Levels

| Metric | Target | Threshold | Escalation |
|--------|--------|-----------|------------|
| Identification complete | End of Week 2 | End of Week 3 | RAV Manager |
| Desk attestations received | End of Week 3 | End of Week 4 | Head of Market Risk |
| MLRC report ready | Week 4 | Before MLRC meeting | Head of Market Risk |
| ICAAP inputs delivered | Week 4 | Before ICAAP deadline | Capital Planning |

---

## 8. Related Documents

| Document | Relationship |
|----------|--------------|
| [Market Risk Process Orchestration](./market-risk-process-orchestration.md) | Parent orchestration |
| [Market Risk Policy](../../L3-Governance/policies/market-risk-policy.md) | Policy requirements (Section 10.6) |
| [Risk Engine Calculation](./risk-engine-calculation.md) | Data source - Concentration VaR |
| [Market Risk Limits Management](./market-risk-limits-management.md) | Related - Concentration limits |
| [Concentration Limits](../../L5-Controls/concentration-limits.md) | Control definitions |
| [MLRC Terms of Reference](../../L3-Governance/committees/mlrc-terms-of-reference.md) | Governance - reporting forum |

---

## 9. Document Control

### 9.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-16 | Initial version - extracted from Market Risk Limits Management as standalone quarterly process | MLRC |

---

*End of Document*
