---
# Policy Metadata
policy_id: MR-L3-004
policy_name: Value-at-Risk Policy
version: 1.0
effective_date: 2025-01-17
next_review_date: 2026-01-17
owner: Head of Market Risk
approving_committee: MLRC
document_classification: Internal
supersedes: null

# Taxonomy Linkages
parent_policy: MR-L3-001  # Market Risk Policy
l1_requirements:
  - REQ-L1-001  # CRR/CRR III
  - REQ-L1-003  # FRTB
  - REQ-L1-004  # SS13/13 Market Risk
  - REQ-L1-013  # SS1/23 Model Risk
l2_risk_types:
  - MR-L2-001   # Market Risk (General)
  - MR-L2-002   # Interest Rate Risk (Trading)
  - MR-L2-003   # Foreign Exchange Risk
  - MR-L2-004   # Equity Risk
  - MR-L2-005   # Commodity Risk
  - MR-L2-006   # Credit Spread Risk (Trading)
l3_governance:
  - MR-L3-001   # Market Risk Policy
  - MR-L3-002   # MLRC Terms of Reference
  - MR-L3-003   # VaR Limit Framework
l4_processes:
  - MR-L4-001   # Market Risk Process Orchestration
  - MR-L4-005   # Time Series Management
  - MR-L4-006   # Risk Engine Calculation
  - MR-L4-007   # Market Risk Reporting & Sign-off
  - MR-L4-008   # Backtesting
l5_controls:
  - MR-L5-001   # VaR and SVaR Limits Controls
  - MR-L5-004   # Backtesting Controls
  - MR-L5-007   # ECAP Controls
l6_models:
  - MR-L6-001   # Historical Simulation VaR/SVaR Methodology
  - MR-L6-002   # ECAP Methodology
l7_systems:
  - SYS-MR-003  # Risk Engine
  - SYS-MR-008  # Risk ODS
  - SYS-MR-010  # Time Series ODS
---

# Value-at-Risk Policy

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Policy ID** | MR-L3-004 |
| **Version** | 1.0 |
| **Effective Date** | 17 January 2025 |
| **Next Review** | 17 January 2026 |
| **Parent Policy** | Market Risk Policy (MR-L3-001) |
| **Owner** | Head of Market Risk |
| **Approving Committee** | Market & Liquidity Risk Committee (MLRC) |

---

## 1. Introduction

### 1.1 Purpose

This Value-at-Risk (VaR) Policy provides comprehensive guidance on the definition, measurement, and use of VaR and Stressed VaR (SVaR) at Meridian Global Bank ("the Bank"). It establishes the control protocols for time series management, proxy governance, Risks Not in VaR (RNIV), and backtesting which are essential for effective market risk measurement for both regulatory capital and risk management purposes.

This Policy supplements the Market Risk Policy (MR-L3-001) with operational detail on VaR governance. Technical computational details are documented separately in the VaR Methodology (MR-L6-001).

### 1.2 Scope

This Policy applies to:
- All Value-at-Risk measures used for risk management and regulatory capital
- All trading book positions within the Management VaR scope
- All positions within IMA (Internal Model Approach) permission scope
- All staff responsible for VaR calculation, validation, sign-off, and governance

### 1.3 Regulatory Context

| Regulation | Reference | Key Requirements |
|------------|-----------|------------------|
| **CRR Art 325bc-be** | IMA VaR requirements | VaR methodology, confidence levels, holding periods |
| **CRR Art 325bk** | SVaR requirements | Stressed period selection, calibration |
| **CRR Art 325bf** | Backtesting | Exception monitoring, multiplier adjustment |
| **PRA SS13/13** | Market risk management | VaR governance, stress testing, model integrity |
| **PRA SS1/23** | Model risk | Model development, validation, governance |

---

## 2. Value-at-Risk Definition

### 2.1 VaR Concept

Value-at-Risk (VaR) is the key portfolio risk measure assigned to all trading books of Meridian Global Bank. VaR calculates an expected loss amount of a portfolio over a given time horizon based on a predefined confidence level. VaR is used for both regulatory capital and risk management purposes.

