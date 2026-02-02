---
# Data Dictionary Metadata
document_id: MR-L7-002
document_name: Market Risk Data Dictionary
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Head of Market Risk
approving_committee: MLRC

# Taxonomy Linkages
parent_architecture: MR-L7-001  # System Architecture
l1_requirements:
  - REQ-L1-002  # BCBS239 (Data Aggregation)
  - REQ-L1-001  # CRR
l2_risk_types:
  - MR-L2-001   # Market Risk
l3_governance:
  - MR-L3-001   # Market Risk Policy
  - MR-L3-003   # VaR Limit Framework
l4_processes:
  - MR-L4-006   # Risk Engine Calculation
  - MR-L4-007   # Market Risk Reporting & Sign-off
l5_controls:
  - MR-L5-001   # VaR Limits Controls
  - MR-L5-002   # Stress Limits Controls
  - MR-L5-003   # Sensitivity Limits Controls
l6_models:
  - MR-L6-001   # VaR/SVaR Methodology
  - MR-L6-002   # ECAP Methodology
---

# Market Risk Data Dictionary

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Document ID** | MR-L7-002 |
| **Version** | 1.0 |
| **Effective Date** | 02 January 2026 |
| **Parent Document** | System Architecture (MR-L7-001) |
| **Owner** | Head of Market Risk |

---

## 1. Purpose

This Data Dictionary defines all data elements, metrics, and attributes used within the Market Risk function at Meridian Global Bank. It serves as:

1. **Single Source of Truth**: Authoritative definitions for all Market Risk data elements
2. **BCBS239 Compliance**: Supports data governance, lineage, and quality requirements
3. **Integration Reference**: Common terminology across source systems, risk engines, and reporting
4. **AI/Agent Context**: Enables precise data element identification in agent queries

---

## 2. Data Categories Overview

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        MARKET RISK DATA TAXONOMY                                        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐ │
│   │  STATIC DATA    │   │  MARKET DATA    │   │  POSITION DATA  │   │  SENSITIVITIES  │ │
│   │                 │   │                 │   │                 │   │  (Greeks)       │ │
│   │ • Book hierarchy│   │ • Spot rates    │   │ • Trade data    │   │ • DV01 / CS01   │ │
│   │ • Counterparty  │   │ • Curves        │   │ • Notionals     │   │ • Delta / Gamma │ │
│   │ • Instruments   │   │ • Surfaces      │   │ • Market values │   │ • Vega / Theta  │ │
│   │ • Product maps  │   │ • Fixings       │   │ • Accruals      │   │ • Rho / Correl  │ │
│   │ • L-bands       │   │ • Time series   │   │ • Clean/Dirty   │   │ • JTD           │ │
│   └─────────────────┘   └─────────────────┘   └─────────────────┘   └─────────────────┘ │
│           │                     │                     │                     │           │
│           └─────────────────────┴──────────┬──────────┴─────────────────────┘           │
│                                            │                                            │
│                                            ▼                                            │
│   ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│   │                           AGGREGATED RISK METRICS                               │   │
│   │  • VaR / SVaR    • Stress P&L    • IRC / RNIV    • ECAP / EaR    • Component VaR│   │
│   └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                            │                                            │
│           ┌─────────────────────┬──────────┴──────────┬─────────────────────┐           │
│           │                     │                     │                     │           │
│           ▼                     ▼                     ▼                     ▼           │
│   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐ │
│   │  CAPITAL        │   │  P&L            │   │  LIMITS         │   │  CONTROLS       │ │
│   │                 │   │                 │   │                 │   │                 │ │
│   │ • IMA Capital   │   │ • Actual P&L    │   │ • VaR limits    │   │ • Backtesting   │ │
│   │ • FRTB Capital  │   │ • Hypothetical  │   │ • Stress limits │   │ • Exceptions    │ │
│   │ • RWA           │   │ • Attribution   │   │ • Sensitivity   │   │ • Traffic light │ │
│   │ • Pillar 2      │   │ • Clean P&L     │   │ • Concentration │   │ • DQ metrics    │ │
│   └─────────────────┘   └─────────────────┘   └─────────────────┘   └─────────────────┘ │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

