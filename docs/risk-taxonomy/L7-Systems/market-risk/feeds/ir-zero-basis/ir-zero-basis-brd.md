---
# Document Metadata
document_id: IRB-BRD-001
document_name: IR Zero Basis - Business Requirements Document
version: 1.0
effective_date: 2025-01-03
next_review_date: 2026-01-03
owner: Market Risk Technology
approving_committee: Risk Technology Change Board

# Taxonomy Reference
parent_node: L7-Systems/market-risk/feeds/ir-zero-basis
feed_family: IR Zero Basis
document_type: BRD
---

# IR Zero Basis - Business Requirements Document

**Meridian Global Bank - Market Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | IRB-BRD-001 |
| **Version** | 1.0 |
| **Effective Date** | 3 January 2025 |
| **Owner** | Market Risk Technology |
| **Approver** | Risk Technology Change Board |

---

## 1. Executive Summary

### 1.1 Purpose

This Business Requirements Document defines the functional and non-functional requirements for the IR Zero Basis sensitivity feed from Murex to downstream market risk systems. The feed provides interest rate basis risk exposures for positions sensitive to spread movements between different interest rate curves in the same currency.

### 1.2 Business Context

Basis risk is a significant component of interest rate risk for portfolios containing:
- **Basis swaps** - Exchange floating payments on different indices
- **Cross-currency swaps** - Exposure to cross-currency basis spreads
- **Multi-curve discounting** - Positions valued with different projection/discount curves

Accurate basis sensitivity measurement is essential for:
- **Risk Management**: Understanding exposure to basis spread movements
- **P&L Attribution**: Explaining daily P&L from basis spread changes
- **Hedging Decisions**: Identifying basis risk to be hedged
- **Regulatory Reporting**: FRTB basis risk capital requirements

### 1.3 Scope

| In Scope | Out of Scope |
|----------|--------------|
| IR basis zero sensitivities | Outright IR Delta (DV01) |
| Zero curve basis bumping | Par curve basis sensitivities |
| Multi-currency basis curves | FX spot/forward sensitivities |
| Regional processing (LN, HK, NY, SP) | Credit spread sensitivities |
| USD equivalent values | Commodity basis risk |

---

## 2. Business Requirements

### 2.1 Functional Requirements

#### BR-IRB-001: Basis Zero Sensitivity Calculation

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IRB-001 |
| **Title** | IR Basis Zero Sensitivity Calculation |
| **Priority** | Critical |
| **Description** | The system shall calculate IR Basis Zero sensitivities by bumping zero coupon basis curves |
| **Acceptance Criteria** | Basis values shall be expressed in local currency and USD equivalent |
| **Business Rationale** | Basis risk is a distinct risk factor requiring separate measurement from outright IR |

#### BR-IRB-002: Basis Curve Coverage

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IRB-002 |
| **Title** | Basis Curve Identification |
| **Priority** | Critical |
| **Description** | The feed shall identify the specific basis curve for each sensitivity |
| **Acceptance Criteria** | Curve name, currency, generator type, and generator name included |
| **Business Rationale** | Different basis curves have different market dynamics and hedging instruments |

#### BR-IRB-003: Pillar Granularity

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IRB-003 |
| **Title** | Maturity Pillar Breakdown |
| **Priority** | Critical |
| **Description** | Sensitivities shall be assigned to standard maturity pillars |
| **Pillar Set** | RISK_VIEW: O/N, T/N, 1W, 1M, 2M, 3M, 6M, 9M, 1Y through 40Y |
| **Business Rationale** | Pillar-level detail required for hedging and limit monitoring |

#### BR-IRB-004: Product Coverage

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IRB-004 |
| **Title** | Basis-Sensitive Product Scope |
| **Priority** | Critical |
| **Description** | The feed shall include all trades with exposure to basis spread movements |
| **Product Types** | Basis swaps, cross-currency swaps, multi-curve swaps |
| **Business Rationale** | Complete coverage ensures no basis risk is unmeasured |

#### BR-IRB-005: Regional Processing

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IRB-005 |
| **Title** | Multi-Region Support |
| **Priority** | High |
| **Description** | The feed shall be produced separately for each trading region |
| **Regions** | London (LN), Hong Kong (HK), New York (NY), Sao Paulo (SP) |
| **Business Rationale** | Regional market data and booking ensures accurate local valuations |

