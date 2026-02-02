---
# Document Metadata
document_id: IRV-CFG-001
document_name: IR Vega Sensitivities - IT Configuration Document
version: 1.0
effective_date: 2025-01-13
next_review_date: 2026-01-13
owner: Market Risk Technology
approving_committee: Risk Technology Change Board

# Taxonomy Reference
parent_node: L7-Systems/market-risk/feeds/ir-vega
feed_family: IR Vega
document_type: IT-Config
---

# IR Vega Sensitivities - IT Configuration Document

**Meridian Global Bank - Market Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | IRV-CFG-001 |
| **Version** | 1.0 |
| **Effective Date** | 13 January 2025 |
| **Owner** | Market Risk Technology |

---

## 1. Overview

This document describes the Murex Global Operating Model (GOM) configuration for the IR Vega Sensitivities feed. The feed calculates interest rate volatility sensitivities (Vega) for option products.

### 1.1 Component Summary

| Component | Name | Purpose |
|-----------|------|---------|
| Simulation View | IRPV01_VEGAS | Vega calculation with formula outputs |
| Datamart Table | A_IR_VEGA.REP | Sensitivity data storage |
| Dynamic Table | A_IRPV01_VEGA | Feeder target table |
| Feeder | A_IRPV01_VEGA | Populates datamart from simulation |
| Data Extractor | DE_IRD_PV01VEGA | Extracts data to CSV |
| Extraction Request | IRPV01_Vega_ZAR | SQL extraction definition |

---

## 2. Market Data Sets

| Region | Market Data Set | Description |
|--------|-----------------|-------------|
| London | LNCLOSE | London close official rates |
| Hong Kong | HKCLOSE | Hong Kong close official rates |
| New York | NYCLOSE | New York close official rates |
| Sao Paulo | SPCLOSE | Sao Paulo close official rates |

---

## 3. Simulation View: IRPV01_VEGAS

### 3.1 View Overview

| Attribute | Value |
|-----------|-------|
| **View Name** | IRPV01_VEGAS |
| **Output Count** | 6 active (9 hidden) |
| **Breakdown Count** | 13 active (7 hidden) |
| **Filter** | Opt_Maturity_Date NOT EMPTY |

### 3.2 Active Outputs

| Output | Dictionary Path | Definition |
|--------|-----------------|------------|
| **Vega_Local** | Output formulas.Numeric | IR Vega in deal currency (formula-based) |
| **Vega_USD** | Output formulas.Numeric | IR Vega in USD (formula-based) |
| **Vega_ZAR** | Output formulas.Numeric | IR Vega in ZAR (deprecated) |
| **ATM_Spread** | Output formulas.Numeric | At-the-money spread (formula-based) |
| **Opt_Maturity** | Output formulas.Numeric | Option maturity pillar (formula-based) |
| **Opt_Maturity_Date** | Output formulas.Numeric | Option maturity date (formula-based) |

### 3.3 Hidden Underlying Outputs

| Output | Dictionary Path | Definition |
|--------|-----------------|------------|
| **Vega_Yield** | Risk Engine.Results.Outputs.Interest rates.Vega.Yield.Value | Sensitivity to yield volatility (deal currency) |
| **Vega_Yield_USD** | Risk Engine.Results.Outputs.Interest rates.Vega.Yield.Value | Sensitivity to yield volatility (USD) |
| **Vega_Yield_ZAR** | Risk Engine.Results.Outputs.Interest rates.Vega.Yield.Value | Sensitivity to yield volatility (ZAR) - deprecated |
| **Flat_Vega** | Risk Engine.Results.Outputs.Interest rates.Vega.Flat.Value | Cap/Floor flat vega (deal currency) |
| **Flat_Vega_USD** | Risk Engine.Results.Outputs.Interest rates.Vega.Flat.Value | Cap/Floor flat vega (USD) |
| **Flat_Vega_ZAR** | Risk Engine.Results.Outputs.Interest rates.Vega.Flat.Value | Cap/Floor flat vega (ZAR) |
| **Normal_Vega** | Risk Engine.Results.Outputs.Interest rates.Vega.Normal.Value | Normal distribution vega (deal currency) |
| **Nor_Vega_USD** | Risk Engine.Results.Outputs.Interest rates.Vega.Normal.Value | Normal distribution vega (USD) |
| **Nor_Vega_ZAR** | Risk Engine.Results.Outputs.Interest rates.Vega.Normal.Value | Normal distribution vega (ZAR) - deprecated |

### 3.4 Output Formula Logic

The formula-based outputs select the appropriate underlying vega type:

```
IF Group == "CF" AND Vol_nature <> "Normal" THEN
{
    Vega_Local := Flat_Vega,
    Vega_USD := Flat_Vega_USD,
    Vega_ZAR := Flat_Vega_ZAR,
    Opt_Maturity := Opt_Maturity_Yield,
    Opt_Maturity_Date := Opt_Maturity_Yield_Date,
    ATM_Spread := ATM_Spread_Yield
}

ELSE IF (Group == "OSWP" OR Group == "CF" OR
         Typology == "CRD - GUARANTEE" OR
         Typology == "CRD - INSURANCE" OR
         Typology == "IRD - CAPS/FLOORS")
         AND Vol_nature == "Normal" THEN
{
    Vega_Local := Normal_Vega,
    Vega_USD := Nor_Vega_USD,
    Vega_ZAR := Nor_Vega_ZAR,
    Opt_Maturity := Opt_Maturity_Nor,
    Opt_Maturity_Date := Opt_Maturity_Nor_Date,
    ATM_Spread := ATM_Spread_Nor
}

ELSE
{
    Vega_Local := Vega_Yield,
    Vega_USD := Vega_Yield_USD,
    Vega_ZAR := Vega_Yield_ZAR,
    Opt_Maturity := Opt_Maturity_Yield,
    Opt_Maturity_Date := Opt_Maturity_Yield_Date,
    ATM_Spread := ATM_Spread_Yield
};
```

### 3.5 Active Breakdowns

| Breakdown | Dictionary Path | Definition |
|-----------|-----------------|------------|
| **Currency** | Risk Engine.Results.Outputs.Interest rates.Vega.Yield.Vega key.Currency | IR Vega currency |
| **Trade Number** | - | Unique trade identifier |
| **Portfolio** | - | Trading book |
| **Closing Entity** | - | Legal entity |
| **Family** | - | Deal family (IRD, CRD) |
| **Group** | - | Deal group (OSWP, CF, CDS) |
| **Type** | - | Deal type |
| **PL Instrument** | - | Index reference |
| **Strike** | Risk Engine.Source.Trade.Elements.Body.Body desc.Option.Strike | Option strike |
| **Typology** | - | Product classification |
| **Vol_nature** | Risk Engine.Results.Outputs.Interest rates.Vega.Yield.Vega key.Vol curve.Vol. nature | Volatility nature |
| **Opt_Maturity_Yield** | Risk Engine.Results.Outputs.Interest rates.Vega.Yield.Opt.maturity | Option maturity pillar (yield) |
| **Und. Maturity** | Risk Engine.Results.Outputs.Interest rates.Vega.Yield.Und.maturity | Underlying maturity pillar |

### 3.6 Hidden Breakdowns

| Breakdown | Dictionary Path | Definition |
|-----------|-----------------|------------|
| **ATM_Spread_Yield** | Risk Engine.Results.Outputs.Interest rates.Vega.Yield.ATM Spread | ATM spread (yield vol) |
| **Opt_Maturity_Yield_Date** | Risk Engine.Results.Outputs.Interest rates.Vega.Yield.Opt.maturity | Option maturity date (yield) |
| **Opt_Maturity_Nor** | Risk Engine.Results.Outputs.Interest rates.Vega.Normal.Opt.maturity | Option maturity pillar (normal) |
| **Opt_Maturity_Nor_Date** | Risk Engine.Results.Outputs.Interest rates.Vega.Normal.Opt.maturity | Option maturity date (normal) |
| **ATM_Spread_Nor** | - | ATM spread (normal vol) |
| **Strike1** | - | ATM strike from volatility curve |

---

## 4. Datamart Tables

### 4.1 Primary Table: A_IR_VEGA.REP

| Attribute | Value |
|-----------|-------|
| **Table Name** | A_IR_VEGA.REP |
| **Alternative** | A_IRPV01_VEGA.REP |
| **Type** | Datamart reporting table |
| **Content** | IR Vega sensitivities by trade, maturity |

### 4.2 Key Columns