**Note on Sensitivities (Greeks)**: Sensitivities are calculated at the **position/trade level** by the trading system (Murex) and then **aggregated** to desk, business unit, and entity levels for risk management. The same metrics serve dual purposes:
- **Trading**: Position-level Greeks for hedging and P&L attribution
- **Risk Management**: Aggregated sensitivities for limit monitoring and risk reporting

---

## 3. Static Data

### 3.1 Book Hierarchy

| Field | Definition | Data Type | Source System | Example |
|-------|------------|-----------|---------------|---------|
| **book_id** | Unique identifier for trading book | VARCHAR(20) | Bookman | `BK-MR-001` |
| **book_name** | Display name for trading book | VARCHAR(100) | Bookman | `G10 Rates Swaps` |
| **desk_id** | Parent desk identifier | VARCHAR(20) | Bookman | `DESK-RATES-01` |
| **desk_name** | Display name for trading desk | VARCHAR(100) | Bookman | `Rates - G10 Swaps` |
| **business_unit_id** | Parent business unit identifier | VARCHAR(20) | Bookman | `BU-RATES` |
| **business_unit_name** | Business unit name | VARCHAR(100) | Bookman | `Rates Trading` |
| **division_id** | Parent division identifier | VARCHAR(20) | Bookman | `DIV-MARKETS` |
| **division_name** | Division name | VARCHAR(100) | Bookman | `Markets` |
| **entity_id** | Legal entity identifier | VARCHAR(20) | Bookman | `MGB` |
| **var_risk_required** | Flag indicating book inclusion in VaR | BOOLEAN | Bookman | `TRUE` |
| **regulatory_var_flag** | Flag for IMA regulatory VaR inclusion | BOOLEAN | Bookman | `TRUE` |
| **trading_book_flag** | Trading book vs banking book | ENUM | Bookman | `TB` / `BB` |

**Source Process**: [Hierarchy Management (FIN-L4-001)](../../L4-Processes/processes/hierarchy-management.md)

### 3.2 Counterparty / Party Data

| Field | Definition | Data Type | Source System | Example |
|-------|------------|-----------|---------------|---------|
| **party_id** | Unique counterparty identifier | VARCHAR(20) | EDM | `CP-001234` |
| **party_name** | Legal name of counterparty | VARCHAR(200) | EDM | `ABC Investment Corp` |
| **party_type** | Classification of counterparty | ENUM | EDM | `CORPORATE`, `BANK`, `SOVEREIGN` |
| **country_code** | Country of domicile (ISO 3166) | CHAR(2) | EDM | `US` |
| **industry_code** | Industry classification (GICS) | VARCHAR(10) | EDM | `40101010` |
| **credit_rating_external** | External credit rating | VARCHAR(10) | FMDM | `A-` |
| **credit_rating_internal** | Internal credit rating | VARCHAR(10) | CRS | `A2` |

### 3.3 Instrument / Security Master

| Field | Definition | Data Type | Source System | Example |
|-------|------------|-----------|---------------|---------|
| **instrument_id** | Unique instrument identifier | VARCHAR(30) | FMDM | `INST-001234` |
| **isin** | International Securities ID Number | CHAR(12) | FMDM | `US0378331005` |
| **cusip** | CUSIP identifier | CHAR(9) | FMDM | `037833100` |
| **sedol** | SEDOL identifier | CHAR(7) | FMDM | `2046251` |
| **instrument_type** | Product classification | ENUM | FMDM | `BOND`, `SWAP`, `OPTION` |
| **currency** | Base currency (ISO 4217) | CHAR(3) | FMDM | `USD` |
| **maturity_date** | Final maturity date | DATE | FMDM | `2030-06-15` |
| **issuer_id** | Link to party master | VARCHAR(20) | FMDM | `CP-001234` |

### 3.4 L-Band Ratings (Liquidity Assessment)

| Field | Definition | Data Type | Source System | Example |
|-------|------------|-----------|---------------|---------|
| **instrument_id** | Reference to instrument | VARCHAR(30) | FMDM | `INST-001234` |
| **l_band** | Liquidity band classification | ENUM(L1-L6) | Market Risk | `L2` |
| **l_band_date** | Date of L-band assessment | DATE | Market Risk | `2025-01-02` |
| **liquidity_horizon_days** | Assumed liquidation period | INTEGER | Market Risk | `10` |

