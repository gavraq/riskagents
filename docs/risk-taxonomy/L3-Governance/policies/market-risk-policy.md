---
# Policy Metadata (for policy-updater skill)
policy_id: MR-L3-001
policy_name: Market Risk Policy
version: 1.6
effective_date: 2025-01-17
next_review_date: 2026-01-15
owner: Chief Risk Officer
approving_committee: RMC
document_classification: Internal
supersedes: null

# Taxonomy Linkages (L1 Requirements)
l1_requirements:
  - REQ-L1-001  # CRR/CRR III
  - REQ-L1-003  # FRTB
  - REQ-L1-004  # SS13/13 Market Risk
  - REQ-L1-013  # SS1/23 Model Risk
  - REQ-L1-022  # BCBS 239

# Taxonomy Linkages (L2 Risk Types)
l2_risk_types:
  - MR-L2-001   # Market Risk (General)
  - MR-L2-002   # Interest Rate Risk (Trading)
  - MR-L2-003   # Foreign Exchange Risk
  - MR-L2-004   # Equity Risk
  - MR-L2-005   # Commodity Risk
  - MR-L2-006   # Credit Spread Risk (Trading)
  - MR-L2-007   # Volatility Risk
  - MR-L2-008   # Illiquidity Risk
  - MR-L2-009   # Concentration Risk (Market)
  - MR-L2-010   # One-Way Risk

# Taxonomy Linkages (L4 Processes)
l4_processes:
  - MR-L4-001   # Market Risk Process Orchestration (Master)
  - MR-L4-002   # Trade Capture Controls
  - MR-L4-003   # EOD Market Data Snapshot
  - MR-L4-005   # Time Series Management
  - MR-L4-006   # Risk Engine Calculation (VaR/SVaR/Stress)
  - MR-L4-007   # Market Risk Reporting & Sign-off
  - MR-L4-008   # Backtesting
  - MR-L4-011   # Stress Testing
  - MR-L4-013   # Market Risk Limits Management (incl. Breach Management)
  - MR-L4-014   # Aged Inventory Monitoring

# Taxonomy Linkages (L5 Controls)
l5_controls:
  - MR-L5-001   # VaR Limits
  - MR-L5-002   # Stress Limits
  - MR-L5-003   # Greeks/Sensitivity Limits
  - MR-L5-004   # Backtesting Exception Limits
  - MR-L5-005   # Concentration Limits
  - MR-L5-006   # Stop-Loss Limits

# Taxonomy Linkages (L6 Models)
l6_models:
  - MR-L6-001   # Historical Simulation VaR
  - MR-L6-002   # Stressed VaR
  - MR-L6-003   # IRC Model
  - MR-L6-004   # Stress Scenario Models

# Taxonomy Linkages (L7 Systems)
l7_systems:
  - SYS-MR-001  # Murex (Trading System)
  - SYS-MR-002  # Valuation Engine
  - SYS-MR-003  # Risk Engine
  - SYS-MR-004  # Risk Reporting DataMart
  - SYS-MR-005  # Trade ODS
  - SYS-MR-006  # Market Data ODS
  - SYS-MR-007  # Valuations ODS
  - SYS-MR-008  # Risk ODS
---

# Market Risk Policy

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Policy ID** | MR-L3-001 |
| **Version** | 1.6 |
| **Effective Date** | 17 January 2025 |
| **Next Review** | 15 January 2026 |
| **Owner** | Chief Risk Officer |
| **Approving Committee** | Risk Management Committee (RMC) |

---

## 1. Purpose and Objectives
<!-- L1: REQ-L1-001, REQ-L1-003, REQ-L1-004 -->

### 1.1 Purpose

This Policy has been formulated to provide comprehensive guidance to ensure that the market risks faced by Meridian Global Bank ("MGB" / "the Bank") are properly identified, measured, controlled, and reported in order to minimise the risk of financial loss.

The Policy establishes a consistent framework for market risk management across all business lines and legal entities, ensuring global consistency of approach while respecting geographical differences in regulatory, compliance, and legal frameworks.

### 1.2 Policy Objectives

The main objectives of this Policy are:

- **Reference Framework**: To serve as the authoritative manual on market risk control policies used by the Market Risk function
- **Operating Model**: To explain how the Market Risk Control framework operates in practice
- **Interaction Model**: To detail the relationships, interactions, and expectations between Market Risk and other departments (and vice versa)
- **Control Principles**: To explain market risk principles including the limits framework and how risks should be identified, controlled, escalated, and reported

**Important Note**: This Policy is not a methodology document. Technical computational details and precise risk parameters are covered in separate methodology documents referenced in Section 11.

### 1.3 Scope of Application

This Policy applies to:

| In Scope | Out of Scope |
|----------|--------------|
| All trading book positions across all asset classes | Interest Rate Risk in the Banking Book (IRRBB) |
| All treasury positions with market risk exposure | Credit Spread Risk in the Banking Book (CSRBB) |
| All legal entities within the Meridian Global Bank Group | Credit Risk arising from counterparty default |
| All branches and subsidiaries globally | FX positions in the banking books (structural) |
| xVA exposures (CVA, FVA) and associated hedges | Large exposure reporting (owned by Treasury) |
| Physical commodity trading exposures in trading book | Staff costs (incentive schemes, post-retirement) |

This Policy applies to all staff who have responsibility and delegation for measuring, controlling, managing, escalating, and reporting limits versus exposure to market risk.

### 1.4 Relationship to Other Policies

Market Risk does not operate in isolation. This Policy is the umbrella policy supported by subsidiary Market Risk policies:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     MARKET RISK POLICY (This Document)                  │
│                           Umbrella Policy (MR-L3-001)                   │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         ▼                           ▼                           ▼
┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
│   VaR Policy        │   │ Stress Testing      │   │ Trading Book        │
│   (MR-L3-004)       │   │ Policy (MR-L3-005)  │   │ Boundary (MR-L3-006)│
│                     │   │                     │   │                     │
│ - VaR/SVaR          │   │ - Pillar Stresses   │   │ - TB vs BB          │
│ - Time Series       │   │ - PoW Process       │   │ - Reclassification  │
│ - Proxying          │   │ - Scenario Design   │   │ - Trading Intent    │
│ - RNIV              │   │ - Stress Limits     │   │ - FRTB Readiness    │
│ - Backtesting       │   │ - Environmental     │   │ - Aged Inventory    │
└─────────────────────┘   └─────────────────────┘   └─────────────────────┘
         │                           │                           │
         └───────────────────────────┴───────────────────────────┘
                                     │
                                     ▼
                    ┌────────────────────────────────┐
                    │   VaR Limit Framework          │
                    │   (MR-L3-003)                  │
                    │   - Detailed limit structure   │
                    └────────────────────────────────┘
