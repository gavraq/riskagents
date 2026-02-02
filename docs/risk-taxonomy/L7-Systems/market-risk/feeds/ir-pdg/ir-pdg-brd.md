---
# Document Metadata
document_id: PDG-BRD-001
document_name: IR Par Delta Gamma (PDG) - Business Requirements Document
version: 1.0
effective_date: 2025-01-03
next_review_date: 2026-01-03
owner: Product Control
approving_committee: Risk Technology Change Board

# Taxonomy Reference
parent_node: L7-Systems/market-risk/feeds/ir-pdg
feed_family: IR Par Delta Gamma
document_type: BRD
---

# IR Par Delta Gamma (PDG) - Business Requirements Document

**Meridian Global Bank - Market Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | PDG-BRD-001 |
| **Version** | 1.0 |
| **Effective Date** | 3 January 2025 |
| **Owner** | Product Control |
| **Approver** | Risk Technology Change Board |

---

## 1. Executive Summary

### 1.1 Purpose

This Business Requirements Document defines the functional and non-functional requirements for the IR Par Delta Gamma (PDG) sensitivity feed from Murex to downstream systems. The feed provides par rate interest rate sensitivities for Product Control requirements.

### 1.2 Business Context

**Important**: This feed is requested by **Product Control**, not Market Risk. While the Market Risk IR Delta & Gamma feed uses zero rate sensitivities for risk management purposes, Product Control requires par rate sensitivities for:

- **P&L Attribution**: Explaining daily P&L from market rate movements
- **Front Office Analytics**: Supporting trading desk analysis
- **Position Reporting**: Sensitivity reporting against quoted market rates
- **Hedge Effectiveness**: Measuring hedge ratios against par curve movements

### 1.3 Par Rate vs Zero Rate Sensitivities

| Aspect | Par Rate (This Feed) | Zero Rate (Market Risk Feed) |
|--------|----------------------|------------------------------|
| **Curve** | Par yield curve (quoted rates) | Zero coupon curve (derived) |
| **Use Case** | P&L, front office | Risk limits, VaR, capital |
| **Consumer** | Product Control | Market Risk |
| **Relationship** | Reflects quoted market instruments | Reflects time value of money |

### 1.4 Scope

| In Scope | Out of Scope |
|----------|--------------|
| IR Par Delta sensitivities | Zero rate sensitivities (separate feed) |
| IR Par Gamma sensitivities | Basis sensitivities |
| Multi-region processing (LN, HK, NY, SP) | FX spot/forward sensitivities |
| Bond and structured product handling | Credit spread sensitivities |
| USD and local currency values | Commodity sensitivities |

---

## 2. Business Requirements

### 2.1 Functional Requirements

#### BR-PDG-001: Par Rate Delta Sensitivity Calculation

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-PDG-001 |
| **Title** | IR Par Delta Sensitivity Calculation |
| **Priority** | Critical |
| **Description** | The system shall calculate IR Delta sensitivities by bumping par yield curves by 1 basis point |
| **Acceptance Criteria** | Delta Par values shall be expressed in local currency and USD equivalent |
| **Business Rationale** | Par rate sensitivities reflect exposure to quoted market rates used by trading desks |

#### BR-PDG-002: Par Rate Gamma Sensitivity Calculation

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-PDG-002 |
| **Title** | IR Par Gamma Sensitivity Calculation |
| **Priority** | Critical |
| **Description** | The system shall calculate IR Gamma (convexity) sensitivities for par rates |
| **Acceptance Criteria** | Gamma Par values shall be expressed in local currency and USD equivalent |
| **Business Rationale** | Gamma measures non-linear exposure critical for options and long-dated positions |

#### BR-PDG-003: Trade-Level Granularity

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-PDG-003 |
| **Title** | Trade-Level Sensitivity Breakdown |
| **Priority** | Critical |
| **Description** | Sensitivities shall be provided at trade level with unique trade identifier |
| **Acceptance Criteria** | Each record contains Trade Number, Portfolio, and product classification |
| **Business Rationale** | Trade-level detail required for P&L attribution and position reconciliation |

#### BR-PDG-004: Pillar Granularity

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-PDG-004 |
| **Title** | Maturity Pillar Breakdown |
| **Priority** | Critical |
| **Description** | Sensitivities shall be assigned to standard maturity pillars |
| **Pillar Set** | LNOFFICIAL: O/N, T/N, 1W, 2W, 1M, 2M, 3M, 6M, 9M, 1Y, 2Y, 3Y, 5Y, 7Y, 10Y, 15Y, 20Y, 30Y |
| **Business Rationale** | Pillar-level detail enables hedging analysis and curve risk reporting |