**L-Band Definitions**:
| L-Band | Description | Liquidity Horizon | Haircut Range |
|--------|-------------|-------------------|---------------|
| **L1** | Highly Liquid (G10 govt, major indices) | 1-2 days | 0-2% |
| **L2** | Liquid (IG corporates, liquid FX) | 5-10 days | 2-5% |
| **L3** | Moderately Liquid (HY, small cap) | 10-20 days | 5-10% |
| **L4** | Less Liquid (EM, structured) | 20-40 days | 10-20% |
| **L5** | Illiquid (distressed, bespoke) | 40-60 days | 20-40% |
| **L6** | Highly Illiquid (no market) | 60+ days | 40%+ |

---

## 4. Market Data

### 4.1 Spot Rates

| Field | Definition | Data Type | Source System | Example |
|-------|------------|-----------|---------------|---------|
| **rate_id** | Unique rate identifier | VARCHAR(30) | FMDM | `FX-EURUSD-SPOT` |
| **rate_type** | Classification of rate | ENUM | FMDM | `FX_SPOT`, `EQUITY_PRICE`, `COMMODITY_SPOT` |
| **rate_value** | Observed rate value | DECIMAL(18,8) | FMDM | `1.08523` |
| **rate_date** | Observation date | DATE | FMDM | `2025-01-02` |
| **rate_time** | Observation timestamp | TIMESTAMP | FMDM | `17:00:00 GMT` |
| **source** | Data source | ENUM | FMDM | `BLOOMBERG`, `REUTERS`, `INTERNAL` |

### 4.2 Yield Curves

| Field | Definition | Data Type | Source System | Example |
|-------|------------|-----------|---------------|---------|
| **curve_id** | Unique curve identifier | VARCHAR(50) | FMDM | `USD-SOFR-OIS` |
| **curve_name** | Display name | VARCHAR(100) | FMDM | `USD SOFR OIS Curve` |
| **curve_type** | Classification | ENUM | FMDM | `OIS`, `LIBOR`, `GOVT`, `CREDIT` |
| **currency** | Curve currency | CHAR(3) | FMDM | `USD` |
| **tenor** | Tenor point | VARCHAR(10) | FMDM | `5Y` |
| **tenor_days** | Tenor in days | INTEGER | FMDM | `1826` |
| **zero_rate** | Zero coupon rate | DECIMAL(10,6) | FMDM | `0.0425` |
| **discount_factor** | Discount factor | DECIMAL(18,10) | FMDM | `0.8127543` |
| **curve_date** | Observation date | DATE | FMDM | `2025-01-02` |

### 4.3 Volatility Surfaces

| Field | Definition | Data Type | Source System | Example |
|-------|------------|-----------|---------------|---------|
| **surface_id** | Unique surface identifier | VARCHAR(50) | FMDM | `EURUSD-VOL` |
| **underlying** | Underlying asset | VARCHAR(30) | FMDM | `EURUSD` |
| **surface_type** | Classification | ENUM | FMDM | `FX_VOL`, `IR_SWAPTION`, `EQUITY_VOL` |
| **expiry** | Option expiry | VARCHAR(10) | FMDM | `3M` |
| **strike_type** | Strike convention | ENUM | FMDM | `DELTA`, `MONEYNESS`, `ABSOLUTE` |
| **strike** | Strike value | DECIMAL(10,4) | FMDM | `25` (for 25 delta) |
| **implied_vol** | Implied volatility | DECIMAL(10,6) | FMDM | `0.0850` |
| **surface_date** | Observation date | DATE | FMDM | `2025-01-02` |

### 4.4 Time Series (Historical Returns)

| Field | Definition | Data Type | Source System | Example |
|-------|------------|-----------|---------------|---------|
| **risk_factor_id** | Unique risk factor identifier | VARCHAR(50) | FMDM | `RF-EURUSD-SPOT` |
| **observation_date** | Date of observation | DATE | FMDM | `2025-01-02` |
| **price_value** | Observed price/rate | DECIMAL(18,8) | FMDM | `1.08523` |
| **return_1d** | 1-day log return | DECIMAL(10,8) | Risk Engine | `-0.00234` |
| **return_10d** | 10-day log return | DECIMAL(10,8) | Risk Engine | `-0.01523` |
| **proxy_level** | Proxy level if applicable | INTEGER(1-4) | Risk Engine | `0` (direct), `1-4` (proxy) |
| **proxy_source_id** | Source risk factor if proxied | VARCHAR(50) | Risk Engine | `RF-GBPUSD-SPOT` |