```

This Policy also interfaces with other risk frameworks:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     MARKET RISK POLICY (This Document)                  │
│                           Trading Book Exposures                        │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
        ┌──────────────┬─────────────┼──────────────┬──────────────┐
        ▼              ▼             ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│Credit Risk   │ │NTMR Policy   │ │Liquidity     │ │Model Risk    │ │Operational   │
│Policy        │ │(IRRBB/CSRBB) │ │Risk Policy   │ │Policy        │ │Risk Policy   │
│- Issuer Risk │ │- Banking     │ │- Funding     │ │- SS1/23      │ │- RCSA        │
│- CVA         │ │  Book        │ │- LCR/NSFR    │ │- Validation  │ │- Controls    │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

When Country Risk allocates issuer risk exposure appetite to Market Risk for trading intent, Market Risk manages that exposure under this Policy. The traded debt issuance can be denominated in either hard currency or local currency. Market Risk measures issuer risk using mark-to-market valuation with a zero-recovery assumption.

---

## 2. Regulatory Framework
<!-- L1: REQ-L1-001, REQ-L1-003, REQ-L1-004, REQ-L1-013, REQ-L1-022 -->

### 2.1 Primary Regulations

The Prudential Regulation Authority's (PRA's) expectations for the management of market risk are set out in:

| Regulation | Reference | Key Requirements |
|------------|-----------|------------------|
| **CRR/CRR III** | Part 3, Title IV (Art 325-377) | Capital requirements for market risk; trading book boundary; Internal Model Approach (IMA) permissions |
| **FRTB** | CRR Art 325-361 | Fundamental Review of Trading Book; Standardised Approach; Internal Models Approach |
| **PRA SS13/13** | Chapters 2-9 | Market risk management expectations; governance; VaR; stress testing; backtesting |
| **PRA SS1/23** | All Principles | Model risk management; development; validation; governance |
| **BCBS 239** | Principles 1-14 | Risk data aggregation and reporting; accuracy; completeness; timeliness |

### 2.2 Internal Model Approval (IMA)

The Bank operates under PRA IMA permission for approved products and business lines. IMA approval requires:

- Documented and validated VaR methodology
- Daily backtesting and exception monitoring
- Regular model review and recalibration
- Compliance with qualitative standards (governance, stress testing, documentation)

Products outside IMA scope are capitalised under the Standardised Approach.

---

## 3. Market Risk Definition and Types
<!-- L2: MR-L2-001 through MR-L2-010 -->

### 3.1 Definition

**Market Risk** in the Trading Book is the risk associated with the change in market value of any market risk underlier, whether "Actual" or "Hypothetical" in nature (in accordance with PRA prescribed definitions under backtesting quarterly reporting). Market risk can be systemic or idiosyncratic in nature and is typically categorised into the asset classes defined below.

### 3.2 Risk Types Addressed

This Policy addresses the following risk types as defined in the Bank's Risk Taxonomy (Level 2):

| Risk Type | Node ID | Definition | Examples |
|-----------|---------|------------|----------|
| **General Market Risk** | MR-L2-001 | Risk of loss from adverse movements in market prices affecting the overall portfolio | Broad market sell-offs; flight to quality |
| **Interest Rate Risk (Trading)** | MR-L2-002 | Risk of loss due to adverse interest rate movements, primarily related to fixed income and interest rate products | Curve steepening; parallel shifts; basis moves |
| **Foreign Exchange Risk** | MR-L2-003 | Risk of loss related to an international financial transaction as a result of currency fluctuations | G10 spot moves; EM devaluations; cross-currency basis |
| **Equity Risk** | MR-L2-004 | Financial risk associated with holding equity investments which may depreciate due to market movements | Index declines; single stock events; sector rotation |
| **Commodity Risk** | MR-L2-005 | Risk of loss due to uncertainty in future market values as a result of fluctuation in commodity prices | Oil price shocks; metals volatility; agricultural supply disruption |
| **Credit Spread Risk (Trading)** | MR-L2-006 | Financial risk associated with changes in the market perception of traded credit risk, excluding interest rate effects | Spread widening; credit events; rating migrations |
| **Volatility Risk** | MR-L2-007 | Risk from changes in implied volatilities affecting option valuations | Vol surface moves; skew changes; term structure shifts |
| **Illiquidity Risk** | MR-L2-008 | Risk from inability to trade at conventional bid-offer spreads within normal timeframes | Market seizures; wide bid-offers; no market depth |
| **Concentration Risk (Market)** | MR-L2-009 | Risk from excessive exposure to single risk factors, issuers, or instruments | Single-name concentrations; curve point concentrations |
| **One-Way Risk** | MR-L2-010 | Risk from crowded positioning where the market moves against a widely-held position | Consensus trades unwinding; basis trades blowing out |

### 3.3 Trading Book Boundary

The Bank maintains a clear boundary between Trading Book and Banking Book per CRR Article 104. The boundary is fundamental to ensuring appropriate risk measurement and capital treatment:

| Trading Book | Banking Book |
|--------------|--------------|
| Positions held with short-term trading intent | Positions held to maturity or contractual term |
| Positions arising from client facilitation | Structural hedges |
| Positions to hedge other trading book items | Strategic equity investments |
| Market-making inventory | Lending and deposit-taking activities |

Boundary management is subject to quarterly review by Market Risk and Finance, with any proposed reclassifications requiring RMC approval.

---

## 4. Governance
<!-- L3: MR-L3-001, MR-L3-002, MR-L3-003 -->

### 4.1 Committee Structure

The Market Risk framework is supported by the Bank's committee structure:

```
                              Board
                                │
                ┌───────────────┴───────────────┐
                │                               │
        Board Risk                        Executive
        Management ◄─────────────────────► Committee
        Committee                               │
                │                               │
                └───────────────┬───────────────┘
                                │
                        Risk Management
                          Committee
                                │
                ┌───────────────┴───────────────┐
                │                               │
        Market &                          Risk Model
       Liquidity Risk                      Approval
        Committee                         Committee
                                                │
                                    ┌───────────┴───────────┐
                                    │                       │
                              Risk Technical          Model Risk
                                 Forum               Management
                                                        Forum
