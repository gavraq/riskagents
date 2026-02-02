# Value at Risk (VaR) P&L Strips Feed - Architecture Overview

**Meridian Global Bank - Market Risk Technology**

---

## 1. Executive Summary

The Value at Risk (VaR) P&L Strips Feed provides historical scenario-based P&L vectors for all trading positions in Murex. Unlike sensitivity feeds that measure exposure to risk factors, VaR feeds capture the **full revaluation impact** of applying historical market movements to current positions. These P&L strips are consumed by VESPA for VaR calculation via percentile cut-offs.

### Key Characteristics

| Attribute | Value |
|-----------|-------|
| **Feed Type** | P&L Strips (Historical Simulation VaR) |
| **Source System** | Murex Market Risk Engine |
| **VaR Types** | 1D VaR, 10D VaR, 10D SVaR, 10D ESVaR |
| **Methodology** | Full Revaluation |
| **Regions** | London, Hong Kong, New York, São Paulo |
| **Target System** | VESPA |
| **Aggregation Currency** | USD |

---

## 2. VaR Types and Holding Periods

### 2.1 VaR Calculation Types

| VaR Type | Holding Period | Observation Period | Scenarios | Purpose |
|----------|----------------|-------------------|-----------|---------|
| **1D VaR** | 1 day | Rolling 1 year | 250 | Daily risk monitoring |
| **10D VaR** | 10 days | Rolling 1 year | 250 | Regulatory capital |
| **10D SVaR** | 10 days | Fixed stress period | 250 | Stressed VaR for capital |
| **10D ESVaR** | 10 days | Jan 2007 to current | Growing | Stress period identification |

### 2.2 Scenario Containers

| Region | 1D VaR | 10D VaR | 10D SVaR | 10D ESVaR |
|--------|--------|---------|----------|-----------|
| LDN | LDN_cont1DVaR | LDN_cont10DVaR | LDN_cont10DSVaR | LDN_cont10DESVaR |
| HKG | HKG_cont1DVaR | HKG_cont10DVaR | HKG_cont10DSVaR | HKG_cont10DESVaR |
| NYK | NYK_cont1DVaR | NYK_cont10DVaR | NYK_cont10DSVaR | NYK_cont10DESVaR |
| SAO | SAO_cont1DVaR | SAO_cont10DVaR | SAO_cont10DSVaR | SAO_cont10DESVaR |

---

## 3. Architecture Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         VaR P&L STRIPS GENERATION                            │
│                           Data Flow Architecture                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐     ┌──────────────────┐
│  Market Data     │     │     Trades       │
│  Platforms       │     │    (Murex)       │
│                  │     │                  │
│ • Asset Control  │     │ • VAR_LDN        │
│ • Xenomorph      │     │ • VAR_HKG        │
│ • FMDM           │     │ • VAR_NYK        │
└────────┬─────────┘     │ • VAR_SAO        │
         │               └────────┬─────────┘
         │                        │
         ▼                        │
┌──────────────────┐              │
│  Market Risk     │              │
│  Single Reports  │              │
│                  │              │
│ • Scenario Gen   │              │
│ • Variation Types│              │
│ • ASCII Files    │              │
└────────┬─────────┘              │
         │                        │
         ▼                        │
┌──────────────────┐              │
│    Scenario      │              │
│   Containers     │◄─────────────┘
│                  │
│ • {RGN}_cont1DVAR│
│ • {RGN}_cont10DVAR│
│ • {RGN}_cont10DSVAR│
│ • {RGN}_cont10DESVAR│
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│         Market Risk Engine               │
│         (Revaluation Runs)               │
│                                          │
│  ANT Script: startvareod.sh              │
│                                          │
│  • Full Revaluation Method               │
│  • Consolidated Mode                     │
│  • VAR_RevalSetting                      │
│  • Risk Class Filtering                  │
└────────────────┬─────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────┐
│         Datamart Tables                  │
│                                          │
│  MRA_EXPORT_{RGN}_{TYPE}_REP             │
│                                          │
│  • 1DVAR, 10DVAR, 10DSVAR, 10DESVAR     │
│  • Per region                            │
└────────────────┬─────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────┐
│         Extraction                       │
│                                          │
│  • DE_1DVAR_SB (non-detailed)           │
│  • DE_1DVAR_D_SB (detailed/TotalCRD)    │
│  • Similar for 10DVAR, 10DSVAR          │
└────────────────┬─────────────────────────┘
                 │
                 ▼ formatriskreport.sh