**Source Process**: [Time Series Management (MR-L4-005)](../../L4-Processes/processes/time-series-management/time-series-overview.md)

---

## 5. Position / Trade Data

### 5.1 Trade Attributes

| Field | Definition | Data Type | Source System | Example |
|-------|------------|-----------|---------------|---------|
| **trade_id** | Unique trade identifier | VARCHAR(30) | Murex | `TRD-001234567` |
| **trade_date** | Date trade was executed | DATE | Murex | `2025-01-02` |
| **value_date** | Settlement/effective date | DATE | Murex | `2025-01-04` |
| **maturity_date** | Final maturity date | DATE | Murex | `2030-01-04` |
| **book_id** | Trading book reference | VARCHAR(20) | Murex | `BK-MR-001` |
| **counterparty_id** | Counterparty reference | VARCHAR(20) | Murex | `CP-001234` |
| **product_type** | Product classification | VARCHAR(50) | Murex | `InterestRateSwap` |
| **buy_sell** | Direction | ENUM | Murex | `BUY`, `SELL` |
| **notional** | Trade notional amount | DECIMAL(18,2) | Murex | `10000000.00` |
| **notional_ccy** | Notional currency | CHAR(3) | Murex | `USD` |
| **trade_status** | Current status | ENUM | Murex | `LIVE`, `MATURED`, `TERMINATED` |

### 5.2 Position Valuations

| Field | Definition | Data Type | Source System | Example |
|-------|------------|-----------|---------------|---------|
| **trade_id** | Trade reference | VARCHAR(30) | Murex | `TRD-001234567` |
| **valuation_date** | Date of valuation | DATE | Murex | `2025-01-02` |
| **market_value** | Mark-to-market value | DECIMAL(18,2) | Murex | `125432.50` |
| **market_value_ccy** | Valuation currency | CHAR(3) | Murex | `USD` |
| **accrued_interest** | Accrued interest | DECIMAL(18,2) | Murex | `15234.75` |
| **clean_price** | Clean price (bonds) | DECIMAL(10,6) | Murex | `99.875` |
| **dirty_price** | Dirty price (bonds) | DECIMAL(10,6) | Murex | `101.234` |

**Note**: Position-level sensitivities (Greeks) are calculated by Murex for each trade and stored alongside valuations. See **Section 6** for sensitivity metric definitions.

---

## 6. Sensitivity Metrics (Greeks)

Sensitivities (also known as "Greeks") measure the rate of change of position value with respect to underlying risk factors. They are:
- **Calculated** at the trade/position level by the trading system (Murex)
- **Aggregated** to desk, business unit, and entity levels for risk management
- **Used for** hedging decisions, P&L attribution, and limit monitoring

### 6.1 Interest Rate Sensitivities

| Metric | Definition | Formula | Unit | Source |
|--------|------------|---------|------|--------|
| **DV01** | Dollar value of 1 basis point | δV/δr for 1bp parallel shift | $ per bp | Murex |
| **PV01** | Present value of 1 basis point | Same as DV01 (alternate name) | $ per bp | Murex |
| **DV01_bucket** | DV01 by tenor bucket | δV/δr(tenor) for 1bp | $ per bp | Murex |
| **Convexity** | Second derivative of value to rates | δ²V/δr² | $ per bp² | Murex |
| **Key Rate Duration** | Sensitivity to specific tenor point | δV/δr(tenor) / V | Years | Murex |

**DV01 Tenor Buckets**:
| Bucket | Tenor Range | Limit Reference |
|--------|-------------|-----------------|
| 0-3M | 0 to 3 months | MR-L5-003 Section 2.3 |
| 3M-1Y | 3 months to 1 year | MR-L5-003 Section 2.3 |
| 1Y-5Y | 1 to 5 years | MR-L5-003 Section 2.3 |
| 5Y-10Y | 5 to 10 years | MR-L5-003 Section 2.3 |
| 10Y+ | Over 10 years | MR-L5-003 Section 2.3 |