```

**Note**: BRMC provides independent risk oversight to the Board, while ExCo handles executive management. RMC reports to both, ensuring alignment between risk governance and business execution. Both the Risk Technical Forum and Model Risk Management Forum sit under RMAC, providing working-level technical support for model development, methodology review, and validation activities.

### 4.2 Committee Responsibilities

**Board Risk Management Committee (BRMC)** meets quarterly and is responsible for:
- Approval of Level 1 Market Risk limits (entity-level risk appetite)
- Quarterly assessment and monitoring of market risk appetite under normal and stress conditions
- Level 1 breach notification and risk updates from the CRO
- Providing the Board with advice on risk strategy including oversight of current risk exposures

**Risk Management Committee (RMC)** meets monthly (or as required for contingency situations) and is responsible for:
- Discussion and challenge on key risks across all risk types
- Recommendation of Level 1 limit changes to BRMC
- Approval of minor policy changes (material changes require BRMC)
- Contingency meetings for limit breaches or stressed market situations

**Market & Liquidity Risk Committee (MLRC)** meets weekly and is responsible for:
- Monitoring and controlling market risk for all trading businesses
- Overseeing adherence to BRMC-approved market risk appetite
- Reviewing and recommending Level 1 market risk limits to RMC
- Annual review of this Market Risk Policy
- Monitoring all key market controls versus trading book limits
- Monitoring Market Risk Regulatory Capital, ECAP, and EaR
- Approving Level 2 limit changes
- Reviewing and noting stress testing methodology

See: [MLRC Terms of Reference](../committees/mlrc-terms-of-reference.md)

**Risk Model Approval Committee (RMAC)** meets monthly and is responsible for:
- Providing assurance that technical aspects of model development, quantitative methodologies, model monitoring, and model validation are independently reviewed
- Ensuring adherence to supervisory model standards (SS1/23)

### 4.3 Three Lines of Defence

In accordance with the Bank's Risk & Control Framework, the Bank operates a three lines of defence model which ensures independence of oversight functions and that Risk has an uninterrupted line of reporting to the Board:

| Line | Function | Market Risk Responsibilities |
|------|----------|------------------------------|
| **1st Line** | Trading Desks, Treasury, Product Control | Day-to-day risk taking within limits; position management; P&L sign-off; trade booking; operating within mandates |
| **2nd Line** | Market Risk, Risk Methodology & Analytics, Model Validation | Independent oversight; limit setting; methodology; reporting; VaR sign-off; model validation |
| **3rd Line** | Internal Audit | Independent assurance over market risk framework; control testing; process audits |

### 4.4 Roles and Responsibilities

**4.4.1 Market Risk** is responsible for:
- Oversight and control of all key market risk controls (Stop Loss, Backtesting, Stress Loss, Traded Limits)
- Monitoring, change, and breach escalation management of all market risk limits
- Daily VaR, IRC, and Backtesting sign-off
- Monthly Point of Weakness (PoW) top risks discussion and challenge
- Stress testing policy, procedures, and parameters
- Level 2 limit setting and allocation
- Selection of appropriate risk factor proxies
- Market risk contribution to the New Product Approval process
- Quarterly review of the market risk Model Registry

**4.4.2 Risk Methodology & Analytics (RMA)** is responsible for:
- VaR methodology documentation
- Risks Not in VaR (RNIV) framework
- Proxy methodology and periodic review of proxy suitability
- Model calibration and maintenance
- Providing New Product Approval input as required

**4.4.3 Model Validation** is responsible for:
- Independent validation of valuation and risk sensitivities
- Validation of VaR/SVaR/IRC/ECAP models and RNIV framework
- Validation of curve interpolation and construction methodologies
- Validation of proxy methodology
- Providing New Product Approval input

**4.4.4 Front Office** is responsible for:
- Operating in compliance with this Policy and trading within approved limits
- Operating reliable trading systems that fully support positioning and risk identification
- Abiding by regulations governing the relevant markets
- Timely sign-off of VaR and P&L
- Owning and operating within trading mandates
- Quarterly review of the Model Registry

**4.4.5 Product Control** is responsible for:
- Ensuring all books are captured in P&L systems
- Maintenance of accounting hierarchies
- Obtaining P&L sign-offs from Front Office
- Secondary control for checking accuracy of Independent Price Verification (IPV)
- Daily distribution of trading summary
- Timely backtesting data delivery and sign-off

**4.4.6 Reporting Analysis & Validation (RAV)** is responsible for:
- Data validation and integrity of market risk reporting processes
- Populating, validating, and maintaining market data time series for VaR and IPV
- Sensitivity data, VaR, and IRC data validation
- Daily sign-off of Market Risk ECAP
- Identification of data points requiring proxying
- Setup of stress scenarios in the Risk Engine
- Market Risk regulatory capital production
- Key market risk controls reporting and excess documentation

### 4.5 Escalation Framework

Market Risk has established clear escalation paths to ensure timely response to risk events:

| Trigger | Escalate To | Timeline | Required Action |
|---------|-------------|----------|-----------------|
| VaR limit warning (80%) | MLRC | Same day | Heightened monitoring; no new risk without approval |
| VaR limit breach (<110%) | CRO + MLRC | Immediate | Action plan within 24 hours |
| VaR limit breach (>110%) | CRO + RMC Chair + Board Risk | Immediate | Emergency RMC; formal reduction plan |
| Backtesting exception | MLRC | Next meeting | P&L explanation required |
| 4+ exceptions (rolling 250 days) | RMC + PRA notification | Within 5 days | Model review triggered |
| Model failure | CRO | Immediate | Contingency procedures activated |
| Stop-loss breach (Level 1) | CRO + RMC + Board | Immediate | Contingency RMC; position reduction |

---

## 5. Risk Appetite
<!-- L1: REQ-L1-001, REQ-L1-003 -->
<!-- L5: MR-L5-001, MR-L5-002, MR-L5-006 -->

### 5.1 Risk Appetite Determination

Risk appetite across all risk types is determined for the Bank as a whole and is reviewed annually as part of the business planning and budgeting process. The Risk Appetite Statement is governed by the Risk Appetite Framework, which is recommended by RMC for Board-level approval.

In determining market risk appetite, consideration is given to:
- Business proposals assessing requirements for risk warehousing
- Anticipated income from position-taking and client facilitation
- Available regulatory and economic capital
- The Bank's overall risk appetite and strategic objectives
- Peer benchmarking and industry standards

### 5.2 Risk Appetite Statement

*"Meridian Global Bank accepts market risk in pursuit of its trading and treasury activities, within a controlled framework that ensures capital adequacy and limits potential losses to levels that do not threaten the Bank's financial stability or strategic objectives. The Bank seeks to generate sustainable returns from market-making and client facilitation, while maintaining robust controls against tail risks and concentrated exposures."*

### 5.3 Quantitative Risk Appetite

Market risk appetite is expressed through Level 1 limits approved by the Board:

| Metric | Target (Appetite) | Limit | Frequency |
|--------|-------------------|-------|-----------|
| **Management VaR** (99%, 1-day) | <$20m | $25m | Daily |
| **Stressed VaR** (99%, 10-day) | <$40m | $50m | Daily |
| **Stress Loss** (Pillar scenarios) | <$125m | $190m | Weekly |
| **Entity Stop-Loss** | N/A | $75m MTD | Daily |
| **Backtesting Exceptions** | <4 (green zone) | <10 (red zone) | Rolling 250 days |

### 5.4 Qualitative Risk Appetite

The Bank has **LOW** appetite for:
- Illiquid positions that cannot be exited within 10 business days at conventional bid-offer spreads
- Concentrated positions exceeding 10% of 30-day average daily volume
- Complex derivatives without established, validated pricing models
- Exposure to emerging market currencies beyond the approved country list
- Aged inventory (positions held >6 months with minimal turnover)
- Positions requiring significant proxy assumptions in VaR

The Bank has **MODERATE** appetite for:
- Directional risk-taking within approved limits and mandates
- Basis and relative value strategies with understood risk profiles
- Market-making activities in approved products and markets

---

## 6. Key Market Risk Controls
<!-- L5: MR-L5-001 through MR-L5-006 -->

In accordance with the Bank's Operational Risk Management framework, Market Risk has identified **four key market risk controls** which are formally tracked and reported to MLRC:

### 6.1 Stop-Loss Controls
<!-- L5: MR-L5-006 -->

Stop-losses are set to ensure that trading losses do not erode, or have the potential to erode, the income generated by market-making and client facilitation activities. Stop-losses represent a critical P&L protection mechanism.

**Stop-Loss Structure**:

| Level | Scope | Owner | Breach Escalation |
|-------|-------|-------|-------------------|
| Level 1 | Entity (Bank-wide) | Board/CRO | Contingency RMC; CEO, Head of Trading, CRO sign-off to continue |
| Level 2 | Business Unit / Region | Market Risk | Head of Market Risk and relevant Trading Head |
| Level 3 | Desk / Trader | Business Head | Managed by business with notification to Market Risk |

**High-Water Mark Methodology**: Stop-losses are measured relative to the year-to-date "high water mark" (HWM) - the maximum year-to-date revenue for the particular trading portfolio. A stop-loss breach occurs when current year-to-date revenue falls below the HWM by more than the stop-loss amount.

### 6.2 Stress Testing Controls
<!-- L5: MR-L5-002 -->

Stress testing is an essential control to assess the loss vulnerabilities of the trading portfolio against tail moves across all trading risk factors. Stress testing is reported daily across a combination of:

- **Top-Down Macro Scenarios**: Pillar stress scenarios that stress the entire portfolio
- **Bottom-Up Point of Weakness**: Weekly identification and stressing of key trading strategies

See Section 9 for detailed stress testing framework.

### 6.3 Backtesting Controls
<!-- L5: MR-L5-004 -->

Backtesting is a VaR model integrity test performed at entity and business levels. Backtesting is conducted daily at the 99% confidence level, comparing:

- **Hypothetical P&L**: Clean P&L from overnight risk factor moves only
- **Actual P&L**: Full P&L including intraday trading, fees, and funding costs

A backtesting exception occurs when the loss exceeds the VaR prediction. Both positive exceptions (gains > VaR) and negative exceptions (losses > VaR) are tracked and analysed.

### 6.4 Limit Monitoring Controls
<!-- L5: MR-L5-001, MR-L5-003, MR-L5-005 -->

Limits are required at all levels (Entity, Business Unit, Desk) and are reviewed annually. All key trading exposures are monitored against limits daily and escalated per the governance structure.

See Section 7 for detailed limit framework.

---

## 7. Limit Framework
<!-- L5: MR-L5-001 through MR-L5-006 -->

### 7.1 Limit Hierarchy

Limits operate at three distinct levels with cascading delegated authority:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        LEVEL 1 LIMITS                                   │
│                    (Board / RMC Approved)                               │
│                                                                         │
│   Entity VaR: $25m │ Entity SVaR: $50m │ Stress: $190m │ Stop: $75m     │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         ▼                          ▼                          ▼
┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
│    LEVEL 2 LIMITS   │   │    LEVEL 2 LIMITS   │   │    LEVEL 2 LIMITS   │
│  (MLRC Approved)    │   │  (MLRC Approved)    │   │  (MLRC Approved)    │
│                     │   │                     │   │                     │
│  Markets: $19m VaR  │   │  Treasury: $6m VaR  │   │  Reserve: $3m VaR   │
│  + Sensitivity      │   │  + Sensitivity      │   │  (Unallocated)      │
│  + Concentration    │   │  + Concentration    │   │                     │
└──────────┬──────────┘   └──────────┬──────────┘   └─────────────────────┘
           │                         │
           ▼                         ▼
┌─────────────────────┐   ┌─────────────────────┐
│    LEVEL 3 LIMITS   │   │    LEVEL 3 LIMITS   │
│  (Business / MR)    │   │  (Business / MR)    │
│                     │   │                     │
│  Desk-level VaR     │   │  Desk-level VaR     │
│  Trader limits      │   │  Trader limits      │
└─────────────────────┘   └─────────────────────┘
```

