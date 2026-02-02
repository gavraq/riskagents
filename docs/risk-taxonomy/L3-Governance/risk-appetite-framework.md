---
# Document Metadata
document_id: GOV-L3-011
document_name: Risk Appetite Framework
acronym: RAF
version: 1.1
effective_date: 2025-01-17
next_review_date: 2026-01-17
owner: Chief Risk Officer
approver: Board Risk Management Committee

# Taxonomy Linkages
risk_appetite_statement: GOV-L3-010  # Risk Appetite Statement
parent_document: null
approval_committee: GOV-L3-002  # BRMC
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

# Risk Appetite Framework (RAF)

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Document ID** | GOV-L3-011 |
| **Version** | 1.1 |
| **Effective Date** | 17 January 2025 |
| **Next Review** | 17 January 2026 |
| **Owner** | Chief Risk Officer |
| **Approver** | Board Risk Management Committee |

---

## 1. Purpose

### 1.1 Document Objective

This Risk Appetite Framework (RAF) describes the methodology, processes, and governance for setting, measuring, monitoring, and reporting against the Bank's Risk Appetite Statement (RAS). It provides the operational detail behind the strategic risk appetite articulated in the RAS.

### 1.2 Scope

This framework applies to all activities of Meridian Global Bank and governs:
- How risk appetite is set and calibrated
- How risk appetite cascades through the organisation
- How risk metrics are calculated and measured
- How appetite is monitored and reported
- How breaches are escalated and remediated

### 1.3 Key Principles

The Bank's risk appetite framework is guided by the following principles:

1. **Strategic Alignment**: Risk appetite is aligned with business strategy and supports strategic objectives
2. **Budget Compatibility**: Risk appetite is compatible with the budgeting and planning process
3. **Stress Testing Integration**: Stress testing results inform risk appetite calibration
4. **Clear Accountability**: Clear ownership and accountability for each risk appetite dimension
5. **Transparent Monitoring**: Regular, transparent monitoring against defined thresholds
6. **Timely Escalation**: Breaches escalated promptly with clear remediation requirements

---

## 2. Terminology

### 2.1 Risk Capacity, Appetite, and Limits

| Term | Definition |
|------|------------|
| **Risk Capacity** | The maximum level of risk the Bank can absorb before becoming insolvent or breaching regulatory requirements |
| **Risk Appetite** | The aggregate level and types of risk the Bank is willing to accept to achieve its objectives |
| **Risk Appetite Limit** | The boundary beyond which risk exposure is unacceptable (Red zone) |
| **Risk Appetite Trigger** | An early warning threshold that prompts management action (Amber zone) |
| **Risk Tolerance** | Acceptable variation around target exposure levels |

### 2.2 Traffic Light System

```
┌──────────────────────────────────────────────────────────────────┐
│                        RED (BREACH)                              │
│                                                                  │
│  If the risk profile falls within this area, the Bank is in      │
│  breach of risk appetite. Immediate escalation and remediation   │
│  required.                                                       │
├──────────────────────────────────────────────────────────────────┤
│                   RISK APPETITE LIMIT                            │
├──────────────────────────────────────────────────────────────────┤
│                     AMBER (WARNING)                              │
│                                                                  │
│  If risk profile falls within this area, the Bank is in breach   │
│  of early warning risk appetite triggers but still within the    │
│  Risk Appetite Limit. Management action required.                │
├──────────────────────────────────────────────────────────────────┤
│                  RISK APPETITE TRIGGER                           │
├──────────────────────────────────────────────────────────────────┤
│                      GREEN (NORMAL)                              │
│                                                                  │
│  If risk profile falls within this area, we are within risk      │
│  appetite and within early warning triggers.                     │
└──────────────────────────────────────────────────────────────────┘
```

### 2.3 Financial Resources

The term "financial resources" in the context of risk capacity refers to:
- **Qualifying Capital**: Available capital measured in terms of regulatory requirements
- **Available Financial Resources (AFR)**: Available capital measured in terms of economic or accounting principles
- **Funding/Liquid Assets**: High-quality liquid assets available to meet obligations
- **Term Lending Capacity**: Capacity to raise term funding in stressed conditions

---

## 3. Cascading Structure

### 3.1 Level 1: Entity Risk Appetite

Level 1 risk appetite refers to the RAS for the Bank as a whole. The dimensions may be either qualitative or quantitative. Level 1 generally relates to financial resources (capital and liquidity) and earnings volatility.