#### BR-PDG-005: Product Coverage

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-PDG-005 |
| **Title** | Comprehensive Product Scope |
| **Priority** | Critical |
| **Description** | The feed shall include all trades with IR sensitivity including bonds and structured products |
| **Product Types** | Swaps, FRAs, Caps/Floors, Swaptions, Bonds, Cross-Currency Swaps |
| **Business Rationale** | Complete coverage ensures accurate P&L attribution across all IR-sensitive positions |

#### BR-PDG-006: Regional Processing

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-PDG-006 |
| **Title** | Multi-Region Support |
| **Priority** | High |
| **Description** | The feed shall be produced separately for each trading region |
| **Regions** | London (LN), Hong Kong (HK), New York (NY), Sao Paulo (SP) |
| **Business Rationale** | Regional market data ensures accurate local valuations |

#### BR-PDG-007: Bond and Structured Product Handling

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-PDG-007 |
| **Title** | Bond Notional and Evaluation Data |
| **Priority** | High |
| **Description** | The feed shall include bond notional amounts and evaluation mode |
| **Data Elements** | act. Notional, Evaluation(Bond) |
| **Business Rationale** | Bond-specific data required for accurate position valuation and reporting |

#### BR-PDG-008: Product Classification

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-PDG-008 |
| **Title** | Extended Product Hierarchy |
| **Priority** | High |
| **Description** | The feed shall include full product classification (Family/Group/Type/Instrument) |
| **Data Elements** | Family, Group, Type, Instrument, Sec_code, Typology |
| **Business Rationale** | Product hierarchy enables aggregated reporting and portfolio analysis |

#### BR-PDG-009: Curve Metadata

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-PDG-009 |
| **Title** | Curve Type and Generator Information |
| **Priority** | Medium |
| **Description** | The feed shall include curve type and generator details |
| **Data Elements** | CurveType, Generat, Curve_Spread, Convexity_Spread |
| **Business Rationale** | Curve metadata supports curve attribution analysis |

### 2.2 Non-Functional Requirements

#### BR-PDG-NFR-001: Timeliness

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-PDG-NFR-001 |
| **Title** | Data Delivery SLA |
| **Priority** | Critical |
| **Description** | Feed must be delivered by 05:30 GMT (T+1) for London region |
| **Measurement** | 95% of deliveries within SLA over rolling 30-day period |

#### BR-PDG-NFR-002: Completeness

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-PDG-NFR-002 |
| **Title** | Data Completeness |
| **Priority** | Critical |
| **Description** | All live IR-sensitive positions must have sensitivity values |
| **Tolerance** | <0.1% missing sensitivity records |

#### BR-PDG-NFR-003: Accuracy

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-PDG-NFR-003 |
| **Title** | Calculation Accuracy |
| **Priority** | Critical |
| **Description** | Sensitivity values must match front office system within tolerance |
| **Tolerance** | ±0.01% for Delta Par, ±0.1% for Gamma Par |

#### BR-PDG-NFR-004: Reconciliation

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-PDG-NFR-004 |
| **Title** | Daily Reconciliation |
| **Priority** | High |
| **Description** | Feed totals must reconcile to Murex Valuation Reports |
| **Breaks Threshold** | ±$10,000 USD at portfolio level |

---

## 3. Data Requirements

### 3.1 Input Data

| Source | Data Element | Description |
|--------|--------------|-------------|
| Murex Trade Repository | Trade attributes | Trade number, portfolio, product hierarchy |
| Murex Valuation | Delta Par values | Per-curve, per-pillar par rate sensitivities |
| Murex Valuation | Gamma Par values | Per-curve, per-pillar par rate convexity |
| Market Data | IR curves | Par yield curves by currency |
| Market Data | FX rates | For USD equivalent conversion |
| Curve Configuration | Curve metadata | Curve type, generator information |
| Bond Data | Notional amounts | Bond face value and evaluation mode |
| Structured Product Data | RBC information | Risk Basket Composition |

