# Stress Testing Feed - Architecture Overview

**Meridian Global Bank - Market Risk Technology**

---

## 1. Executive Summary

The Stress Testing Feed provides scenario-based P&L results for all trading positions in Murex under pre-defined hypothetical stress scenarios. Unlike VaR which uses historical scenarios, Stress Testing applies hypothetical shocks to risk factors representing extreme but plausible market conditions. These stress results are consumed by VESPA for aggregation across business and regulatory hierarchies.

### Key Characteristics

| Attribute | Value |
|-----------|-------|
| **Feed Type** | Stress Results (Hypothetical Scenarios) |
| **Source System** | Murex Market Risk Engine |
| **Methodology** | Full Revaluation |
| **Regions** | London, Hong Kong, New York, São Paulo |
| **Target System** | VESPA |
| **Aggregation Currency** | USD |

---

## 2. Key Differences: Stress Testing vs VaR

| Aspect | Stress Testing | VaR |
|--------|----------------|-----|
| **Scenario Type** | Pre-defined hypothetical shocks | Historical scenarios |
| **Scenario Source** | FMDM (most risk factors), Xenomorph (metals) | Asset Control, Xenomorph |
| **Number of Scenarios** | Multiple named scenarios (e.g., 9/11, IR shock) | 250 (rolling 1-year) |
| **FX Volatility** | ATM only | Full smile |
| **Bond Adjustment Spread** | Included | Not included |
| **Recovery Rates** | Included | Not included |
| **Scenario Container** | One per region ({RGN}_contST) | Multiple per region/type |

---

## 3. Architecture Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         STRESS TESTING GENERATION                            │
│                           Data Flow Architecture                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐     ┌──────────────────┐
│  Market Data     │     │     Trades       │
│  Platforms       │     │    (Murex)       │
│                  │     │                  │
│ • FMDM           │     │ • VAR_LDN        │
│ • Xenomorph      │     │ • VAR_HKG        │
│   (Metals)       │     │ • VAR_NYK        │
└────────┬─────────┘     │ • VAR_SAO        │
         │               └────────┬─────────┘
         │                        │
         ▼                        │
┌──────────────────┐              │
│  Market Risk     │              │
│  Single Reports  │              │
│                  │              │
│ • **_V_ST        │              │
│ • Hypothetical   │              │
│   Shocks         │              │
└────────┬─────────┘              │
         │                        │
         ▼                        │
┌──────────────────┐              │
│    Scenario      │◄─────────────┘
│   Containers     │
│                  │
│ • {RGN}_contST   │
│   (One per region)│
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│         Market Risk Engine               │
│         (Revaluation Runs)               │
│                                          │
│  ANT Script: startvareod.sh              │
│  Risk Metric: StressTesting              │
│                                          │
│  • Full Revaluation Method               │
│  • Consolidated Mode                     │
│  • ST_RevalSetting                       │
│  • Risk Class Filtering                  │
└────────────────┬─────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────┐
│         Datamart Tables                  │
│                                          │
│  MRA_EXPORT_{RGN}_STRESSTESTING_REP      │
│                                          │
│  • Per region (LDN, HKG, NYK, SAO)       │
└────────────────┬─────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────┐
│         Extraction                       │
│                                          │
│  • ER_StressTesting_SB                   │
│  • Joins: SB_SE_HEAD_REP, SB_CP_REP      │
│  • Static data enrichment                │
└────────────────┬─────────────────────────┘
                 │
                 ▼ formatriskreport.sh
┌──────────────────────────────────────────┐
│         Stress Test Files                │
│         (Per Risk Class)                 │
│                                          │
│  StressTest_MxGts_***_All.zip            │
│  ├── _Commodities.txt (StrCommodity)     │
│  ├── _FX.txt (GenFX)                     │
│  ├── _IR.txt (GenIR)                     │
│  ├── _Recovery.txt (RR)                  │
│  ├── _Credit.txt (CRD)                   │
│  ├── _Bond_Basi.txt (BCS)                │
│  ├── _IR_FX_Com.txt (TotalStr)           │
│  └── _Total.txt (TotalStrCRD)            │
└────────────────┬─────────────────────────┘
                 │
                 ▼ MFT