### 6.2 Credit Sensitivities

| Metric | Definition | Formula | Unit | Source |
|--------|------------|---------|------|--------|
| **CS01** | Credit spread sensitivity | δV/δcs for 1bp spread widening | $ per bp | Murex |
| **CS01_bucket** | CS01 by rating bucket | δV/δcs(rating) for 1bp | $ per bp | Murex |
| **Recovery_Rate_Sens** | Sensitivity to recovery rate | δV/δRR for 1% change | $ per % | Murex |
| **Jump_to_Default** | Loss on immediate default | V - Recovery × Notional | $ | Murex |

**CS01 Rating Buckets**:
| Bucket | Rating Range | Limit Reference |
|--------|--------------|-----------------|
| IG (A- and above) | AAA to A- | MR-L5-003 Section 2.4 |
| IG (BBB) | BBB+ to BBB- | MR-L5-003 Section 2.4 |
| HY (BB) | BB+ to BB- | MR-L5-003 Section 2.4 |
| HY (B and below) | B+ and below | MR-L5-003 Section 2.4 |

### 6.3 Option Sensitivities

| Metric | Definition | Formula | Unit | Source |
|--------|------------|---------|------|--------|
| **Delta** | Sensitivity to underlying price | δV/δS | $ per % | Murex |
| **Gamma** | Rate of change of delta | δ²V/δS² | $ per %² | Murex |
| **Vega** | Sensitivity to implied volatility | δV/δσ for 1% vol move | $ per % vol | Murex |
| **Weighted_Vega** | Time-weighted vega | Vega × sqrt(T) weighting | $ per % vol | Murex |
| **Theta** | Time decay per day | δV/δt | $ per day | Murex |
| **Rho** | Sensitivity to interest rates | δV/δr for 1% rate move | $ per % | Murex |

### 6.4 FX Sensitivities

| Metric | Definition | Formula | Unit | Source |
|--------|------------|---------|------|--------|
| **FX_Delta** | Sensitivity to FX spot | δV/δFX for 1% move | $ per % | Murex |
| **FX_Gamma** | Second derivative to FX | δ²V/δFX² | $ per %² | Murex |
| **FX_Vega** | Sensitivity to FX vol | δV/δσ_FX for 1% vol move | $ per % vol | Murex |

### 6.5 Correlation Sensitivity

| Metric | Definition | Formula | Unit | Source |
|--------|------------|---------|------|--------|
| **Correlation_Sens** | Sensitivity to correlation | δV/δρ for 1% correlation move | $ per % | Murex |

**Used for**: XVA calculations, basket products, correlation trading

---

## 7. Risk Metrics

### 7.1 Value at Risk (VaR) Metrics

| Metric | Definition | Parameters | Unit | Source | Control Reference |
|--------|------------|------------|------|--------|-------------------|
| **VaR_1d_99** | 1-day VaR at 99% confidence | 99%, 1-day, HS 500-day | $ | Risk Engine | MR-L5-001 |
| **VaR_10d_99** | 10-day VaR at 99% confidence | 99%, 10-day, scaled | $ | Risk Engine | MR-L5-001 |
| **SVaR_1d_99** | 1-day Stressed VaR | 99%, 1-day, HS stressed period | $ | Risk Engine | MR-L5-001 |
| **SVaR_10d_99** | 10-day Stressed VaR | 99%, 10-day, scaled | $ | Risk Engine | MR-L5-001 |
| **VaR_avg_60d** | 60-day average VaR | Rolling 60-day average | $ | Risk Engine | Capital calc |
| **SVaR_avg_60d** | 60-day average SVaR | Rolling 60-day average | $ | Risk Engine | Capital calc |
| **MVaR** | Management VaR (all trading book) | 99%, 1-day | $ | Risk Engine | Internal |
| **IMA_VaR** | Regulatory VaR (IMA-approved) | 99%, 10-day | $ | Risk Engine | Regulatory |

**Methodology Reference**: [VaR/SVaR Methodology (MR-L6-001)](../market-risk/var-svar-methodology.md)