The Bank uses **Historical Simulation VaR**, which in most cases employs a full revaluation approach based on the loss calculation and aggregation of all market risk factors (the risk drivers associated with all approved traded products in the trading portfolio) to produce a loss result in GBP-denominated amount.

### 2.2 VaR Types

| VaR Type | Definition | Use |
|----------|------------|-----|
| **Regulatory VaR (RVaR/IMA VaR)** | Expected loss on IMA-approved portfolios based on a 10-day return over the current 1-year trading horizon using a 99% confidence interval | Key capital metric for calculating market risk regulatory capital |
| **Management VaR (MVaR)** | Expected loss calculated on Global Markets or any sub-portfolios, based on a 1-day return over the current 1-year trading horizon using a 99% confidence interval | Key daily market risk management measure; works alongside stress testing for portfolio risk assessment |

### 2.3 Risk Factor Coverage

The Bank's VaR measure covers all material market risk factors in its trading book (as defined by the Trading Book Policy Statement) or in the Banking Book for instruments held at fair value. VaR specifically covers:

- General interest rate risk (excluding Interest Rate Risk in the Banking Book)
- Specific interest rate risk (in conjunction with general market risk, accounting for traded credit spread risk)
- Foreign exchange risk
- Equity risk
- Commodity risk
- Volatility risk (where material)

VaR implicitly captures the correlations between individual risk factors, both within and across asset class categories.

---

## 3. VaR Measurement

### 3.1 Methodology Parameters

| Parameter | Management VaR | Regulatory VaR | Rationale |
|-----------|----------------|----------------|-----------|
| **Confidence Level** | 99% | 99% | Regulatory standard |
| **Holding Period** | 1 day | 10 days (scaled) | Daily monitoring vs capital |
| **Lookback Period** | 500 business days | 500 business days | ~2 years; captures multiple regimes |
| **Weighting** | Equal | Equal | Conservative; no decay |
| **Simulation Count** | 500 scenarios | 500 scenarios | Full historical window |

### 3.2 Calculation Approach

The Regulatory VaR (RVaR) calculation is the footing for IMA capital, while Management VaR (MVaR) is the key measure for monitoring portfolio exposure versus limits (Level 1 and Level 2 limits as defined in the Market Risk Policy Section 7).

The Bank reports VaR with a 99% confidence loss interval, but also calculates 1% confidence interval (gain side) for positive backtesting exception reporting.

### 3.3 Revaluation Methods

Risk Methodology & Analytics (RMA) is responsible for specifying, justifying, and documenting the simulation re-pricing methodology used for each product or risk factor:

| Method | Description | Typical Use |
|--------|-------------|-------------|
| **Full Revaluation** | Complete revaluation using validated pricing models | Complex derivatives, non-linear products |
| **Sensitivity-Based** | Taylor series expansion using Greeks (delta, gamma, vega) | Linear products, simple options |
| **Grid Interpolation** | Two-dimensional scenario grids (e.g., spot-volatility) | Options with material gamma/vega |

### 3.4 Methodology Changes

Any changes to the VaR methodology (as detailed in the VaR Methodology document MR-L6-001) require:

1. **Review**: Risk Methodology & Analytics (RMA) prepares impact assessment
2. **Approval**: Risk Model Approval Committee (RMAC) approval required
3. **Notification**: Material changes submitted to MLRC for noting
4. **Documentation**: RMA ensures detailed documentation is maintained
5. **Regulatory Compliance**: Market Risk ensures changes comply with IMA requirements

RMA must ensure Model Validation is fully informed of any proposed alternatives and/or extensions to the VaR methodology. Model Validation conducts a review following Model Validation Policy standards, with results and recommendations submitted to RMAC.

---

## 4. Stressed VaR (SVaR)

### 4.1 Definition

Stressed VaR (SVaR) is a key portfolio measure intrinsic to the Bank's market risk regulatory capital, introduced under Basel 2.5. Like VaR, SVaR is historical simulation based and calculates an expected loss over a given horizon at a predefined confidence level.

The defining difference: where VaR uses the current 1-year trading horizon, **SVaR identifies the worst 1-year trading window** from historical data back to 2007 to perform its loss calculation.