┌──────────────────────────────────────────┐
│              VESPA                       │
│                                          │
│  • Aggregation by hierarchy              │
│  • Business & regulatory reporting       │
│  • Stress limit monitoring               │
└──────────────────────────────────────────┘
```

---

## 4. Risk Factors

### 4.1 Risk Factor Scope

| Risk Factor | Description | Variation Type |
|-------------|-------------|----------------|
| Bond Adjustment Spread | Spread on rate curve for bond pricing | Absolute |
| Cap Floors Volatility | ATM volatility for cap floors | Absolute |
| Commodity Market Rates | Future prices, lease rates, spot prices | Percentage/Absolute |
| Commodity Smile | Volatility structure across delta | Percentage |
| Credit Market Rates | Credit curve market rates | Percentage/Absolute |
| FX Volatility | ATM volatility across time | Absolute |
| FX Spot | Leading currency pairs | Percentage |
| Rates Curves Zero Coupons | Zero coupon rates | Absolute/Percentage |
| Recovery Rates | Recovery percentages in default | Percentage |
| Security Spot | Bond prices | Percentage |
| Security Volatility | ATM volatility across time | Absolute |
| Swaption Volatility | ATM volatility for swaptions | Absolute |

### 4.2 Perturbation Types

| Type | Formula | Example Use |
|------|---------|-------------|
| **Standard/Absolute** | x(t+1) - x(t) | Zero coupons, Credit rates, Bond spread |
| **Percentage** | (x(t+1) - x(t)) / x(t) | FX Spot, Commodities |
| **Log** | Ln(\|x(t+1)/x(t)\|) | Special cases |

---

## 5. Risk Classes (P&L Decomposition)

### 5.1 Non-Diversified Stress Testing (Partials)

| Risk Class | Risk Factors |
|------------|--------------|
| **StrCommodity** | Commodity market rates, Commodity Smile |
| **RR** | Recovery Rates |
| **BCS** | Bond credit spread |
| **GenFX** | FX Spot, FX Volatility, FX Smile |
| **GenIR** | Security Volatility, Zero coupons, Swaption Volatility, Cap Floors Volatility |
| **CRD** | CRD Market Rates, Credit Volatility |

### 5.2 Diversified Stress Testing

| Risk Class | Risk Factors |
|------------|--------------|
| **TotalStr** | Security Volatility, FX Spot, FX Volatility, Zero coupons, Swaption Volatility, Cap Floors Volatility, FX Smile, Commodity market rates, Commodity Smile |
| **TotalStrCRD** | All risk factors including Security Spot, Bond credit spread, CRD Market rates, Recovery Rates |

---

## 6. Stress Testing Methodology

### 6.1 Revaluation Settings (ST_RevalSetting)

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
| **Revaluation Method** | Full Revaluation |
| **Central Point** | Murex P&L (market value + past cash + future cash) |
| **P&L Conversion** | Perturbed FX spots from scenario |
| **Weighting** | Equal weights for all scenarios |
| **Volatility Smile Mode** | Absolute (Commodity) |

### 6.3 Zero Coupon Propagation

- **Mode**: No propagation
- **Interpolation**: Linear between surrounding shifts
- **Extrapolation**: Flat before and after

---

## 7. Market Data Sets

| Region | Market Data Set | Description |
|--------|-----------------|-------------|
| LDN | LNVARVAL | London stress valuation |
| HKG | SGVARVAL | Singapore/HK stress valuation |
| NYK | NYVARVAL | New York stress valuation |
| SAO | SPVARVAL | São Paulo stress valuation |

**Note**: Same market data sets as VaR (different from closing sets used for sensitivities).

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

**Note**: No additional filters applied - all trades in combined portfolios included.

---

## 9. Output Files

### 9.1 File Structure

Each region generates a ZIP file containing 8 risk class reports:

| ZIP File | Contains |
|----------|----------|
| StressTest_MxGts_***_All_yyyymmdd.zip | 8 risk class files |

### 9.2 Risk Class Files

| File Name Pattern | Risk Class |
|-------------------|------------|
| _Commodities.txt | StrCommodity |
| _FX.txt | GenFX |
| _IR.txt | GenIR |
| _Recovery.txt | RR |
| _Credit.txt | CRD |
| _Bond_Basi.txt | BCS |
| _IR_FX_Com.txt | TotalStr |
| _Total.txt | TotalStrCRD |

---

## 10. Related Documentation

| Document | Description |
|----------|-------------|
| [stress-testing-brd.md](stress-testing-brd.md) | Business requirements |
| [stress-testing-config.md](stress-testing-config.md) | Murex configuration |
| [stress-testing-idd.md](stress-testing-idd.md) | Interface design |

---

*Document Version: 1.0 | Last Updated: 2025-01-13*