### 7.2 Component VaR (Attribution)

| Metric | Definition | Formula | Unit | Source |
|--------|------------|---------|------|--------|
| **Component_VaR** | VaR contribution by dimension | ρ(i,P) × σ(i) × Pos(i) / σ(P) × VaR | $ | Risk Engine |
| **Marginal_VaR** | Incremental VaR for position | VaR(P) - VaR(P excl i) | $ | Risk Engine |
| **Diversification_Benefit** | Risk reduction from diversification | (Undiv VaR - Div VaR) / Undiv VaR | % | Risk Engine |

**Attribution Dimensions**:
- By Desk / Book / Business Unit
- By Asset Class
- By Risk Factor
- By Issuer / Counterparty
- By Currency
- By Country

### 7.3 Stress Testing Metrics

| Metric | Definition | Parameters | Unit | Source | Control Reference |
|--------|------------|------------|------|--------|-------------------|
| **Stress_PnL_GFC** | P&L under GFC 2008-09 scenario | Historical scenario | $ | Risk Engine | MR-L5-002 |
| **Stress_PnL_COVID** | P&L under COVID-19 scenario | Historical scenario | $ | Risk Engine | MR-L5-002 |
| **Stress_PnL_Rates_200** | P&L for +200bp rate shock | Hypothetical | $ | Risk Engine | MR-L5-002 |
| **Stress_PnL_EM_Crisis** | P&L under EM crisis scenario | Historical scenario | $ | Risk Engine | MR-L5-002 |
| **Stress_PnL_Vol_Spike** | P&L for +100% volatility | Hypothetical | $ | Risk Engine | MR-L5-002 |
| **Worst_Pillar_Stress** | Worst loss across pillar scenarios | Maximum of scenarios | $ | Risk Engine | MR-L5-002 |

**Methodology Reference**: [Stress Testing Policy (MR-L3-005)](../../L3-Governance/policies/stress-testing-policy.md)

### 7.4 Incremental Risk Charge (IRC)

| Metric | Definition | Parameters | Unit | Source |
|--------|------------|------------|------|--------|
| **IRC** | Incremental Risk Charge | 99.9%, 1-year, MC | $ | DAMAS |
| **IRC_default** | Default component of IRC | Simulated defaults | $ | DAMAS |
| **IRC_migration** | Migration component of IRC | Rating transitions | $ | DAMAS |

### 7.5 Risk Not in VaR (RNIV)

| Metric | Definition | Source | Control Reference |
|--------|------------|--------|-------------------|
| **RNIV_total** | Total RNIV capital add-on | EUMA | MR-L5-001 |
| **RNIV_basis** | Basis risk add-on | EUMA | MR-L5-001 |
| **RNIV_gap** | Gap risk add-on | EUMA | MR-L5-001 |
| **RNIV_correlation** | Correlation risk add-on | EUMA | MR-L5-001 |

### 7.6 Economic Capital (ECAP)

| Metric | Definition | Parameters | Unit | Source | Control Reference |
|--------|------------|------------|------|--------|-------------------|
| **ECAP_MR** | Market Risk Economic Capital | 99.9%, 1-year, liquidity-adj | $ | MRS | MR-L5-007 |
| **ECAP_liquidity_addon** | Illiquidity add-on | Extended horizon | $ | MRS | MR-L5-007 |

**Methodology Reference**: [ECAP Methodology (MR-L6-002)](../market-risk/ecap-methodology.md)

### 7.7 Earnings at Risk (EaR)

| Metric | Definition | Parameters | Unit | Source |
|--------|------------|------------|------|--------|
| **EaR_MR** | Market Risk Earnings at Risk | 90%, 1-year | $ | EUMA |
| **EaR_Entity** | Entity-level diversified EaR | 90%, 1-year, 40% correlation | $ | EUMA |

**Scaling Factor**: EaR = VaR × 8.71 (derived from 90% CI, 1-year vs 99% CI, 1-day)

---

## 8. Capital Metrics

### 8.1 IMA Capital Components