| Column | Type | Description |
|--------|------|-------------|
| M_TRADE_NUM | Numeric | Trade number |
| M_CURRENCY | VarChar | Vega currency |
| M_FAMILY | VarChar | Deal family |
| M_GROUP | VarChar | Deal group |
| M_TYPE | VarChar | Deal type |
| M_CATEGO | VarChar | Category |
| M_PORTFOLIO | VarChar | Portfolio |
| M_COSTCENT | VarChar | Cost centre |
| M_OPT__MATU | VarChar | Option maturity pillar |
| M_OPT__MATUD | Date | Option maturity date |
| M_UND__MATU | VarChar | Underlying maturity pillar |
| M_UND__MATUD | Date | Underlying maturity date |
| M_STRIKE | Numeric | Option strike |
| M_ATM_SPREA | Numeric | ATM spread |
| M_VEGA_LOCA | Numeric | Vega (local currency) |
| M_VEGA_USD | Numeric | Vega (USD) |
| M_VEGA_ZAR | Numeric | Vega (ZAR) |
| M_TYPOLOGY | VarChar | Typology |
| M_PL_INSTRU | VarChar | PL Instrument |
| M_STRIKE1 | Numeric | ATM strike |
| M_LEGAL_ENT | VarChar | Legal entity |
| M_CLOSING_E | VarChar | Closing entity |
| M_REF_DATA | Numeric | Reference data key |

### 4.3 Reference Tables

| Table | Purpose | Join Key |
|-------|---------|----------|
| **SB_RT_INDEX_REP** | Interest rate index definition | M_INDEX |
| **TBL_ADP_RT_RANGE_REP** | Range accrual range definition | M_RNG_NB (Trade Number) |
| **TBL_MD_FXSPOTS_REP** | FX spot rates | M_NUMERATOR/M_DENUMERAT |
| **DYN_AUDIT_REP** | Dynamic table audit | M_OUTPUTTBL, M_TAG_DATA |

---

## 5. Feeder Configuration

### 5.1 Feeder Summary

| Attribute | Value |
|-----------|-------|
| **Feeder Name** | A_IRPV01_VEGA |
| **Source** | IRPV01_VEGAS Simulation View |
| **Target** | A_IR_VEGA.REP Datamart Table |
| **Dynamic Table** | A_IRPV01_VEGA |

### 5.2 Regional Feeder Configuration

#### London Region (3 Batches - Legacy)

| Batch | Processing Script | Global Filter | Portfolio Nodes |
|-------|-------------------|---------------|-----------------|
| BF_PRVIRVEA_LN | LN_IRVEGA_FDR | BF_PRVIRVEA_LN | FXDLN, PMLN |
| BF_PRVIRVEB_LN | LN_IRVEGA_FDR | BF_PRVIRVEB_LN | IRLNSBL |
| BF_PRVIRVEC_LN | LN_IRVEGA_FDR | BF_PRVIRVEC_LN | LMLNSBL |

**Note**: London uses 3 batches due to historical Murex processing constraints in older versions.

#### Hong Kong Region

| Batch | Processing Script | Global Filter | Portfolio Nodes |
|-------|-------------------|---------------|-----------------|
| B_A_PRVIRVE_HKG | HK_IRVEGA_FDR | B_A_PRVFXDE_HKG | FXDHK, FXDHKSBA, FXHKSBL, HKSBSA, LMHKSBL, LMHKSBL01, LMHKSBL02, LMHKSBLC1-C9, LMHKSBLCL, LMHKSBLP1, LMHKSBLPROP, LMHKSBLR1, LMHKSBLR2, LMHKSBLSO, LMHKSBLT1, LMHKSBLT2, LMHKSBLTP, LMHKSGACU, LMHKSGDBU, PMSG |

#### New York Region

| Batch | Processing Script | Global Filter | Portfolio Nodes |
|-------|-------------------|---------------|-----------------|
| B_A_PRVIRVE_NYK | NY_IRVEGA_FDR | B_A_PRVFXDE_NYK | FXNYSBL, FXNYSBLSPROPOP1, FXNYSBLSPROPOP2, LMNYSBL, LMNYSBLLEMI1, LMNYSBLLEMT1, LMNYSBLSO, NYSBSA, PMNY |

#### Sao Paulo Region

| Batch | Processing Script | Global Filter | Portfolio Nodes |
|-------|-------------------|---------------|-----------------|
| B_A_PRVIRVE_SAO | SP_IRVEGA_FDR | B_A_PRVFXDE_SAO | CTBASBLALL, CTSPSBLALL, LMBASBLALL, LMSPBSI, LMSPFIA, LMSPFND, LMSPSBLALL, LMSPSBLSO |

### 5.3 Portfolio Filtering Note

**Issue**: Current configuration mixes Level 4 and Level 5 portfolio nodes:
- London: Uses Level 4 nodes appropriately
- Other Regions: Mix of Level 4 (PM portfolios) and Level 5 (all others)
- Includes inactive portfolios (e.g., FXDHK, LMHKSBL01)

**Recommendation**: Standardize to Level 4 portfolio nodes only.

---

## 6. Extraction Configuration

### 6.1 Processing Scripts