**Note**: Sum of sub-limits may exceed parent limit due to assumed diversification benefit (typically 20-30% at division level).

### 7.2 Limit Types

| Limit Type | Node ID | Purpose | Monitoring | Approval |
|------------|---------|---------|------------|----------|
| **VaR Limits** | MR-L5-001 | Control overall portfolio risk | Daily | Level 1: Board; Level 2: MLRC |
| **Stress Limits** | MR-L5-002 | Control tail risk exposure | Weekly (daily in stressed periods) | RMC |
| **Sensitivity Limits** | MR-L5-003 | Control risk factor concentrations (DV01, CS01, Vega, FX Delta) | Intraday (hourly) | MLRC |
| **Backtesting Limits** | MR-L5-004 | Monitor model performance | Daily | MLRC |
| **Concentration Limits** | MR-L5-005 | Avoid single-name/factor risk | Daily | MLRC |
| **Stop-Loss Limits** | MR-L5-006 | P&L protection | Intraday (hourly) | Level 1: Board; Level 2: MLRC |

### 7.3 Limit Breach Classification

Limit breaches are classified into three categories with different escalation requirements:

**Major Breach**:
- Any Level 1 limit breach; OR
- A Level 2 limit where the excess is greater than 25% of that limit

**Minor Breach**:
- A Level 2 limit where the excess is less than 25% of the limit

**Technical Breach**:
- Excess caused by Front Office / Risk IT system issues (with associated OpRisk incident)
- New issuer risk exposures not yet assigned to static data
- Market Risk approved limit changes that missed system cut-off
- Late trades booked after platform close with appropriate notification

Technical breaches are classified at the sole discretion of Market Risk and assessed on a case-by-case basis.

### 7.4 Limit Breach Management

| Breach Type | Notification | Documentation | Resolution |
|-------------|--------------|---------------|------------|
| **Technical** | Market Risk to relevant parties | Logged in Market Risk System; OpRisk if incident | Resolve within 4 hours |
| **Minor** | Same-day notification to trader and desk head | Breach log to MLRC monthly | Action plan agreed with Trading Head |
| **Major** | Immediate notification to CRO, Head of Trading, Head of Market Risk | Full breach report to MLRC/RMC | Contingency RMC if Level 1; immediate risk reduction |

### 7.5 Temporary Limit Excesses

| Authority | Maximum Excess | Maximum Duration | Conditions |
|-----------|----------------|------------------|------------|
| MLRC | 10% of limit | 5 business days | Documented rationale; daily monitoring |
| RMC | 20% of limit | 10 business days | Formal request; reduction trajectory |
| Board | >20% of limit | As approved | Exceptional circumstances only |

See: [VaR Limit Framework](./var-limit-framework.md)

---

## 8. Risk Measurement
<!-- L6: MR-L6-001, MR-L6-002, MR-L6-003 -->

### 8.1 Measurement Framework

The measurement of market risks addresses both normal market conditions and stressed market conditions separately. The risk measures can be categorised as follows:

| Category | Measures | Purpose |
|----------|----------|---------|
| **Positional Risk** | Notional, MTM value, sensitivities (Greeks), issuer risk | Initial identification and control of trading exposures |
| **Value at Risk** | Management VaR (1d 99%), IMA VaR (10d 99%), SVaR | Probabilistic loss estimate under normal/stressed conditions |
| **Stress Testing** | Top-down pillar stresses, bottom-up Point of Weakness | Tail risk identification and quantification |
| **Capital Measures** | Economic Capital (ECAP), Regulatory Capital | Capital adequacy and allocation |

### 8.2 Value at Risk (VaR)
<!-- L6: MR-L6-001 -->

**Methodology**: Historical Simulation VaR