### 3.2 Output Data

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| PORTFOLIO | String | Trading book code | Trade Repository |
| Family | String | Product family | Trade Repository |
| Group | String | Product group | Trade Repository |
| Type | String | Product type | Trade Repository |
| Instrument | String | P&L instrument | Trade Repository |
| Sec_code | String | Security code | Trade Repository |
| Trade Number | Numeric | Unique trade identifier | Trade Repository |
| CURRENCY | String | Curve currency | Curve Configuration |
| CURVE_NAM | String | Interest rate curve name | Valuation Engine |
| CurveType | String | Curve type | A_RTCT_REP |
| Generat | String | Generator name | Valuation Engine |
| DATE | String | Pillar date | Maturity Set |
| Delta Par | Numeric | IR Delta Par (local CCY) | Valuation Engine |
| Delta Par(USD) | Numeric | IR Delta Par in USD | Valuation Engine |
| Gamma Par | Numeric | IR Gamma Par (local CCY) | Valuation Engine |
| Gamma Par(USD) | Numeric | IR Gamma Par in USD | Valuation Engine |
| act. Notional | Numeric | Bond notional | Trade Parameters |
| Evaluation(Bond) | String | Bond evaluation mode | Bond Market Data |
| Typology | String | Product classification | Trade Repository |
| Curve_Spread | String | Spread flag (Y/N) | A_RTCT_REP |
| Convexity_Spread | String | Convexity spread flag (Y/N) | A_RATES_REP |

### 3.3 Data Quality Rules

| Rule ID | Field | Rule | Action on Failure |
|---------|-------|------|-------------------|
| DQ-PDG-001 | Trade Number | Must not be null (0 for DEAD trades) | Reject record |
| DQ-PDG-002 | Delta Par | Must be numeric | Reject record |
| DQ-PDG-003 | DATE | Must be valid pillar | Reject record |
| DQ-PDG-004 | CURVE_NAM | Must exist in curve inventory | Warning |
| DQ-PDG-005 | Non-zero filter | DV01__PA1<>0.OR.DV01__PAR<>0 | Exclude if both zero |
| DQ-PDG-006 | Legal Entity | Must not be SBSA | Exclude record |

---

## 4. Business Rules

### 4.1 Sensitivity Filtering Rules

| Rule ID | Condition | Action |
|---------|-----------|--------|
| BR-FILTER-001 | Delta Par = 0 AND Gamma Par = 0 | Exclude record |
| BR-FILTER-002 | Legal Entity = 'SBSA' | Exclude record |
| BR-FILTER-003 | HKG: SGD/USD XCCY swaps | Exclude specific instruments |

### 4.2 Currency Conversion Rules

| Rule ID | Condition | Action |
|---------|-----------|--------|
| BR-FX-001 | Local CCY = USD | Delta Par(USD) = Delta Par |
| BR-FX-002 | Local CCY ≠ USD | Delta Par(USD) = Delta Par × FX Spot Rate |
| BR-FX-003 | FX Rate unavailable | Use previous day rate |

### 4.3 Maturity Set Rules

The LNOFFICIAL maturity set defines the standard pillar structure:

| Tenor Bucket | Pillars |
|--------------|---------|
| Short-term | O/N, T/N, 1W, 2W |
| Money Market | 1M, 2M, 3M, 6M, 9M |
| Short Swaps | 1Y, 2Y, 3Y |
| Medium Swaps | 5Y, 7Y, 10Y |
| Long Swaps | 15Y, 20Y, 30Y |

### 4.4 Product-Specific Rules

#### Gamma Products

| Rule ID | Condition | Action |
|---------|-----------|--------|
| BR-GAMMA-001 | Family/Group = IRD\|CF\| | Include in Gamma calculation |
| BR-GAMMA-002 | Family/Group = IRD\|OSWP\| | Include in Gamma calculation |

#### Bond Handling

| Rule ID | Condition | Action |
|---------|-----------|--------|
| BR-BOND-001 | TRN_GRP = "BOND" | Lookup notional from A_BOND_NOTIONAL.REP |
| BR-BOND-002 | Trade is STB dummy bond | Apply STB-specific processing |
| BR-BOND-003 | M_TYPE is null | Set CurveType = 'Bond' |

### 4.5 Deprecated Fields

| Field | Original Purpose | Current Status |
|-------|------------------|----------------|
| ZAR_PROCESSING | JBSBSA entity flag | Deprecated |
| Delta Par(ZAR) | ZAR equivalent | Deprecated - SBSA exclusion |
| Gamma Par(ZAR) | ZAR Gamma equivalent | Deprecated - SBSA exclusion |

---

## 5. Processing Requirements

### 5.1 Processing Schedule

