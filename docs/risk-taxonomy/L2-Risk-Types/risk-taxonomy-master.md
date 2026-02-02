# Risk Taxonomy - Master Document

**Reference Bank**: Meridian Global Bank
**Version**: 2.0
**Effective Date**: January 2025
**Review Date**: January 2026
**Approved By**: Risk Management Committee
**Classification**: Internal Use Only

---

## 1. Introduction

### 1.1 Purpose

This taxonomy classifies Meridian Global Bank's (the "Bank") universe of risks into risk types and, where appropriate, sub-types and sub-sub types. This ensures consistent terminology throughout the Bank and provides the foundation for:

- Risk identification, assessment, and measurement
- Capital allocation and regulatory reporting (ICAAP/ILAAP)
- Governance, policy framework, and committee structure alignment
- Risk appetite framework and limit setting
- Skills and automation mapping in the Risk Agents platform
- Regulatory communication and audit trail

### 1.2 Scope

All risk types applicable to the Bank's current business model are defined in this taxonomy. Each risk type links to:

- **L1 (Requirements)**: Regulatory and business drivers
- **L3 (Governance)**: Applicable policies and committees
- **L4 (Processes)**: Business processes and procedures
- **L5 (Controls)**: Key controls, limits, and metrics
- **L6 (Models)**: Risk models and methodologies
- **L7 (Data & Systems)**: Data sources and systems

### 1.3 Regulatory Foundation

This taxonomy aligns with:
- **PRA Rulebook** (ICAAP Section, Chapter 3) - Firms must consider each source of risk they are or might be exposed to
- **CRR/CRD** - Capital requirements for credit, market, and operational risk
- **BCBS Principles** - Basel Committee risk management standards
- **SS1/23** - Model Risk Management
- **SS5/25** - Climate-related financial risks

---

## 2. Risk Classification Overview

### 2.1 Risk Types Where Capital Held

| Risk Type | Risk Sub-type | Applicable | Material | EaR/RAS | ECap/RAS | Reverse Stress Test | Capital Held |
|-----------|---------------|:----------:|:--------:|:-------:|:--------:|:-------------------:|:------------:|
| **Business Risk** | | Y | Y | Y | Y | Y | Y |
| | Concentration Risk (Business) | Y | Y | Y | Y | Y | Y |
| **Credit Risk** | | Y | Y | Y | Y | Y | Y |
| | Counterparty Risk | Y | Y | Y | Y | Y | Y |
| | - Primary Credit Risk | Y | Y | Y | Y | Y | Y |
| | - Pre-Settlement Risk | Y | Y | Y | Y | Y | Y |
| | - Issuer Risk (Banking Book) | Y | Y | Y | Y | Y | Y |
| | - Settlement Risk | Y | Y | N | Y | N | Y |
| | - Contingent Counterparty Risk | Y | Y | Y | Y | Y | Y |
| | Credit Concentration Risk | Y | Y | Y | Y | Y | Y |
| | Country Risk | Y | Y | N | N | Y | N |
| | Equity Risk | Y | N | Y | Y | N | Y |
| **Market Risk** | | Y | Y | Y | Y | Y | Y |
| | Trading Book Market Risk | Y | Y | Y | Y | Y | Y |
| | Fair Value Banking Book | Y | Y | Y | Y | Y | Y |
| | Issuer Risk (Trading Book) | Y | Y | Y | Y | Y | Y |
| **Interest Rate Risk in Banking Book** | | Y | Y | Y | Y | N | Y |
| **Operational Risk** | | Y | Y | Y | Y | Y | Y |
| | Internal Fraud | Y | Y | Y | Y | Y | Y |
| | External Fraud | Y | Y | Y | Y | Y | Y |
| | Employment Practices | Y | Y | Y | Y | Y | Y |
| | Clients, Products & Practices | Y | Y | Y | Y | Y | Y |
| | Damage to Physical Assets | Y | Y | Y | Y | Y | Y |
| | Business Disruption | Y | Y | Y | Y | Y | Y |
| | Execution & Process Management | Y | Y | Y | Y | Y | Y |

### 2.2 Risk Types Where Capital Not Held

| Risk Type | Risk Sub-type | Applicable | Material | EaR/RAS | ECap/RAS | Reverse Stress Test | Capital Held |
|-----------|---------------|:----------:|:--------:|:-------:|:--------:|:-------------------:|:------------:|
| **Liquidity & Funding Risk** | | Y | Y | N | N | Y | N |
| **Group Risk** | | Y | Y | N | N | Y | N |
| **Leverage Risk** | | Y | N | N | N | Y | N |
| **Pension Obligation Risk** | | N | N | N | N | N | N |
| **Reputational Risk** | | Y | N | N | N | Y | N |
| **Model Risk** | | Y | Y | N | N | Y | N |
| **Sustainability Risk** | | Y | Y | N | N | Y | N |
| | Environmental Risk | Y | Y | N | N | Y | N |
| | - Climate Risk (Physical) | Y | Y | N | N | Y | N |
| | - Climate Risk (Transition) | Y | Y | N | N | Y | N |
| | Social Risk | Y | N | N | N | N | N |
| | Governance Risk | Y | N | N | N | N | N |

### 2.3 Rationale for Not Holding Capital Against Certain Risk Types

**Liquidity & Funding Risk**: Managed through the Liquidity Coverage Ratio (LCR), Net Stable Funding Ratio (NSFR), and internal stress measures. Also captured through reverse stress test scenarios. Higher funding costs eroding margins are considered as part of Business Risk.

**Group Risk**: From a capital perspective, the Bank relies on group support arrangements. From a revenue perspective, the business risk model captures impacts from adverse group relationship effects. A reverse stress test captures this risk.

**Leverage Risk**: While applicable, not currently material enough to hold separate capital. The underlying risk is captured by the existing framework for market risk, credit risk (notional and concentration), and operational risk. A reverse stress test captures leverage risk.

