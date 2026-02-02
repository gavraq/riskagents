---
# Document Metadata
document_id: IRV-BRD-001
document_name: IR Vega Sensitivities - Business Requirements Document
version: 1.0
effective_date: 2025-01-13
next_review_date: 2026-01-13
owner: Market Risk Technology
approving_committee: Risk Technology Change Board

# Taxonomy Reference
parent_node: L7-Systems/market-risk/feeds/ir-vega
feed_family: IR Vega
document_type: BRD
---

# IR Vega Sensitivities - Business Requirements Document

**Meridian Global Bank - Market Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | IRV-BRD-001 |
| **Version** | 1.0 |
| **Effective Date** | 13 January 2025 |
| **Owner** | Market Risk Technology |
| **Approver** | Risk Technology Change Board |

---

## 1. Executive Summary

### 1.1 Purpose

This Business Requirements Document defines the functional and non-functional requirements for the IR Vega sensitivity feed from Murex to downstream market risk systems. The feed provides interest rate volatility risk exposures for options and option-embedded products.

### 1.2 Business Context

Vega risk is a critical component of interest rate risk for portfolios containing:
- **Swaptions** - Options on interest rate swaps
- **Caps and Floors** - Interest rate options providing rate protection
- **Structured Products** - Products with embedded optionality (range accruals, callables)
- **Credit Derivatives** - CRD guarantees and insurance with volatility sensitivity

Accurate vega sensitivity measurement is essential for:
- **Risk Management**: Understanding exposure to volatility movements
- **P&L Attribution**: Explaining daily P&L from implied volatility changes
- **Hedging Decisions**: Identifying vega exposures requiring delta-hedging
- **Regulatory Reporting**: FRTB vega risk capital requirements
- **Limit Monitoring**: Tracking against vega risk limits

### 1.3 Scope

| In Scope | Out of Scope |
|----------|--------------|
| IR Vega sensitivities | FX Vega sensitivities |
| Option maturity pillars | Equity Vega sensitivities |
| Underlying maturity pillars | Credit spread Vega |
| Strike and ATM spread | Commodity Vega |
| Multiple vega types (Flat, Normal, Yield) | Theta/time decay |
| Regional processing (LN, HK, NY, SP) | Realized volatility measures |

---

## 2. Business Requirements

### 2.1 Functional Requirements

#### BR-IRV-001: IR Vega Sensitivity Calculation

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IRV-001 |
| **Title** | IR Vega Sensitivity Calculation |
| **Priority** | Critical |
| **Description** | The system shall calculate IR Vega sensitivities representing the change in NPV for a 1% change in implied volatility |
| **Acceptance Criteria** | Vega values expressed in local currency and USD equivalent |
| **Business Rationale** | Vega is a distinct risk factor requiring separate measurement from delta risks |

#### BR-IRV-002: Volatility Type Selection

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IRV-002 |
| **Title** | Appropriate Vega Type Selection |
| **Priority** | Critical |
| **Description** | The feed shall select the appropriate vega output based on product type and volatility nature |
| **Vega Types** | Flat Vega (Cap/Floor non-normal), Normal Vega (Swaptions/normal vol), Vega Yield (default) |
| **Business Rationale** | Different products require different volatility models for accurate risk measurement |

#### BR-IRV-003: Two-Dimensional Maturity Structure

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IRV-003 |
| **Title** | Option and Underlying Maturity Pillars |
| **Priority** | Critical |
| **Description** | Sensitivities shall include both option maturity and underlying maturity dimensions |
| **Data Elements** | Option Maturity (pillar and date), Underlying Maturity (pillar and date) |
| **Business Rationale** | Volatility surfaces are two-dimensional; both expiry and tenor affect vega exposure |

#### BR-IRV-004: Strike Information

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IRV-004 |
| **Title** | Option Strike and ATM Spread |
| **Priority** | High |
| **Description** | The feed shall include option strike and ATM spread for smile curve positioning |
| **Data Elements** | Strike, ATM Spread, ATM Strike |
| **Business Rationale** | Smile risk requires understanding position relative to ATM for accurate Greeks |

