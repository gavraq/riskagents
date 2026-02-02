---
# Document Metadata
document_id: GOV-L3-010
document_name: Risk Appetite Statement
acronym: RAS
version: 1.1
effective_date: 2025-01-17
next_review_date: 2026-01-17
owner: Chief Risk Officer
approver: Board of Directors

# Taxonomy Linkages
governance_framework: GOV-L3-011  # Risk Appetite Framework
parent_document: null  # Apex risk appetite document
approval_committee: GOV-L3-002  # BRMC recommends to Board
monitoring_committee: GOV-L3-004  # RMC
l1_requirements:
  - REQ-L1-001   # CRR/CRR III
  - REQ-L1-002   # Basel III/IV
  - REQ-L1-008   # PRA Rulebook
  - REQ-L1-019   # SS1/23 Model Risk
related_policies:
  - MR-L3-001   # Market Risk Policy
  - CR-L3-001   # Credit Risk Policy
  - OR-L3-001   # Operational Risk Policy
  - LR-L3-001   # Liquidity Risk Policy
---

# Risk Appetite Statement (RAS)

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Document ID** | GOV-L3-010 |
| **Version** | 1.1 |
| **Effective Date** | 17 January 2025 |
| **Next Review** | 17 January 2026 |
| **Owner** | Chief Risk Officer |
| **Approver** | Board of Directors |

---

## 1. Purpose

### 1.1 Overview

This Risk Appetite Statement (RAS) defines the aggregate level and types of risk that Meridian Global Bank ("the Bank") is willing to accept, or avoid, in order to achieve its business objectives. The RAS provides a common framework for the Board, management, and business lines to understand, discuss, and manage risk.

### 1.2 Scope

This statement applies to all activities of Meridian Global Bank and its subsidiaries, covering:
- Market Risk (including trading book and banking book exposures)
- Credit Risk (including counterparty credit risk, gap risk, and concentration risk)
- Operational Risk (including conduct, cyber, and third-party risks)
- Liquidity Risk
- Interest Rate Risk in the Banking Book (IRRBB)
- Business Risk
- Other Risks (compliance, legal, reputational)

### 1.3 Risk Appetite Philosophy

The Bank's risk appetite is set to ensure that:
- The Bank remains solvent under severe but plausible stress conditions
- Earnings volatility remains within acceptable bounds for shareholders
- Regulatory capital requirements are met with adequate buffer
- Liquidity is sufficient to meet obligations under stress
- The Bank maintains its reputation and regulatory standing

---

## 2. Risk Appetite Framework

### 2.1 Three-Level Structure

| Level | Description | Owner | Approval |
|-------|-------------|-------|----------|
| **Level 1** | Entity-wide risk appetite | CRO | Board (via BRMC) |
| **Level 2** | Risk type allocations | Risk Type Heads | RMC |
| **Level 3** | Portfolio/desk limits | Business Heads | Risk Type Committees |

### 2.2 Trigger and Limit Framework