**Reputational Risk**: While applicable, not material enough for separate capital. Captured through operational risk scenarios and reverse stress testing.

**Model Risk**: Not held separately; captured in respective risk types (RNIVs under market risk, operational risk scenario modelling). Reverse stress testing includes model risk scenarios.

**Sustainability Risk**: As an emerging cross-cutting risk type, capital requirements form part of the primary risk types (e.g., climate-adjusted credit ratings, climate stress scenarios in market risk).

---

## 3. Risk Type Definitions

### 3.1 Business Risk

**Node ID**: `BR-L2-001`
**Parent**: `REQ-L1-001` (CRR/CRD - Own Funds Requirements)

#### Definition

Business Risk is the catch-all for residual earnings variability after considering the effects of market risk, credit risk, structural interest rate risk, and operational risk. Business risk is not directly attributable to internal operational failures or external market events, but covers risks such as:

- Price wars, margin reduction
- Failed client strategies (e.g., failure to capture new clients)
- Failed financing strategy (e.g., failure to deploy the balance sheet appropriately)
- Failed relationship with Group entities
- Unplanned spike in costs
- Unplanned spike in funding costs

#### Sub-Types

| Sub-Type | ID | Definition |
|----------|-----|------------|
| **Revenue Risk** | BR-L2-002 | Risk from unexpected decline in fee income or trading revenue |
| **Cost Risk** | BR-L2-003 | Risk from unexpected increase in operating costs |
| **Margin Risk** | BR-L2-004 | Risk from compression of net interest margin or trading spreads |
| **Business Concentration Risk** | BR-L2-005 | Risk from over-reliance on specific clients, products, or geographies |

#### Key Metrics

- Revenue concentration indices (HHI)
- Cost-income ratio and trends
- Net interest margin volatility
- Client concentration by revenue
- Product mix analysis

#### Capital Treatment

Capital held via Business Risk component in ICAAP for:
- Revenue volatility scenarios
- Client loss scenarios
- Market disruption scenarios

---

### 3.2 Credit Risk

**Node ID**: `CR-L2-001`
**Parent**: `REQ-L1-005` (CRR Part 3 - Credit Risk)

#### Definition

Credit Risk is the risk of loss arising from the failure of counterparties to meet their financial or contractual obligations when due. It comprises Counterparty Risk, Concentration Risk, Country Risk, Equity Risk, and Credit Insurance Risk.

#### 3.2.1 Counterparty Risk

**Node ID**: `CR-L2-002`

Counterparty Risk is the risk of loss to the Bank arising from a counterparty being unwilling or unable to meet its financial or contractual obligations. The core components are:

##### Primary Credit Risk (CR-L2-003)

The Exposure at Default (EAD) arising from lending and related banking product activities, including their underwriting.

##### Pre-Settlement Credit Risk (CR-L2-004)

The EAD arising from unsettled forward and derivative transactions, measured as the cost of replacing the transaction at current market rates if the counterparty defaults before settlement.

##### Issuer Risk - Banking Book (CR-L2-005)

The EAD arising from credit and equity products capable of being traded, including their underwriting. Issuer Risk arising from government securities is recognised and managed under the Credit Risk framework.

*Note: Issuer Risk booked in the Trading Book is managed under the Market Risk framework but is subject to allocation of country and credit limits from the Credit Risk processes.*

##### Settlement Risk (CR-L2-006)

The risk of loss from the failure of a transaction settlement where value is exchanged such that the counter value is not received in whole or part. Includes risk of loss on unsettled forward or delivery dates.

##### Contingent Counterparty Risk (CR-L2-007)

The risk that approved credit risk mitigation techniques prove less effective than expected from adverse correlation effects.

#### 3.2.2 Exit Risk

**Node ID**: `CR-L2-008`

Exit Risk is the risk of an unexpected shortfall relating to the release of commodity, inventory financing, or repo facilities, where the Bank calculates the cost to sell/liquidate a physical commodity (to which it has title and control) in the secondary market if the underlying counterparty fails to buy it back.

Exit risk costs include:
- **Logistic costs**: Warehouse/storage fees, freight costs
- **Price risk costs**: Having to roll prices, exposure to backwardation

##### Stressed Exit Risk (CR-L2-009)

Recognises low probability but plausible tail-event risks over and above the base Exit Risk model that could be faced in extreme market conditions. These may be based on:
- Protracted base Exit Risk scenarios
- Additional direct or indirect costs
- Scenario-based quantification for challenging jurisdictions

Stressed Exit Risk is calculated and included within monthly economic capital calculations where applicable.

#### 3.2.3 Gap Risk

**Node ID**: `CR-L2-010`

Gap Risk is the risk of a shortfall due to dislocation of collateral value from a sudden unexpected change in its price. This arises where the value of recourse to the counterparty is deemed low or zero because:
- There is no legal recourse
- The collateral represents all or a significant portion of the counterparty value (e.g., an SPV whose only assets are the collateral)
- There is significant correlation between recourse value and underlying collateral

*Note: Gap Risk is largely a "hybrid" between Market and Credit risk.*

#### 3.2.4 Wrong Way Risk (WWR)

**Node ID**: `CR-L2-011`

Wrong Way Risk arises from positive correlation between counterparty credit exposure and credit quality. WWR is present where the risk of default increases as the Bank's credit exposure increases or as collateral value decreases.

##### Specific Wrong Way Risk (CR-L2-012)

Occurs where there is a direct or very strong positive correlation between counterparty exposure and probability of default due to:
- Legal relationship
- Economic group relationship in absence of diversified portfolio
- Counterparty being a commodity producer (consumer) being net long (short) the commodity it produces (consumes)
- Other substantially similar factors

##### General Wrong Way Risk (CR-L2-013)

Occurs where positive correlation between counterparty exposure and probability of default is due to macro factors rather than a direct relationship.