| Parameter | SVaR Value |
|-----------|------------|
| **Confidence Level** | 99% |
| **Holding Period** | 10 days |
| **Historical Window** | Back to 2007 (17+ years) |
| **Stress Period Selection** | Dynamic - worst 1-year window for current portfolio |

### 4.2 Regulatory Capital Treatment

SVaR contributes to market risk regulatory capital as follows:

```
Market Risk Regulatory Capital = Max(VaR, 60d Avg VaR × m) + Max(SVaR, 60d Avg SVaR × m) + IRC + RNIV
```

Where m = multiplier (3.0 base, adjusted for backtesting exceptions)

SVaR, because of its stressed calculation approach capturing the worst 1-year horizon, provides an effective complement to current VaR and stress testing for worst-case loss consideration.

### 4.3 Dynamic Stress Period Selection

The Bank employs a **dynamic stress period selection methodology** rather than fixing to a single historical event:

**Extended SVaR (ESVaR) Process**:
1. Weekly, the full VaR calculation is run using all historical windows back to 2007
2. For each potential 12-month stress window, portfolio VaR is calculated
3. The window producing the highest VaR for the current portfolio is selected
4. This ensures SVaR captures stress conditions most relevant to actual risk profile

This methodology is superior to a fixed stress period because:
- It adapts to changes in portfolio composition
- It captures stress periods most relevant to current exposures
- It avoids understating risk if current portfolio differs from historical crisis
- It satisfies regulatory intent to capture "significant financial stress"

### 4.4 SVaR Window Change Process

**Monitoring**: Market Risk reviews weekly ESVaR calculations and reports results to Head of Market Risk, CRO, business heads, and Technology/Operations.

**Change Assessment**: Risk change assessment focuses on at least **3 consecutive results** pointing to a competing window alternative to the incumbent SVaR window. Weekly ESVaR trends are illustrated and discussed at every MLRC cycle.

**Change Implementation**:
1. If assessment establishes a challenging window, Market Risk communicates to:
   - Desk heads
   - Risk Methodology & Analytics
   - Treasury Capital Markets
   - CRO
   - Risk Change/RAV
2. Minimum **2-week notice** given to IT Risk Production and Capital Reporting
3. All changes formally noted at nearest MLRC cycle

**Regulatory Notification**: Market Risk informs the PRA of any SVaR window changes in quarterly backtesting reporting, including a summary of window review results.

---

## 5. Historical Time Series Management

### 5.1 Time Series Governance

The historical time series used in VaR, SVaR, and ESVaR calculations are maintained in the Time Series ODS (SYS-MR-010). Time series for Regulatory VaR are updated daily (window rolled forward by one day with appropriate lag for data cleaning).

### 5.2 Roles and Responsibilities

| Role | Responsibilities |
|------|------------------|
| **Risk Reporting, Analysis & Validation (RAV)** | Updating and maintaining time series data; implementing proxy assignments; providing proxy reporting |
| **Market Risk** | Reviewing time series parameters annually; assigning suitable proxies; approving proxy choices |
| **Risk Methodology & Analytics (RMA)** | Reviewing proxy analysis; providing challenge; final proxy approval |

### 5.3 Time Series Adjustments

Any adjustment to individual time series (other than routine data cleaning such as backfilling missing dates) to reflect material changes or discontinuity in market conditions requires **Head of Market Risk approval**.

> **Process Reference**: For detailed time series management procedures, see [Time Series Management Suite (MR-L4-005)](../../L4-Processes/processes/time-series-management/).

---

## 6. Proxy Governance

### 6.1 Proxy Framework

Where a reliable historical time series is not available for a particular risk factor, Market Risk is responsible for assigning a suitable proxy per the Proxy Methodology guidelines and providing evidence to justify the choice.

Where no suitable proxy is available or proxying extent is deemed too high, Market Risk notifies RAV (run-the-bank) and RMA (new products) that the risk should be accounted for via an alternative VaR measurement technique (e.g., RNIV framework).

### 6.2 Proxy Levels