| Step | Time (GMT) | Description |
|------|------------|-------------|
| 1 | 18:00 | Market data close (London) |
| 2 | 21:00 | Valuation batch complete |
| 3 | 02:00 | IR Delta feeder batch start |
| 4 | 02:30 | IR Gamma feeder batch start |
| 5 | 03:30 | All feeder batches complete |
| 6 | 04:00 | Extraction batch start |
| 7 | 04:30 | File generation |
| 8 | 05:00 | File packaging |
| 9 | 05:30 | MFT delivery |

### 5.2 Dependencies

| Upstream | Dependency Type | Impact if Delayed |
|----------|-----------------|-------------------|
| Market Data | Hard | Feed cannot run |
| Valuation Batch | Hard | Feed cannot run |
| Curve Configuration | Hard | Missing curve metadata |
| Bond Market Data | Soft | Missing evaluation mode |
| FX Rates | Soft | Previous day rates used |

### 5.3 Error Handling

| Error Type | Handling | Escalation |
|------------|----------|------------|
| Missing market data | Abort feed | Immediate to Risk Tech |
| Valuation failure | Retry once, then abort | Immediate to Risk Tech |
| Bond lookup failure | Log warning, continue | Daily summary |
| Curve lookup failure | Default to blank/Bond | Daily summary |
| MFT delivery failure | Retry 3 times | After 3rd failure to Ops |

---

## 6. Reporting Requirements

### 6.1 Standard Reports

| Report | Frequency | Audience |
|--------|-----------|----------|
| Feed Completion Status | Daily | Risk Technology |
| Data Quality Summary | Daily | Risk Operations |
| Reconciliation Breaks | Daily | Product Control |
| Sensitivity Summary by Portfolio | Daily | Product Control |

### 6.2 Reconciliation Requirements

| Check | Frequency | Tolerance |
|-------|-----------|-----------|
| Feed vs Murex Totals | Daily | ±$10,000 |
| Record Count | Daily | ±5% |
| Portfolio Coverage | Daily | 100% |

---

## 7. Stakeholders

### 7.1 Business Stakeholders

| Role | Responsibility |
|------|----------------|
| Head of Product Control | Business owner, sign-off |
| Product Control Manager | Daily user, requirements |
| Trading Desk Heads | Data consumer |
| Finance | P&L reporting |

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
| All IR-sensitive trades covered | Product inventory reconciliation |
| Delta Par values correct | Sample validation vs front office |
| Gamma Par values correct | Sample validation vs front office |
| Bond data populated | Field completeness check |
| Regional files generated | File existence check |

### 8.2 Non-Functional Acceptance

| Criteria | Verification Method |
|----------|---------------------|
| Delivery by 05:30 GMT | Timestamp monitoring |
| <0.1% missing records | Completeness report |
| ±0.01% Delta accuracy | Reconciliation report |
| 99.5% availability | Uptime monitoring |

---

## 9. Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Valuation batch delays | High | Medium | Buffer time in schedule |
| Complex STB handling errors | Medium | Medium | Enhanced testing, monitoring |
| Bond data lookup failures | Medium | Low | Default handling, warnings |
| Portfolio filter issues | Medium | High | Standardize to Level 4 nodes |
| Gamma view contention | Low | Low | Separate feeder batches |

---

## 10. Known Issues

### 10.1 Portfolio Filtering

The current portfolio selection mixes Level 4 and Level 5 nodes:
- Some feeders select Level 5 nodes that are the only children of Level 4
- The Bond Notional feeder for London includes extra portfolios (IFXMMLNIC, IFXMMLNLH) no longer used

**Recommendation**: Standardize to Level 4 portfolio nodes only.

### 10.2 HKG Expression Filter

The HKG feeder includes an expression filter to exclude specific SGD/USD cross-currency swaps. These deals may have expired.

**Recommendation**: Review and remove if no longer relevant.

### 10.3 Shared Gamma Simulation View

The IRPV02_GAMMAS view produces both zero and par rate gamma. The PDG extraction must carefully select only par rate outputs.

**Recommendation**: Document clearly in IT Config to prevent extraction errors.

---

## 11. Document Control

### 11.1 Version History

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | 2025-01-03 | Initial version | Risk Technology |

### 11.2 Approval

| Role | Name | Date |
|------|------|------|
| Business Owner | Head of Product Control | |
| Technical Owner | Head of Risk Technology | |
| Approver | Risk Technology Change Board | |

---

*End of Document*