```
┌─────────────────────────────────────────────────────────────────┐
│                    RISK APPETITE BREACH (RED)                   │
│              If risk profile falls in this area,                │
│              the Bank is in breach of risk appetite             │
├─────────────────────────────────────────────────────────────────┤
│               Risk Appetite Limit                               │
├─────────────────────────────────────────────────────────────────┤
│                EARLY WARNING ZONE (AMBER)                       │
│              If risk profile falls in this area,                │
│              Bank is in breach of early warning triggers        │
│              but still within Risk Appetite Limit               │
├─────────────────────────────────────────────────────────────────┤
│               Risk Appetite Trigger                             │
├─────────────────────────────────────────────────────────────────┤
│                  WITHIN APPETITE (GREEN)                        │
│              If risk profile falls in this area,                │
│              we are within risk appetite and                    │
│              within early warning triggers                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Level 1 Risk Appetite Metrics

### 3.1 Quantitative Dimensions

| Dimension | Metric | Green | Amber | Red | Frequency |
|-----------|--------|-------|-------|-----|-----------|
| **Earnings at Risk** | EaR (90% CI, 1-year) | < $220m | $220m - $245m | > $245m | Monthly |
| **Economic Capital** | AFR/ECap Ratio | > 130% | 120% - 130% | < 120% | Monthly |
| **CET1 Capital** | Surplus over CIB + $30m | > CIB + $30m | CIB to CIB + $30m | < CIB | Daily |
| **Tier 1 Capital** | Surplus over CIB + $30m | > CIB + $30m | CIB to CIB + $30m | < CIB | Daily |
| **Total Capital** | Surplus over CIB + $30m | > CIB + $30m | CIB to CIB + $30m | < CIB | Daily |
| **ILG Headroom** | Surplus over requirement | > $500m | $0m - $500m | < $0m | Daily |
| **91-Day Stress** | Survival period surplus | > $500m | $0m - $500m | < $0m | Monthly |
| **NSFR** | Surplus over 100% | > $500m | $0m - $500m | < $0m | Monthly |
| **Leverage Ratio** | Tier 1 / Exposure | > 3.50% | 3.25% - 3.50% | < 3.25% | Daily |

*CIB = Capital Internal Buffer; AFR = Available Financial Resources; ECap = Economic Capital; All amounts in USD*

### 3.2 Qualitative Dimensions (Other Risks)

| Risk Category | Metric | Trigger | Limit |
|---------------|--------|---------|-------|
| **Large Exposures** | Persistence of breach | 1 day | >1 day or >1 breach/month |
| **Single Op Risk Event** | Net loss impact | N/A | > $6m |
| **L1 Stop Loss** | Cumulative P&L loss | Per Market Risk Policy | Board-approved limit |
| **Other Risks** | Material breach | Qualitative assessment | RMC determination |

---

## 4. Level 2 Risk Appetite Allocations

### 4.1 Earnings at Risk (EaR) Allocation

| Risk Type | Undiversified EaR | Correlation | Diversified EaR | Owner |
|-----------|-------------------|-------------|-----------------|-------|
| Credit Risk | $120m | 40% | $48m | Head of Credit Risk |
| Market Risk | $105m | 40% | $42m | Head of Market Risk |
| Operational Risk | $65m | 40% | $26m | Head of Operational Risk |
| IRRBB | $50m | 40% | $20m | Head of Liquidity Risk |
| Business Risk | $95m | 40% | $38m | Head of Treasury |
| **Total Undiversified** | **$435m** | - | - | - |
| **Diversification Benefit** | - | - | **($135m)** | - |
| **Total Diversified** | - | - | **$220m** | CRO |

*Note: 40% correlation factor applied to calculate diversification benefit*

### 4.2 Economic Capital (ECap) Allocation

| Risk Type | ECap Allocation | % of Total | Owner |
|-----------|-----------------|------------|-------|
| Credit Risk | $650m | 40.6% | Head of Credit Risk |
| Market Risk | $500m | 31.3% | Head of Market Risk |
| Operational Risk | $195m | 12.1% | Head of Operational Risk |
| IRRBB | $95m | 5.9% | Head of Liquidity Risk |
| Business Risk | $160m | 10.2% | Head of Treasury |
| **Total ECap** | **$1,600m** | **100%** | CRO |

### 4.3 Supplementary Level 2 Metrics

| Risk Type | Metric | Limit | Owner |
|-----------|--------|-------|-------|
| **Market Risk** | Entity VaR (99%, 1-day) | $25m | Head of Market Risk |
| **Market Risk** | Entity VaR (99%, 10-day) | $79m | Head of Market Risk |
| **Market Risk** | Max Stress Loss | $190m | Head of Market Risk |
| **Credit Risk** | Portfolio Expected Loss | $55m | Head of Credit Risk |
| **Credit Risk** | Concentration (Single Name) | 10% of CET1 | Head of Credit Risk |
| **IRRBB** | Economic Value Sensitivity | $45m (200bp shock) | Head of Liquidity Risk |
| **Operational Risk** | Annual Expected Loss | $20m | Head of Operational Risk |

---

## 5. Level 3 Portfolio Limits

### 5.1 Market Risk Limits

| Portfolio | VaR Limit (1-day) | Owner |
|-----------|-------------------|-------|
| Rates Trading | $12m | Head of Rates |
| FX Trading | $8m | Head of FX |
| Credit Trading | $6m | Head of Credit Trading |
| Equities | $4m | Head of Equities |
| Commodities | $3m | Head of Commodities |
| **Entity Total** | **$25m** | Head of Market Risk |

*Note: Business unit limits sum to more than entity limit due to diversification assumption*

### 5.2 Credit Risk Limits

| Dimension | Limit | Owner |
|-----------|-------|-------|
| Single Counterparty (Investment Grade) | $65m | Head of Credit Risk |
| Single Counterparty (Sub-Investment Grade) | $30m | Head of Credit Risk |
| Country Limit (Tier 1) | $125m | Head of Credit Risk |
| Country Limit (Tier 2) | $65m | Head of Credit Risk |
| Country Limit (Tier 3) | $30m | Head of Credit Risk |
| Industry Concentration | 25% of portfolio | Head of Credit Risk |

---

## 6. Risk Appetite Statement

### 6.1 Overarching Statement

> Meridian Global Bank seeks to generate sustainable returns for shareholders while maintaining:
> - **Capital Adequacy**: Sufficient capital to absorb unexpected losses at a 99.9% confidence level
> - **Earnings Stability**: Earnings volatility within acceptable bounds at a 90% confidence level over a one-year horizon
> - **Liquidity Resilience**: Ability to meet obligations for at least 91 days under combined stress
> - **Regulatory Compliance**: Meeting all regulatory requirements with appropriate buffers
> - **Reputational Integrity**: Maintaining trust with clients, regulators, and the market

### 6.2 Risk Type Statements

#### 6.2.1 Market Risk

> The Bank accepts market risk arising from client-driven trading activities and proprietary positioning within clearly defined limits. The Bank does not seek to take speculative positions that could materially impact earnings or capital.

**Key Appetite Boundaries:**
- Maximum daily VaR of $25m at 99% confidence
- Maximum stress loss of $190m under severe market scenarios
- Stop loss limits to protect against adverse market movements

#### 6.2.2 Credit Risk

> The Bank accepts credit risk from lending, trading, and investment activities with creditworthy counterparties. The Bank maintains a diversified portfolio and avoids excessive concentration to any single name, sector, or geography.

**Key Appetite Boundaries:**
- Expected loss within budgeted provisions
- Single name exposure limits based on credit quality
- Country and sector concentration limits

#### 6.2.3 Operational Risk

> The Bank accepts a low level of operational risk inherent in its business activities. The Bank invests in controls, systems, and people to minimise operational losses and protect against conduct failures.

**Key Appetite Boundaries:**
- Zero tolerance for material compliance breaches
- Single event loss limit of $6m
- Low appetite for cyber and data security incidents

#### 6.2.4 Liquidity Risk

> The Bank maintains sufficient liquidity to meet obligations under normal and stressed conditions. The Bank does not rely on short-term wholesale funding for long-term assets.

**Key Appetite Boundaries:**
- ILG surplus maintained at all times
- 91-day survival under combined idiosyncratic and market-wide stress
- NSFR maintained above 100%

#### 6.2.5 IRRBB

> The Bank accepts limited interest rate risk in the banking book from maturity transformation activities. The Bank hedges where economic value sensitivity exceeds appetite.

**Key Appetite Boundaries:**
- Economic value sensitivity within $45m for 200bp parallel shock
- NII sensitivity within budget variance tolerance

#### 6.2.6 Business Risk

> The Bank accepts business risk arising from revenue volatility, strategic initiatives, and competitive dynamics. The Bank maintains cost flexibility to respond to revenue shortfalls.

**Key Appetite Boundaries:**
- Revenue at risk within budget contingency
- Strategic initiatives approved within capital allocation

---

## 7. Monitoring and Reporting

### 7.1 Dashboard Reporting

| Report | Frequency | Recipient |
|--------|-----------|-----------|
| RAS Dashboard | Daily | CRO, CFO, Business Heads |
| RAS Dashboard | Monthly | RMC, ALCO, ExCo |
| RAS Dashboard | Quarterly | BRMC, Board |
| Detailed Limit Report | Monthly | Risk Type Committees |

### 7.2 Breach Escalation

| Level | Breach Type | Initial Escalation | Ultimate Escalation |
|-------|-------------|-------------------|---------------------|
| Level 1 | EaR/ECap/Capital/Liquidity | CRO to ExCo | Board via BRMC |
| Level 1 | Leverage Ratio | CFO to ExCo/ALCO | Board via BRMC |
| Level 2 | Risk Type Allocation | Risk Type Head to RMC | ExCo/BRMC if unresolved |
| Level 3 | Portfolio/Desk Limit | Desk Head to BU Risk | Risk Type Committee |

### 7.3 Remediation Requirements

| Status | Action Required | Timeframe |
|--------|-----------------|-----------|
| **Green** | Continue monitoring | N/A |
| **Amber** | Management action plan | Within 5 business days |
| **Red** | Immediate escalation and remediation | Within 24 hours |

---

## 8. Governance

### 8.1 Annual Review

The RAS will be reviewed at least annually as part of the budgeting process. The review will consider:
- Changes in business strategy
- Changes in risk profile
- Regulatory developments
- Stress testing results
- Historical performance against appetite

### 8.2 Approval Process

```
┌─────────────────────────────────────────────────────────────────┐
│                      BOARD OF DIRECTORS                         │
│              Final approval of Level 1 RAS                      │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ Recommendation
┌─────────────────────────────────────────────────────────────────┐
│         BOARD RISK MANAGEMENT COMMITTEE (BRMC)                  │
│              Review and recommend RAS to Board                  │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ Recommendation
┌─────────────────────────────────────────────────────────────────┐
│             EXECUTIVE COMMITTEE (ExCo)                          │
│              Review and recommend RAS to BRMC                   │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ Recommendation
┌─────────────────────────────────────────────────────────────────┐
│           RISK MANAGEMENT COMMITTEE (RMC)                       │
│              Draft and propose RAS to ExCo                      │
│              Approve Level 2 allocations                        │
└─────────────────────────────────────────────────────────────────┘
```

### 8.3 Out-of-Cycle Changes

Material changes to the RAS outside the annual review require Board approval. Changes may be triggered by:
- Material change in business strategy
- Acquisition or divestiture
- Significant market event
- Regulatory requirement
- Material breach requiring appetite adjustment

---

## 9. Linkage to Other Frameworks

### 9.1 Stress Testing

Risk appetite is calibrated against stress testing results:
- **ICAAP Stress**: Capital remains above regulatory minimum under severe stress
- **ILAAP Stress**: Liquidity remains positive for 91 days under combined stress
- **Reverse Stress Test**: Scenarios that would breach risk appetite are identified and monitored

### 9.2 Business Planning

- Annual budget incorporates risk appetite constraints
- New business proposals assessed against risk appetite
- Capital allocation aligned with risk appetite by business

### 9.3 Remuneration

- Risk-adjusted performance metrics linked to appetite
- Bonus pools consider risk appetite utilisation
- Material risk takers subject to additional restrictions

---

## 10. Definitions

| Term | Definition |
|------|------------|
| **AFR** | Available Financial Resources - capital available to absorb losses under economic principles |
| **CIB** | Capital Internal Buffer - management buffer above regulatory minimum |
| **ECap** | Economic Capital - capital required at 99.9% confidence to absorb unexpected losses |
| **EaR** | Earnings at Risk - potential loss at 90% confidence over one-year horizon |
| **ILG** | Individual Liquidity Guidance - PRA-determined liquidity requirement |
| **NSFR** | Net Stable Funding Ratio - long-term liquidity requirement |
| **RAS** | Risk Appetite Statement |
| **VaR** | Value at Risk - potential loss at specified confidence over holding period |

---

## 11. Related Documents

| Document | Relationship |
|----------|--------------|
| Risk Appetite Framework | Methodology and governance for RAS |
| Enterprise Risk Management Framework | Overall risk management approach |
| ICAAP | Capital adequacy assessment |
| ILAAP | Liquidity adequacy assessment |
| Market Risk Policy | Market risk appetite implementation |
| Credit Risk Policy | Credit risk appetite implementation |
| Operational Risk Policy | Operational risk appetite implementation |
| Liquidity Risk Policy | Liquidity risk appetite implementation |

---

## 12. Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-17 | Initial version | Board |
| 1.1 | 2025-01-17 | Converted all amounts from GBP to USD for reporting consistency | Board |

---

*This document is the property of Meridian Global Bank. Unauthorised distribution is prohibited.*

*End of Document*
