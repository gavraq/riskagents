# Stress Testing Feed - Business Requirements Document

**Meridian Global Bank - Market Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | ST-BRD-001 |
| **Version** | 1.0 |
| **Effective Date** | 13 January 2025 |
| **Owner** | Market Risk Technology |

---

## 1. Business Context

### 1.1 Purpose

This document defines the business requirements for the Stress Testing Feed, which provides scenario-based P&L results for all trading positions under pre-defined hypothetical stress scenarios. Unlike VaR which uses historical scenarios, Stress Testing applies extreme but plausible market shocks to assess portfolio vulnerability.

### 1.2 Business Need

The Market Risk function requires:
- Market risk stress results for all risk factors based on pre-defined hypothetical shocks
- P&L vectors for stress scenario aggregation in VESPA
- Risk class decomposition for stress attribution analysis
- Static data enrichment for downstream reporting and aggregation
- Support for both historical event scenarios (e.g., 9/11) and hypothetical shocks

### 1.3 Scope

**In Scope**:
- All trades booked in Murex across VaR portfolios
- Pre-defined hypothetical stress scenarios
- Eight risk classes for stress decomposition
- Four reporting regions: London, New York, Hong Kong, São Paulo
- Static data enrichment (counterparty, security, issuer information)

**Out of Scope**:
- Stress scenario generation (performed in FMDM/Xenomorph)
- Stress aggregation and limit calculation (performed in VESPA)
- Reverse stress testing
- Intraday stress calculations

---

## 2. Business Requirements

### 2.1 Functional Requirements

#### FR-ST-001: Hypothetical Stress Scenario Application
**Requirement**: The feed shall apply pre-defined hypothetical stress scenarios to current positions.

**Business Rule**:
- Apply pre-defined market data shifts representing extreme scenarios
- Scenarios include both historical events (e.g., 9/11) and hypothetical shocks
- Market parameter variations built outside Murex (FMDM, Xenomorph)
- Import via Market Risk Single Reports

**Acceptance Criteria**:
- All defined stress scenarios applied to positions
- P&L results available for each scenario

---

#### FR-ST-002: Full Revaluation Methodology
**Requirement**: The feed shall use full revaluation methodology to generate stress P&L results.

**Business Rule**:
- Apply stress scenario shifts to current market data
- Perform full repricing of deals for each scenario
- Use aggregated positions (consolidated mode) for performance
- Convert P&L to USD using perturbed FX spots from each scenario

**Acceptance Criteria**:
- Stress results reflect full revaluation impact
- Each scenario produces complete position revaluation

---

#### FR-ST-003: Risk Factor Coverage - Standard Factors
**Requirement**: The feed shall cover all standard risk factors for comprehensive stress testing.

**Business Rule**:
Risk factors to include:

| Risk Factor | Variation Type |
|-------------|----------------|
| Cap Floors Volatility | Absolute |
| Commodity Market Rates | Percentage (futures/spot), Absolute (lease) |
| Commodity Smile | Percentage |
| Credit Market Rates | Percentage/Absolute |
| FX Volatility | Absolute (ATM only) |
| FX Spot | Percentage |
| Rates Curves Zero Coupons | Absolute/Percentage |
| Security Spot | Percentage |
| Security Volatility | Absolute |
| Swaption Volatility | Absolute |

**Acceptance Criteria**:
- All standard risk factors shocked according to scenario definitions
- Variation types correctly applied

---

#### FR-ST-004: Risk Factor Coverage - Stress-Specific Factors
**Requirement**: The feed shall include stress-specific risk factors not used in VaR.

**Business Rule**:
Additional stress-specific risk factors:

| Risk Factor | Description | Variation Type |
|-------------|-------------|----------------|
| Bond Adjustment Spread | Spread on rate curve for bond pricing | Absolute |
| Recovery Rates | Recovery percentage in default | Percentage |

**Note**: FX Volatility shocks ATM only (vs full smile in VaR)

**Acceptance Criteria**:
- Bond Adjustment Spread correctly applied to bond positions
- Recovery Rate shocks correctly applied to credit positions
- FX Volatility limited to ATM (no smile impact)

---

#### FR-ST-005: Risk Class Decomposition
**Requirement**: The feed shall provide P&L results decomposed by risk class.

**Business Rule**:
Generate separate P&L vectors for:

| Type | Risk Class | Risk Factors |
|------|------------|--------------|
| Non-Diversified | StrCommodity | Commodity market rates, Commodity Smile |
| Non-Diversified | RR | Recovery Rates |
| Non-Diversified | BCS | Bond credit spread |
| Non-Diversified | GenFX | FX Spot, FX Volatility, FX Smile |
| Non-Diversified | GenIR | Security Volatility, Zero coupons, Swaption Vol, Cap Floors Vol |
| Non-Diversified | CRD | CRD Market Rates, Credit Volatility |
| Diversified | TotalStr | All except Security Spot, Bond spread, CRD, Recovery |
| Diversified | TotalStrCRD | All risk factors |

**Acceptance Criteria**:
- 8 risk class files generated per region
- Non-diversified partials enable stress attribution
- TotalStr and TotalStrCRD enable diversified stress calculation

---

#### FR-ST-006: Static Data Enrichment
**Requirement**: The feed shall include trade-level static data for downstream aggregation.

**Business Rule**:
Required static data attributes:

| Attribute | Source | Purpose |
|-----------|--------|---------|
| Portfolio | MRA_EXPORT | Desk/book identification |
| Currency | MRA_EXPORT | Trade currency |
| Family/Group/Type | MRA_EXPORT | Product classification |
| PL Instrument | MRA_EXPORT | Instrument identification |
| Risk Section | MRA_EXPORT | Risk categorization |
| CIF ID | MRA_EXPORT (UDF) | Counterparty identifier |
| GLOBUS ID | MRA_EXPORT | Issuer identifier |
| Issuer | MRA_EXPORT/SB_CP_REP | Issuer name |
| Country | MRA_EXPORT/SB_CP_REP | Counterparty country |
| ISIN | MRA_EXPORT/SB_SE_HEAD_REP | Security identifier |

**Acceptance Criteria**:
- All static attributes populated where applicable
- Joins to SB_SE_HEAD_REP and SB_CP_REP for SCF enrichment
- Enable downstream slicing by counterparty, country, issuer

---

#### FR-ST-007: Scenario Weighting
**Requirement**: All stress scenarios shall have equal weight.

**Business Rule**:
- No decay weighting applied to scenarios
- All scenarios treated equally
- Consistent with pre-defined shock methodology

**Acceptance Criteria**:
- Equal weights confirmed in output files

---

#### FR-ST-008: Zero Coupon Propagation
**Requirement**: Zero coupon shifts shall be applied without propagation.

**Business Rule**:
- No propagation between curves or through shared instruments
- Linear interpolation between surrounding shifts
- Flat extrapolation before first and after last shift

**Acceptance Criteria**:
- Rate/rate, Rate/Credit, Rate/FX propagation disabled
- Interpolation method documented and consistent

---

#### FR-ST-009: Market Data Flooring
**Requirement**: Risk factors shall be floored to prevent unrealistic values.

**Business Rule**:
- Volatilities already floored to 0 in FO module
- User-defined floors for zero coupon curves (e.g., -0.5 for some curves)
- Floors for commodity market rates (e.g., -5 for precious metals)
- Floors defined in ST_FullRevalOutput template

**Acceptance Criteria**:
- No unrealistic negative values in shocked data
- Floors applied per curve/commodity configuration

---

#### FR-ST-010: Central Point Definition
**Requirement**: The feed shall use Murex P&L as the central point for stress calculation.

**Business Rule**:
- Central point = Market Value + Past Cash + Future Cash
- Calculated using Murex pricing models or Flex API
- Stress P&L = Scenario P&L - Central Point

**Acceptance Criteria**:
- RESULT field contains scenario P&L
- RESULTV field contains difference from central point

---

#### FR-ST-011: Trade Scope
**Requirement**: The feed shall include all trades in VaR portfolios without additional filtering.

**Business Rule**:
- Use same combined portfolios as VaR (VAR_LDN, VAR_HKG, VAR_NYK, VAR_SAO)
- No filter on typology, P&L instruments, or usage
- All trades in combined portfolios included

**Acceptance Criteria**:
- 100% of trades in VaR portfolios included in stress results
- No trade exclusions based on product type

---

### 2.2 Non-Functional Requirements

#### NFR-ST-001: Timeliness
**Requirement**: Stress results must be available within the EOD batch window.

#### NFR-ST-002: Completeness
**Requirement**: 100% of trades in VaR portfolios must be included.

#### NFR-ST-003: Accuracy
**Requirement**: Stress results must reconcile to Murex Risk Engine within tolerance.

#### NFR-ST-004: Data Quality
**Requirement**: Static data enrichment must correctly link to reference data.

---

## 3. Business Rules Summary

### 3.1 Stress vs VaR Risk Factor Differences

| Risk Factor | VaR | Stress |
|-------------|-----|--------|
| FX Volatility | Full smile | ATM only |
| Bond Adjustment Spread | Not included | Included |
| Recovery Rates | Not included | Included |

### 3.2 Revaluation Settings (ST_RevalSetting)

| Setting | Value |
|---------|-------|
| Discounting | On |
| Financing | Off |
| P&L Display | Aggregated |
| P&L Breakdown | Redefined to Aggregated |
| FX Spot Conversion | Discounted |
| Brokerage Fees | Off |
| Revaluation Mode | Consolidated |

### 3.3 Volatility Smile Mode

| Scenario Type | Smile Mode |
|---------------|------------|
| Commodity Smile | Absolute |

---

## 4. Data Consumers

| Consumer | Usage |
|----------|-------|
| VESPA | Stress aggregation across hierarchies |
| Risk Control | Daily stress monitoring and reporting |
| Regulatory Reporting | Stress testing submissions |
| Risk Committee | Board-level stress reports |
| Front Office | Desk-level stress analysis |

---

## 5. Assumptions and Dependencies

### 5.1 Assumptions
- Stress scenarios are generated and maintained by FMDM/Xenomorph
- All trades in VaR portfolios are correctly booked and valued
- Static data tables (SB_SE_HEAD_REP, SB_CP_REP) are current
- Scenario definitions are approved by Market Risk management

### 5.2 Dependencies
- FMDM/Xenomorph scenario generation
- Market data scenario containers populated
- Murex valuation batch completion
- VESPA availability for downstream aggregation
- Reference data availability (security, counterparty)

---

## 6. Change History

| Version | Date | Author | Change Description |
|---------|------|--------|-------------------|
| 1.0 | 2025-01-13 | Risk Technology | Initial document |

---

*Document Version: 1.0 | Last Updated: 2025-01-13*