The Bank uses Historical Simulation VaR as its primary risk measure. This methodology:
- Applies actual historical market movements to current positions
- Makes no assumptions about the distribution of returns
- Captures fat tails and non-linearities present in historical data
- Provides intuitive scenario-based explanations of VaR

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Confidence Level | 99% | Regulatory standard; captures 1-in-100 day loss |
| Holding Period | 1 day (scaled to 10-day for capital) | Daily risk management horizon |
| Lookback Period | 500 business days (~2 years) | Captures multiple market regimes |
| Weighting | Equal weighting | Conservative approach; no decay of extreme events |
| Simulation Count | 500 scenarios | Full historical window |

**Production Schedule**: Daily by T+1 07:00 GMT

**Distinction**: The Bank distinguishes between:
- **Management VaR (MVaR)**: Encompasses all trading book activity
- **IMA VaR**: Subset of businesses and products approved by PRA for Internal Model Approach capital calculation

See: [VaR Methodology Document](../../L6-Models/market-risk/var-svar-methodology.md)

### 8.3 Stressed VaR (SVaR)
<!-- L6: MR-L6-002 -->

**Methodology**: Historical Simulation using dynamically-selected stressed period

Unlike approaches that fix the stress period to a single historical event, the Bank employs a dynamic stress period selection methodology that ensures the SVaR captures the most severe conditions relevant to the current portfolio:

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Historical Window | Back to 2007 (17+ years) | Captures GFC, European Sovereign Crisis, COVID, and other stress events |
| Confidence Level | 99% | Consistent with VaR |
| Holding Period | 10 days | Regulatory requirement |
| Stress Period Selection | **Dynamic - Weekly recalibration** | Selects 12-month window producing worst VaR for current portfolio |

**Dynamic Stress Period Selection Process**:
1. Weekly, the full VaR calculation is run using all historical windows back to 2007
2. For each potential 12-month stress window, the portfolio VaR is calculated
3. The window producing the highest VaR for the current portfolio is selected as the stress period
4. This ensures SVaR captures the stress conditions most relevant to the Bank's actual risk profile
5. The selected stress period and rationale are documented and reported to MLRC

This methodology is superior to a fixed stress period (e.g., permanently using 2008-2009) because:
- It adapts to changes in portfolio composition
- It captures stress periods most relevant to current exposures
- It avoids understating risk if the current portfolio differs significantly from 2008
- It satisfies regulatory intent to capture "significant financial stress"

### 8.4 Incremental Risk Charge (IRC)
<!-- L6: MR-L6-003 -->

For positions subject to default and migration risk (primarily credit trading book):

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Confidence Level | 99.9% | Regulatory requirement |
| Horizon | 1 year | Capture full credit cycle |
| Liquidity Horizons | 3-12 months by rating | Higher-rated names more liquid |
| Correlation Model | Constant maturity approach | Industry standard |

### 8.5 Sensitivities (Greeks)

The Bank calculates and monitors the following sensitivities to enable granular risk factor control:

| Greek | Risk Factor | Definition | Use |
|-------|-------------|------------|-----|
| **Delta** | Underlying price | First-order price sensitivity | Directional exposure control |
| **Gamma** | Underlying price | Second-order price sensitivity | Non-linearity identification |
| **Vega** | Volatility | Sensitivity to implied vol | Options risk control |
| **Theta** | Time | Time decay | P&L attribution |
| **Rho** | Interest rates | IR sensitivity | Duration management |
| **CS01** | Credit spread | 1bp credit spread sensitivity | Credit trading control |
| **DV01** | Interest rates | 1bp rate sensitivity | Rates trading control |

Sensitivities are aggregated to appropriate control levels and monitored against limits on an intraday (hourly) basis.

### 8.6 Economic Capital (ECAP)

For management purposes, Economic Capital is calculated to provide a more complete view of risk than regulatory capital:

| Parameter | ECAP | Regulatory Capital | Difference |
|-----------|------|-------------------|------------|
| Confidence Interval | 99.9% | 99% | ECAP more conservative |
| Horizon | 10-25 days (asset class dependent) | 10 days | ECAP captures illiquidity |
| SVaR Treatment | Worst of VaR/SVaR | VaR + SVaR | Regulatory more conservative |
| Multiplier | 1.0 | 3.0-4.0 | Regulatory includes buffer |

#### 8.6.1 ECAP Regulatory Drivers

ECAP forms a core component of the Bank's Internal Capital Adequacy Assessment Process (ICAAP):

| Regulation | Requirement | Policy Response |
|------------|-------------|-----------------|
| **CRD VI Art 76** | Firms must have sound internal capital adequacy assessment processes | ECAP provides internal market risk capital for ICAAP |
| **CRR Art 73-96** | Pillar 2 supervisory review requires internal assessment beyond Pillar 1 minimums | ECAP evidence used in SREP dialogue with PRA |
| **PRA SS13/13** | Firms should calculate economic capital for market risk | ECAP methodology aligned to SS13/13 expectations |
| **BCBS Pillar 2** | Banks must assess capital for all material risks not fully captured under Pillar 1 | ECAP captures illiquidity and concentration beyond IMA |

#### 8.6.2 ECAP Governance

- **Daily Production**: ECAP calculated overnight alongside VaR/SVaR by Risk Engine (MR-L4-006)
- **Daily Sign-off**: RAV signs off ECAP as part of Market Risk Report (MR-L4-007)
- **MLRC Monitoring**: ECAP vs. Regulatory Capital comparison reported weekly to MLRC
- **ICAAP Contribution**: Quarterly feed to Capital Planning for ICAAP submission
- **ALCO Reporting**: Monthly ECAP utilisation against allocated capital

---

## 9. Stress Testing
<!-- L4: MR-L4-003 -->
<!-- L5: MR-L5-002 -->
<!-- L6: MR-L6-004 -->

### 9.1 Stress Testing Framework

Stress testing is essential to understand the portfolio's vulnerability to tail events that may not be captured in VaR. The framework operates at multiple levels:

| Type | Frequency | Purpose | Governance |
|------|-----------|---------|------------|
| **Regulatory Scenarios** | Weekly | ICAAP, capital planning, regulatory reporting | RMC approval |
| **Historical Scenarios** | Weekly | Calibration to known crisis events | MLRC review |
| **Hypothetical Scenarios** | Monthly | Emerging risks, what-if analysis | MLRC approval |
| **Reverse Stress Tests** | Quarterly | Identify conditions that threaten viability | RMC review |
| **Point of Weakness (PoW)** | Weekly | Bottom-up stress of key trading strategies | MLRC review |

### 9.2 Stress Scenario Design

Stress tests capture the following effects where applicable:

- **Concentration risk**: Impact of unwinding large positions relative to market depth
- **Abnormal market movements**: Yield curves (parallel, steepening, flattening), volatility surfaces, spot underliers, credit spreads
- **Liquidity deterioration**: Reduced volumes, wider bid-offers, crowding out effects
- **Non-linearity**: Deep out-of-the-money options, gap risk, convexity
- **Credit events**: Defaults, rating migrations, recovery rate changes
- **Correlation breakdown**: Historical correlations failing under stress
- **Basis risk**: Hedge effectiveness under stress
- **Central bank actions**: What-if scenarios around monetary policy