*Treatment: GWWR is captured in pre-settlement risk measures for securities financing trades. For other products, GWWR is captured through Exposure Conditional on Default (ECoD) runs and WWR monitoring framework. SWWR is subject to deal-by-deal specific adjustments.*

#### 3.2.5 Credit Concentration Risk

**Node ID**: `CR-L2-014`

The risk of loss resulting from excessive concentration of exposure to:
- A single counterparty
- A country or geography
- An industry sector

Under Pillar 2A, concentration risk is based on the PRA's recommended Herfindahl-Hirschman Index (HHI) methodology for calculating single name, country, and geographical concentration risk.

#### 3.2.6 Credit Insurance Risk

**Node ID**: `CR-L2-015`

The risk of non-payment or partial non-payment by a provider of credit insurance due to:
- Incorrect insurance documentation
- Insurer failing to make payment under policy terms

*Note: This is distinct from the insurer's credit risk (inability to pay), which is captured under Counterparty Risk.*

#### 3.2.7 Country Risk (Cross-Border)

**Node ID**: `CR-L2-016`

The uncertainty that obligors (including the relevant sovereign, branches, and subsidiaries) may not be able to fulfil obligations outside the host country because of political or economic conditions. This includes:
- Group equity investments in host country
- Physical inventories owned by the Bank
- Obligations that may be impaired inside the host country

#### 3.2.8 Equity Risk (Banking Book)

**Node ID**: `CR-L2-017`

The risk of loss from decline in value of equity instruments held, caused by:
- Deterioration in issuer performance, net asset, or enterprise value
- Decline in market price

Sub-categories:
- **Subsidiary Equity Risk**: Risk in equity held in subsidiaries (controlling interest for strategic reasons)
- **Associate Equity Risk**: Risk in equity held in associate companies or joint ventures
- **Banking Book Equity Risk**: Any equity investment not in above categories (captured via Credit Issuer Risk framework)

#### Key Metrics

| Metric | Description |
|--------|-------------|
| Probability of Default (PD) | Likelihood of counterparty default over 1 year |
| Loss Given Default (LGD) | Percentage of exposure lost if default occurs |
| Exposure at Default (EAD) | Total exposure at time of default |
| Expected Loss (EL) | PD × LGD × EAD |
| Unexpected Loss (UL) | Capital held against credit loss volatility |
| Credit VaR | Value at Risk for credit portfolio |
| Potential Future Exposure (PFE) | Maximum expected exposure at given confidence level |
| Expected Positive Exposure (EPE) | Average expected exposure over time |
| Credit Valuation Adjustment (CVA) | Fair value adjustment for counterparty credit risk |
| Large Exposures (LE) | Exposures >10% of capital |
| Concentration Index (HHI) | Measure of portfolio concentration |

#### Applicable Skills

- `climate-scorecard-filler` - ESG/Climate credit assessment (SS5/25 aligned)
- `process-documenter` - Credit approval workflow documentation

---

### 3.3 Market Risk

**Node ID**: `MR-L2-001`
**Parent**: `REQ-L1-003` (FRTB), `REQ-L1-004` (SS13/13)

#### Definition

Market Risk is the risk associated with the change in market value, earnings, or future cash flows of financial instruments. Market risk can be systemic or idiosyncratic and exists in all asset classes.

#### Market Risk Sensitivities

Standalone measures include:
- **Delta**: Notional, interest rate, credit and recovery spread sensitivities
- **Vega**: Volatility sensitivity
- **Theta**: Time decay
- **Gamma**: Second-order price sensitivity
- **Higher order terms**: Product, curve, and maturity mismatches

#### Sub-Types

| Sub-Type | ID | Definition |
|----------|-----|------------|
| **Interest Rate Risk (Trading)** | MR-L2-002 | Risk from changes in interest rates affecting trading book instruments |
| **Foreign Exchange Risk** | MR-L2-003 | Risk from changes in currency exchange rates |
| **Equity Risk** | MR-L2-004 | Risk from changes in equity prices and indices |
| **Commodity Risk** | MR-L2-005 | Risk from changes in commodity prices (precious metals, base metals, energy) |
| **Credit Spread Risk (Trading)** | MR-L2-006 | Risk from changes in credit spreads for traded instruments |
| **Volatility Risk** | MR-L2-007 | Risk from changes in implied volatilities |

#### Special Risk Categories

##### Illiquidity Risk (MR-L2-008)

The degree to which any asset class, market risk factor, or product underlier cannot be traded at conventional prices. This affects the ability to exit or hedge positions without significant market impact.

##### Concentration Risk (Market) (MR-L2-009)

Occurs when a relative percentage holding of a particular underlier versus its total traded volume creates a tipping point on:
- Stressed bid-offer spreads
- Increased price volatility
- Potential price gap risk

##### One-Way Risk (MR-L2-010)

Occurs where a majority of market participants are positioned the same way on a risk factor or underlier. Accumulation of these trades can give rise to concentration risk and illiquidity risk, especially when market participants are required to exit positions simultaneously.

##### Foreign Currency Risk (MR-L2-011)

The financial risk that exists when a transaction is denominated in a currency other than the Bank's base currency. Includes risk from investment value changes due to exchange rate movements.

##### Issuer Risk (Trading Book) (MR-L2-012)

Issuer risk for credit and equity instruments in the trading book, managed under Market Risk framework. Subject to country and credit limits from Credit Risk processes.

#### Key Metrics

| Metric | Description |
|--------|-------------|
| Value at Risk (VaR) | 1-day 99% confidence loss estimate |
| Stressed VaR (SVaR) | 1-day 99% VaR under stressed market conditions |
| Expected Shortfall (ES) | 1-day 97.5% average loss beyond VaR (FRTB) |
| Incremental Risk Charge (IRC) | Default and migration risk for credit products |
| Stress P&L | P&L under defined stress scenarios |
| Greeks | Delta, Gamma, Vega, Theta sensitivities |
| DV01/PV01 | Interest rate sensitivity per basis point |
| CS01 | Credit spread sensitivity per basis point |
| Position limits | Notional, VaR, Greeks limits by desk/book |