**Level 1 Quantitative Dimensions:**
- Earnings at Risk (EaR)
- Economic Capital (ECap)
- Regulatory Capital (CET1, Tier 1, Total)
- Liquidity (ILG, 91-day stress, NSFR)
- Leverage

**Level 1 Qualitative Dimensions:**
- Other Risks (Operational, Compliance, Conduct, Legal, Reputational)

### 3.2 Level 2: Risk Type Limits

Level 2 limits are second line of defence limits. Risk type heads are responsible for agreeing and setting Level 2 limits. Level 2 risk appetite links directly to Level 1 limits.

**Examples of Level 2 limits:**
- Allocation of EaR to individual risk types
- Allocation of ECap to individual risk types
- Entity VaR limit for Market Risk
- Portfolio Expected Loss for Credit Risk

**Purpose of Level 2 Risk Appetite:**
- Ensure proactive risk management and timely initiation of management action
- Enable risk control and reporting purposes
- Monitor utilisation of available financial resources
- Monitor and manage risk profile and risk appetite

### 3.3 Level 3: Portfolio Limits

Level 3 risk appetite is defined as portfolio limits. These metrics measure the legal entity exposure by risk type. Level 3 metrics may also be set and monitored at lower levels in the organisation, e.g., at product portfolio or desk levels.

**Characteristics of Level 3 Limits:**
- First line of defence limits
- Not necessarily required to be mathematically derived on a 1-to-1 basis from Level 1 or 2 limits
- Should be broadly congruent with Level 1 and 2
- Approved by relevant risk type governance committee

**Examples of Level 3 limits:**
- VaR limits at desk level
- Single name credit limits
- Stop loss limits

---

## 4. Measurement and Methodology

### 4.1 Earnings at Risk (EaR)

#### 4.1.1 Definition

Earnings at Risk is a forward-looking measure which ensures that the current portfolio of risk will not put more than a specified amount at risk at a 90% confidence interval over a one-year horizon.

**Confidence Interval Rationale:**
EaR lies in the unlikely but plausible confidence interval range (90%), as opposed to:
- The extreme confidence interval range (99.9%) relevant to economic capital
- The expected confidence interval range (50%) relevant to provisioning

#### 4.1.2 Calibration

EaR is calibrated to represent a financial loss over a one-year horizon and provide a directly comparable risk metric across risk classes, relevant for the annual budget.

The 90th percentile represents losses that are sufficiently remote to cause the Bank concern but not so extreme as to threaten solvency. In the event of an extreme shock, through its holding of ECap, the Bank should still have the ability to wind down in an orderly manner.

#### 4.1.3 Methodology by Risk Type

| Risk Type | Calculation Method | Owner | Frequency |
|-----------|-------------------|-------|-----------|
| **Credit Risk** | Monte Carlo simulation using RiskFrontier | Risk Methodologies & Analytics | Monthly |
| **Market Risk** | Scaled from VaR: EaR = VaR(1d,99%) × (Normsinv(0.9)/Normsinv(0.99)) × √250 | Market Risk | Monthly (daily available) |
| **Operational Risk** | Scenario analysis at 90% confidence | Operational Risk / RMA | Annual (or more if model changes) |
| **IRRBB** | Based on ECap scaled: EaR = ECap × (Normsinv(0.9)/Normsinv(0.999)) | Market & Liquidity Risk | Monthly (daily available) |
| **Business Risk** | Scenario analysis on projected budget | TCM / RMA | Annual (or more if business changes) |

**Market Risk EaR Formula:**

```
EaR_Market = VaR(1d,99%) × (Normsinv(0.9) / Normsinv(0.99)) × √250
```

Where:
- VaR(1d,99%) = Average daily VaR for the preceding 60 business days at 99% confidence
- Normsinv(0.9)/Normsinv(0.99) = Scaling from 99% to 90% confidence
- √250 = Scaling from 1-day to 1-year horizon

#### 4.1.4 Correlation and Diversification

Total diversified EaR is calculated by applying a correlation factor to the sum of risk type EaR. The correlation factor is based on a flat 40% correlation between each risk type.

```
Total Diversified EaR = √(Σ(EaR_i)² + 2 × ρ × Σ(EaR_i × EaR_j))
```

Where ρ = 40% correlation factor (reviewed annually)

#### 4.1.5 Triggers

The risk appetite trigger for EaR is set at 10% below the risk appetite limit. This:
- Considers the risk profile of the Bank
- Allows sufficient time for management action
- Reflects the short-dated nature of a significant portion of the portfolio

#### 4.1.6 Update Frequency

