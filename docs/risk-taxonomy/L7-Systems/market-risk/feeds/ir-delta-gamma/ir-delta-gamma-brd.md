---
# Document Metadata
document_id: IR-BRD-001
document_name: IR Delta & Gamma - Business Requirements Document
version: 1.0
effective_date: 2025-01-03
next_review_date: 2026-01-03
owner: Market Risk Technology
approving_committee: Risk Technology Change Board

# Taxonomy Reference
parent_node: L7-Systems/market-risk/feeds/ir-delta-gamma
feed_family: IR Delta & Gamma
document_type: BRD
---

# IR Delta & Gamma - Business Requirements Document

**Meridian Global Bank - Market Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | IR-BRD-001 |
| **Version** | 1.0 |
| **Effective Date** | 3 January 2025 |
| **Owner** | Market Risk Technology |
| **Approver** | Risk Technology Change Board |

---

## 1. Executive Summary

### 1.1 Purpose

This Business Requirements Document defines the functional and non-functional requirements for the IR Delta & Gamma sensitivity feed from Murex to downstream market risk systems. The feed provides interest rate risk exposures (DV01) and convexity measures (Gamma) for the Interest Rate Derivatives (IRD) trading book.

### 1.2 Business Context

Interest rate risk is a primary driver of Profit & Loss for the Rates trading desk. Accurate and timely DV01 and Gamma sensitivities are essential for:

- **Risk Management**: Daily position monitoring and limit utilization
- **Trading Decisions**: Understanding portfolio sensitivity to rate movements
- **Regulatory Reporting**: FRTB SA/IMA calculations, IRRBB compliance
- **P&L Attribution**: Explaining daily P&L through sensitivity-based decomposition

### 1.3 Scope

| In Scope | Out of Scope |
|----------|--------------|
| IR Delta (DV01) calculation | FX Delta sensitivities |
| IR Gamma calculation | Credit spread sensitivities |
| Zero curve sensitivities | Equity sensitivities |
| USD equivalent values | Commodity sensitivities |
| Regional processing (LN, HK, NY, SP) | Cross-gamma calculations |

---

## 2. Business Requirements

### 2.1 Functional Requirements

#### BR-IR-001: Delta (DV01) Calculation

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IR-001 |
| **Title** | DV01 Sensitivity Calculation |
| **Priority** | Critical |
| **Description** | The system shall calculate DV01 (Dollar Value of a 01 - one basis point shift) for all IRD positions against zero coupon yield curves |
| **Acceptance Criteria** | DV01 values shall be expressed in local currency and USD equivalent |
| **Business Rationale** | DV01 is the primary measure of interest rate risk exposure |

#### BR-IR-002: Gamma Calculation

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IR-002 |
| **Title** | Gamma Sensitivity Calculation |
| **Priority** | High |
| **Description** | The system shall calculate Gamma (rate of change of Delta for a 1bp shift) for products with embedded optionality |
| **Acceptance Criteria** | Gamma calculated only for Caps/Floors (IRD\|CF\|) and Swaptions (IRD\|OSWP\|); Gamma = 0 for linear products |
| **Business Rationale** | Gamma measures convexity risk for option portfolios |

#### BR-IR-003: Product Coverage

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IR-003 |
| **Title** | IRD Product Scope |
| **Priority** | Critical |
| **Description** | The feed shall cover all IRD product types traded in Murex |
| **Product Families** | IRD (Interest Rate Derivatives) |
| **Product Groups** | CF (Caps/Floors), OSWP (Swaptions), SWAP (Swaps), FRA, FUT, BOND, REPO |

#### BR-IR-004: Curve Granularity

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IR-004 |
| **Title** | Interest Rate Curve Breakdown |
| **Priority** | Critical |
| **Description** | Sensitivities shall be broken down by interest rate curve and pillar date |
| **Curve Examples** | USD_LIBOR_3M, EUR_EURIBOR_6M, GBP_SONIA, USD_SOFR |
| **Pillar Set** | LNOFFICIAL: O/N, T/N, 1W, 2W, 1M, 2M, 3M, 6M, 9M, 1Y-30Y |