┌──────────────────────────────────────────┐
│         P&L Strip Files                  │
│         (Per Risk Class)                 │
│                                          │
│  P&LStrips_MxGts_***_1D_VAR_All.zip     │
│  ├── _IR.txt                             │
│  ├── _FX.txt                             │
│  ├── _IRVol.txt                          │
│  ├── _FXVol.txt                          │
│  ├── _GenIR.txt                          │
│  ├── _GenFX.txt                          │
│  ├── _Com.txt                            │
│  ├── _Credit_Curve.txt                   │
│  ├── _IR_FX_Com.txt (Total)              │
│  └── _detail_Total.txt (TotalCRD)        │
└────────────────┬─────────────────────────┘
                 │
                 ▼ MFT
┌──────────────────────────────────────────┐
│              VESPA                       │
│                                          │
│  • Aggregation by hierarchy              │
│  • Percentile cut-off (99%)              │
│  • VaR calculation                       │
└──────────────────────────────────────────┘
```

---

## 4. Risk Factors and Variation Types

### 4.1 Risk Factor Scope

| Risk Factor | Description | Variation Type |
|-------------|-------------|----------------|
| Cap Floors Volatility | ATM volatility for cap floors | Percentage |
| Commodity Market Rates | Future prices, lease rates, spot prices | Percentage (futures/spot), Absolute (lease) |
| Commodity Smile | Volatility structure across delta | Percentage |
| Credit Market Rates | Credit curve market rates | Absolute |
| FX Smile | Volatility structure across delta | Percentage |
| FX Spot | Leading currency pairs | Percentage |
| Rates Curves Zero Coupons | Zero coupon rates | Absolute |
| Security Spot | Bond prices | Absolute |
| Security Volatility | ATM volatility across time | Percentage |
| Swaption Volatility | ATM volatility for swaptions | Percentage |

### 4.2 Perturbation Types

| Type | Formula | Example Use |
|------|---------|-------------|
| **Standard/Absolute** | x(t+1) - x(t) | Zero coupons, Credit rates |
| **Percentage** | (x(t+1) - x(t)) / x(t) | FX Spot, Volatilities |
| **Log** | Ln(\|x(t+1)/x(t)\|) | Special cases |

### 4.3 Volatility Smile Mode

| Scenario Type | Smile Mode |
|---------------|------------|
| FX Smile | Absolute |
| Commodity Smile | Absolute |
| Cap Floor Smile | Spread |
| Swaption Smile | Spread |

---

## 5. Risk Classes (P&L Decomposition)

### 5.1 Non-Diversified VaR (Partials)

| Risk Class | Risk Factors | VaR/SVaR | ESVaR |
|------------|--------------|----------|-------|
| **Commodities** | Commodity market rates, Commodity Smile | ✓ | |
| **FX** | FX Spot | ✓ | |
| **FXVol** | FX Volatility*, FX Smile | ✓ | |
| **GenFX** | FX Spot, FX Volatility*, FX Smile | ✓ | ✓ |
| **GenIR** | Security Volatility, Zero coupons, Swaption Vol, Cap Floors Vol | ✓ | ✓ |
| **IR** | Zero coupons | ✓ | |
| **IRVol** | Security Volatility, Swaption Vol, Cap Floors Vol | ✓ | |
| **CRD** | CRD Market Rates + Security Spots (TotalCRD - Total) | ✓ | |

*FX volatility selected but no perturbations generated

### 5.2 Diversified VaR

| Risk Class | Risk Factors | Description |
|------------|--------------|-------------|
| **Total** | All except Security Spot & CRD Market Rates | Diversified VaR |
| **TotalCRD** | All risk factors including Security Spot & CRD | Full diversified VaR |

---

## 6. VaR Methodology Configuration

### 6.1 Revaluation Settings (VAR_RevalSetting)

| Setting | Value |
|---------|-------|
| Aggregation Currency | USD |
| Discounting | On |
| Financing | Off |
| P&L Display | Aggregated |
| P&L Breakdown | Redefined to Aggregated |
| FX Spot Conversion | Discounted |
| Brokerage Fees | Off |
| Revaluation Mode | Consolidated |

### 6.2 Key Methodology Elements

| Parameter | Configuration |
|-----------|---------------|
| **Holding Period** | 1 day, 10 days (overlapping) |
| **Observation Period** | 250 scenarios (1 year rolling) |
| **Confidence Level** | 99% (applied in VESPA) |
| **Weighting** | Equal weights for all scenarios |
| **Scaling** | No time scaling (actual 10-day variation) |
| **Open Days Calendar** | VAR_SCN (excludes weekends, 1 Jan) |

### 6.3 Zero Coupon Propagation

- **Mode**: No propagation
- **Interpolation**: Linear between surrounding shifts
- **Extrapolation**: Flat before and after

### 6.4 Flooring/Capping

User-defined floors configured in `VAR_FullRevalOutput` template for:
- Zero coupon curves (e.g., AR1:Std floor = 0.00000)
- Volatilities (already floored to 0 in FO module)

---

## 7. Market Data Sets

| Region | Market Data Set | Description |
|--------|-----------------|-------------|
| LDN | LNVARVAL | London VaR valuation |
| HKG | SGVARVAL | Singapore/HK VaR valuation |
| NYK | NYVARVAL | New York VaR valuation |
| SAO | SPVARVAL | São Paulo VaR valuation |

**Note**: These are different from closing market data sets used for sensitivity calculations.

---

## 8. Portfolio Scope

### 8.1 Combined Portfolios by Region

| Region | Combined Portfolio | Portfolio Nodes |
|--------|-------------------|-----------------|
| London | VAR_LDN | BMLN, FXDLNSBL, FXLNSBL, IFXMMLNIC, IRLNSBL, LMLNSBL, LNSBSA*, PMLN |
| Hong Kong | VAR_HKG | FXHKSBL, HKSBSA*, LMHKSBL, LMHKSGACU, LMHKSGDBU, PMSG |
| New York | VAR_NYK | FXNYSBL, LMNYSBLAMER, LMNYSBLDORMANT, NYSBSA*, PMNY |
| São Paulo | VAR_SAO | LMSPBSI, LMSPFIA, LMSPFND, LMSPSBL |

*Legacy portfolio nodes still included for completeness

---

## 9. Output Files

### 9.1 File Structure

Each VaR type generates a ZIP file containing 10 risk class reports:

| ZIP File | Contains |
|----------|----------|
| P&LStrips_MxGts_***_1D_VAR_All_yyyymmdd.zip | 10 risk class files |
| P&LStrips_MxGts_***_10D_VAR_All_yyyymmdd.zip | 10 risk class files |
| P&LStrips_MxGts_***_10D_SVAR_All_yyyymmdd.zip | 10 risk class files |

### 9.2 Risk Class Files

| File Name Pattern | Risk Class |
|-------------------|------------|
| _IR.txt | IR (Zero Coupons) |
| _FX.txt | FX (FX Spot) |
| _IRVol.txt | IRVol |
| _FXVol.txt | FXVol |
| _GenIR.txt | GenIR |
| _GenFX.txt | GenFX |
| _Com.txt | Commodities |
| _Credit_Curve.txt | CRD |
| _IR_FX_Com.txt | Total |
| _detail_Total.txt | TotalCRD |

---

## 10. Related Documentation

| Document | Description |
|----------|-------------|
| [var-brd.md](var-brd.md) | Business requirements |
| [var-config.md](var-config.md) | Murex configuration |
| [var-idd.md](var-idd.md) | Interface design |

---

*Document Version: 1.0 | Last Updated: 2025-01-13*