#### BR-IRV-005: Product Coverage

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IRV-005 |
| **Title** | Vega-Sensitive Product Scope |
| **Priority** | Critical |
| **Description** | The feed shall include all trades with exposure to IR volatility movements |
| **Product Types** | Swaptions (OSWP), Caps/Floors (CF), CRD Guarantees, CRD Insurance, Range Accruals |
| **Exclusions** | Bond Options (Group = 'OPT') |
| **Business Rationale** | Complete coverage ensures no vega risk is unmeasured |

#### BR-IRV-006: Regional Processing

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IRV-006 |
| **Title** | Multi-Region Support |
| **Priority** | High |
| **Description** | The feed shall be produced separately for each trading region |
| **Regions** | London (LN), Hong Kong (HK), New York (NY), Sao Paulo (SP) |
| **Business Rationale** | Regional market data and booking ensures accurate local valuations |

#### BR-IRV-007: Range Accrual Currency Resolution

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IRV-007 |
| **Title** | Index Currency for Range Accruals |
| **Priority** | High |
| **Description** | For range accrual products, currency shall be derived from the interest rate index definition |
| **Logic** | Use RT_INDEX currency if available, otherwise use trade currency |
| **Business Rationale** | Range accruals reference indices that may differ from trade currency |

### 2.2 Non-Functional Requirements

#### BR-IRV-NFR-001: Timeliness

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IRV-NFR-001 |
| **Title** | Data Delivery SLA |
| **Priority** | Critical |
| **Description** | Feed must be delivered by 05:30 GMT (T+1) for London region |
| **Measurement** | 95% of deliveries within SLA over rolling 30-day period |

#### BR-IRV-NFR-002: Completeness

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IRV-NFR-002 |
| **Title** | Data Completeness |
| **Priority** | Critical |
| **Description** | All live vega-sensitive positions must have sensitivity values |
| **Tolerance** | <0.1% missing sensitivity records |

#### BR-IRV-NFR-003: Accuracy

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IRV-NFR-003 |
| **Title** | Calculation Accuracy |
| **Priority** | Critical |
| **Description** | Vega values must match front office system within tolerance |
| **Tolerance** | ±0.01% for Vega values |

#### BR-IRV-NFR-004: Reconciliation

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IRV-NFR-004 |
| **Title** | Daily Reconciliation |
| **Priority** | High |
| **Description** | Feed totals must reconcile to Murex Valuation Reports |
| **Breaks Threshold** | ±$5,000 USD at portfolio level |

---

## 3. Data Requirements

### 3.1 Input Data

| Source | Data Element | Description |
|--------|--------------|-------------|
| Murex Trade Repository | Trade attributes | Trade number, portfolio, typology, family/group/type |
| Murex Valuation | Vega values | Per-option maturity, per-underlying maturity sensitivities |
| Market Data | Volatility surfaces | IR swaption and cap volatilities |
| Market Data | FX rates | For USD equivalent conversion |
| Reference Data | RT_INDEX | Interest rate index definitions |
| Reference Data | RT_RANGE | Range accrual definitions |

### 3.2 Output Data

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| TRADE_NUM | Numeric | Unique trade identifier | Trade Repository |
| CURRENCY | VarChar | Vega currency (index or trade) | Derived |
| FAMILY | VarChar | Deal family (IRD, CRD) | Simulation View |
| GROUP | VarChar | Deal group (OSWP, CF, CDS) | Simulation View |
| TYPE | VarChar | Deal type | Simulation View |
| Category | VarChar | Category (blank) | Dynamic Table |
| Portfolio | VarChar | Trading book code | Simulation View |
| Profit Centre | VarChar | Cost centre | Dynamic Table |
| Option Maturity | VarChar | Option maturity pillar | Simulation View |
| Option Maturity Date | Date | Option maturity date | Simulation View |
| Underl Maturity | VarChar | Underlying maturity pillar | Simulation View |
| Underl Maturity Date | Date | Underlying maturity date | Simulation View |
| Strike | Numeric | Option strike | Simulation View |
| ATM Spread | Numeric | Distance from ATM | Simulation View |
| Vega Yield (local cur) | Numeric | IR Vega in local currency | Derived |
| ZAR_PROCESSING | VarChar | JBSBSA flag (Y/N) | Extraction |
| Vega Yield (USD) | Numeric | IR Vega in USD | Simulation View |
| Vega Yield (ZAR) | Numeric | IR Vega in ZAR | Simulation View |
| Typology | VarChar | Product classification | Simulation View |
| Index | VarChar | PL instrument | Simulation View |
| ATM Strike | Numeric | ATM strike level | Simulation View |