#### Applicable Skills

- `pillar-stress-generator` - Stress scenario parameterization
- `stress-scenario-suggester` - Emerging market risk identification
- `process-documenter` - VaR production process documentation

---

### 3.4 Interest Rate Risk in the Banking Book (IRRBB)

**Node ID**: `IRRBB-L2-001`
**Parent**: `REQ-L1-001` (CRR/CRD)

#### Definition

IRRBB is the current or prospective risk to the Bank's economic value and earnings arising from adverse movements in interest rates that affect interest rate sensitive instruments in the Banking Book.

#### Sub-Types

##### Re-pricing Risk (IRRBB-L2-002)

Risk arising from timing mismatches in the maturity and repricing of assets and liabilities (on and off-balance sheet). Positions typically have different repricing dates or floating interest rates.

##### Yield Curve Risk (IRRBB-L2-003)

Risk arising when unanticipated shifts in the yield curve have adverse effects on the Bank's income or underlying economic value.

*Note: Re-pricing Risk and Yield Curve Risk are commonly captured under the term "Gap Risk".*

##### Basis Risk (IRRBB-L2-004)

Risk arising from the impact of relative changes in interest rates on instruments that have similar maturities but are priced off different interest rate indices.

##### Optionality Risk (IRRBB-L2-005)

Risk arising from options where the institution or its customer can alter the level and timing of cash flows:

- **Embedded/Explicit Options**: Where the holder will almost certainly exercise if financially beneficial
- **Behavioural Options**: Flexibility embedded within instrument terms (e.g., mortgage early repayment) where customer behaviour depends on interest rate levels

##### Credit Spread Risk in the Banking Book (CSRBB) (IRRBB-L2-006)

Risk driven by changes in market perception about the price of credit, liquidity premium, and other components, introducing price fluctuations not explained by IRRBB or expected credit/jump-to-default risk. Applies to MTM and AFS bond portfolios in the Banking Book.

#### Key Metrics

| Metric | Description |
|--------|-------------|
| Economic Value of Equity (EVE) | Change in present value of all cash flows |
| Net Interest Income (NII) | Change in 12-month projected NII |
| Earnings at Risk (EaR) | Potential impact on earnings |
| Interest Rate Gap | Repricing mismatches by time bucket |
| Duration | Weighted average maturity |
| Key Rate Durations | Sensitivity to specific tenor points |

#### Capital Treatment

Capital held under Pillar 2A based on:
- Standard EVE shocks (±200bp parallel, steepening, flattening)
- Internal stress scenarios
- Outlier test thresholds

---

### 3.5 Operational Risk

**Node ID**: `OR-L2-001`
**Parent**: `REQ-L1-008` (SMA), `REQ-L1-009` (SS1/21)

#### Definition

Operational Risk is the risk of loss resulting from inadequacy of, or failure in, internal processes, people, and systems, or from external events. It incorporates legal risk, losses arising from insurance risk, and losses related to physical commodities.

#### Basel Event Categories

##### Internal Fraud (OR-L2-002)

Losses due to acts intended to defraud, misappropriate property, or circumvent regulations, law, or company policy, involving at least one internal party. Includes certain financial crime risks.

##### External Fraud (OR-L2-003)

Losses due to acts intended to defraud, misappropriate property, or circumvent the law by a third party. Includes:
- Theft from transport/warehouse
- Collusion in form of theft or misappropriation
- Custodian risk
- Cyber-crimes (ransomware, authorised push payments)

##### Employment Practices & Workplace Safety (OR-L2-004)

Losses arising from acts inconsistent with employment, health, or safety laws, agreements, or regulations.

##### Clients, Products & Business Practices (OR-L2-005)

Losses arising from unintentional or negligent failure to meet professional obligations to clients (including fiduciary and suitability requirements), or from the nature or design of a product.

##### Damage to Physical Assets (OR-L2-006)

Losses from loss or damage to physical assets from natural disaster or other events.

##### Business Disruption & Systems Failure (OR-L2-007)

Losses from disruption of business or system failures. Includes disruption from:
- Utility breakdowns
- Software failures, data loss
- Hardware, electronic devices, networks, telecommunications
- Organisational structure changes

##### Execution, Delivery & Process Management (OR-L2-008)

Losses from failed transaction processing or process management, or disputes with trade counterparties and vendors.

#### Embedded Risk Types

| Risk Type | Node ID | Definition | Primary Event Category |
|-----------|---------|------------|----------------------|
| **Legal Risk** | OR-L2-009 | Risk that business is conducted outside applicable laws; contracts not enforceable; property rights infringed; liability incurred | Clients, Products & Practices |
| **Compliance Risk** | OR-L2-010 | Risk of sanctions, financial loss, or reputational damage from failure to comply with laws, regulations, codes of conduct | Clients, Products & Practices |
| **Conduct Risk** | OR-L2-011 | Risk that business practices lead to poor outcomes for clients or markets | Clients, Products & Practices |
| **Financial Crime Risk** | OR-L2-012 | Risk from money laundering, terrorist financing, bribery, corruption, tax evasion, fraud, sanctions violations | Internal/External Fraud |
| **Information Risk** | OR-L2-013 | Risk of unauthorized use, modification, disclosure, or destruction of information compromising confidentiality, integrity, or availability | Multiple categories |
| **Information Technology Risk** | OR-L2-014 | Risk from IT events impacting service availability, performance, or function | Business Disruption |
| **Insurance Risk** | OR-L2-015 | Risk of claim repudiation or delay in settlement due to faulty proof of claim or failure to meet policy requirements | Execution & Process |
| **Change Risk** | OR-L2-016 | Risk from changes to processes due to changes in people, process, or technology affecting operations | Execution & Process |
| **Environmental Risk (Op)** | OR-L2-017 | Risk of financial loss from environmental damage resulting from Bank's activities | Damage to Physical Assets |