| Level | Description | Preference |
|-------|-------------|------------|
| **Level 1** | Own time series (actual market data) | Preferred |
| **Level 2** | Specific proxy (closely related instrument) | Acceptable with justification |
| **Level 3** | Generic proxy (asset class/sector proxy) | Requires enhanced monitoring |
| **Level 4** | RNIV treatment | Last resort; capital add-on |

### 6.3 Proxy Assignment Process

**Roles and Responsibilities**:
- **RAV**: Initial identification when proxy is required; alerting Market Risk; implementation after approval; proxy reporting
- **Market Risk**: Determining if existing proxy should change; performing analysis to identify appropriate proxy; documenting analysis
- **RMA**: Reviewing analysis; providing challenge; final proxy approval

### 6.4 Proxy Scoring and Review

Market Risk works with RAV to provide the Market Risk Model Risk Management Forum visibility on:
- Top proxied positions VaR time series via explicit review and rescoring
- Top positions using own time series
- Minimum coverage of >50% of total analysed proxied portfolio positions

All proxy scoring failures are immediately informed to Market Risk for formal approval or rationale documentation.

### 6.5 Proxy Governance Forum

Quarterly Proxy & RNIV Governance Forum reviews:
- Material proxies across all asset classes
- Proxy scoring results and failures
- RNIV framework adequacy
- Early Warning Indicators (EWIs)

> **Process Reference**: For detailed proxying procedures, see [Proxying Process (MR-L4-005g)](../../L4-Processes/processes/time-series-management/proxying-process.md).

---

## 7. Risks Not in VaR (RNIV)

### 7.1 RNIV Framework

Where the VaR model does not fully capture all market risks (due to proxy assignments, missing risk factors, or model limitations), these risks are identified and quantified as Risks Not in VaR (RNIV).

### 7.2 Roles and Responsibilities

| Role | Responsibility |
|------|----------------|
| **Market Risk** | Monitoring approved RNIV scope; escalating scope changes; reporting to Model Risk Forum |
| **RMA** | Review/improvement of existing RNIV methodology; development of new methodologies; quarterly/annual recalibrations; ownership of EUC-calculated RNIVs |
| **RAV** | Monitoring, updating and control of BAU RNIVs; running EUCs on agreed frequency; updating results |
| **Model Validation** | Ongoing validation and review of RNIV methodologies |

### 7.3 RNIV Identification

RNIVs are identified through:

1. **Backtesting Analysis**: Market Risk analyses exceptions to identify P&L from risk factors not captured in VaR
2. **Model Review**: Annual and targeted reviews ensure models capture all risks and price correctly
3. **Daily VaR/SVaR Analysis**: Review of large movements highlights missing risk factors
4. **Early Warning Indicators**: Periodic monitoring of EWIs targeting specific model weaknesses
5. **Front Office Interaction**: Regular meetings where information exchange may identify uncaptured risks
6. **New Product Approval**: Assessment of market risks for new products/markets

### 7.4 RNIV Calculation

For each risk factor within RNIV scope:
- VaR and SVaR metric calculated where sufficient data available
- Stressed period for RNIV SVaR consistent with main SVaR unless agreed otherwise
- **No offsetting or diversification** recognised across RNIV risk factors
- Standard multipliers applied to generate capital requirement

Where VaR/SVaR metric not appropriate, methodology must be based on stress test/stressed add-on with confidence level and horizon commensurate with risk factor liquidity.

### 7.5 Regulatory Notification

RMA is responsible for pre-notifying the PRA of all extensions and changes to the RNIV framework per SS13/13 requirements. Market Risk includes pre- and post-notifications in quarterly PRA reporting.

---

## 8. Backtesting

### 8.1 Purpose

Backtesting is a key market risk control ensuring VaR model performance integrity. It serves as one mechanism for ongoing validation under the IMA licence.

### 8.2 Backtesting Approach

For regulatory and internal purposes, backtesting is conducted using both:
- **99% confidence level**: Loss exceptions (loss > VaR)
- **1% confidence level**: Gain exceptions (gain > VaR) for positive backtesting

### 8.3 P&L Definitions

