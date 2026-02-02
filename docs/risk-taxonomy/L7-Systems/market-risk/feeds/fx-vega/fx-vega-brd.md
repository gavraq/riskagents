# FX Vega Sensitivities - Business Requirements Document

**Meridian Global Bank - Market Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | FXV-BRD-001 |
| **Version** | 1.0 |
| **Effective Date** | 13 January 2025 |
| **Owner** | Market Risk Technology |

---

## 1. Executive Summary

### 1.1 Purpose

This Business Requirements Document defines the functional and non-functional requirements for the FX Vega sensitivity feed from Murex to downstream market risk systems. The feed provides foreign exchange volatility risk exposures for non-linear (options) FX products with sensitivities assigned to maturity pillars and strike levels.

### 1.2 Business Context

FX Vega risk is critical for institutions with FX options and exotic derivatives exposure:

- **FX Options Desks**: Volatility exposure management and hedging
- **Exotic Desks**: Quanto products and range accruals risk measurement
- **Risk Management**: Aggregate FX volatility exposure reporting and limits
- **Capital**: FRTB sensitivities-based approach for market risk capital

### 1.3 Scope

| In Scope | Out of Scope |
|----------|--------------|
| FX vega sensitivities | FX delta (linear products) |
| Non-linear FX products | FX gamma |
| Quanto derivatives with FX vega | IR vega on cross-currency products |
| Strike & maturity bucketing | Credit spread vega |
| Trade-level granularity | Commodity vega |
| Regional processing (LN, HK, NY, SP) | Intraday positions |

---

## 2. Business Requirements

### 2.1 Functional Requirements

#### BR-FXV-001: FX Vega Calculation

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-FXV-001 |
| **Title** | FX Vega Calculation |
| **Priority** | Critical |
| **Description** | The system shall calculate FX vega representing the change in market value for a 1% move in FX volatility |
| **Measure Type** | Discounted vega (discounted from settlement date to today) |
| **Currency** | USD equivalent using zero day FX spot rate |
| **Acceptance Criteria** | Vega expressed in USD equivalent |

#### BR-FXV-002: Maturity Pillar Assignment

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-FXV-002 |
| **Title** | Maturity Pillar Bucketing |
| **Priority** | Critical |
| **Description** | The feed shall assign vega sensitivities to standard maturity pillars from the RISK_VIEW4 maturity set |
| **Pillar Set** | O/N, T/N, 1W, 2W, 1M, 2M, 3M, 6M, 9M, 1Y, 18M, 2Y, 3Y, 4Y, 5Y, 6Y, 7Y, 8Y, 9Y, 10Y, 12Y, 15Y, 20Y, 25Y, 30Y, 35Y |
| **Split Mode** | Nearest pillar with distance-weighted split |

#### BR-FXV-003: Strike Level Assignment

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-FXV-003 |
| **Title** | Vega Strike Bucketing |
| **Priority** | Critical |
| **Description** | The feed shall assign vega sensitivities to strike levels on the volatility surface |
| **Strike Levels** | 0, 5, 10, 25, 50 (ATM), 75, 90, 95, 100 delta |
| **Call/Put Classification** | Strike < 50 = Call, Strike = 50 = ATM, Strike > 50 = Put |

#### BR-FXV-004: Product Coverage

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-FXV-004 |
| **Title** | Non-Linear FX Product Coverage |
| **Priority** | Critical |
| **Description** | The feed shall include all non-linear FX products with vega sensitivity |
| **Product Types** | QFX Range Accruals, Quanto Forward Swaps, FX Options |
| **Exclusions** | Linear FX products (covered by FX Delta feed) |

#### BR-FXV-005: Currency Pair Identification

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-FXV-005 |
| **Title** | FX Contract Identification |
| **Priority** | High |
| **Description** | The feed shall identify the underlying FX currency pair using standard quotation modes |
| **Reference** | TBL_FX_CNT_REP for quotation mode lookup |
| **Format** | First currency of default spot quotation (typically USD or JPY) |

