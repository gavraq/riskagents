# Value at Risk (VaR) P&L Strips Feed - IT Configuration

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
│  • ***_1DVAR        • ***_10DVAR                   │
│  • ***_10DSVAR      • ***_10DESVAR                 │
└────────────────────────┬────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│               Datamart Tables                       │
│                                                     │
│  MRA_EXPORT_***_1DVAR_REP                          │
│  MRA_EXPORT_***_10DVAR_REP                         │
│  MRA_EXPORT_***_10DSVAR_REP                        │
│  MRA_EXPORT_***_10DESVAR_REP                       │
└────────────────────────┬────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                  Extractions                        │
│                                                     │
│  DE_1DVAR_SB / DE_1DVAR_D_SB                       │
│  DE_10DVAR_SB / DE_10DVAR_D_SB                     │
│  DE_10DSVAR_SB / DE_10DSVAR_D_SB                   │
│  DE_10DESVAR_SB                                     │
└────────────────────────┬────────────────────────────┘
                         │
                         ▼  formatriskreport.sh
┌─────────────────────────────────────────────────────┐
│               P&L Strip Files                       │
│                                                     │
│  P&LStrips_MxGts_***_{VaR_Type}_All_yyyymmdd.zip   │
└─────────────────────────────────────────────────────┘
```

---

## 2. Market Data Sets

VaR uses dedicated market data sets different from closing sets used for sensitivities:

| Region | VaR Market Data Set | Description |
|--------|---------------------|-------------|
| London | LNVARVAL | London VaR valuation |
| Hong Kong | SGVARVAL | Singapore/HK VaR valuation |
| New York | NYVARVAL | New York VaR valuation |
| São Paulo | SPVARVAL | São Paulo VaR valuation |

**Note**: These market data sets are specific to VaR and distinct from the LNCLOSE, HKCLOSE, etc. used for sensitivity calculations.

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

**Note**: No additional filters (typology, P&L instruments, etc.) are applied for VaR - all trades in the combined portfolios are included.

---

## 4. Scenario Generation

### 4.1 Market Risk Single Reports

Scenarios are generated using Market Risk Single Reports which import variation data from external sources:

| Risk Factor | ASCII File Pattern | Variation Type | Import Type |
|-------------|--------------------|----------------|-------------|
| Security Spot | vaV1D_price_LDN.txt | Standard | Time series |
| Security Volatility | vaV1D_vol.txt | Percentage (%) | Time series |
| FX Spot | vaV1D_fxspt.txt | Percentage (%) | Time series |
| Zero Coupons | vaV1D_zc.txt | Standard | Time series |
| Swaption Volatility | vaV1D_swv.txt | Percentage (%) | Time series |
| Cap Floors Volatility | vaV1D_cfv.txt | Percentage (%) | Time series |
| FX Smile | vaV1D_fxsmc.txt | Percentage (%) | Time series |
| CRD Market Rates | vaV1D_cdmr_LDN.txt | Standard | Time series |
| Commodity Market Rates | vaV1D_cmr_fut.txt | Percentage (%) | Time series |
| Commodity Smile | vaV1D_cms.txt | Percentage (%) | Time series |

### 4.2 Commodity Market Rates Appender

Some commodity scenarios require separate import due to different file formats:

| Description | Type | ASCII File | Import Type |
|-------------|------|------------|-------------|
| Commodity Market Rates | Standard | var_V1D_cmr.txt | Import variation from ASCII |

---

## 5. Scenario Containers

### 5.1 Container Configuration by Region and VaR Type

| Region | 1D VaR | 10D VaR | 10D SVaR | 10D ESVaR |
|--------|--------|---------|----------|-----------|
| LDN | LDN_cont1DVaR | LDN_cont10DVaR | LDN_cont10DSVaR | LDN_cont10DESVaR |
| HKG | HKG_cont1DVaR | HKG_cont10DVaR | HKG_cont10DSVaR | HKG_cont10DESVaR |
| NYK | NYK_cont1DVaR | NYK_cont10DVaR | NYK_cont10DSVaR | NYK_cont10DESVaR |
| SAO | SAO_cont1DVaR | SAO_cont10DVaR | SAO_cont10DSVaR | SAO_cont10DESVaR |

### 5.2 Volatility Configuration

Settings stored at scenario container level:

| Scenario Type | Smile Mode |
|---------------|------------|
| Security Smile | Spread |
| FX Smile | Absolute |
| Cap Floors Smile | Spread |
| Swaption Smile | Spread |
| Commodity Smile | Absolute |
| Correlation Smile | Spread |
| Inflation Cap Floors | Spread |
| Credit Smile | Spread |

### 5.3 Open Days Calendar

| Setting | Value |
|---------|-------|
| Calendar | VAR_SCN |
| Open Days Only | Enabled |
| Non-Open Days | Weekends, 1st January |
| Special Open Days | 01 Jan 2008, 01 Jan 2009, 01 Jan 2010, 01 Jan 2013 |

---

## 6. Revaluation Run Configuration

### 6.1 VaR Run Parameters

| Region | VaR Type | Revaluation Run | Scenario Container | Market Data | Currency |
|--------|----------|-----------------|-------------------|-------------|----------|
| HKG | 1DVAR | HKG_1DVAR | HKG_cont1DVaR | SGVARVAL | USD |
| HKG | 10DVAR | HKG_10DVAR | HKG_cont10DVaR | SGVARVAL | USD |
| HKG | 10DSVAR | HKG_10DSVAR | HKG_cont10DSVaR | SGVARVAL | USD |
| HKG | 10DESVAR | HKG_10DESVAR | HKG_cont10DESVaR | SGVARVAL | USD |
| LDN | 1DVAR | LDN_1DVAR | LDN_cont1DVaR | LNVARVAL | USD |
| LDN | 10DVAR | LDN_10DVAR | LDN_cont10DVaR | LNVARVAL | USD |
| LDN | 10DSVAR | LDN_10DSVAR | LDN_cont10DSVaR | LNVARVAL | USD |
| LDN | 10DESVAR | LDN_10DESVAR | LDN_cont10DESVaR | LNVARVAL | USD |
| NYK | 1DVAR | NYK_1DVAR | NYK_cont1DVaR | NYVARVAL | USD |
| NYK | 10DVAR | NYK_10DVAR | NYK_cont10DVaR | NYVARVAL | USD |
| NYK | 10DSVAR | NYK_10DSVAR | NYK_cont10DSVaR | NYVARVAL | USD |
| NYK | 10DESVAR | NYK_10DESVAR | NYK_cont10DESVaR | NYVARVAL | USD |
| SAO | 1DVAR | SAO_1DVAR | SAO_cont1DVaR | SPVARVAL | USD |
| SAO | 10DVAR | SAO_10DVAR | SAO_cont10DVaR | SPVARVAL | USD |
| SAO | 10DSVAR | SAO_10DSVAR | SAO_cont10DSVaR | SPVARVAL | USD |
| SAO | 10DESVAR | SAO_10DESVAR | SAO_cont10DESVaR | SPVARVAL | USD |

### 6.2 Processing Script

**Script Path**: `/apps/murex/client/scripts/var/eod/startvareod.sh`

**Parameters**:
- Region: HKG, LDN, NYK, SAO
- Risk Metric: VaR/SVaR/ESVaR
- Time Period: 1 (for 1 day) or 10 (for 10 day)
- Currency: N/A

---

## 7. Risk Class Configuration

### 7.1 Full Revaluation Outputs Template

| Risk Class | Template | Risk Factors Selected |
|------------|----------|----------------------|
| Commodities | VAR_FullRevalOutput | Commodity market rates, Commodity Smile |
| FX | VAR_FullRevalOutput | FX Spot |
| FXVol | VAR_FullRevalOutput | FX Volatility*, FX Smile |
| GenFX | VAR_FullRevalOutput / ESVAR_FullRevalOutput | FX Spot, FX Volatility*, FX Smile |
| GenIR | VAR_FullRevalOutput / ESVAR_FullRevalOutput | Security Volatility, Zero coupons, Swaption Vol, Cap Floors Vol |
| IR | VAR_FullRevalOutput | Zero coupons |
| IRVol | VAR_FullRevalOutput | Security Volatility, Swaption Vol, Cap Floors Vol |
| Total | VAR_FullRevalOutput / ESVAR_FullRevalOutput | All except Security Spot & CRD Market Rates |
| TotalCRD | VAR_FullRevalOutput / ESVAR_FullRevalOutput | All risk factors |

### 7.2 TotalCRD Instrument Configuration

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
✗ Bond credit spread
✗ Cap Floors Smile
✗ CRD default spread
✓ CRD Market rates
✗ Credit spread curves
✗ Repo margin
✓ Commodity market rates
✗ Recovery Rates
✗ Theoretical CMC
✗ Commodities volatility
✗ Market correlations
✗ Base correlations
✗ Inflation curves
✗ Market corr. upfront amt
✗ Credit Volatility
```