| P&L Type | Definition | Use |
|----------|------------|-----|
| **Hypothetical P&L** | P&L that would have occurred had the portfolio remained unchanged (clean P&L from overnight market moves only) | Model validation; internal reporting; PRA reporting; multiplier calculation |
| **Actual P&L** | Actual change in portfolio value excluding fees, commissions, and net interest income | PRA reporting; multiplier calculation |

For IMA positions, backtesting must use both Actual and Hypothetical P&L. For non-IMA positions, backtesting may use only Actual P&L if Hypothetical not available.

### 8.4 Backtesting Levels

For IMA scope positions, backtesting is conducted daily at:
- Entity level (Meridian Global Bank)
- Trading Area / Risk Class level
- Trading Desk level

Backtesting is also performed daily for overall management scope (IMA and non-IMA) per agreed SLAs.

### 8.5 Exception Definition

- **Regulatory Exception**: P&L loss exceeding corresponding 1-day 99% VaR per CRR Article 366 or PRA agreement
- **Internal Exception**: Any backtested P&L exceeding corresponding 1-day 99% VaR

### 8.6 Multiplier Adjustment

Market Risk assesses regulatory exceptions over the most recent 250 days to determine multiplier updates:

| Zone | Exceptions (250 days) | Plus Factor |
|------|----------------------|-------------|
| **Green** | 0-4 | 0.00 |
| **Yellow** | 5 | 0.40 |
| | 6 | 0.50 |
| | 7 | 0.65 |
| | 8 | 0.75 |
| | 9 | 0.85 |
| **Red** | 10+ | 1.00 |

RAV ensures multiplier is updated in risk reporting and Treasury Capital Markets is informed.

### 8.7 Exception Investigation

**Product Control**: Responsible for P&L accuracy; provides commentary explaining profits/losses including market commentary and breakdown by sub-portfolio and risk factor.

**Market Risk**: Responsible for investigating exception source; must provide detailed commentary on all 99% negative exceptions explaining why P&L exceeded VaR.

**RMA**: Performs independent review within 5 working days covering:
- Whether exception driven by genuine 99%+ market moves
- If genuine: detail observed moves versus prior year history
- If not genuine: detail potential model deficiency
- Any mitigants from capitalisation perspective (e.g., RNIV)
- Final assessment: Is there a model flaw? Is the bank potentially undercapitalised?
- Current exception count and trend behaviour
- Recommended actions and timelines

### 8.8 Escalation and Reporting

| Trigger | Action | Timeline |
|---------|--------|----------|
| Any negative exception | Market Risk notifies RMA and Model Validation with commentary | Day of sign-off |
| 5+ exceptions (12 months) | Formal review to RTF/RMAC indicating RMA comfort | Tracked via EWI dashboard |
| Regulatory exception | Notify PRA | Within 2 business days |
| Monthly reporting | All exceptions (positive and negative, L1 and L2) to MLRC and RMC | Monthly |

### 8.9 Regulatory Reporting

Market Risk ensures:
- Backtesting results covering all IMA positions reported to PRA quarterly
- Summary in electronic format per model permission requirements
- Ad hoc regulatory reporting requirements met as needed

> **Process Reference**: For detailed backtesting procedures, see [Backtesting Process (MR-L4-008)](../../L4-Processes/processes/backtesting.md).

---

## 9. VaR Limit Controls

### 9.1 Limit Structure

VaR limits operate at three levels with cascading delegated authority:

| Level | Scope | Approval | Monitoring |
|-------|-------|----------|------------|
| **Level 1** | Entity (Bank-wide) | Board/RMC | Daily by Market Risk |
| **Level 2** | Business Unit / Region | MLRC | Daily by Market Risk |
| **Level 3** | Desk / Trader | Business Head | Managed by business; notification to Market Risk |

VaR limits have a "pyramid" structure where limits at higher aggregation levels are less than sum of sub-limits (diversification assumption). Excesses at higher levels can occur without excesses at lower levels.

### 9.2 Limit Review