### 9.3 Standard Pillar Scenarios

| Scenario | Type | Key Shocks | Limit |
|----------|------|------------|-------|
| Global Financial Crisis | Historical | Credit spreads +500bp, Equities -40%, Vol +200% | $190m |
| COVID-19 Shock | Historical | Vol +300%, Oil -50%, Credit +300bp | $125m |
| Rates Shock Up | Hypothetical | Parallel +200bp across curves | $100m |
| EM Crisis | Hypothetical | EM FX -30%, EM Spreads +300bp | $95m |
| Stagflation | Hypothetical | Rates +150bp, Equities -25%, Commodities +30% | $95m |
| Worst-of Pillar | Dynamic | Worst result across all scenarios | $190m |

### 9.4 Point of Weakness (PoW) Process

The Point of Weakness process provides bottom-up stress testing of key trading strategies:

1. **Weekly Identification**: Market Risk identifies top risk positions and strategies
2. **Bottom-Up Stressing**: Specific stress scenarios designed for each strategy
3. **Discussion Forum**: Weekly PoW discussion with Trading Heads and Risk
4. **Monthly Deep Dive**: Monthly meeting with CRO, Head of Trading, and senior risk

This supplements top-down pillar stresses by focusing on specific vulnerabilities in current positioning.

### 9.5 Environmental Risk Stress Testing

Environmental risk can manifest through:
- **Transition Risk**: Policy changes, carbon pricing, technology disruption affecting asset values
- **Physical Risk**: Weather events affecting commodity prices, collateral values

Environmental stress scenarios are designed at the same severity as other pillar stresses and reviewed annually. Considerations include:
- Carbon pricing scenarios
- Policy change impacts on specific sectors
- Physical event impacts on commodity portfolios
- Collateral accessibility under physical stress

See: [Pillar Stress Generator Skill](../../../../.claude/skills/pillar-stress-generator/)

---

## 10. Risk Identification and Management Processes
<!-- L2: MR-L2-001 through MR-L2-010 -->
<!-- L4: MR-L4-001 through MR-L4-006 -->

### 10.1 Risk Identification

The process for ensuring all market risks are accurately captured is dynamic and requires continuous evaluation. Market Risk engages in both tactical (daily) and strategic (periodic) risk identification:

**Daily Identification Activities**:
- Review of market and price information from Bloomberg, Reuters
- Daily P&L analysis and decomposition
- Position and sensitivity monitoring
- VaR and stress movements

**Periodic Identification Activities**:
- Meetings with regulators, credit agencies, exchanges
- Review of regulatory letters and industry reports
- Risk & Control Self-Assessments (RCSA) with Operational Risk
- New Products and Significant Transactions Approval (NPSTA) process
- Model Risk management and maintenance
- Environmental risk assessment

### 10.2 New Product Approval Process
<!-- L4: MR-L4-004 -->

All new products, instruments, or trading strategies must be approved through the NPSTA process before trading commences. Market Risk and RMA are members of the NPSTA Working Group.

**Approval Requirements**:
1. Risk identification and assessment
2. Pricing model validation (or plan for validation)
3. System capability confirmation (booking, risk, P&L)
4. Limit structure proposal
5. Regulatory capital treatment confirmation
6. MLRC approval (RMC for material/complex products)

### 10.3 Trade Capture and Booking

Timely and accurate trade capture is essential for risk measurement. Front Office is expected to:
- Book trades within 15 minutes of execution
- Ensure bookings fully represent the economic payoff and risk
- Notify Market Risk and Product Control of late bookings (after system close)
- Log and follow up on any approximate bookings

### 10.4 Daily Risk Sign-Off Process
<!-- L4: MR-L4-001 -->

| Time (T+1) | Activity | Owner |
|------------|----------|-------|
| 06:00 | Risk systems produce overnight VaR, sensitivities | Risk IT |
| 07:00 | VaR report available; initial review | RAV |
| 07:30 | Market Risk review and challenge | Market Risk |
| 08:00 | Front Office VaR sign-off | Trading Desks |
| 08:30 | P&L sign-off | Product Control |
| 09:00 | Backtesting sign-off | Market Risk + Product Control |

### 10.5 Trading Risk Reviews

Regular meetings between Front Office, Market Risk, and Product Control ensure formalised communication and discussion of emerging risks. The Point of Weakness weekly reporting is central to this process.

**Typical Agenda**:
- Market developments and geopolitical changes
- P&L review and main contributing factors
- Valuations and reserves (if required)
- Risk positions and disputed items
- Limit breaches or high utilisation
- New markets, products, or notable deals

### 10.6 Aged Inventory Management

The Bank monitors aged positions to identify potential illiquidity and concentration risks:

**Definition**: Positions held for >6 months with minimal turnover and/or outside agreed expectations at time of initial trade request.

**Monitoring**:
- Quarterly analysis by Market Risk
- Focus on issuer risk positions >$5m equivalent
- Results feed into illiquidity/concentration ICAAP assessments
- Reported to MLRC

#### 10.6.1 Aged Inventory Regulatory Drivers

| Regulation | Requirement | Policy Response |
|------------|-------------|-----------------|
| **CRR Art 325** | Trading book positions must have trading intent and be capable of being sold/hedged in an orderly manner | Quarterly attestation of trading intent for aged positions |
| **PRA SS13/13 Ch 2** | IMA scope requires positions to demonstrate exit capability | Exit strategy documented and monitored for aged inventory |
| **CRD VI Art 79** | Firms must manage concentration risk in trading book | Aged inventory cross-referenced to concentration limits |
| **BCBS 239** | Risk data aggregation must be complete and accurate | Comprehensive aged inventory tracking and reporting |

> **Process Reference**: For detailed aged inventory monitoring procedures, see [Market Risk Limits Management (MR-L4-013) Section 10](../../L4-Processes/processes/market-risk-limits-management.md).

---

## 11. Model Risk Management
<!-- L1: REQ-L1-013 -->
<!-- L6: MR-L6-001 through MR-L6-004 -->

### 11.1 Model Governance

All market risk models are subject to the Bank's Model Risk Management Framework (SS1/23 compliant). Since the introduction of the PRA's SS1/23 in May 2023, there are heightened expectations for model risk management across all risk disciplines.

| Stage | Requirement | Governance |
|-------|-------------|------------|
| Development | Documented methodology, assumptions, limitations | RMA ownership |
| Validation | Independent validation before production use | Model Validation |
| Approval | Model Risk Committee approval | RMAC |
| Monitoring | Ongoing performance monitoring, backtesting | Market Risk |
| Maintenance | Calibration, data updates, parameter reviews | RMA |
| Review | Annual revalidation and fitness-for-purpose assessment | Model Validation |

### 11.2 Model Inventory (Market Risk)

| Model ID | Model Name | Tier | Owner | Last Validated |
|----------|------------|------|-------|----------------|
| MR-L6-001 | Historical Simulation VaR | 1 | RMA | 2024-06 |
| MR-L6-002 | Stressed VaR | 1 | RMA | 2024-06 |
| MR-L6-003 | IRC Model | 1 | RMA | 2024-09 |
| MR-L6-004 | Stress Scenario Framework | 2 | Market Risk | 2024-03 |