Risk appetite limits and triggers are reviewed at least annually during the budgeting process. Actual EaR is monitored monthly against the RAS.

| Risk Type | Calculation Frequency | Owner |
|-----------|----------------------|-------|
| Credit | Monthly | RMA |
| Market | Monthly (daily available) | Market Risk |
| Operational | Annual | Operational Risk / RMA |
| IRRBB | Monthly (daily available) | Market & Liquidity Risk |
| Business | Annual | TCM / RMA |

---

### 4.2 Economic Capital (ECap)

#### 4.2.1 Definition

Economic Capital represents the amount of capital required to absorb unexpected losses at a 99.9% confidence interval. This calibrates to a probability of default of approximately 0.1% (or a credit rating of BBB).

#### 4.2.2 Methodology

The economic capital ratio in the RAS is:

```
ECap Ratio = AFR / ECap
```

Where:
- AFR = Available Financial Resources (economic capital base)
- ECap = Total economic capital requirement

ECap is calculated as a simple sum of the economic capital attributable to each risk type:

```
ECap_Total = ECap_Credit + ECap_Market + ECap_Operational + ECap_IRRBB + ECap_Business
```

**Note:** Business risk is outside Pillar 2A (internal assessment) at PRA request, but within the stress testing framework (Pillar 2B).

#### 4.2.3 Market Risk ECap Calculation

Market Risk ECap is derived from the 99% 1-day Management VaR, subject to a 90-day averaging calculation and aggregated with issuer risk:

```
ECap_Market = VaR(1d,99%) × (Normsinv(0.999)/Normsinv(0.99)) × √250 × EWMA(90d)
```

Key considerations:
- Uses 20-day EWMA (exponentially weighted moving average)
- Scales from 99% to 99.9% confidence
- Scales to 1-year horizon using square root of time
- Uses weighted holding day period assumption per asset class decomposition
- Includes RNIMV (Risk Not In Management VaR)

#### 4.2.4 Correlation

There is no correlation matrix applied to aggregate total ECap (correlation assumed to be 1 at the tail). The same loss distribution is used but with a 99.9% confidence interval as opposed to EaR's 90%.

#### 4.2.5 Triggers

ECap refers to the amount of capital required such that, should a tail risk event occur, the Bank has sufficient capital to absorb the losses.

- **Risk Appetite Limit**: Set with headroom above minimum required ECap
- **Risk Appetite Trigger**: Set at 10% above the risk appetite limit

---

### 4.3 Regulatory Capital

#### 4.3.1 Methodology

Methodology is defined by the regulator. RWA, Total, Tier 1, and CET1 regulatory capital are calculated by the Capital Reporting team as part of standard regulatory reporting requirements.

The metric represents the capital surplus over capital buffers measured at CET1, Tier 1, and Total capital levels.

#### 4.3.2 Triggers

The trigger is set at $30m below the Capital Internal Buffer (CIB) for CET1, Tier 1, and Total capital levels to ensure management has sufficient time to enact management actions.

| Metric | Green | Amber | Red |
|--------|-------|-------|-----|
| CET1 Surplus | > CIB + $30m | CIB to CIB + $30m | < CIB |
| Tier 1 Surplus | > CIB + $30m | CIB to CIB + $30m | < CIB |
| Total Capital Surplus | > CIB + $30m | CIB to CIB + $30m | < CIB |

#### 4.3.3 Update Frequency

Risk appetite limits and triggers are reviewed at least annually during the budgeting process. Actual regulatory capital surplus is monitored daily against RAS limits. The lowest capital surplus during the month is reflected in the RAS dashboard.

#### 4.3.4 Limit Cascade

Regulatory Capital is managed at the Bank level and not cascaded further. Management Information is produced to provide a breakdown of calculation.

| Risk Type | Cascade | Owner |
|-----------|---------|-------|
| Market Risk | Desk level extracted from Market Risk System | Market Risk |
| Credit/Counterparty Risk | Allocated via Ambit Capital Manager | Credit Risk |
| Operational Risk | Allocated based on revenues | Operational Risk |

---

### 4.4 Liquidity

#### 4.4.1 Overview

Liquidity is managed in accordance with regulatory requirements and internal limits. The Bank manages:
- Short-term liquidity resilience against ILG and Combined Internal Stress Test
- Longer-term liquidity resilience against NSFR

#### 4.4.2 Methodology

