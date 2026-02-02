# Stress Testing Feed - IT Configuration

**Meridian Global Bank - Market Risk Technology**

---

## 1. Murex Dataflow

```
┌─────────────────┐     ┌─────────────────┐
│   ANT Script    │     │   ANT Script    │
│  startEODRun    │     │  exportEODRun   │
└────────┬────────┘     └────────┬────────┘
         │                       │
         ▼                       │
┌─────────────────────────────────────────────────────┐
│                Market Risk Engine                   │
│                (Revaluation Runs)                   │
│                                                     │
│  • {RGN}_StressTesting                             │
│  • One run per region                               │
└────────────────────────┬────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│               Datamart Tables                       │
│                                                     │
│  MRA_EXPORT_HKG_STRESSTESTING_REP                  │
│  MRA_EXPORT_LDN_STRESSTESTING_REP                  │
│  MRA_EXPORT_NYK_STRESSTESTING_REP                  │
│  MRA_EXPORT_SAO_STRESSTESTING_REP                  │
└────────────────────────┬────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                  Extractions                        │
│                                                     │
│  DE_StressTesting_SB                               │
│  + Joins: SB_SE_HEAD_REP, SB_CP_REP                │
└────────────────────────┬────────────────────────────┘
                         │
                         ▼  formatriskreport.sh
┌─────────────────────────────────────────────────────┐
│               Stress Test Files                     │
│                                                     │
│  StressTest_MxGts_***_All_yyyymmdd.zip             │
└─────────────────────────────────────────────────────┘
```

---

## 2. Market Data Sets

Stress Testing uses the same market data sets as VaR:

| Region | Market Data Set | Description |
|--------|-----------------|-------------|
| London | LNVARVAL | London stress valuation |
| Hong Kong | SGVARVAL | Singapore/HK stress valuation |
| New York | NYVARVAL | New York stress valuation |
| São Paulo | SPVARVAL | São Paulo stress valuation |

**Note**: These Market Data Sets are different from the closing Market Data Sets used for valuation and sensitivity calculations.

---

## 3. Portfolio Scope

### 3.1 Combined Portfolios by Region

| Region | Combined Portfolio | Portfolio Nodes |
|--------|-------------------|-----------------|
| London | VAR_LDN | BMLN, FXDLNSBL, FXLNSBL, IFXMMLNIC, IRLNSBL, LMLNSBL, LNSBSA*, PMLN |
| Hong Kong | VAR_HKG | FXHKSBL, HKSBSA*, LMHKSBL, LMHKSGACU, LMHKSGDBU, PMSG |
| New York | VAR_NYK | FXNYSBL, LMNYSBLAMER, LMNYSBLDORMANT, NYSBSA*, PMNY |
| São Paulo | VAR_SAO | LMSPBSI, LMSPFIA, LMSPFND, LMSPSBL |

*Legacy portfolio nodes still included for completeness

**Note**: No filter (on typologies, P&L instruments, usage). All trades booked in the combined portfolios are included.

---

## 4. Scenario Configuration

### 4.1 Scenario Containers

For Stress Testing runs, there is **one scenario container per region**:

| Region | Scenario Container |
|--------|-------------------|
| HKG | HKG_contST |
| LDN | LDN_contST |
| NYK | NYK_contST |
| SAO | SAO_contST |

### 4.2 Scenario Sources

| Source | Risk Factors |
|--------|-------------|
| FMDM | All risk factors except metals |
| Xenomorph | Base & Precious Metals |

### 4.3 Volatility Configuration

Settings stored at scenario container level:

| Scenario Type | Smile Mode |
|---------------|------------|
| Commodity Smile | Absolute |

### 4.4 Scenario Weighting

- Same weight applied to all scenarios
- No decay weighting (unlike some VaR implementations)
- Setting accessible in Market Risk Single Report screen

---

## 5. Revaluation Run Configuration

### 5.1 Stress Testing Run Parameters

| Region | Scope | Run | Scenario Container | Market Data | Currency |
|--------|-------|-----|-------------------|-------------|----------|
| HKG | VAR_HKG | HKG_StressTesting | HKG_contST | SGVARVAL | USD |
| LDN | VAR_LDN | LDN_StressTesting | LDN_contST | LNVARVAL | USD |
| NYK | VAR_NYK | NYK_StressTesting | NYK_contST | NYVARVAL | USD |
| SAO | VAR_SAO | SAO_StressTesting | SAO_contST | SPVARVAL | USD |

### 5.2 Processing Script

**Script Path**: `/apps/murex/client/scripts/var/eod/startvareod.sh`

**Parameters**:
- Region: HKG, LDN, NYK, SAO
- Risk Metric: StressTesting
- Time Period: 1 (for 1 day)
- Currency: N/A

---

## 6. Risk Class Configuration

### 6.1 Full Revaluation Outputs Template

| Risk Class | Template | Risk Factors Selected |
|------------|----------|----------------------|
| StrCommodity | ST_FullRevalOutput | Commodity market rates, Commodity Smile |
| RR | ST_FullRevalOutput | Recovery Rates |
| BCS | ST_FullRevalOutput | Bond credit spread |
| GenFX | ST_FullRevalOutput | FX Spot, FX Volatility, FX Smile |
| GenIR | ST_FullRevalOutput | Security Volatility, Zero coupons, Swaption Vol, Cap Floors Vol |
| CRD | ST_FullRevalOutput | CRD Market Rates, Credit Volatility |
| TotalStr | ST_FullRevalOutput | All except Security Spot, Bond spread, CRD, Recovery |
| TotalStrCRD | ST_FullRevalOutput | All risk factors |

