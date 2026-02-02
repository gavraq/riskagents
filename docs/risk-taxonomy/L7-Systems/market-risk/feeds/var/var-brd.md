# Value at Risk (VaR) P&L Strips Feed - Business Requirements Document

**Meridian Global Bank - Market Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | VAR-BRD-001 |
| **Version** | 1.0 |
| **Effective Date** | 13 January 2025 |
| **Owner** | Market Risk Technology |

---

## 1. Business Context

### 1.1 Purpose

This document defines the business requirements for the Value at Risk (VaR) P&L Strips Feed, which provides historical scenario-based P&L vectors for all trading positions. Unlike sensitivity feeds that measure exposure to risk factors, VaR feeds capture the full revaluation impact of applying historical market movements to current positions.

### 1.2 Business Need

The Market Risk function requires:
- Market risk P&L strips for all risk factors based on historical scenarios
- P&L vectors for Value at Risk calculations in VESPA
- Risk class decomposition for non-diversified VaR reporting
- Multiple holding periods (1-day, 10-day) for regulatory and internal purposes
- Stressed VaR (SVaR) for regulatory capital calculations
- Extended Stressed VaR (ESVaR) for stress period identification

### 1.3 Scope

**In Scope**:
- All trades booked in Murex across VaR portfolios
- Four VaR calculation types: 1D VaR, 10D VaR, 10D SVaR, 10D ESVaR
- Ten risk classes for VaR decomposition
- Four reporting regions: London, Hong Kong, New York, São Paulo

**Out of Scope**:
- VaR calculation (percentile cut-offs performed in VESPA)
- Scenario generation (performed in FMDM/Asset Control)
- Proxying (performed in FMDM prior to Murex)

---

## 2. Business Requirements

### 2.1 Functional Requirements

#### FR-VAR-001: Historical Simulation VaR Methodology
**Requirement**: The feed shall use full revaluation methodology to generate P&L strips based on historical scenarios.

**Business Rule**:
- Apply historical market data shifts to current positions
- Perform full repricing of deals for each scenario
- Use aggregated positions (consolidated mode) for performance
- Convert P&L to USD using perturbed FX spots from each scenario

**Acceptance Criteria**:
- P&L strips reflect full revaluation impact, not delta approximation
- Each scenario produces a complete position revaluation

---

#### FR-VAR-002: 1-Day VaR P&L Strips
**Requirement**: The feed shall provide P&L strips for 1-day holding period VaR.

**Business Rule**:
- Use rolling 1-year observation period (250 scenarios)
- Apply 1-day market variations
- Use overlapping scenario periods
- No time scaling applied

**Acceptance Criteria**:
- 250 scenarios generated per business day
- P&L strips available for all 10 risk classes

---

#### FR-VAR-003: 10-Day VaR P&L Strips
**Requirement**: The feed shall provide P&L strips for 10-day holding period VaR.

**Business Rule**:
- Use rolling 1-year observation period (250 scenarios)
- Apply actual 10-day market variations (no square root scaling)
- Use overlapping scenario periods

**Acceptance Criteria**:
- 250 scenarios with 10-day holding period
- Suitable for regulatory capital calculations

---

#### FR-VAR-004: 10-Day Stressed VaR (SVaR) P&L Strips
**Requirement**: The feed shall provide P&L strips for Stressed VaR calculations.

**Business Rule**:
- Use fixed 1-year stress period (250 scenarios)
- Stress period selected as worst 1-year period since January 2007
- Apply 10-day holding period variations
- Stress period determined by ESVaR analysis

**Acceptance Criteria**:
- 250 scenarios from identified stress period
- Stress period dates documented and justified

---

#### FR-VAR-005: 10-Day Extended Stressed VaR (ESVaR) P&L Strips
**Requirement**: The feed shall provide P&L strips for stress period identification.

**Business Rule**:
- Observation period from 2 January 2007 to current date
- Continuously growing scenario set
- Apply 10-day holding period variations
- Run weekly to identify worst 1-year period for SVaR

**Acceptance Criteria**:
- Complete historical coverage since 2007
- Enables identification of stress period for SVaR

---

#### FR-VAR-006: Risk Factor Coverage
**Requirement**: The feed shall cover all relevant risk factors for comprehensive VaR.

**Business Rule**:
Risk factors to include:

| Risk Factor | Variation Type |
|-------------|----------------|
| Cap Floors Volatility | Percentage |
| Commodity Market Rates | Percentage (futures/spot), Absolute (lease) |
| Commodity Smile | Percentage |
| Credit Market Rates | Absolute |
| FX Smile | Percentage |
| FX Spot | Percentage |
| Rates Curves Zero Coupons | Absolute |
| Security Spot | Absolute |
| Security Volatility | Percentage |
| Swaption Volatility | Percentage |

**Acceptance Criteria**:
- All risk factors shocked according to specified variation type
- Complete coverage of trading book risk exposures

---

#### FR-VAR-007: Risk Class Decomposition
**Requirement**: The feed shall provide P&L strips decomposed by risk class.

**Business Rule**:
Generate separate P&L vectors for:

| Type | Risk Class | Risk Factors | VaR/SVaR | ESVaR |
|------|------------|--------------|----------|-------|
| Non-Diversified | Commodities | Commodity market rates, Commodity Smile | ✓ | |
| Non-Diversified | FX | FX Spot | ✓ | |
| Non-Diversified | FXVol | FX Volatility*, FX Smile | ✓ | |
| Non-Diversified | GenFX | FX Spot, FX Volatility*, FX Smile | ✓ | ✓ |
| Non-Diversified | GenIR | Security Volatility, Zero coupons, Swaption Vol, Cap Floors Vol | ✓ | ✓ |
| Non-Diversified | IR | Zero coupons | ✓ | |
| Non-Diversified | IRVol | Security Volatility, Swaption Vol, Cap Floors Vol | ✓ | |
| Non-Diversified | CRD | CRD Market Rates, Security Spot (TotalCRD - Total) | ✓ | |
| Diversified | Total | All factors except Security Spot & CRD | ✓ | ✓ |
| Diversified | TotalCRD | All risk factors | ✓ | ✓ |

*FX volatility selected but no perturbations generated

**Acceptance Criteria**:
- 10 risk class files generated per VaR type
- Non-diversified VaR partials enable risk decomposition
- Total and TotalCRD enable diversified VaR calculation

---

#### FR-VAR-008: Scenario Weighting
**Requirement**: All scenarios shall have equal weight in VaR calculation.

**Business Rule**:
- No decay weighting applied to historical scenarios
- Most recent 250 scenarios treated equally
- Consistent with regulatory requirements

**Acceptance Criteria**:
- Equal weights confirmed in VESPA VaR calculation

---

#### FR-VAR-009: Zero Coupon Propagation
**Requirement**: Zero coupon shifts shall be applied without propagation.

**Business Rule**:
- No propagation between curves or through shared instruments
- Linear interpolation between surrounding shifts
- Flat extrapolation before first and after last shift

**Acceptance Criteria**:
- Rate/rate, Rate/Credit, Rate/FX propagation disabled
- Interpolation method documented and consistent

---

#### FR-VAR-010: Market Data Flooring
**Requirement**: Risk factors shall be floored to prevent negative values where appropriate.

**Business Rule**:
- Volatilities already floored to 0 in FO module
- User-defined floors for zero coupon curves
- Floors defined in VAR_FullRevalOutput template

**Acceptance Criteria**:
- No negative volatilities in shocked data
- Zero coupon floors applied per curve configuration

---

#### FR-VAR-011: Open Days Calendar
**Requirement**: Scenarios shall be generated only for open business days.

**Business Rule**:
- Use VAR_SCN calendar for scenario generation
- Exclude weekends
- Exclude 1st January (except 2008, 2009, 2010, 2013)
- Align with Asset Control and Xenomorph time series

**Acceptance Criteria**:
- No scenarios for non-business days
- Calendar aligned with market data sources

---

### 2.2 Non-Functional Requirements

#### NFR-VAR-001: Timeliness
**Requirement**: VaR P&L strips must be available within the EOD batch window.

#### NFR-VAR-002: Completeness
**Requirement**: 100% of trades in VaR portfolios must be included.

#### NFR-VAR-003: Accuracy
**Requirement**: P&L strips must reconcile to Murex Risk Engine within tolerance.

#### NFR-VAR-004: Scalability
**Requirement**: Feed must handle ESVaR's growing scenario count (since 2007).

---

## 3. Business Rules Summary

### 3.1 VaR Methodology Parameters

| Parameter | Configuration |
|-----------|---------------|
| Revaluation Method | Full Revaluation |
| Holding Periods | 1 day, 10 days (overlapping) |
| Observation Period | 250 scenarios (1 year rolling) |
| Confidence Level | 99% (applied in VESPA) |
| Scenario Weighting | Equal weights |
| Time Scaling | None (actual 10-day variation) |
| Aggregation Currency | USD |

### 3.2 Revaluation Settings (VAR_RevalSetting)

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
| FX Smile | Absolute |
| Commodity Smile | Absolute |
| Cap Floor Smile | Spread |
| Swaption Smile | Spread |

---

## 4. Data Consumers

| Consumer | Usage |
|----------|-------|
| VESPA | VaR calculation via percentile cut-offs |
| Risk Control | Daily VaR monitoring and reporting |
| Regulatory Reporting | Market risk capital calculations |
| Back-Testing | VaR model validation |

---

## 5. Assumptions and Dependencies

### 5.1 Assumptions
- Historical scenarios are generated by FMDM/Asset Control/Xenomorph
- Proxying is performed upstream before scenarios reach Murex
- All trades in VaR portfolios are correctly booked and valued

### 5.2 Dependencies
- Market data scenario containers populated from external sources
- Murex valuation batch completion
- VESPA availability for downstream VaR calculation

---

## 6. Change History

| Version | Date | Author | Change Description |
|---------|------|--------|-------------------|
| 1.0 | 2025-01-13 | Risk Technology | Initial document |

---

*Document Version: 1.0 | Last Updated: 2025-01-13*