**ILG (Individual Liquidity Guidance):**
The ILG represents the regulatory view of the Bank's liquidity stressed funding requirements. The Bank must ensure it holds sufficient HQLA to meet cumulative net cash outflows as at calendar day 30. The applicable ILG is 100% of the LCR requirement plus any Pillar 2 add-ons.

**Combined Internal Stress Test:**
Models the Bank's internal view of a severe combined idiosyncratic and market-wide liquidity stress scenario. The Bank must ensure sufficient HQLA to meet cumulative net cash outflows, post management actions, for a survival horizon of 91 days.

**NSFR:**
```
NSFR = ASF (Available Stable Funding) / RSF (Required Stable Funding) ≥ 100%
```

#### 4.4.3 Triggers

| Metric | Green | Amber | Red |
|--------|-------|-------|-----|
| ILG Headroom | > $500m | $0m - $500m | < $0m |
| 91-Day Stress Headroom | > $500m | $0m - $500m | < $0m |
| NSFR Headroom | > $500m | $0m - $500m | < $0m |

The $500m trigger headroom allows sufficient time to react to a potential breach and prompt management action.

#### 4.4.4 Update Frequency

Liquidity risk appetite is reviewed annually or more frequently if required.

- LCR and NSFR: Submitted monthly to PRA
- Daily monitoring: Low-point LCR and NSFR reflected in monthly RAS dashboard
- Additional Internal Stress: Monitored as EWI in Liquidity Limit/EWI monitoring policy

#### 4.4.5 Limit Cascade

Short-term resilience liquidity limits are set at entity level and not cascaded further to business line/desk. To assist with NSFR management, individual desk and business unit ceilings are included as Early Warning Indicators (EWI).

---

### 4.5 Leverage

#### 4.5.1 Methodology

The leverage ratio is a measure of the Bank's capital to its total assets and uses Tier 1 capital to judge how leveraged the Bank is in relation to its consolidated assets.

```
Leverage Ratio = Tier 1 Capital / Exposure Measure
```

The calculation is prescribed in the Leverage Ratio (CRR) part of the PRA rulebook. The Bank is required to maintain a minimum leverage ratio of 3.25%.

#### 4.5.2 Triggers

| Metric | Green | Amber | Red |
|--------|-------|-------|-----|
| Leverage Ratio | > 3.50% | 3.25% - 3.50% | < 3.25% |

The trigger is set at 3.50% to ensure sufficient headroom above the 3.25% minimum.

#### 4.5.3 Update Frequency

Risk appetite limits and triggers are reviewed at least annually. The low point of the leverage ratio during the month is monitored against the RAS.

#### 4.5.4 Limit Cascade

Leverage ratio is managed at the Bank level and not cascaded further.

---

### 4.6 Other Risks

#### 4.6.1 Large Exposures

**Regulatory Requirement:** Banking book exposures to 3rd party and group counterparties cannot exceed 25% of Tier 1 resources. Trading book exposures can exceed this limit at the expense of punitive capital charges.

**RAS Metric:** Persistence (over one day) of breach during the month or more than one breach in a month.

| Status | Definition |
|--------|------------|
| Green | No breach |
| Amber | Large Exposure excess mitigated in one day |
| Red | Excess not mitigated in one day, or >1 excess during month |

#### 4.6.2 Single Operational Risk Loss Event

Although operational risk losses are monitored through EaR and ECap metrics, the Bank strives to reduce single event operational risk losses.

**RAS Metric:** Net loss from single operational risk event

| Status | Definition |
|--------|------------|
| Green | No single event loss > $6m |
| Red | Single event loss ≥ $6m |

The limit is set at 25% of the operational risk EaR number.

#### 4.6.3 L1 Stop Loss Breach

Stop losses are a control to ensure trading losses do not erode the P&L of the Bank. They are defined in the Market Risk Policy and split between levels 1-3.

The Level 1 limit is approved by the Board.

#### 4.6.4 Other Risks (Qualitative)

Other risks include:
- Operational risks
- Compliance risks
- Conduct risks
- Legal risks
- Reputational risks

**Monitoring:** Potential exposure to 'other risks' are monitored through various committees including:
- Operational Risk Committee
- Regulatory Compliance Committee
- Conduct & Culture Committee
- Transaction Acceptance Committee

**Breach Definition:** Any material breach of "other risks" constitutes a risk appetite excess by definition. A material breach is defined as one that results in a Level 1 (non-financial) operational risk incident as per the operational risk incident materiality matrix.

RMC will act as the final determinant as to whether an incident constitutes a breach of the RAS.

---

## 5. Level 2 Limit Setting

### 5.1 Process