#### Key Metrics

| Metric | Description |
|--------|-------------|
| Operational Risk Capital | SMA basis calculation |
| Key Risk Indicators (KRIs) | Leading indicators by risk category |
| Loss Events | Frequency, severity, recovery |
| Near Misses | Events without financial loss |
| Control Effectiveness | Testing results, control ratings |
| Audit Findings | Open/closed, aging |
| RCSA Ratings | Risk and Control Self-Assessment scores |
| Important Business Services | Tolerance metrics (Operational Resilience) |

#### Applicable Skills

- `itc-template-filler` - IT governance documentation
- `icc-business-case-filler` - Change governance documentation
- `meeting-minutes` - Committee meeting documentation
- `process-documenter` - RCSA and process documentation

---

### 3.6 Liquidity and Funding Risk

**Node ID**: `LR-L2-001`
**Parent**: `REQ-L1-011` (LCR), `REQ-L1-012` (NSFR)

#### Definition

**Liquidity Risk** means the risk that the Bank, although solvent, does not have sufficient financial resources to meet its obligations as they fall due.

**Funding Risk** means the Bank does not have stable sources of funding in the medium and long term to meet financial obligations as they fall due, either at all or only at excessive cost. Includes increases to funding costs in times of stress.

#### Sub-Types

| Sub-Type | ID | Definition |
|----------|-----|------------|
| **Short-term Liquidity Risk** | LR-L2-002 | Risk of inability to meet obligations within 30 days |
| **Funding Liquidity Risk** | LR-L2-003 | Risk of inability to raise funds at reasonable cost |
| **Market Liquidity Risk** | LR-L2-004 | Risk of inability to liquidate assets without significant loss |
| **Intraday Liquidity Risk** | LR-L2-005 | Risk of inability to meet intraday payment obligations |

#### Key Metrics

| Metric | Regulatory/Internal | Minimum |
|--------|---------------------|---------|
| Liquidity Coverage Ratio (LCR) | Regulatory | 100% |
| Net Stable Funding Ratio (NSFR) | Regulatory | 100% |
| Survival Horizon | Internal | 90 days |
| HQLA Buffer | Internal | As per risk appetite |
| Funding Concentration | Internal | Limits by counterparty/type |
| Intraday Liquidity | Regulatory | Self-sufficiency |

#### Capital Treatment

No direct capital held. Managed through:
- Regulatory ratios (LCR, NSFR)
- Internal stress testing and survival period metrics
- Contingency Funding Plan (CFP)
- Recovery and Resolution Planning

---

### 3.7 Model Risk

**Node ID**: `MDR-L2-001`
**Parent**: `REQ-L1-013` (SS1/23), `REQ-L1-014` (SR 11-7)

#### Definition

Model Risk relates to the potential costs (financial or reputational) of relying on models that are incorrect, imperfect, or misused.

#### Three Pillars of Model Risk

| Pillar | Description |
|--------|-------------|
| **Correctness** | Are the mathematics and implementation of the model correct? |
| **Applicability** | Is the model, including assumptions and approximations, fit for purpose given its limitations and business environment? |
| **Data Risk** | Impact of subjectivity and uncertainty around employed data, e.g., for calibration |

#### Scope of Models

The definition covers models in the traditional sense (relying on assumptions, statistics, quantitative and qualitative methods) as well as calculators based on decision rules or algorithms that:
- Are complex in nature
- Have bearing on business decisions related to:
  - General business model and strategy
  - Client advisory and trading activities
  - Financial, risk, capital, and liquidity measurement
  - Regulatory reporting
  - Any decision relevant to safety and soundness

#### Model Categories

| Category | ID | Examples |
|----------|-----|----------|
| **Valuation Models** | MDR-L2-002 | Pricing models, fair value models |
| **Risk Models** | MDR-L2-003 | VaR, SVaR, ES, PFE, stress testing |
| **Rating Models** | MDR-L2-004 | PD, LGD, EAD, scorecards |
| **Capital Models** | MDR-L2-005 | RWA, economic capital, ICAAP |
| **Financial Models** | MDR-L2-006 | P&L attribution, forecasting, budgeting |
| **Liquidity Models** | MDR-L2-007 | LCR, NSFR, stress testing |
| **AI/ML Models** | MDR-L2-008 | Machine learning, NLP (emerging, enhanced governance) |

#### Key Metrics

- Model inventory completeness
- Validation coverage and frequency
- Findings open/closed/aging
- Model tiering distribution
- Back-testing performance (pass/fail)
- Model Risk Capital add-ons (RNIV)

#### Capital Treatment

No separate capital held. Captured through:
- **Risk Not in VaR (RNIV)** for market risk models
- **PRA Model Risk add-ons** in Pillar 2A
- **Operational Risk scenarios** for model failures

---

### 3.8 Sustainability Risk (ESG)

**Node ID**: `SR-L2-001`
**Parent**: `REQ-L1-015` (SS5/25), `REQ-L1-016` (TCFD), `REQ-L1-023` (FCA SDR)

#### Definition

Sustainability Risk means an Environmental, Social, or Governance (ESG) event or condition that, if it occurs, could cause actual or potential material negative impact on the Bank's capital, reputation, earnings, and liquidity.

While each ESG risk has its own definition, there is often overlap, particularly between environmental and social risks. Governance plays a fundamental role in ensuring inclusion of environmental and social considerations.

#### 3.8.1 Environmental Risk

**Node ID**: `SR-L2-002`

Environmental risk consists of both environment-related risks and climate-related risks.

##### Environment-Related Risks (SR-L2-003)