Market Risk ensures all Level 2 limits are consistent across the Bank. VaR limits are reviewed at least annually considering:
- Overall risk appetite (Market Risk Appetite Statement)
- Reasonable concentration/diversification
- Historical metrics (past average and peak usage, desk discipline)
- Forward-looking metrics (business appetite, expected plan, desk strategy, market conditions)

### 9.3 Limit Adherence

Front Office must make every reasonable effort to ensure VaR limits are adhered to at all times. Any change to confidence level or holding period for risk appetite purposes requires RMC approval.

> **Framework Reference**: For detailed limit structure and values, see [VaR Limit Framework (MR-L3-003)](./var-limit-framework.md).

---

## 10. Daily Sign-Off Requirements

### 10.1 VaR Sign-Off

Market Risk and Front Office review and sign off VaR daily per agreed SLAs:

| Time (T+1) | Activity | Owner |
|------------|----------|-------|
| 06:00 | Risk systems produce overnight VaR | Risk Technology |
| 07:00 | VaR report available; initial review | RAV |
| 07:30 | Market Risk review and challenge | Market Risk |
| 08:00 | Front Office VaR sign-off | Trading Desks |
| 08:30 | P&L sign-off | Product Control |
| 09:00 | Backtesting sign-off | Market Risk + Product Control |

Late sign-offs must be reported to Business Management & Control.

### 10.2 Sign-Off Responsibilities

| Party | Responsibility |
|-------|----------------|
| **Market Risk** | Daily integrity of VaR and backtesting sign-off |
| **Front Office** | Daily VaR sign-off confirming position accuracy |
| **Product Control** | Daily P&L sign-off confirming P&L accuracy |

If operational failure occurs in VaR or P&L reporting, Market Risk and Product Control use estimates on whatever basis deemed appropriate and report revised figures when actual data available.

---

## 11. Related Documents

### 11.1 Parent and Sibling Policies

| Document | Relationship |
|----------|--------------|
| [Market Risk Policy (MR-L3-001)](./market-risk-policy.md) | Parent policy; overall framework |
| [Stress Testing Policy (MR-L3-005)](./stress-testing-policy.md) | Sibling policy; stress framework |
| [Trading Book Boundary Policy (MR-L3-006)](./trading-book-boundary-policy.md) | Sibling policy; boundary management |
| [VaR Limit Framework (MR-L3-003)](./var-limit-framework.md) | Detailed limit structure |

### 11.2 Supporting Processes

| Process | Reference |
|---------|-----------|
| Time Series Management | MR-L4-005 |
| Risk Engine Calculation | MR-L4-006 |
| Market Risk Reporting & Sign-off | MR-L4-007 |
| Backtesting | MR-L4-008 |

### 11.3 Methodology Documents

| Document | Reference |
|----------|-----------|
| VaR/SVaR Methodology | MR-L6-001 |
| ECAP Methodology | MR-L6-002 |

---

## 12. Exceptions

There are no exceptions to this Policy. Any deviations require MLRC approval and must be documented.

---

## 13. Definitions

| Term | Definition |
|------|------------|
| **VaR** | Value at Risk - estimated maximum loss at given confidence level over specified holding period |
| **MVaR** | Management VaR - 1-day 99% VaR for risk management purposes |
| **RVaR** | Regulatory VaR - 10-day 99% VaR for capital calculation |
| **SVaR** | Stressed VaR - VaR calculated using a stressed market period |
| **ESVaR** | Extended SVaR - process for identifying worst stress period |
| **RNIV** | Risks Not in VaR - risks not fully captured by VaR model |
| **IMA** | Internal Model Approach - regulatory approval to use internal models |
| **Proxy** | Substitute time series used when actual data unavailable |
| **EWI** | Early Warning Indicator - metric targeting model weaknesses |

---

## 14. Policy Contact

| Field | Details |
|-------|---------|
| **Policy Owner** | Head of Market Risk |
| **Technical Queries** | Risk Methodology & Analytics |
| **Operational Queries** | Risk Reporting, Analysis & Validation |

---

## 15. Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-17 | Initial version | MLRC |

---

*This policy is the property of Meridian Global Bank. Unauthorised distribution is prohibited.*

*End of Document*