The setting of quantitative limits at legal entity and risk type level is an iterative process that serves to embed risk appetite throughout the Bank. Risk type heads are responsible for ensuring that Level 2 risk appetite at different levels in the organisation:
- Are set at appropriate levels
- Are consistent with Level 1 risk appetite
- Are in line with the Bank's strategy and the way it operates

It is acceptable to only set a risk appetite limit and not a risk appetite trigger at Level 2.

### 5.2 Purpose

Purpose of Level 2 risk appetite:
- Ensure proactive risk management and timely initiation of management action
- Enable risk control and reporting purposes
- Monitor utilisation of available financial resources
- Monitor and manage risk profile and risk appetite

### 5.3 Earnings at Risk Allocation

EaR limits per risk type are allocated on the basis of perceived business demand for the forthcoming financial year and determined as part of the budget cycle.

The EaR Level 1 limit is allocated to risk types on a top-down basis with consideration to business strategy and growth. The limits proposed for each risk type are aggregated as an undiversified number through a correlation matrix. The net diversified number must tie back to the overall Level 1 limit.

### 5.4 Economic Capital Allocation

ECap limits per risk type are allocated on the basis of perceived business demand for the forthcoming financial year and determined as part of the budget cycle.

The ECap Level 1 limit is set as a solvency ratio; however, Level 2 limits reflect an actual allocation of the total AFR. The level of ECap allocated to risk types is set with a buffer to the total AFR.

No diversification benefit is granted as correlation is assumed to be high (1.0) under a 99.9% scenario.

### 5.5 Reallocation

Level 2 limits are able to be reallocated amongst risk types by RMC during the course of the year as long as the total Board-approved Level 1 limit is not exceeded.

### 5.6 Monitoring

Level 2 limit utilisation is monitored monthly at RMC.

---

## 6. Level 3 Limit Setting

### 6.1 Definition

Level 3 risk appetite is defined as portfolio limits. These metrics measure the legal entity exposure by risk type. Level 3 metrics may also be set and monitored at lower levels in the organisation, e.g., at product portfolio or desk levels.

### 6.2 Methodology

It is accepted that setting portfolio limits on a basis that is mathematically derived on a 1-to-1 basis (to Level 1 or 2 limits) is, in many cases, not possible. The interrelationship between variables is such that there is rarely one specific level of a portfolio variable that would lead to a breach in risk appetite.

Portfolio limits at different levels and cross-sections in the organisation need to be consistent. Thresholds or a target range should be set for each limit to ensure performance is at expected/acceptable levels. There is no prescribed format that limits should follow.

### 6.3 Approval

The setting of Level 3 risk appetite is the responsibility of the risk type head and limits must be approved by the relevant risk type governance committee.

### 6.4 Purpose

Purpose of Level 3 risk appetite:
- Ensure proactive risk management and timely initiation of management action
- Enable risk control and reporting purposes
- Monitor and manage risk profile and risk appetite

---

## 7. Monitoring and Reporting

### 7.1 RAS Dashboard

Compliance with the RAS (Level 1 limits), both current and in stressed conditions, is monitored at:
- Risk Management Committee (RMC): Monthly
- Asset & Liability Committee (ALCO): Monthly
- Executive Committee (ExCo): Monthly
- Board Risk Management Committee (BRMC): Quarterly

Some RAS metrics are calculated and monitored daily.

### 7.2 Reporting Cadence

| Report | Frequency | Recipients | Owner |
|--------|-----------|------------|-------|
| RAS Dashboard | Daily | CRO, CFO, Business Heads | Risk Operations |
| RAS Dashboard | Monthly | RMC, ALCO, ExCo | Risk Operations |
| RAS Dashboard | Quarterly | BRMC, Board | Risk Operations |
| Level 2 Utilisation | Monthly | RMC | Risk Type Heads |
| Level 3 Limits | Daily/Monthly | Risk Type Committees | Desk/Portfolio Heads |

### 7.3 Annual Review Process

The RAS and corresponding triggers and limits are reviewed at least annually:
- Risk is responsible for coordinating the annual process and tabling documents to BRMC and Board for approval
- Prior to submission to Board, the RAS must be recommended by RMC to ExCo who in turn recommends to BRMC
- The CRO will oversee the process
- The RAS should be noted at ALCO
- Risk is responsible for setting the Risk Appetite limits for Board approval
- As owners of the computations for Capital and Liquidity metrics, TCM will provide a limit recommendation to Risk

---

## 8. Governance

### 8.1 Approval Process