#### BR-IRB-006: Generator Information

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IRB-006 |
| **Title** | Rate Curve Generator Details |
| **Priority** | Medium |
| **Description** | The feed shall include generator type and name from curve configuration |
| **Data Elements** | Generator Type (e.g., "Basis swap"), Generator Name (e.g., "_EUR ESTR 3M /USD SOFR 3M") |
| **Business Rationale** | Generator details identify the specific market instrument driving the basis curve |

### 2.2 Non-Functional Requirements

#### BR-IRB-NFR-001: Timeliness

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IRB-NFR-001 |
| **Title** | Data Delivery SLA |
| **Priority** | Critical |
| **Description** | Feed must be delivered by 05:30 GMT (T+1) for London region |
| **Measurement** | 95% of deliveries within SLA over rolling 30-day period |

#### BR-IRB-NFR-002: Completeness

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IRB-NFR-002 |
| **Title** | Data Completeness |
| **Priority** | Critical |
| **Description** | All live basis-sensitive positions must have sensitivity values |
| **Tolerance** | <0.1% missing sensitivity records |

#### BR-IRB-NFR-003: Accuracy

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IRB-NFR-003 |
| **Title** | Calculation Accuracy |
| **Priority** | Critical |
| **Description** | Basis values must match front office system within tolerance |
| **Tolerance** | ±0.01% for Basis Zero |

#### BR-IRB-NFR-004: Reconciliation

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-IRB-NFR-004 |
| **Title** | Daily Reconciliation |
| **Priority** | High |
| **Description** | Feed totals must reconcile to Murex Valuation Reports |
| **Breaks Threshold** | ±$5,000 USD at portfolio level |

---

## 3. Data Requirements

### 3.1 Input Data

| Source | Data Element | Description |
|--------|--------------|-------------|
| Murex Trade Repository | Trade attributes | Trade number, portfolio, typology |
| Murex Valuation | Basis Zero values | Per-curve, per-pillar sensitivities |
| Market Data | Basis curves | Zero coupon basis curves by currency pair |
| Market Data | FX rates | For USD equivalent conversion |
| Curve Configuration | Generator details | Rate curve generator type and name |

### 3.2 Output Data

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| PORTFOLIO | String | Trading book code | Trade Repository |
| Trade Number | Numeric | Unique trade identifier | Trade Repository |
| CURRENCY | String | Basis curve currency | Curve Configuration |
| CURVE_NAM | String | Interest rate curve name | Valuation Engine |
| Type | String | Generator type | A_RTCT_REP |
| Generat | String | Generator name | A_RTCT_REP |
| DATE | String | Pillar date | Maturity Set |
| Basis Zero | Numeric | IR Basis Zero (local) | Valuation Engine |
| Basis Zero (USD) | Numeric | IR Basis Zero in USD | Valuation Engine |
| Typology | String | Product classification | Trade Repository |

### 3.3 Data Quality Rules

| Rule ID | Field | Rule | Action on Failure |
|---------|-------|------|-------------------|
| DQ-IRB-001 | Trade Number | Must not be null | Reject record |
| DQ-IRB-002 | Basis Zero | Must be numeric | Reject record |
| DQ-IRB-003 | DATE | Must be valid pillar | Reject record |
| DQ-IRB-004 | CURVE_NAM | Must exist in curve inventory | Warning |
| DQ-IRB-005 | Non-zero filter | At least one Basis field non-zero | Exclude if both zero |

---

## 4. Business Rules

### 4.1 Sensitivity Filtering Rules

| Rule ID | Condition | Action |
|---------|-----------|--------|
| BR-FILTER-001 | Basis Zero (local) = 0 AND Basis Zero (ZAR) = 0 | Exclude record |
| BR-FILTER-002 | Legal Entity = 'SBSA' | Exclude record |
| BR-FILTER-003 | Trade has basis curve exposure | Include record |

### 4.2 Currency Conversion Rules

| Rule ID | Condition | Action |
|---------|-----------|--------|
| BR-FX-001 | Local CCY = USD | Basis Zero (USD) = Basis Zero |
| BR-FX-002 | Local CCY ≠ USD | Basis Zero (USD) = Basis Zero × FX Spot Rate |
| BR-FX-003 | FX Rate unavailable | Use previous day rate |