Risks posed by exposure to activities that may cause or be affected by environmental degradation:
- Air or water pollution
- Water scarcity
- Reduced biodiversity
- Land contamination and land use change
- Deforestation and desertification

##### Climate-Related Risks (SR-L2-004)

Risks posed by exposure to physical and transition risks caused by or related to climate change.

###### Physical Risks

| Type | ID | Description | Examples |
|------|-----|-------------|----------|
| **Acute** | SR-L2-005 | Risks from climate and weather-related events | Hurricanes, floods, wildfires, droughts |
| **Chronic** | SR-L2-006 | Risks from longer-term climate shifts | Rising temperatures, sea level rise, ocean acidification |

###### Transition Risks

| Transmission Channel | ID | Description |
|---------------------|-----|-------------|
| **Policy & Regulation** | SR-L2-007 | Carbon taxes, emissions regulations, disclosure requirements |
| **Technology** | SR-L2-008 | Stranded assets from clean technology disruption |
| **Market & Sentiment** | SR-L2-009 | Shifting consumer preferences, investor sentiment |
| **Legal & Litigation** | SR-L2-010 | Climate litigation, greenwashing claims, duty of care |

##### Climate Risk Transmission to Principal Risks

| Principal Risk | Climate Transmission Example |
|----------------|------------------------------|
| Credit Risk | Rising carbon taxes reducing demand for counterparty's product; physical damage to assets; stranded asset impairment |
| Market Risk | Sudden decline in asset values from policy change; climate-driven commodity price volatility |
| Operational Risk | Extreme weather disrupting operations; greenwashing allegations |
| Liquidity Risk | Climate-related market stress reducing asset liquidity |

#### 3.8.2 Social Risk

**Node ID**: `SR-L2-011`

Risks posed by exposure to current or prospective negative impacts of social factors on counterparties or assets. Negative social impacts can affect various stakeholder groups through direct operations and value chains.

Criteria include:
- Society and community relations
- Employee relationships and labour standards
- Customer treatment
- Human rights
- Poverty and inequality

#### 3.8.3 Governance Risk

**Node ID**: `SR-L2-012`

Risks posed by exposure to governance practices of counterparties. Relates to:

**Corporate Governance**: How a company governs itself through policies, processes, and controls to demonstrate compliance and transparency.

**Business Integrity**: How a company seeks to avoid corruption, bribery, and engagement with politically exposed persons who may pose reputational risk.

#### Key Metrics (per SS5/25)

| Metric Category | Examples |
|-----------------|----------|
| **Portfolio Metrics** | Carbon intensity, financed emissions (Scope 1, 2, 3), green asset ratio |
| **Physical Risk** | Exposure by geography, acute/chronic risk scores |
| **Transition Risk** | Exposure by sector carbon intensity, stranded asset risk |
| **Scenario Analysis** | Climate VaR, scenario P&L impacts |
| **Counterparty** | Climate scorecard ratings, transition preparedness |

#### Capital Treatment

Currently embedded in primary risk types:
- **Credit Risk**: Climate-adjusted PD/LGD, credit rating overlays
- **Market Risk**: Climate stress scenarios (SS5/25 requirement)
- **Operational Risk**: Climate-related operational scenarios

*Note: Explicit climate capital requirements are emerging under CRR III and Pillar 2 guidance.*

#### Applicable Skills

- `climate-scorecard-filler` - Counterparty climate assessment (SS5/25 aligned)
- `stress-scenario-suggester` - Climate scenario identification
- `pillar-stress-generator` - Climate stress parameterization

---

### 3.9 Group Risk

**Node ID**: `GR-L2-001`
**Parent**: `REQ-L1-001` (CRR/CRD)

#### Definition

Group Risk is the risk that the Bank's financial position may be adversely affected by its relationships (financial or non-financial) with other entities in the same Group, or by risks that may affect the financial position of the whole group, including reputational contagion.

#### Sub-Types

| Sub-Type | ID | Definition |
|----------|-----|------------|
| **Intra-Group Credit Risk** | GR-L2-002 | Exposures to other group entities |
| **Contagion Risk** | GR-L2-003 | Risk from group-wide events or reputational damage |
| **Capital Support Risk** | GR-L2-004 | Risk that group support may not be available when needed |
| **Operational Dependency** | GR-L2-005 | Risk from shared services or operational dependencies |

#### Capital Treatment

- Managed through group support arrangements
- Business risk model captures impacts from adverse group relationships
- Reverse stress test captures group risk scenarios

---

### 3.10 Leverage Risk

**Node ID**: `LEV-L2-001`
**Parent**: `REQ-L1-001` (CRR/CRD - Leverage Ratio)

#### Definition

Leverage Risk is the risk that the Bank's assets and exposures are too high relative to its capital resources (measured as Tier 1 Capital).

#### Key Metrics

| Metric | Regulatory Minimum |
|--------|-------------------|
| Leverage Ratio | 3.25% (UK requirement) |
| Countercyclical Leverage Buffer | Variable |

#### Capital Treatment

- Managed through leverage ratio requirement
- Not separately capitalised in ICAAP
- Reverse stress test captures leverage scenarios

---

### 3.11 Reputational Risk

**Node ID**: `REP-L2-001`
**Parent**: `REQ-L1-001` (CRR/CRD)

#### Definition

Reputational Risk is the potential or actual damage to the Bank's public image which may impair the profitability and/or sustainability of its business. Such damage could result from breakdown of trust, confidence, or business relationships with:
- Customers
- Counterparties
- Investors
- Regulators

This can adversely affect the ability to maintain existing or generate new business relationships and continued access to funding sources.

#### Capital Treatment

- Not separately capitalised
- Captured through operational risk scenarios
- Reverse stress test includes reputational scenarios

---

### 3.12 Regulatory Risk

**Node ID**: `RR-L2-001`
**Parent**: `REQ-L1-001` to `REQ-L1-023` (All applicable regulations)

#### Definition