| Level | Owner | Approval Authority |
|-------|-------|-------------------|
| Level 1 & 2 Risk Appetite | CRO | Board (on recommendation from BRMC) |
| Level 2 Risk Type Allocations | Risk Type Heads | RMC |
| Level 3 Portfolio Limits | Desk/Portfolio Heads | Risk Type Committees |

**Note:** Board approves the total risk appetite amount annually. RMC has discretion to amend the allocation of appetite amongst risk types in line with business requirements so long as the total remains within the Board-approved tolerance.

### 8.2 Escalation and Remediation

#### 8.2.1 Level 1 Limit Breaches

**Earnings at Risk:**
- Escalation through RMC. If remediation not possible at RMC, Contingency ExCo convened
- CRO notifies ExCo and BRMC of breach and recommends corrective actions or condonation
- CRO responsible for ensuring resolution is implemented and tracked

**Economic Capital:**
- Escalation through RMC. If remediation not possible at RMC, Contingency ExCo convened
- CRO notifies ExCo and BRMC of breach and recommends corrective actions or condonation
- CRO responsible for ensuring resolution is implemented and tracked

**Regulatory Capital:**
- Escalation through Contingency ALCO
- CFO notifies ExCo and BRMC of breach including management actions to resolve
- CFO responsible for notifying PRA and Head Office of breach
- CFO responsible for ensuring resolution is implemented and tracked

**Liquidity:**
- Escalation through Contingency ALCO
- CFO notifies ExCo and BRMC of breach and recommends corrective actions or condonation
- CFO responsible for ensuring resolution is implemented and tracked

**Leverage:**
- Escalation through Contingency ALCO
- CFO reports Amber status or breach including management actions to monthly ALCO
- CFO responsible for notifying PRA (for leverage ratio breaches)
- CFO responsible for ensuring resolution is implemented and tracked

**Other Risks:**

| Breach Type | Escalation | Owner |
|-------------|------------|-------|
| Large Exposure | Capital Sub-Committee | CFO |
| Single Op Risk Event | RMC | CRO |
| Other Risks | RMC | CRO |

#### 8.2.2 Level 2 and 3 Limit Breaches

Breaches in Level 2 and 3 limits are escalated through RMC and the respective risk type committees. The CRO and RMC will monitor that appropriate management action is taken.

---

## 9. Exceptions

There are no exceptions to this Framework.

---

## 10. Related Policies and Standards

Please refer to the following related documents for further information:
- Risk Appetite Statement (GOV-L3-010)
- Enterprise Risk Management Framework
- Market Risk Policy (MR-L3-001)
- Credit Risk Policy (CR-L3-001)
- Operational Risk Policy (OR-L3-001)
- Liquidity Risk Policy (LR-L3-001)
- Large Exposures Policy
- Stop Loss Policy

All Bank policies can be located via the Bank's Intranet Document Portal.

---

## 11. Definitions

| Term | Definition |
|------|------------|
| **AFR** | Available Financial Resources |
| **ALCO** | Asset & Liability Committee |
| **BRMC** | Board Risk Management Committee |
| **CIB** | Capital Internal Buffer |
| **CRO** | Chief Risk Officer |
| **CFO** | Chief Financial Officer |
| **EaR** | Earnings at Risk |
| **ECap** | Economic Capital |
| **ExCo** | Executive Committee |
| **EWMA** | Exponentially Weighted Moving Average |
| **ILG** | Individual Liquidity Guidance |
| **IRRBB** | Interest Rate Risk in the Banking Book |
| **LCR** | Liquidity Coverage Ratio |
| **NSFR** | Net Stable Funding Ratio |
| **RAS** | Risk Appetite Statement |
| **RMA** | Risk Methodologies and Analytics |
| **RMC** | Risk Management Committee |
| **RNIMV** | Risk Not In Management VaR |
| **TCM** | Treasury & Capital Management |
| **VaR** | Value at Risk |

---

## 12. Contact

| Role | Name | Department |
|------|------|------------|
| Document Owner | Chief Risk Officer | Risk Management |
| Framework Contact | Head of Risk Operations | Risk Operations |

---

## 13. Version History

| Version | Date | Purpose | Key Changes |
|---------|------|---------|-------------|
| 1.0 | January 2025 | Initial version | New document aligned with ICBCS framework standards |
| 1.1 | January 2025 | Currency standardization | Converted all amounts from GBP to USD for reporting consistency |

---

*This document is the property of Meridian Global Bank. Unauthorised distribution is prohibited.*

*End of Document*
