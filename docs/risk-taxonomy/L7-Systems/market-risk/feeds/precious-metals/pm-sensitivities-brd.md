# Precious Metals Sensitivities Feed - Business Requirements Document

**Meridian Global Bank - Market Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | PMS-BRD-001 |
| **Version** | 1.0 |
| **Effective Date** | 13 January 2025 |
| **Owner** | Market Risk Technology |

---

## 1. Business Context

### 1.1 Purpose

This document defines the business requirements for the Precious Metals (PM) Sensitivities Feed, which provides comprehensive commodity risk factor sensitivities for precious metals trading activity.

### 1.2 Business Need

The Market Risk function requires:
- Trade-level precious metals sensitivities for VaR calculation
- Multiple greek measures (delta, gamma, vega, theta, vanna, volga)
- Tenor-bucketed exposures for limit monitoring
- Volatility surface risk distribution for options positions
- Lease rate sensitivity for forward positions
- Time-weighted vega for volatility risk management

### 1.3 Scope

**In Scope**:
- All precious metals trades booked in Murex
- Gold (XAU), Silver (XAG), Platinum (XPT), Palladium (XPD)
- OTC forwards, swaps, options, structured products
- Listed futures and futures options
- All trading regions (LDN, HKG, NYK, SAO)

**Out of Scope**:
- Non-commodity sensitivities (IR, FX) from PM trades (covered in separate feeds)
- Base metals (covered in separate feed)

---

## 2. Business Requirements

### 2.1 Functional Requirements

#### FR-PMS-001: Forward Delta Calculation
**Requirement**: The feed shall provide Forward Delta (Nominal) representing the undiscounted change in value for a $1 move in the forward price.

**Business Rule**:
- Express in both USD and native units (OZ.TR)
- This is an undiscounted measure showing forward value impact
- Note: For listed products (daily margined), no discounting concept applies

**Acceptance Criteria**:
- Nominal (USD) matches Murex Risk Engine output
- Nominal (OZ) correctly expressed in troy ounces

---

#### FR-PMS-002: Forward Delta Adapted Calculation
**Requirement**: The feed shall provide Forward Delta Adapted representing the discounted change in value for a $1 move in the forward price, including volatility smile impact.

**Business Rule**:
- Express in both USD and native units (OZ.TR)
- Include smile impact (change in option value due to volatility change as price moves)
- Discount from settlement date to today
- Use zero-day FX spot rate for currency conversion
- Note: For listed products, Adapted Delta equals Nominal (no discounting)

**Acceptance Criteria**:
- Adapted Delta (USD) matches Murex with Simplified=Off setting
- Smile impact correctly incorporated

---

#### FR-PMS-003: Spot Delta Adapted Calculation
**Requirement**: The feed shall provide Spot Delta Adapted representing the discounted change in value for a $1 move in the spot price, including smile impact.

**Business Rule**:
- Express in both USD and native units (OZ.TR)
- Include smile impact
- Discount from settlement date to today

**Acceptance Criteria**:
- Correctly reflects spot price sensitivity vs forward price sensitivity

---

#### FR-PMS-004: Gamma Calculation
**Requirement**: The feed shall provide Adapted Gamma representing the change in Adapted Delta for a $1 change in forward price.

**Business Rule**:
- Express in native units (OZ)
- This is always a discounted measure (no "simplified" option)
- Include smile impact (second derivative)

**Acceptance Criteria**:
- Gamma values consistent with delta changes across price scenarios

---

#### FR-PMS-005: Vega Calculation
**Requirement**: The feed shall provide Vega representing the change in option value for a 1% move in volatility.

**Business Rule**:
- Express in USD
- Non-adapted vega (standard Black-Scholes style)
- Discount from settlement date to today
- Allocate across both tenor pillars AND delta-based volatility surface

**Acceptance Criteria**:
- Vega bucketed to 7 delta pillars (5, 10, 25, 50, 75, 90, 95)
- Total vega across surface equals trade-level vega

---

#### FR-PMS-006: Weighted Vega Calculation
**Requirement**: The feed shall provide Weighted Vega applying time-based weights to native Vega exposure.

**Business Rule**:
- Weight formula: `SQRT(30 / DaysToMaturity) * Vega`
- 1M tenor (30 days) = baseline weight of 1.0
- Tenors < 1M have weight > 1 (front-end volatilities more volatile)
- Tenors > 1M have weight < 1 (back-end volatilities more stable)

**Weighted Vega Calculation Example**:
| Expiry | Days | Vol Shift | Vega | Weighted Vega |
|--------|------|-----------|------|---------------|
| 1d | 1 | 5.48% | 60 | 329 |
| 1w | 7 | 2.07% | 470 | 973 |
| 2w | 14 | 1.46% | 854 | 1250 |
| 1m | 30 | 1.00% | 1447 | 1447 |
| 2m | 60 | 0.71% | 2140 | 1513 |
| 3m | 91 | 0.57% | 2707 | 1554 |
| 6m | 182 | 0.41% | 3860 | 1567 |
| 9m | 273 | 0.33% | 4750 | 1575 |
| 1y | 365 | 0.29% | 5482 | 1572 |
| 2y | 730 | 0.20% | 7737 | 1568 |

**Acceptance Criteria**:
- Weighted Vega calculation matches formula
- Pillared to same delta surface as native Vega

---

#### FR-PMS-007: Higher-Order Greek Calculations
**Requirement**: The feed shall provide Volga, Vanna, and Theta sensitivities.

**Business Rule**:
- **Volga**: Sensitivity of Vega to volatility (1% vol move)
- **Vanna**: Sensitivity of Delta to volatility (1% vol move)
- **Theta**: Sensitivity of option value to time decay
- All are discounted measures