Regulatory Risk is the risk of sanctions, fines, enforcement actions, or reputational damage arising from failure to comply with applicable laws, regulations, and supervisory expectations.

#### Sub-Types

| Sub-Type | ID | Definition |
|----------|-----|------------|
| **Compliance Risk** | RR-L2-002 | Risk from regulatory non-compliance |
| **Regulatory Change Risk** | RR-L2-003 | Risk from failure to adapt to new regulations |
| **Capital Adequacy Risk** | RR-L2-004 | Risk of insufficient capital to meet requirements |
| **Reporting Risk** | RR-L2-005 | Risk from inaccurate or late regulatory reporting |

#### Key Metrics

- Regulatory findings (open/closed/aging)
- Capital ratios vs requirements and buffers
- Regulatory submission timeliness
- Regulatory change pipeline status

#### Capital Treatment

Captured via Operational Risk capital through:
- Compliance failure scenarios
- Regulatory fine scenarios

#### Applicable Skills

- `regulatory-risk-researcher` - Regulatory monitoring
- `regulatory-change-assessor` - Impact assessment
- `status-reporter` - Regulatory change project tracking
- `project-planner` - Regulatory implementation planning

---

### 3.13 Strategic Risk

**Node ID**: `STR-L2-001`
**Parent**: `REQ-L1-001` (ICAAP, Business Planning)

#### Definition

Strategic Risk is the risk of current or prospective impact on earnings or capital arising from adverse business decisions, improper implementation of decisions, or lack of responsiveness to industry changes.

#### Sub-Types

| Sub-Type | ID | Definition |
|----------|-----|------------|
| **Business Model Risk** | STR-L2-002 | Risk from unviable or outdated business model |
| **Competitive Risk** | STR-L2-003 | Risk from competitive actions eroding market position |
| **Innovation Risk** | STR-L2-004 | Risk from failure to adapt to technological change |
| **Concentration Risk (Strategic)** | STR-L2-005 | Business concentration in clients, products, geography |

#### Key Metrics

- Revenue concentration indices
- Market share trends
- Client retention rates
- NPS scores
- Strategic initiative success rates

#### Capital Treatment

Captured via Business Risk capital in ICAAP for:
- Revenue volatility scenarios
- Client loss scenarios
- Market disruption scenarios

#### Applicable Skills

- `stakeholder-analysis` - Strategic initiative stakeholder mapping
- `stress-scenario-suggester` - Strategic risk identification

---

### 3.14 Change Risk

**Node ID**: `CM-L2-001`
**Parent**: `REQ-L1-009` (SS1/21 - Operational Resilience)

#### Definition

Change Risk is the risk that emerges through changes, updates, or alterations made to operational processes due to changes in people, process, or technology. Change Risk can individually or collectively affect business and technology operations and service delivery.

#### Sub-Types

| Sub-Type | ID | Definition |
|----------|-----|------------|
| **Project Execution Risk** | CM-L2-002 | Risk of project failure to deliver outcomes |
| **Implementation Risk** | CM-L2-003 | Risk from poorly implemented changes |
| **Transition Risk** | CM-L2-004 | Risk during transition from old to new state |
| **Integration Risk** | CM-L2-005 | Risk from integration failures |

#### Key Metrics

| Metric | Description |
|--------|-------------|
| Project RAG Distribution | Red/Amber/Green status of portfolio |
| Budget Variance | Planned vs actual spend |
| Timeline Variance | Planned vs actual delivery |
| Defect Rate | Post-implementation defects |
| Rollback Frequency | Failed changes requiring rollback |
| Change-Related Incidents | Incidents attributed to changes |

#### Capital Treatment

Captured via Operational Risk through:
- Failed implementation scenarios
- System outage scenarios from change

#### Applicable Skills

- `project-planner` - Project planning and structuring
- `status-reporter` - Project status tracking
- `itc-template-filler` - IT governance documentation
- `icc-business-case-filler` - Business case development
- `meeting-minutes` - Project meeting documentation
- `stakeholder-analysis` - Change stakeholder mapping
- `process-documenter` - Change process documentation

---

## 4. Risk Interconnections

### 4.1 Risk Overlap Matrix

```
              Market  Credit  OpRisk  Liquid  Model   ESG    Reg    Strat  Change  IRRBB
Market          -      CVA     Sys     Mkt     VaR     Clim   RegCap  Bus    Proj     -
Credit        CVA       -      Fraud   Fund    Rating  Clim   RegCap  Conc   Proj     -
OpRisk        Sys     Fraud     -      Ops     Model   Gov    Compl   Rep    Impl     -
Liquid       Mkt      Fund     Ops       -     LCR     Trans  LCR     Fund   Proj     -
Model         VaR    Rating   Model    LCR      -      ESG    Cap    Model  Test     IR
ESG          Clim    Clim      Gov    Trans    ESG      -     Disc    Rep    Impl     -
Reg          RegCap  RegCap   Compl   LCR    Capital  Disc      -     Fine   Proj     -
Strat         Bus     Conc    Rep     Fund   Model    Rep     Fine      -    Proj     -
Change        Proj    Proj    Impl    Proj    Test    Impl    Proj    Proj     -      -
IRRBB          -       -       -       -       IR      -       -       -       -      -
```

### 4.2 Key Risk Intersections

| Intersection | Risks Involved | How They Interact |
|--------------|----------------|-------------------|
| **CVA/DVA** | Market + Credit | Credit spread movements create P&L on derivative portfolios |
| **Wrong Way Risk** | Market + Credit | Exposure increases as counterparty credit deteriorates |
| **Climate** | All | Cross-cutting risk affecting all primary risk types |
| **Model** | Market + Credit | Model failures manifest in primary risk calculations |
| **Regulatory Change** | All | New regulations affect governance across all risk types |
| **Operational Resilience** | Op + Liquidity | System failures impact payment processing |
| **Gap Risk** | Market + Credit | Hybrid risk from collateral value dislocation |