#### BR-IR-005: Regional Processing

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IR-005 |
| **Title** | Multi-Region Support |
| **Priority** | High |
| **Description** | The feed shall be produced separately for each trading region using region-specific market data |
| **Regions** | London (LN), Hong Kong (HK), New York (NY), Singapore (SP) |
| **Market Data** | Each region uses its own EOD market data set |

#### BR-IR-006: Delta-Gamma Combination

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IR-006 |
| **Title** | Combined Output File |
| **Priority** | High |
| **Description** | Delta and Gamma shall be combined into a single output file using LEFT JOIN logic |
| **Join Key** | TRADE_NUM + CURVENAME + DATE |
| **Default Gamma** | 0 for non-option products |

### 2.2 Non-Functional Requirements

#### BR-IR-NFR-001: Timeliness

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IR-NFR-001 |
| **Title** | Data Delivery SLA |
| **Priority** | Critical |
| **Description** | Feed must be delivered by 05:00 GMT (T+1) for London region |
| **Measurement** | 95% of deliveries within SLA over rolling 30-day period |

#### BR-IR-NFR-002: Completeness

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IR-NFR-002 |
| **Title** | Data Completeness |
| **Priority** | Critical |
| **Description** | All live IRD positions must have Delta values; option positions must have Gamma values |
| **Tolerance** | <0.1% missing sensitivity records |

#### BR-IR-NFR-003: Accuracy

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IR-NFR-003 |
| **Title** | Calculation Accuracy |
| **Priority** | Critical |
| **Description** | DV01 and Gamma values must match front office system within tolerance |
| **Tolerance** | ±0.01% for DV01; ±0.1% for Gamma |

#### BR-IR-NFR-004: Reconciliation

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IR-NFR-004 |
| **Title** | Daily Reconciliation |
| **Priority** | High |
| **Description** | Feed totals must reconcile to Murex Valuation Reports |
| **Breaks Threshold** | ±$10,000 USD at portfolio level |

---

## 3. Data Requirements

### 3.1 Input Data

| Source | Data Element | Description |
|--------|--------------|-------------|
| Murex Trade Repository | Trade attributes | Trade number, portfolio, typology |
| Murex Valuation | DV01 values | Per-curve, per-pillar sensitivities |
| Murex Valuation | Gamma values | Option convexity measures |
| Market Data | Yield curves | Zero coupon curves by currency |
| Market Data | Volatility surfaces | For option Greeks calculation |

### 3.2 Output Data

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| TRADE_NUM | String | Unique trade identifier | Trade Repository |
| PORTFOLIO | String | Trading book code | Trade Repository |
| DATE | Date | Pillar date | Maturity Set |
| CURVENAME | String | Interest rate curve | Valuation Engine |
| TYPOLOGY | String | Product classification | Trade Repository |
| DELTAUSD | Numeric | DV01 in USD | Valuation Engine |
| GAMMAUSD | Numeric | Gamma in USD | Valuation Engine |

### 3.3 Data Quality Rules

| Rule ID | Field | Rule | Action on Failure |
|---------|-------|------|-------------------|
| DQ-IR-001 | TRADE_NUM | Must not be null | Reject record |
| DQ-IR-002 | DELTAUSD | Must be numeric | Reject record |
| DQ-IR-003 | DATE | Must be valid date | Reject record |
| DQ-IR-004 | CURVENAME | Must exist in curve inventory | Warning |
| DQ-IR-005 | GAMMAUSD | Must be 0 for non-options | Correct to 0 |

---

## 4. Business Rules

### 4.1 Gamma Filtering Rules

| Rule ID | Condition | Action |
|---------|-----------|--------|
| BR-GAMMA-001 | Product = IRD\|CF\|* | Calculate Gamma |
| BR-GAMMA-002 | Product = IRD\|OSWP\|* | Calculate Gamma |
| BR-GAMMA-003 | Product = any other | Set Gamma = 0 |
| BR-GAMMA-004 | Deal is purged | Set Gamma = 0 |

### 4.2 Currency Conversion Rules

| Rule ID | Condition | Action |
|---------|-----------|--------|
| BR-FX-001 | Local CCY = USD | DELTAUSD = DV01 |
| BR-FX-002 | Local CCY ≠ USD | DELTAUSD = DV01 × FX Rate |
| BR-FX-003 | FX Rate unavailable | Use previous day rate |

### 4.3 Maturity Set Rules

The LNOFFICIAL maturity set defines the pillar structure:

| Tenor Bucket | Pillars |
|--------------|---------|
| Short-term | O/N, T/N, 1W, 2W |
| Money Market | 1M, 2M, 3M, 6M, 9M |
| Swap Tenors | 1Y, 2Y, 3Y, 5Y, 7Y, 10Y, 15Y, 20Y, 30Y |

### 4.4 Deprecated Fields

The following fields are retained for backward compatibility but are no longer actively used:

| Field | Original Purpose | Current Status |
|-------|------------------|----------------|
| ZAR_PROCESSING | SBSA flag | Deprecated |
| DELTAZAR | ZAR equivalent DV01 | Deprecated |
| GAMMAZAR | ZAR equivalent Gamma | Deprecated |
| PARDELTAZAR | Par ZAR Delta | Deprecated |
| PARGAMMAZAR | Par ZAR Gamma | Deprecated |

---

## 5. Processing Requirements

### 5.1 Processing Schedule

| Step | Time (GMT) | Description |
|------|------------|-------------|
| 1 | 18:00 | Market data close (London) |
| 2 | 21:00 | Valuation batch complete |
| 3 | 02:00 | Delta feeder batch start |
| 4 | 02:30 | Gamma feeder batch start |
| 5 | 03:30 | Both feeders complete |
| 6 | 04:00 | Extraction (LEFT JOIN) |
| 7 | 04:30 | File generation |
| 8 | 05:00 | MFT delivery |

### 5.2 Dependencies

| Upstream | Dependency Type | Impact if Delayed |
|----------|-----------------|-------------------|
| Market Data | Hard | Feed cannot run |
| Valuation Batch | Hard | Feed cannot run |
| Trade Repository | Hard | Missing trades |
| FX Rates | Soft | Previous day rates used |

### 5.3 Error Handling

| Error Type | Handling | Escalation |
|------------|----------|------------|
| Missing market data | Abort feed | Immediate to Risk Tech |
| Valuation failure | Retry once, then abort | Immediate to Risk Tech |
| Partial trade failures | Continue with warnings | Morning summary email |
| MFT delivery failure | Retry 3 times | After 3rd failure to Ops |

---

## 6. Reporting Requirements

### 6.1 Standard Reports

| Report | Frequency | Audience |
|--------|-----------|----------|
| Feed Completion Status | Daily | Risk Technology |
| Data Quality Summary | Daily | Risk Operations |
| Reconciliation Breaks | Daily | Risk Control |
| Monthly Volumes | Monthly | Management |

### 6.2 Reconciliation Requirements

| Check | Frequency | Tolerance |
|-------|-----------|-----------|
| Feed vs Murex Totals | Daily | ±$10,000 |
| Record Count | Daily | 0% variance |
| Portfolio Coverage | Daily | 100% |

---

## 7. Stakeholders

### 7.1 Business Stakeholders

| Role | Responsibility |
|------|----------------|
| Head of Rates Trading | Business owner, sign-off |
| Rates Risk Manager | Daily user, requirements |
| Market Risk COO | Operational oversight |
| Regulatory Reporting | FRTB/IRRBB data consumer |

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
| All IRD products covered | Product inventory reconciliation |
| DV01 values correct | Sample validation vs front office |
| Gamma values correct | Option pricing model validation |
| Regional files generated | File existence check |
| LEFT JOIN logic correct | Delta records without Gamma = 0 |

### 8.2 Non-Functional Acceptance

| Criteria | Verification Method |
|----------|---------------------|
| Delivery by 05:00 GMT | Timestamp monitoring |
| <0.1% missing records | Completeness report |
| ±0.01% accuracy | Reconciliation report |
| 99.5% availability | Uptime monitoring |

---

## 9. Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Valuation batch delays | High | Medium | Buffer time in schedule |
| Market data gaps | High | Low | Previous day fallback |
| High trade volumes | Medium | Medium | Performance optimization |
| Curve inventory changes | Medium | Low | Change management process |

---

## 10. Document Control

### 10.1 Version History

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | 2025-01-03 | Initial version | Risk Technology |

### 10.2 Approval

| Role | Name | Date |
|------|------|------|
| Business Owner | Head of Rates Trading | |
| Technical Owner | Head of Risk Technology | |
| Approver | Risk Technology Change Board | |

---

*End of Document*