| Metric | Definition | Formula | Unit | Source |
|--------|------------|---------|------|--------|
| **IMA_Capital** | Total IMA market risk capital | VaR_component + SVaR_component + IRC | $ | Risk Engine |
| **VaR_Capital** | VaR capital component | max(VaR_t-1, mc × VaR_avg) | $ | Risk Engine |
| **SVaR_Capital** | SVaR capital component | max(SVaR_t-1, ms × SVaR_avg) | $ | Risk Engine |
| **mc** | VaR multiplier | 3.0 + backtesting add-on | Ratio | Risk Engine |
| **ms** | SVaR multiplier | 3.0 + backtesting add-on | Ratio | Risk Engine |

### 8.2 FRTB Metrics (Future)

| Metric | Definition | Status | Unit | Source |
|--------|------------|--------|------|--------|
| **FRTB_SbM** | Sensitivities-based Method | Planned | $ | MRS |
| **FRTB_DRC** | Default Risk Charge | Planned | $ | MRS |
| **FRTB_RRAO** | Residual Risk Add-On | Planned | $ | MRS |
| **ES** | Expected Shortfall | Planned | $ | Risk Engine |

### 8.3 RWA Metrics

| Metric | Definition | Formula | Unit | Source |
|--------|------------|---------|------|--------|
| **RWA_MR** | Market Risk RWA | Capital × 12.5 | $ | Finance |
| **RWA_MR_pct** | MR RWA as % of total | RWA_MR / Total_RWA | % | Finance |

---

## 9. P&L Metrics

### 9.1 P&L Types

| Metric | Definition | Use Case | Unit | Source |
|--------|------------|----------|------|--------|
| **Actual_PnL** | Actual daily P&L including fees | P&L reporting | $ | Plato |
| **Hypothetical_PnL** | P&L assuming static positions | Backtesting | $ | Plato |
| **Clean_PnL** | P&L excluding new trades, fees | Backtesting | $ | Plato |
| **Risk_Theoretical_PnL** | P&L from risk model | Backtesting comparison | $ | Risk Engine |

### 9.2 P&L Attribution

| Metric | Definition | Unit | Source |
|--------|------------|------|--------|
| **PnL_Delta** | P&L from delta exposure | $ | Plato |
| **PnL_Gamma** | P&L from gamma exposure | $ | Plato |
| **PnL_Vega** | P&L from vega exposure | $ | Plato |
| **PnL_Theta** | P&L from time decay | $ | Plato |
| **PnL_Rates** | P&L from rate moves | $ | Plato |
| **PnL_Credit** | P&L from credit spread moves | $ | Plato |
| **PnL_FX** | P&L from FX moves | $ | Plato |
| **PnL_Unexplained** | Residual unexplained P&L | $ | Plato |

### 9.3 Backtesting Metrics

| Metric | Definition | Threshold | Control Reference |
|--------|------------|-----------|-------------------|
| **Backtesting_Exception** | Day where loss > VaR | Binary flag | MR-L5-004 |
| **Exception_Count_250d** | Count of exceptions in 250 days | 0-4 Green, 5-9 Amber, 10+ Red | MR-L5-004 |
| **Traffic_Light_Zone** | Basel traffic light status | GREEN, YELLOW, RED | MR-L5-004 |
| **Clean_PnL_vs_VaR** | Clean P&L divided by VaR | Ratio | MR-L5-004 |

---

## 10. Limit Metrics

### 10.1 Limit Utilisation

| Metric | Definition | Formula | Unit | Source |
|--------|------------|---------|------|--------|
| **Limit_Utilisation** | Current usage vs limit | Current / Limit × 100 | % | Risk Engine |
| **Limit_Headroom** | Available capacity | Limit - Current | $ | Risk Engine |
| **Warning_Threshold** | Warning level (typically 80%) | Limit × 0.80 | $ | Risk Engine |

### 10.2 Limit Status

| Status | Utilisation Range | Action Required |
|--------|-------------------|-----------------|
| **Green** | 0-79% | Normal operations |
| **Amber** | 80-99% | MLRC notification; heightened monitoring |
| **Red** | 100-109% | Immediate escalation; action plan |
| **Black** | ≥110% | CRO escalation; RMC notification |

**Control Reference**: [VaR Limit Framework (MR-L3-003)](../../L3-Governance/policies/var-limit-framework.md)

---