### 3.3 Data Quality Rules

| Rule ID | Field | Rule | Action on Failure |
|---------|-------|------|-------------------|
| DQ-IRV-001 | Trade Number | Must not be null | Reject record |
| DQ-IRV-002 | Vega values | Must be numeric | Reject record |
| DQ-IRV-003 | Option Maturity Date | Must not be empty | Reject record (filter) |
| DQ-IRV-004 | Currency | Must resolve (index or trade) | Warning |
| DQ-IRV-005 | Legal Entity | Must not be SBSA | Exclude record |

---

## 4. Business Rules

### 4.1 Vega Type Selection Rules

| Rule ID | Condition | Vega Output Used |
|---------|-----------|------------------|
| BR-VEGA-001 | Group = "CF" AND Vol_nature <> "Normal" | Flat_Vega, Flat_Vega_USD |
| BR-VEGA-002 | (Group IN ("OSWP", "CF") OR Typology IN ("CRD - GUARANTEE", "CRD - INSURANCE", "IRD - CAPS/FLOORS")) AND Vol_nature = "Normal" | Normal_Vega, Nor_Vega_USD |
| BR-VEGA-003 | All other cases | Vega_Yield, Vega_Yield_USD |

### 4.2 Product Filtering Rules

| Rule ID | Condition | Action |
|---------|-----------|--------|
| BR-FILTER-001 | Opt_Maturity_Date is empty | Exclude (simulation view filter) |
| BR-FILTER-002 | Family = 'IRD' OR Typology IN ('CRD - GUARANTEE', 'CRD - INSURANCE') | Include |
| BR-FILTER-003 | Group = 'OPT' | Exclude (bond options) |
| BR-FILTER-004 | Legal Entity = 'SBSA' | Exclude |

### 4.3 Currency Resolution Rules

| Rule ID | Condition | Action |
|---------|-----------|--------|
| BR-CCY-001 | Trade is range accrual | Use RT_INDEX.M_CURRENCY |
| BR-CCY-002 | No range accrual | Use IR_VEGA.M_CURRENCY |
| BR-CCY-003 | Currency = 'USD' | No FX conversion needed |
| BR-CCY-004 | Currency <> 'USD' | Convert using TBL_MD_FXSPOTS_REP |

### 4.4 Deprecated Fields

| Field | Original Purpose | Current Status |
|-------|------------------|----------------|
| Vega_ZAR | ZAR equivalent | Deprecated - should be decommissioned |
| Normal_Vega_ZAR | Normal Vega ZAR | Deprecated - should be decommissioned |
| Vega_Yield_ZAR | Yield Vega ZAR | Deprecated - should be decommissioned |

---

## 5. Processing Requirements

### 5.1 Processing Schedule

| Step | Time (GMT) | Description |
|------|------------|-------------|
| 1 | 18:00 | Market data close (London) |
| 2 | 21:00 | Valuation batch complete |
| 3 | 02:30 | Vega feeder batch start |
| 4 | 03:30 | Vega feeder batch complete |
| 5 | 04:00 | Extraction start |
| 6 | 04:30 | File generation |
| 7 | 05:00 | File packaging |
| 8 | 05:30 | MFT delivery |

### 5.2 Dependencies

| Upstream | Dependency Type | Impact if Delayed |
|----------|-----------------|-------------------|
| Market Data | Hard | Feed cannot run |
| Valuation Batch | Hard | Feed cannot run |
| FX Rates | Soft | Previous day rates used |
| Reference Tables (RT_INDEX, RT_RANGE) | Hard | Range accrual currency missing |