#### BR-FXV-006: Instrument Type Mapping

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-FXV-006 |
| **Title** | Instrument Classification |
| **Priority** | High |
| **Description** | The feed shall map Murex instruments to standardized type codes for downstream categorization |
| **Mapping Rules** | QFX Range Accrual → IRD_IRS_RA, Quanto Forward Swap → IRD_IRS_FX |

#### BR-FXV-007: Regional Processing

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-FXV-007 |
| **Title** | Multi-Region Support |
| **Priority** | High |
| **Description** | The feed shall be produced separately for each trading region |
| **Regions** | London (LN), Hong Kong (HK), New York (NY), Sao Paulo (SP) |

### 2.2 Non-Functional Requirements

#### BR-FXV-NFR-001: Timeliness

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-FXV-NFR-001 |
| **Title** | Data Delivery SLA |
| **Priority** | Critical |
| **Description** | Feed must be delivered by 05:30 GMT (T+1) for London region |
| **Measurement** | 95% of deliveries within SLA over rolling 30-day period |

#### BR-FXV-NFR-002: Completeness

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-FXV-NFR-002 |
| **Title** | Data Completeness |
| **Priority** | Critical |
| **Description** | All live FX options positions must have vega values |
| **Tolerance** | <0.1% missing vega records for live trades |

#### BR-FXV-NFR-003: Accuracy

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-FXV-NFR-003 |
| **Title** | Calculation Accuracy |
| **Priority** | Critical |
| **Description** | Vega values must match front office system within tolerance |
| **Tolerance** | ±0.01% for Vega values in USD |

#### BR-FXV-NFR-004: Pillar Coverage

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-FXV-NFR-004 |
| **Title** | Maturity Pillar Completeness |
| **Priority** | High |
| **Description** | All trades with vega sensitivity must be assigned to at least one maturity pillar |
| **Tolerance** | 100% pillar assignment for non-zero vega |

---

## 3. Data Requirements

### 3.1 Input Data

| Source | Data Element | Description |
|--------|--------------|-------------|
| Murex Trade Repository | Trade attributes | Trade number, portfolio, instrument, model |
| Murex Valuation | FX vega values | Strike & maturity based vega per currency pair |
| Market Data | FX volatility surface | For vega calculation |
| Market Data | FX spot rates | For USD equivalent conversion |
| Reference Data | TBL_FX_CNT_REP | FX contract definitions and quotation modes |

### 3.2 Output Data

| Field | Type | Length | Description |
|-------|------|--------|-------------|
| PORTFOLIO | VarChar | 16 | Trading book code |
| TRADE_NUMBER | Numeric | 10 | Trade ID |
| INSTRUMENT | VarChar | 16 | Instrument label |
| INSTRUMENT_TYPE | VarChar | 12 | Standardized type code |
| LEV_QOT | VarChar | 4 | First currency of quotation mode |
| CP | VarChar | 4 | Call/Put/ATM flag |
| PILLAR | VarChar | 64 | Vega maturity pillar |
| ENDDATE | Date | 12 | Vega date |
| VEGASTK | Numeric | 10 | Vega strike |
| VEGA | Numeric | 12 | FX Vega in USD |
| CCY | VarChar | 4 | Currency of vega (USD) |

### 3.3 Data Quality Rules

| Rule ID | Field | Rule | Action |
|---------|-------|------|--------|
| DQ-FXV-001 | TRADE_NUMBER | Must be numeric | Reject |
| DQ-FXV-002 | PORTFOLIO | Must not be null | Reject |
| DQ-FXV-003 | PILLAR | Must be valid pillar from RISK_VIEW4 | Warning |
| DQ-FXV-004 | VEGA | Must be numeric | Reject |
| DQ-FXV-005 | VEGASTK | Must be > 0 | Exclude |
| DQ-FXV-006 | Legal Entity | Must not be SA | Exclude |

---

## 4. Business Rules

### 4.1 Call/Put/ATM Classification