---

## 5. Skills Coverage Analysis

### 5.1 Current Skills by Risk Domain

| Risk Domain | Skills Available | Coverage Assessment |
|-------------|-----------------|---------------------|
| Market Risk | 2 (pillar-stress, stress-suggester) | Partial - stress scenarios |
| Credit Risk | 1 (climate-scorecard) | Low - ESG only |
| Operational Risk | 2 (itc, icc templates) | Partial - change governance |
| Liquidity Risk | 0 | None |
| Model Risk | 0 | None |
| Sustainability Risk | 1 (climate-scorecard) | Partial - credit only |
| Regulatory Risk | 2 (researcher, assessor) | Good - monitoring and assessment |
| Strategic Risk | 0 | None |
| Change Management | 7 (all change skills) | Strong |
| Cross-Cutting | 2 (meeting-minutes, process-documenter) | Partial |

### 5.2 Priority Skill Gaps

| Priority | Domain | Skill Need | Rationale |
|----------|--------|------------|-----------|
| 1 | Credit Risk | Credit memo generator | Core credit workflow |
| 2 | Market Risk | VaR analyzer | Daily production support |
| 3 | Liquidity Risk | LCR calculator | Regulatory requirement |
| 4 | Model Risk | Validation assistant | SS1/23 compliance |
| 5 | IRRBB | EVE/NII calculator | Banking book risk |

---

## 6. Document Control

### 6.1 Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-01-01 | Risk Taxonomy Team | Initial release |
| 2.0 | 2025-12-11 | Risk Taxonomy Team | Major expansion: added IRRBB, WWR, Exit Risk, Gap Risk detail; expanded Sustainability Risk per SS5/25; added Group Risk, Leverage Risk; enhanced all definitions |

### 6.2 Approval

| Role | Name | Date |
|------|------|------|
| CRO | [Pending] | |
| Head of Enterprise Risk | [Pending] | |
| Document Owner | Risk Taxonomy Team | 2025-12-11 |

---

## Appendix A: Taxonomy Node Index

| Node ID | Name | Layer | Domain |
|---------|------|-------|--------|
| BR-L2-001 | Business Risk | L2 | Business Risk |
| CR-L2-001 | Credit Risk | L2 | Credit Risk |
| CR-L2-002 | Counterparty Risk | L2 | Credit Risk |
| CR-L2-008 | Exit Risk | L2 | Credit Risk |
| CR-L2-010 | Gap Risk | L2 | Credit Risk |
| CR-L2-011 | Wrong Way Risk | L2 | Credit Risk |
| CR-L2-014 | Credit Concentration Risk | L2 | Credit Risk |
| CR-L2-016 | Country Risk | L2 | Credit Risk |
| MR-L2-001 | Market Risk | L2 | Market Risk |
| MR-L2-008 | Illiquidity Risk | L2 | Market Risk |
| MR-L2-009 | Concentration Risk (Market) | L2 | Market Risk |
| MR-L2-010 | One-Way Risk | L2 | Market Risk |
| IRRBB-L2-001 | Interest Rate Risk Banking Book | L2 | IRRBB |
| IRRBB-L2-006 | CSRBB | L2 | IRRBB |
| OR-L2-001 | Operational Risk | L2 | Operational Risk |
| OR-L2-009 | Legal Risk | L2 | Operational Risk |
| OR-L2-010 | Compliance Risk | L2 | Operational Risk |
| OR-L2-012 | Financial Crime Risk | L2 | Operational Risk |
| OR-L2-016 | Change Risk | L2 | Operational Risk |
| LR-L2-001 | Liquidity Risk | L2 | Liquidity Risk |
| MDR-L2-001 | Model Risk | L2 | Model Risk |
| SR-L2-001 | Sustainability Risk | L2 | Sustainability Risk |
| SR-L2-004 | Climate Risk | L2 | Sustainability Risk |
| GR-L2-001 | Group Risk | L2 | Group Risk |
| LEV-L2-001 | Leverage Risk | L2 | Leverage Risk |
| REP-L2-001 | Reputational Risk | L2 | Reputational Risk |
| RR-L2-001 | Regulatory Risk | L2 | Regulatory Risk |
| STR-L2-001 | Strategic Risk | L2 | Strategic Risk |
| CM-L2-001 | Change Risk | L2 | Change Management |

---

## Appendix B: Glossary

| Term | Definition |
|------|------------|
| **CVA** | Credit Valuation Adjustment - Fair value adjustment for counterparty credit risk |
| **DVA** | Debit Valuation Adjustment - Own credit adjustment |
| **EAD** | Exposure at Default |
| **EaR** | Earnings at Risk |
| **ECap** | Economic Capital |
| **EPE** | Expected Positive Exposure |
| **ES** | Expected Shortfall |
| **EVE** | Economic Value of Equity |
| **HHI** | Herfindahl-Hirschman Index - Concentration measure |
| **HQLA** | High Quality Liquid Assets |
| **ICAAP** | Internal Capital Adequacy Assessment Process |
| **ILAAP** | Internal Liquidity Adequacy Assessment Process |
| **LCR** | Liquidity Coverage Ratio |
| **LGD** | Loss Given Default |
| **NII** | Net Interest Income |
| **NSFR** | Net Stable Funding Ratio |
| **PD** | Probability of Default |
| **PFE** | Potential Future Exposure |
| **RAS** | Risk Appetite Statement |
| **RCSA** | Risk and Control Self-Assessment |
| **RNIV** | Risk Not in VaR |
| **RWA** | Risk-Weighted Assets |
| **SMA** | Standardised Measurement Approach (Operational Risk) |
| **SVaR** | Stressed Value at Risk |
| **VaR** | Value at Risk |
| **WWR** | Wrong Way Risk |

---

*This document is the property of Meridian Global Bank and is intended for internal use only.*