| Region | Processing Script | Batch Extraction | Single Extraction |
|--------|-------------------|------------------|-------------------|
| HKG | HK_VSPA_IRVEGA_RPT | BE_PRVIRVE_HKG | DE_IRD_PV01VEGA |
| LDN | LN_VSPA_IRVEGA_RPT | BE_PRVIRVE_LDN | DE_IRD_PV01VEGA |
| NYK | NY_VSPA_IRVEGA_RPT | BE_PRVIRVE_NYK | DE_IRD_PV01VEGA |
| SAO | SP_VSPA_IRVEGA_RPT | BE_PRVIRVE_SAO | DE_IRD_PV01VEGA |

### 6.2 Extraction Request: IRPV01_Vega_ZAR

The extraction request uses a SQL query to join vega data with reference tables:

```sql
SELECT IR_VEGA.M_TRADE_NUM ,
       COALESCE(RT_INDEX.M_CURRENCY, IR_VEGA.M_CURRENCY) AS CURRENCY ,
       IR_VEGA.M_FAMILY ,
       IR_VEGA.M_GROUP ,
       IR_VEGA.M_TYPE ,
       IR_VEGA.M_CATEGO,
       IR_VEGA.M_PORTFOLIO AS PORTFOLIO ,
       IR_VEGA.M_COSTCENT ,
       IR_VEGA.M_OPT__MATU ,
       COALESCE(TO_CHAR(M_OPT__MATUD, 'DD/MM/YYYY'), '') ,
       IR_VEGA.M_UND__MATU ,
       IR_VEGA.M_UND__MATUD ,
       IR_VEGA.M_STRIKE ,
       IR_VEGA.M_ATM_SPREA ,
       -- Vega Local: Convert from USD if range accrual with FX available
       CASE WHEN RT_INDEX.M_CURRENCY IS NOT NULL
            THEN (CASE WHEN FXSPOTS.M_DISCOUNTE IS NULL
                       THEN 1
                       ELSE FXSPOTS.M_DISCOUNTE END) * IR_VEGA.M_VEGA_USD
            ELSE IR_VEGA.M_VEGA_LOCA END ,
       -- JBSBSA Flag
       CASE WHEN IR_VEGA.M_CLOSING_E = 'JBSBSA'
            THEN 'Y'
            ELSE 'N' END ,
       IR_VEGA.M_VEGA_USD ,
       IR_VEGA.M_VEGA_ZAR ,
       IR_VEGA.M_TYPOLOGY ,
       IR_VEGA.M_PL_INSTRU ,
       IR_VEGA.M_STRIKE1

FROM DM.A_IR_VEGA_REP IR_VEGA

-- Join to Range Accrual definition
LEFT OUTER JOIN DM.TBL_ADP_RT_RANGE_REP RT_RANGE
  ON RT_RANGE.M_RNG_NB = IR_VEGA.M_TRADE_NUM
  AND RT_RANGE.M_REF_DATA IN (
      SELECT M_REF_DATA
      FROM DM.DYN_AUDIT_REP
      WHERE M_OUTPUTTBL = 'TBL_ADP_RT_RANGE.REP'
        AND M_TAG_DATA = @MxTagData:C
        AND TO_CHAR(M_DATEKEY) = @MxReportingDate:D
  )

-- Join to Interest Rate Index for currency
LEFT OUTER JOIN DM.SB_RT_INDEX_REP RT_INDEX
  ON RT_INDEX.M_INDEX = RT_RANGE.M_RNG_INDEX
  AND RT_INDEX.M_REF_DATA = @MxHistoricalData:N

-- Join to FX Spots for currency conversion
LEFT OUTER JOIN DM.TBL_MD_FXSPOTS_REP FXSPOTS
  ON COALESCE(RT_INDEX.M_CURRENCY, IR_VEGA.M_CURRENCY) =
     (CASE WHEN FXSPOTS.M_NUMERATOR = 'USD'
           THEN FXSPOTS.M_DENUMERAT
           ELSE FXSPOTS.M_NUMERATOR END)
  AND FXSPOTS.M_DATE = @MxReportingDate:D
  AND FXSPOTS.M_MARKETSET = @MxMarketSet:C
  AND 'USD' IN (FXSPOTS.M_NUMERATOR, FXSPOTS.M_DENUMERAT)
  AND FXSPOTS.M_REF_DATA IN (
      SELECT M_REF_DATA
      FROM DM.DYN_AUDIT_REP
      WHERE M_OUTPUTTBL = 'TBL_MD_FXSPOTS.REP'
        AND M_TAG_DATA = @MxTagMarketData:C
        AND TO_CHAR(M_DATEKEY) = @MxReportingDate:D
  )

WHERE IR_VEGA.M_REF_DATA = @MxDataSetKey:N
  AND @MxSQLExpression:C  -- Legal Entity filter: IR_VEGA.M_LEGAL_ENT<>'SBSA'
  AND (IR_VEGA.M_FAMILY = 'IRD' OR IR_VEGA.M_TYPOLOGY IN ('CRD - GUARANTEE', 'CRD - INSURANCE'))
  AND IR_VEGA.M_GROUP <> 'OPT'  -- Exclude bond options
  AND (rtrim(COALESCE(RT_INDEX.M_CURRENCY, IR_VEGA.M_CURRENCY)) = 'USD'
       OR FXSPOTS.M_DATE IS NOT NULL)

ORDER BY PORTFOLIO, CURRENCY, IR_VEGA.M_TRADE_NUM
```