| Rule ID | Condition | Classification |
|---------|-----------|----------------|
| BR-CP-001 | VEGA_STK < 50 | Call |
| BR-CP-002 | VEGA_STK = 50 | ATM |
| BR-CP-003 | VEGA_STK > 50 | Put |

### 4.2 Instrument Type Mapping

| Rule ID | Murex Instrument | Mapped Type |
|---------|------------------|-------------|
| BR-INST-001 | QFX Range Accrua | IRD_IRS_RA |
| BR-INST-002 | Quanto Forward S | IRD_IRS_FX |
| BR-INST-003 | QIR Range Accrua | IRD_IRS_RA |
| BR-INST-004 | Insurance Instru | CRD_CDS_INS |
| BR-INST-005 | Guarantee Instru | CRD_CDS_GUA |
| BR-INST-006 | Other | Empty string |

### 4.3 Maturity Pillar Assignment

| Rule ID | Description | Logic |
|---------|-------------|-------|
| BR-PIL-001 | Standard pillars | Use RISK_VIEW4 maturity set |
| BR-PIL-002 | Split mode | Nearest pillar with distance weighting |
| BR-PIL-003 | Pillar dates | Computed dynamically from reference date |

### 4.4 Transaction Filtering

| Rule ID | Filter | Value |
|---------|--------|-------|
| BR-TXN-001 | Transaction types | Interest rate swaps, Default swaps |
| BR-TXN-002 | Deal status | Not DEAD |
| BR-TXN-003 | Vega maturity | Not NULL |
| BR-TXN-004 | Vega strike | > 0 |

---

## 5. Processing Requirements

### 5.1 Processing Schedule

| Step | Time (GMT) | Description |
|------|------------|-------------|
| 1 | 18:00 | Market data close (London) |
| 2 | 21:00 | Valuation batch complete |
| 3 | 02:00 | FX Vega feeder batch start |
| 4 | 03:30 | Feeder batch complete |
| 5 | 04:00 | Extraction start |
| 6 | 04:30 | File generation |
| 7 | 05:00 | File packaging |
| 8 | 05:30 | MFT delivery |

### 5.2 Dependencies

| Upstream | Dependency Type | Impact if Delayed |
|----------|-----------------|-------------------|
| Market Data | Hard | Feed cannot run |
| Valuation Batch | Hard | Feed cannot run |
| FX Volatility Surface | Hard | Vega calculation fails |
| TBL_FX_CNT_REP | Hard | Quotation mode lookup fails |

---

## 6. Stakeholders

### 6.1 Business Stakeholders

| Role | Responsibility |
|------|----------------|
| Head of FX Options Trading | Business owner |
| FX Vega Risk Manager | Daily user, requirements |
| Exotic Derivatives Desk | Quanto product coverage |
| Risk Management | Aggregate exposure reporting |

### 6.2 Technical Stakeholders

| Role | Responsibility |
|------|----------------|
| Risk Technology Lead | Technical delivery |
| Murex Support Team | Source system support |
| Data Warehouse Team | Target system integration |

---

## 7. Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Strike level granularity | Medium | Low | Validate strike coverage with trading |
| Pillar assignment accuracy | High | Low | Daily reconciliation vs. front office |
| New exotic products | Medium | Medium | Regular product review |
| Portfolio node gaps | Medium | Low | Periodic portfolio coverage audit |

---

## 8. Known Issues

### 8.1 Deprecated Outputs

Two outputs are deprecated in the simulation view:
- FX Default Vega
- FX Vega Without Splitting

### 8.2 Portfolio Node Gap (Hong Kong)

FXHKSBL portfolio node is not included in Hong Kong region. Business rationale to be documented.

### 8.3 Incomplete Breakdown Documentation

Some breakdowns reference IR Sensitivity document for definitions. Cross-reference documentation needed.

### 8.4 Legal Entity Filtering

SA legal entity exclusion logic needs full documentation.

---

*Document Version: 1.0 | Last Updated: 2025-01-13*