## 11. XVA Metrics

### 11.1 Valuation Adjustments

| Metric | Definition | Unit | Source |
|--------|------------|------|--------|
| **CVA** | Credit Valuation Adjustment | $ | FO Systems |
| **Managed_CVA** | CVA with hedging | $ | FO Systems |
| **Portfolio_CVA** | Unmanaged CVA reserve | $ | FO Systems |
| **DVA** | Debit Valuation Adjustment | $ | FO Systems |
| **FVA** | Funding Valuation Adjustment | $ | FO Systems |
| **ColVA** | Collateral Valuation Adjustment | $ | FO Systems |
| **KVA** | Capital Valuation Adjustment | $ | FO Systems |

---

## 12. Data Quality Metrics

### 12.1 Completeness Metrics

| Metric | Definition | Target | Source |
|--------|------------|--------|--------|
| **Trade_Capture_Rate** | % of trades captured in risk | >99.5% | Risk Engine |
| **Risk_Factor_Coverage** | % of positions with risk factors | >99% | Risk Engine |
| **Time_Series_Completeness** | % of risk factors with full history | >98% | FMDM |
| **Proxy_Rate** | % of positions using proxies | <5% | Risk Engine |

### 12.2 Timeliness Metrics

| Metric | Definition | Target | Source |
|--------|------------|--------|--------|
| **VaR_Production_Time** | Time to complete VaR run | <4 hours | Risk Engine |
| **Market_Data_Latency** | Delay in market data | <15 mins | FMDM |
| **Trade_Data_Latency** | Delay in trade capture | <30 mins | Murex |

### 12.3 Accuracy Metrics

| Metric | Definition | Target | Source |
|--------|------------|--------|--------|
| **PnL_Explain_Rate** | % of P&L explained by risk | >95% | Plato |
| **Recon_Break_Count** | Number of reconciliation breaks | 0 | Risk Engine |
| **Backtesting_Exception_Rate** | Exceptions / 250 days | <4 | Risk Engine |

---

## 13. System Source Reference

| System Code | System Name | Data Domain | Owner |
|-------------|-------------|-------------|-------|
| **Murex** | Trading & Risk Platform | Trades, Positions, Greeks | Front Office |
| **FMDM** | Financial Market Data Management | Market Data, Time Series, Risk Factors | Market Risk |
| **Bookman** | Book Hierarchy System | Book/Desk/Entity structure | Finance |
| **EDM** | Enterprise Data Management | Counterparty, Instrument master | CMU |
| **CRS** | Credit Rating System | Internal credit ratings | Credit Risk |
| **Plato** | P&L System | P&L, Attribution | Finance |
| **DAMAS** | Default & Migration System | IRC calculation | Market Risk |
| **EUMA** | Economic/Management Analytics | ECAP, EaR, RNIV | RMA |
| **MRS** | Market Risk System | VaR, Stress, Sensitivities | Market Risk |
| **Adaptiv** | Credit Risk System | Credit exposures, PFE | Credit Risk |
| **Vespa** | VaR Engine (Legacy) | VaR calculation | Market Risk |

---

## 14. Related Documents

| Document | Relationship |
|----------|--------------|
| [System Architecture (MR-L7-001)](./system-architecture.md) | Parent architecture document |
| [VaR/SVaR Methodology (MR-L6-001)](./var-svar-methodology.md) | Methodology definitions |
| [ECAP Methodology (MR-L6-002)](./ecap-methodology.md) | ECAP methodology |
| [Risk Engine Calculation (MR-L4-006)](../../L4-Processes/processes/risk-engine-calculation.md) | Data flow process |
| [VaR Limits Controls (MR-L5-001)](../../L5-Controls/market-risk/var-limits-controls.md) | Control definitions |
| [Sensitivity Limits Controls (MR-L5-003)](../../L5-Controls/market-risk/sensitivity-limits-controls.md) | Sensitivity definitions |

---

## 15. Document Control

### 15.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2026-01-02 | Initial version incorporating ICBCS reference data and existing taxonomy metrics | MLRC |

### 15.2 Review Schedule

- Full review: Annually (January)
- Metric additions: As new products/systems onboarded
- System changes: Upon material system change

---

*End of Document*