---

## 8. Revaluation Settings (VAR_RevalSetting)

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

---

## 9. Flooring Configuration

### 9.1 Floor Query (VaR/SVaR)

```sql
SELECT M_REF as Risk_Class,
       TRIM(M_LABEL0) as Instrument_Type,
       TRIM(M_LABEL1) as Market_Parameter,
       TRIM(M_LABEL2) as Curve_or_Index,
       TRIM(M_LABEL3) as Commodity_Index,
       M_FLOOR_VAL as Floor
FROM MX.VAR_FLCF_DBF
WHERE M_REF IN ('Commodities', 'FX', 'FXVol', 'GenFX', 'GenIR', 'IR', 'IRVol', 'Total', 'TotalCRD')
ORDER BY 1,2,3,4,5
```

### 9.2 Example Floor Configuration

| Risk Class | Curve | Floor | Cap |
|------------|-------|-------|-----|
| IR | AR1:Std | 0.00000 | 0.00000 |
| GenIR | AR1:Std | 0.00000 | 0.00000 |

**Note**: For ESVaR, similar configuration exists but filter is on 'GenIR' and 'GenFX' only.

---

## 10. Zero Coupon Interpolation

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

## 11. File Storage Locations

| Component | Path |
|-----------|------|
| Processing Script | /apps/murex/client/scripts/var/eod/startvareod.sh |
| Export Configuration | /apps/murex/mx/fs/public/mxres/mxmarketrisk_service/scripts/ant-targets-sources-EOD.mxres |
| Revaluation Runs | /apps/murex/mx/mra_sources/mrb_run_0 (ser files) |
| Normalized Results | /apps/murex/mx/mra_sources/mr_engine_all (ser files) |
| Raw Reports | [App directory]/reports/today/eod/source_dump |
| Final Reports | [App directory]/reports/today/eod/ |

---

*Document Version: 1.0 | Last Updated: 2025-01-13*