### 6.3 SQL Logic Explained

| Step | Logic | Purpose |
|------|-------|---------|
| 1 | Select from A_IR_VEGA_REP | Base vega sensitivity data |
| 2 | LEFT JOIN TBL_ADP_RT_RANGE_REP | Get range accrual definition by trade number |
| 3 | LEFT JOIN SB_RT_INDEX_REP | Get interest rate index currency for range accruals |
| 4 | LEFT JOIN TBL_MD_FXSPOTS_REP | Get FX spot rate for currency conversion |
| 5 | COALESCE currency | Use index currency if range accrual, else trade currency |
| 6 | Convert Vega Local | Multiply USD vega by FX if range accrual |
| 7 | Filter products | IRD family or CRD guarantee/insurance |
| 8 | Exclude bond options | Group <> 'OPT' |
| 9 | Filter entity | Exclude SBSA |
| 10 | Filter FX availability | Only include if USD or FX rate available |

### 6.4 Expression Filter

```
@MxSQLExpression: IR_VEGA.M_LEGAL_ENT<>'SBSA'
```

This excludes the SBSA legal entity from all regional extractions.

---

## 7. Output Configuration

### 7.1 File Details

| Attribute | Value |
|-----------|-------|
| **File Pattern** | MxGTS_Vespa_IR_Vega_{Region}_{YYYYMMDD}.csv |
| **Output Path** | ./reports/today/eod |
| **Delimiter** | Semicolon (;) |
| **Field Count** | 20 |
| **Packaging Script** | process_reports.sh |
| **Package Name** | MxGTS_Vespa_Sensitivities_{Region}_{YYYYMMDD}.zip |

### 7.2 Regional File Names

| Region | File Name Pattern |
|--------|-------------------|
| LDN | MxGTS_Vespa_IR_Vega_LN_{YYYYMMDD}.csv |
| HKG | MxGTS_Vespa_IR_Vega_HK_{YYYYMMDD}.csv |
| NYK | MxGTS_Vespa_IR_Vega_NY_{YYYYMMDD}.csv |
| SAO | MxGTS_Vespa_IR_Vega_SP_{YYYYMMDD}.csv |

---

## 8. Delivery Configuration

### 8.1 MFT Transfer IDs

| Destination | MFT ID Pattern |
|-------------|----------------|
| Plato | MurexGTSSensitivitiesToPlato_{Region} |
| RDS | MurexGTSSensitivitiesToRDS_{Region} |

### 8.2 Regional MFT IDs

| Region | Plato MFT ID | RDS MFT ID |
|--------|--------------|------------|
| LDN | MurexGTSSensitivitiesToPlato_LN | MurexGTSSensitivitiesToRDS_LN |
| HKG | MurexGTSSensitivitiesToPlato_HK | MurexGTSSensitivitiesToRDS_HK |
| NYK | MurexGTSSensitivitiesToPlato_NY | MurexGTSSensitivitiesToRDS_NY |
| SAO | MurexGTSSensitivitiesToPlato_SP | MurexGTSSensitivitiesToRDS_SP |

---

## 9. Processing Schedule

| Step | Component | Time (GMT) | Description |
|------|-----------|------------|-------------|
| 1 | Market Data | 18:00 | London close |
| 2 | Valuation | 21:00 | Batch complete |
| 3 | Feeder | 02:30 | **_IRVEGA_FDR start |
| 4 | Feeder | 03:30 | Feeder complete |
| 5 | Extraction | 04:00 | **_VSPA_IRVEGA_RPT start |
| 6 | File Gen | 04:30 | CSV generation |
| 7 | Packaging | 05:00 | ZIP creation |
| 8 | MFT | 05:30 | Delivery |

---

## 10. Configuration Change Log

| Date | Change | Impact | Approver |
|------|--------|--------|----------|
| 2025-01-13 | Initial documentation | Documentation only | Risk Tech |

---

*End of Document*