### 11.3 Risks Not in VaR (RNIV)

Where the VaR model does not fully capture all market risks (due to proxy assignments, missing risk factors, or model limitations), these risks are identified and quantified as Risks Not in VaR (RNIV). The RNIV framework includes:

- Identification of missing risk factors
- Quantification methodology
- Capital add-on calculation
- Quarterly review at Model Risk Management Forum

---

## 12. Data, Systems, and Reporting
<!-- L1: REQ-L1-022 -->
<!-- L7: SYS-MR-001 through SYS-MR-005 -->

### 12.1 Systems Architecture

The architecture separates valuation (EOD snapshot) from risk calculation (time series based):

```
                              SOURCE SYSTEMS
┌──────────────────────────────────────────────────────────────────────────────┐
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐                      │
│  │    Murex     │   │  Market Data │   │  Time Series │                      │
│  │  (Trading)   │   │   Service    │   │   Service    │                      │
│  │              │   │ (EOD Prices, │   │ (Historical  │                      │
│  │   Trades     │   │   Curves)    │   │  Returns)    │                      │
│  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘                      │
└─────────┼──────────────────┼──────────────────┼──────────────────────────────┘
          │                  │                  │
          ▼                  │                  │
┌──────────────────────────┐ │                  │
│      TRADE ODS           │ │                  │
│  (Positions, Trades)     │ │                  │
└───────────┬──────────────┘ │                  │
            │                │                  │
            │    ┌───────────┘                  │
            │    │                              │
            ▼    ▼                              │
┌─────────────────────────┐                     │
│   VALUATION ENGINE      │                     │
│                         │                     │
│  Trades + EOD Market    │                     │
│  Data Snapshot          │                     │
│         │               │                     │
│         ▼               │                     │
│  ┌─────────────────┐    │                     │
│  │  MTM, Greeks,   │    │                     │
│  │  Sensitivities  │    │                     │
│  └────────┬────────┘    │                     │
└───────────┼─────────────┘                     │
            │                                   │
            ▼                                   │
┌──────────────────────────┐                    │
│    VALUATIONS ODS        │                    │
│  (MTM, Sensitivities)    │                    │
└───────────┬──────────────┘                    │
            │                                   │
            │         ┌─────────────────────────┘
            │         │
            ▼         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     RISK ENGINE                                             │
│                                                                             │
│   Sensitivities + Positions + Time Series                                   │
│                         │                                                   │
│         ┌───────────────┼───────────────┐                                   │
│         ▼               ▼               ▼                                   │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                            │
│  │     VaR     │ │   Stress    │ │    FRTB     │                            │
│  │  (HistSim,  │ │ (Scenarios, │ │  (IMA, SA,  │                            │
│  │  SVaR, IRC) │ │   PoW)      │ │    DRC)     │                            │
│  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘                            │
│         │               │               │                                   │
│         └───────────────┼───────────────┘                                   │
│                         ▼                                                   │
└─────────────────────────┼───────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DATA LAKEHOUSE (Apache Iceberg)                   │
├─────────────────────────────────────────────────────────────────────────────┤
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│   │   Trade      │  │  Market Data │  │     Risk     │  │  Valuations  │    │
│   │     ODS      │  │     ODS      │  │     ODS      │  │     ODS      │    │
│   │ (Positions)  │  │   (Curves,   │  │(VaR, Stress, │  │    (MTM,     │    │
│   │              │  │   Prices,    │  │    IRC)      │  │    Greeks)   │    │
│   │              │  │ Time Series) │  │              │  │              │    │
│   └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           REPORTING LAYER                                   │
│   ┌──────────────────────────────┐   ┌──────────────┐                       │
│   │   Risk Reporting DataMart    │   │  Regulatory  │                       │
│   │   (Dashboards, Sign-off)     │   │  (COREP)     │                       │
│   └──────────────────────────────┘   └──────────────┘                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Key Data Flows:**
1. **Trade Flow**: Murex → Trade ODS (positions, trades)
2. **Valuation Flow**: Trade ODS + EOD Market Data → Valuation Engine → Valuations ODS (MTM, Sensitivities)
3. **Risk Flow**: Sensitivities + Positions + Time Series → Risk Engine → Risk ODS (VaR, SVaR, Stress, IRC)

### 12.2 Key Systems

| System | Node ID | Purpose | Data Flow |
|--------|---------|---------|-----------|
| **Murex** | SYS-MR-001 | Trade capture, pricing, position management | Source → Trade ODS |
| **Valuation Engine** | SYS-MR-002 | MTM calculation, Greeks, sensitivities | Trade ODS + EOD Market Data → Valuations ODS |
| **Risk Engine** | SYS-MR-003 | VaR, SVaR, IRC, stress testing, FRTB | Sensitivities + Time Series → Risk ODS |
| **Risk Reporting DataMart** | SYS-MR-004 | Risk reporting, sign-off workflow, breach management | Risk ODS → Reports |
| **Trade ODS** | SYS-MR-005 | Consolidated positions and trades | Murex → Lakehouse |
| **Market Data ODS** | SYS-MR-006 | Curves, prices, time series | Vendors → Lakehouse |
| **Valuations ODS** | SYS-MR-007 | MTM values, Greeks, sensitivities | Valuation Engine → Lakehouse |
| **Risk ODS** | SYS-MR-008 | VaR, stress results, IRC | Risk Engine → Lakehouse |

### 12.3 Data Quality (BCBS 239)

Per BCBS 239 principles, the Bank maintains robust data quality controls:

| Principle | Control | Monitoring |
|-----------|---------|------------|
| **Completeness** | All trades captured; reconciliation to Finance | Daily |
| **Accuracy** | Price validation; sensitivity reasonableness | Daily |
| **Timeliness** | T+1 deadlines; SLA tracking | Daily KPIs |
| **Consistency** | Single source of truth; reconciliation | Daily |
| **Adaptability** | Flexible reporting; ad-hoc capability | Quarterly review |

Data quality thresholds and KPIs are tracked monthly at MLRC.

### 12.4 Reporting Framework

| Report | Frequency | Content | Recipients |
|--------|-----------|---------|------------|
| Daily VaR Report | T+1 07:00 | VaR by desk, limit utilisation, exceptions | MLRC, Trading Heads |
| Daily P&L Flash | T+1 08:00 | P&L, VaR usage, backtesting | Trading, Finance |
| MLRC Pack | Weekly | VaR trends, stress results, exceptions, approvals | MLRC members |
| Backtesting Report | Weekly | P&L vs VaR, exception analysis | MLRC |
| RMC Market Risk Report | Monthly | Executive summary, appetite utilisation | RMC |
| Regulatory Capital | Monthly | IMA capital, add-ons | Finance, RMC |
| Model Performance | Monthly | VaR accuracy, model MI | RMAC |
| BRMC Report | Quarterly | Board-level summary, Level 1 status | BRMC |

---

## 13. Related Documents

### 13.1 Subsidiary Market Risk Policies

| Policy | Reference | Purpose |
|--------|-----------|---------|
| [VaR Policy](./var-policy.md) | MR-L3-004 | VaR/SVaR governance, time series, proxying, RNIV, backtesting |
| [Stress Testing Policy](./stress-testing-policy.md) | MR-L3-005 | Pillar stresses, PoW, scenario design, stress limits |
| [Trading Book Boundary Policy](./trading-book-boundary-policy.md) | MR-L3-006 | TB vs BB boundary, reclassification, trading intent |
| [VaR Limit Framework](./var-limit-framework.md) | MR-L3-003 | Detailed limit structure and values |

### 13.2 Other Linked Policies

| Policy | Relationship |
|--------|--------------|
| Credit Risk Policy | CVA, Issuer risk overlap; credit approval for trading book issuers |
| Non-Traded Market Risk Policy | Banking book interest rate risk (IRRBB, CSRBB) |
| Model Risk Policy | Model governance framework; SS1/23 compliance |
| Capital Policy | Capital allocation for market risk |
| Liquidity Risk Policy | Market liquidity stress; funding risk |
| Operational Risk Policy | RCSA; control framework; incident management |

### 13.3 Linked Procedures

| Procedure | Node ID | Purpose |
|-----------|---------|---------|
| Market Risk Process Orchestration | MR-L4-001 | Master orchestration for all Market Risk processes |
| Trade Capture Controls | MR-L4-002 | Trade completeness, validation, and reconciliation |
| EOD Market Data Snapshot | MR-L4-003 | Official EOD prices, curves, volatilities |
| Time Series Management | MR-L4-005 | Risk factor setup, price collection, cleaning, proxying |
| Risk Engine Calculation | MR-L4-006 | VaR/SVaR/Stress calculation engine |
| Market Risk Reporting & Sign-off | MR-L4-007 | All three streams: Sensitivities, VaR, Stress |
| Backtesting | MR-L4-008 | P&L vs VaR comparison and exception management |
| Stress Testing | MR-L4-011 | Scenario design, execution, and reporting |
| Market Risk Limits Management | MR-L4-013 | Full limit lifecycle: setup, monitoring, breach management |
| Aged Inventory Monitoring | MR-L4-014 | Quarterly inventory review, ICAAP illiquidity input |
| New Product Approval | NPSTA-L4-001 | Product onboarding and risk assessment (cross-functional) |

### 13.4 Linked Frameworks and Methodologies

| Document | Purpose |
|----------|---------|
| [VaR Limit Framework](./var-limit-framework.md) | Detailed limit structure and values |
| [MLRC Terms of Reference](../committees/mlrc-terms-of-reference.md) | Committee governance and authority |
| [VaR Methodology](../../L6-Models/market-risk/var-svar-methodology.md) | Technical VaR calculation methodology |
| Stress Testing Methodology | Scenario design and parameterisation |
| IRC Methodology | Default and migration risk calculation |
| Proxy Methodology | Risk factor proxy assignment |

---

## 14. Policy Review and Maintenance

### 14.1 Review Cycle

| Review Type | Frequency | Trigger | Approval |
|-------------|-----------|---------|----------|
| Annual Review | Yearly (Q4) | Scheduled | RMC (minor); BRMC (material) |
| Regulatory Update | As needed | New regulation | RMC |
| Material Change | As needed | Business change, new products | RMC |
| Post-Incident | As needed | Risk event, breach | CRO decision |

### 14.2 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-15 | Initial version | RMC |
| 1.1 | 2025-01-15 | Enhanced with reference content; dynamic SVaR methodology | RMC |
| 1.2 | 2025-01-16 | Aligned L4 process metadata with actual documentation; updated Section 13.2 Linked Procedures | RMC |
| 1.3 | 2025-01-16 | Added Section 8.6.1 (ECAP Regulatory Drivers) and Section 10.6.1 (Aged Inventory Regulatory Drivers); enhanced ECAP governance; cross-referenced L4 processes | RMC |
| 1.4 | 2025-01-16 | Added MR-L4-014 Aged Inventory Monitoring to L4 processes and linked procedures (standalone document) | RMC |
| 1.5 | 2025-01-17 | Added subsidiary policy structure (MR-L3-004 VaR Policy, MR-L3-005 Stress Testing Policy, MR-L3-006 Trading Book Boundary Policy); updated Section 1.4 and 13.1 | RMC |
| 1.6 | 2025-01-17 | Converted all amounts from GBP to USD for reporting consistency | RMC |

### 14.3 Document Control

| Control | Value |
|---------|-------|
| Classification | Internal |
| Retention | 7 years from supersession |
| Distribution | Risk, Trading, Finance, Compliance, Audit |
| Storage | Document Management System |

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| **VaR** | Value at Risk - estimated maximum loss at given confidence level over specified holding period |
| **SVaR** | Stressed VaR - VaR calculated using a stressed market period |
| **IRC** | Incremental Risk Charge - default and migration risk charge for credit trading book |
| **FRTB** | Fundamental Review of Trading Book - Basel Committee framework for trading book capital |
| **MLRC** | Market & Liquidity Risk Committee |
| **Greeks** | Sensitivity measures (Delta, Gamma, Vega, etc.) |
| **Backtesting** | Comparison of predicted VaR vs actual/hypothetical outcomes |
| **ECAP** | Economic Capital - internal measure of risk capital requirement |
| **EaR** | Earnings at Risk - potential earnings variability measure |
| **RNIV** | Risks Not in VaR - risks not fully captured by VaR model |
| **HWM** | High Water Mark - peak year-to-date P&L for stop-loss measurement |
| **PoW** | Point of Weakness - bottom-up stress testing of specific strategies |
| **IMA** | Internal Model Approach - regulatory approval to use internal models for capital |
| **NPSTA** | New Products and Significant Transactions Approval |

---

## Appendix B: Regulatory Reference Map

| Section | CRR Article | SS13/13 Chapter | SS1/23 Principle |
|---------|-------------|-----------------|------------------|
| Trading Book Boundary | Art 104 | Chapter 2 | - |
| VaR Requirements | Art 325bc-be | Chapter 3 | - |
| SVaR Requirements | Art 325bk | Chapter 4 | - |
| IRC Requirements | Art 325bl-bo | Chapter 5 | - |
| Backtesting | Art 325bf | Chapter 9 | - |
| Stress Testing | Art 325bh | Chapter 8 | - |
| Model Governance | - | Chapter 6 | Principles 1-9 |
| Model Validation | - | Chapter 7 | Principles 3-4 |

---

## Appendix C: Key Market Risk Control Summary

| Control | Entity Level | Business Level | Frequency | Governance |
|---------|--------------|----------------|-----------|------------|
| **Stop-Loss** | Level 1: $75m MTD | Level 2: By business | Daily | Level 1: BRMC (Q4); Level 2: MLRC |
| **Stress Testing** | Level 1: $190m | Business breakdown | Weekly | BRMC (Q4) |
| **Backtesting** | Level 1: <10 exceptions | Level 2: By business | Daily | Exception reporting to RMC/BRMC |
| **Limits** | Level 1: $25m VaR | Level 2/3: Cascaded | Daily | Level 1: BRMC; Level 2: MLRC |

---

*This policy is the property of Meridian Global Bank. Unauthorised distribution is prohibited.*

*End of Document*