### 6.2 TotalStrCRD Instrument Configuration

```
Selected Risk Factors:
✓ Security Spot
✓ Security Volatility
✗ Security Dividends
✓ FX Spot
✓ FX Volatility
✓ Zero coupons
✓ Swaption Volatility
✓ Cap Floors Volatility
✗ Correlation
✗ Horizon
✗ CNV Credit Spread
✗ Security Smile
✗ Market rates
✓ FX Smile
✗ Generic Market Parameter
✓ Bond credit spread
✗ Cap Floors Smile
✗ CRD default spread
✓ CRD Market rates
✗ Credit spread curves
✗ Repo margin
✓ Commodity market rates
✓ Recovery Rates
✗ Theoretical CMC
✗ Commodities volatility
✗ Market correlations
✗ Base correlations
✗ Inflation curves
✗ Market corr. upfront amt
✗ Credit Volatility
✓ Commodity Smile
✗ Market Rates Inflation curves
✗ Inflation CPI
```

---

## 7. Revaluation Settings (ST_RevalSetting)

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

**Reference**: MxDoc, "Simulation and Reporting Settings", DocID 13339

---

## 8. Flooring Configuration

### 8.1 Floor Query

```sql
SELECT M_REF as Risk_Class,
       TRIM(M_LABEL0) as Instrument_Type,
       TRIM(M_LABEL1) as Market_Parameter,
       TRIM(M_LABEL2) as Curve_or_Index,
       TRIM(M_LABEL3) as Commodity_Index,
       M_FLOOR_VAL as Floor
FROM MX.VAR_FLCF_DBF
WHERE M_REF IN ('StrCommodity','GenFX', 'CRD', 'BCS', 'RR', 'TotalStr', 'TotalStrCRD', 'GenIR')
ORDER BY 1,2,3,4,5
```

### 8.2 Floor Configuration Summary

#### CRD Floors

| Risk Class | Market Parameter | Floor |
|------------|-----------------|-------|
| CRD | CRD Market rates | 0.00001 |
| TotalStrCRD | CRD Market rates | 0.00001 |

#### GenIR Floors (Zero Coupons)

| Curve | Floor | Notes |
|-------|-------|-------|
| AR1:Std, AR2:Std | 0 | ARS standard curves |
| ARS:Std, ARS:BOND | 0 | ARS bond curves |
| CN1:Std, CNH:Std | -2 | CNY/CNH curves |
| CNY:Std, CNY:BOND | -2 | CNY bond curves |
| NG1:Std, NGO:Std | -0.5 | NGN curves |
| RU1:Std, RUB:Std | -2 | RUB curves |
| RUB:EUROBOND | -2 | RUB Eurobond curve |

#### StrCommodity Floors

| Instrument | Market Parameter | Index | Floor |
|------------|-----------------|-------|-------|
| Commodity | Market rates | AG LBMA | -5 |
| Commodity | Market rates | AU LBMA | -5 |
| Commodity | Market rates | PD LPPM | -2.5 |
| Commodity | Market rates | PT LPPM | -2.5 |
| Commodity | Market rates | RH LPPM | -1.5 |
| Commodity | Smile Index | AG LBMA/CMX | 0 |
| Commodity | Smile Index | AU LBMA/CMX | 0 |
| Commodity | Smile Index | PD LPPM/NMX | 0 |
| Commodity | Smile Index | PT LPPM/NMX | 0 |

#### TotalStr and TotalStrCRD Floors

Same commodity floors as StrCommodity, plus:

| Risk Class | Instrument | Market Parameter | Floor |
|------------|------------|-----------------|-------|
| TotalStr | Rates | Zero coupons | -0.5 |
| TotalStrCRD | Rates | Zero coupons | -0.5 |

---

## 9. Zero Coupon Interpolation

| Parameter | Configuration |
|-----------|---------------|
| Propagation Mode | No propagation |
| Rate/Rate Propagation | Disabled |
| Rate/Credit Propagation | Disabled |
| Rate/FX Propagation | Disabled |
| Interpolation | Linear between surrounding shifts |
| Extrapolation Before | Flat |
| Extrapolation After | Flat |

---

## 10. Proxies Configuration

Proxying is the method of replacing one risk factor variation with another.

| Configuration | Setting |
|--------------|---------|
| Proxy Module | Not used for Stress Testing |
| Proxying Location | Performed in FMDM/Asset Control |
| Timing | Prior to sending shifts to Murex |

**Note**: If linear regression is used, beta calibration can be performed outside Murex.

---

## 11. File Storage Locations

| Component | Path |
|-----------|------|
| Processing Script | /apps/murex/client/scripts/var/eod/startvareod.sh |
| Export Configuration | /apps/murex/mx/fs/public/mxres/mxmarketrisk_service/scripts/ant-targets-sources-EOD.mxres |
| Revaluation Runs | /apps/murex/mx/mra_sources/mrb_run_0 (ser files) |
| Normalized Results | /apps/murex/mx/mra_sources/mr_engine_all (ser files) |
| Raw Reports | [App directory]/reports/today/eod/source_dump |
| Final Reports | [App directory]/reports/today/eod/ |
| Format Script | /apps/murex/client/scripts/var/eod/formatriskreport.sh |

---

*Document Version: 1.0 | Last Updated: 2025-01-13*