### 4.3 Maturity Set Rules

The RISK_VIEW maturity set defines an extended pillar structure:

| Tenor Bucket | Pillars |
|--------------|---------|
| Short-term | O/N, T/N, 1W |
| Money Market | 1M, 2M, 3M, 6M, 9M |
| Short Swaps | 1Y, 2Y, 3Y, 4Y, 5Y |
| Medium Swaps | 6Y, 7Y, 8Y, 9Y, 10Y, 12Y |
| Long Swaps | 15Y, 20Y, 25Y, 30Y, 35Y, 40Y |

**Note**: Extended to 40Y compared to standard 30Y sets for long-dated basis exposure.

### 4.4 Deprecated Fields

| Field | Original Purpose | Current Status |
|-------|------------------|----------------|
| ZAR_PROCESSING | JBSBSA entity flag | Deprecated |
| Basis Zero (ZAR) | ZAR equivalent | Deprecated - SBSA exclusion |

---

## 5. Processing Requirements

### 5.1 Processing Schedule

| Step | Time (GMT) | Description |
|------|------------|-------------|
| 1 | 18:00 | Market data close (London) |
| 2 | 21:00 | Valuation batch complete |
| 3 | 02:30 | Basis feeder batch start |
| 4 | 03:30 | Basis feeder batch complete |
| 5 | 04:00 | Extraction start |
| 6 | 04:30 | File generation |
| 7 | 05:00 | File packaging |
| 8 | 05:30 | MFT delivery |

### 5.2 Dependencies

| Upstream | Dependency Type | Impact if Delayed |
|----------|-----------------|-------------------|
| Market Data | Hard | Feed cannot run |
| Valuation Batch | Hard | Feed cannot run |
| Curve Configuration | Hard | Missing generator details |
| FX Rates | Soft | Previous day rates used |

### 5.3 Error Handling

| Error Type | Handling | Escalation |
|------------|----------|------------|
| Missing market data | Abort feed | Immediate to Risk Tech |
| Valuation failure | Retry once, then abort | Immediate to Risk Tech |
| Curve lookup failure | Log warning, continue | Daily summary |
| MFT delivery failure | Retry 3 times | After 3rd failure to Ops |

---

## 6. Reporting Requirements

### 6.1 Standard Reports

| Report | Frequency | Audience |
|--------|-----------|----------|
| Feed Completion Status | Daily | Risk Technology |
| Data Quality Summary | Daily | Risk Operations |
| Reconciliation Breaks | Daily | Risk Control |
| Basis Exposure Summary | Daily | Rates Trading |

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
| Head of Rates Trading | Business owner, sign-off |
| Rates Risk Manager | Daily user, requirements |
| Basis Trading Desk | Primary data consumer |
| Treasury | Funding basis exposure |

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
| All basis-sensitive trades covered | Product inventory reconciliation |
| Basis values correct | Sample validation vs front office |
| Generator details populated | Field completeness check |
| Regional files generated | File existence check |

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
| Basis curve additions | Medium | Medium | Automated curve discovery |
| Portfolio filter issues | Medium | High | Standardize to Level 4 nodes |
| Generator lookup failures | Low | Low | Default to blank if missing |

---

## 10. Known Issues

### 10.1 Portfolio Filtering

The current portfolio selection requires cleanup:
- Mixing Level 4 and Level 5 portfolio nodes
- Some inactive portfolios included (e.g., JBSBSA)
- Some active portfolios missing (e.g., PMSG for Singapore)

**Recommendation**: Standardize to Level 4 portfolio nodes only.

### 10.2 HK Global Filter

The HKG feeder includes an expression filter to exclude specific currency swaps:
```
NOT.(TRN_GRP="CS".AND.(INSTRUMENT="SGD/USD F/F 6M".OR.INSTRUMENT="SGD/USD F/V 3M".OR.INSTRUMENT="SGD/USD V/V 6M"))
```

**Recommendation**: Remove as related deals have long expired.

---

## 11. Document Control

### 11.1 Version History

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | 2025-01-03 | Initial version | Risk Technology |

### 11.2 Approval

| Role | Name | Date |
|------|------|------|
| Business Owner | Head of Rates Trading | |
| Technical Owner | Head of Risk Technology | |
| Approver | Risk Technology Change Board | |

---

*End of Document*