### 5.3 Error Handling

| Error Type | Handling | Escalation |
|------------|----------|------------|
| Missing market data | Abort feed | Immediate to Risk Tech |
| Valuation failure | Retry once, then abort | Immediate to Risk Tech |
| FX rate unavailable | Use default rate of 1 | Daily summary |
| Range lookup failure | Use trade currency | Warning log |
| MFT delivery failure | Retry 3 times | After 3rd failure to Ops |

---

## 6. Reporting Requirements

### 6.1 Standard Reports

| Report | Frequency | Audience |
|--------|-----------|----------|
| Feed Completion Status | Daily | Risk Technology |
| Data Quality Summary | Daily | Risk Operations |
| Reconciliation Breaks | Daily | Risk Control |
| Vega Exposure Summary | Daily | Options Trading |

### 6.2 Reconciliation Requirements

| Check | Frequency | Tolerance |
|-------|-----------|-----------|
| Feed vs Murex Totals | Daily | ±$5,000 |
| Record Count | Daily | ±5% |
| Portfolio Coverage | Daily | 100% |

---

## 7. Stakeholders

### 7.1 Business Stakeholders

| Role | Responsibility |
|------|----------------|
| Head of Options Trading | Business owner, sign-off |
| Rates Risk Manager | Daily user, requirements |
| Options Trading Desk | Primary data consumer |
| Treasury | ALM optionality exposure |

### 7.2 Technical Stakeholders

| Role | Responsibility |
|------|----------------|
| Risk Technology Lead | Technical delivery |
| Murex Support Team | Source system support |
| Data Warehouse Team | Target system integration |
| MFT Operations | File transfer |

---

## 8. Acceptance Criteria

### 8.1 Functional Acceptance

| Criteria | Verification Method |
|----------|---------------------|
| All vega-sensitive trades covered | Product inventory reconciliation |
| Correct vega type selected | Sample validation by product type |
| Option/underlying maturity populated | Field completeness check |
| Regional files generated | File existence check |
| Range accrual currency correct | Sample validation vs RT_INDEX |

### 8.2 Non-Functional Acceptance

| Criteria | Verification Method |
|----------|---------------------|
| Delivery by 05:30 GMT | Timestamp monitoring |
| <0.1% missing records | Completeness report |
| ±0.01% accuracy | Reconciliation report |
| 99.5% availability | Uptime monitoring |

---

## 9. Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Valuation batch delays | High | Medium | Buffer time in schedule |
| New product types | Medium | Medium | Regular product review |
| Vol surface changes | Medium | Low | Automated curve discovery |
| Range accrual lookup failure | Low | Low | Default to trade currency |
| London 3-batch complexity | Medium | Medium | Consider consolidation |

---

## 10. Known Issues

### 10.1 London Three-Batch Configuration

The London region uses 3 separate feeder batches due to historical Murex processing constraints. This adds complexity and should be reviewed for consolidation.

**Recommendation**: Evaluate if current Murex version supports single-batch processing.

### 10.2 Portfolio Filtering

The portfolio selection includes both Level 4 and Level 5 portfolio nodes inconsistently:
- London uses Level 4 nodes appropriately
- Other regions mix Level 4 and Level 5 nodes
- Some inactive portfolios included (e.g., FXDHK, LMHKSBL01)

**Recommendation**: Standardize to Level 4 portfolio nodes only.

### 10.3 ZAR Fields Deprecated

Multiple ZAR-denominated fields are flagged for decommissioning:
- Vega_ZAR
- Vega_Yield_ZAR
- Normal_Vega_ZAR

**Recommendation**: Remove ZAR fields in next feed update cycle.

---

## 11. Document Control

### 11.1 Version History

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | 2025-01-13 | Initial version | Risk Technology |

### 11.2 Approval

| Role | Name | Date |
|------|------|------|
| Business Owner | Head of Options Trading | |
| Technical Owner | Head of Risk Technology | |
| Approver | Risk Technology Change Board | |

---

*End of Document*