**Acceptance Criteria**:
- Greeks consistent with Murex Risk Engine outputs

---

#### FR-PMS-008: Lease Rate Risk (Metal DV01)
**Requirement**: The feed shall provide Metal DV01 representing sensitivity to lease rate changes.

**Business Rule**:
- Also known as Phi
- Represents change in P&L for 1bp lease rate shift
- Assume yield curve held constant when shifting lease rates
- Discounted measure

**Acceptance Criteria**:
- Metal DV01 matches Murex Adapted Delta Yield output

---

#### FR-PMS-009: Maturity Pillaring
**Requirement**: All sensitivities shall be bucketed to standardized maturity pillars.

**Business Rule**:
- Use PM RISK maturity set
- Pillars: TODAY, TOM, SPOT, 1W, 1M, 2M, 3M, 4M, 5M, 6M, 9M, 1Y, 18M, 2Y, 3Y, 4Y, 5Y, 10Y
- Split mode: Surrounding pillars (fractional allocation)
- Non-native pillaring used (from today, not from spot)

**Acceptance Criteria**:
- Sum of pillared sensitivities equals total trade sensitivity
- Consistent with downstream aggregation requirements

---

#### FR-PMS-010: Volatility Surface Pillaring
**Requirement**: Vega and Weighted Vega shall be pillared across the delta-based volatility surface.

**Business Rule**:
- Delta pillars: 5, 10, 25, 50, 75, 90, 95
- Allocate to ALL surface points (hypothetical distribution)
- Not just adjacent delta pillars

**Acceptance Criteria**:
- VEGASTK field populated for Vega and Weighted Vega records
- Sum across delta pillars equals total vega

---

#### FR-PMS-011: Product Scope Filtering
**Requirement**: The feed shall include only trades with Precious typology.

**Business Rule**:
- Filter by typology category = 'PRECIOUS'
- Exclude IR and FX portfolio nodes
- Include all precious metals: Gold, Silver, Platinum, Palladium

**Acceptance Criteria**:
- No base metals included
- All PM typologies captured

---

#### FR-PMS-012: Static Data Attributes
**Requirement**: The feed shall include trade-level static data for downstream aggregation.

**Required Attributes**:
| Attribute | Purpose |
|-----------|---------|
| M_METAL | Precious metal ISO code (XAU, XAG, etc.) |
| M_LOCATION | Commodity location |
| M_INDEX | Underlying commodity index |
| M_LEADING_C | Leading curve for risk aggregation |
| M_CALL_PUT | Option type (Call/Put) |
| M_STRIKE | Option strike price |
| M_TYPOLOGY | Trade typology |
| DELIVERY_TYPE | Physical vs cash delivery |
| PKG_NB | Package reference number |
| PKG_TYPOLOGY | Package typology |

**Acceptance Criteria**:
- All static attributes populated where applicable
- Enable downstream slicing and aggregation

---

### 2.2 Non-Functional Requirements

#### NFR-PMS-001: Timeliness
**Requirement**: Feed must be available within 3 hours of EOD batch completion.

#### NFR-PMS-002: Completeness
**Requirement**: 100% of precious metals trades in scope must be included.

#### NFR-PMS-003: Accuracy
**Requirement**: Sensitivity values must reconcile to Murex Risk Engine within $1,000 tolerance at portfolio level.

#### NFR-PMS-004: Traceability
**Requirement**: Each record must be traceable to source trade via M_TRADE_NUM.

---

## 3. Business Rules Summary

### 3.1 Discounting Rules

| Sensitivity | Discounted | Note |
|-------------|------------|------|
| Nominal (Forward Delta) | No | Forward value |
| Adapted Delta | Yes | Settlement to today |
| Adapted Spot Delta | Yes | Settlement to today |
| Adapted Gamma | Yes | Always discounted |
| Vega | Yes | Settlement to today |
| Weighted Vega | Yes | Derived from Vega |
| Volga | Yes | Settlement to today |
| Vanna | Yes | Settlement to today |
| Theta | Yes | Settlement to today |
| Metal DV01 | Yes | Settlement to today |

### 3.2 Smile Inclusion

| Sensitivity | Includes Smile |
|-------------|----------------|
| Nominal (Forward Delta) | No |
| Adapted Delta | Yes |
| Adapted Spot Delta | Yes |
| Adapted Gamma | Yes |
| Vega | No (standard) |

### 3.3 Currency Conversion
- All USD conversions use zero-day FX spot rate
- Native unit (OZ.TR) outputs also provided for delta measures

---

## 4. Data Consumers

| Consumer | Usage |
|----------|-------|
| Plato | Risk aggregation and reporting |
| VESPA (via RDS) | VaR calculation |
| Limit System | PM position monitoring |
| Risk Control | Daily risk reports |
| Front Office | P&L attribution |

---

## 5. Assumptions and Dependencies

### 5.1 Assumptions
- Murex valuation batch completes successfully before feed generation
- Market data (commodity curves, volatility surfaces) is available
- Typology configuration correctly categorizes all PM products

### 5.2 Dependencies
- Murex Risk Engine batch completion
- Market data set availability (LNCLOSE, HKCLOSE, etc.)
- SB_TYPOLOGY_REP reference data
- TBL_FX_CNT_REP for currency conversion

---

## 6. Change History

| Version | Date | Author | Change Description |
|---------|------|--------|-------------------|
| 1.0 | 2025-01-13 | Risk Technology | Initial document |

---

*Document Version: 1.0 | Last Updated: 2025-01-13*
