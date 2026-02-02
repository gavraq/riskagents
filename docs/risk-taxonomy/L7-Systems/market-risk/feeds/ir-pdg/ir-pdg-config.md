---
# Document Metadata
document_id: PDG-CFG-001
document_name: IR Par Delta Gamma (PDG) - IT Configuration
version: 1.0
effective_date: 2025-01-03
next_review_date: 2026-01-03
owner: Product Control
approving_committee: Risk Technology Change Board

# Taxonomy Reference
parent_node: L7-Systems/market-risk/feeds/ir-pdg
feed_family: IR Par Delta Gamma
document_type: IT Config
---

# IR Par Delta Gamma (PDG) - IT Configuration

**Meridian Global Bank - Market Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | PDG-CFG-001 |
| **Version** | 1.0 |
| **Effective Date** | 3 January 2025 |
| **Owner** | Product Control |
| **Approver** | Risk Technology Change Board |

---

## 1. Overview

This document describes the Murex Global Operating Model (GOM) configuration for the IR Par Delta Gamma (PDG) feed. The feed combines IR Delta (par rate) and IR Gamma (par rate) sensitivities from two separate simulation views into a single output file for Product Control.

### 1.1 GOM Components

| Component | IR Delta | IR Gamma |
|-----------|----------|----------|
| **Simulation View** | MDS_IRPV01TTL | IRPV02_GAMMAS |
| **Dynamic Table** | A_IRD_IRPV01_TTL | A_IRPV02_GAMMA |
| **Datamart Table** | A_IRD_PV01_TTL.REP | A_IRPV02_GAMMA.REP |
| **Feeder** | A_IRD_PV01_TTL / A_IRD_PV01_TTL1 / A_IRD_PV01_TTL2 | TF_IRPV02_GAMMA |
| **Data Extractor** | DE_IRD_PV01_TTL | (merged in extraction) |
| **Extraction Request** | IRD_PV01_Par_Delta_Gamma_TLZAR | (single request) |

### 1.2 Additional Components

| Component | Purpose |
|-----------|---------|
| **Bond Notional Feeder** | A_BOND_NOTIONAL |
| **Bond Notional Table** | A_BOND_NOTIONAL.REP |
| **Reference Tables** | A_RTCT_REP, A_RATES_REP, TBL_BOND_MKTDATA_REP, SB_SE_RBC_REP, SB_TP_REP, SB_TP_BD_REP |

---

## 2. Market Data Sets

| Region | Market Data Set | Description |
|--------|-----------------|-------------|
| LDN | LNCLOSE | London EOD official rates |
| HKG | HKCLOSE | Hong Kong EOD official rates |
| NYK | NYCLOSE | New York EOD official rates |
| SAO | SPCLOSE | Sao Paulo EOD official rates |

---

## 3. Simulation Views

### 3.1 MDS_IRPV01TTL (IR Delta Par)

| Property | Value |
|----------|-------|
| **View Name** | MDS_IRPV01TTL |
| **Purpose** | IR Par Rate Delta Sensitivities |
| **Outputs** | 3 |
| **Breakdowns** | 16 |
| **Maturity Set** | LNOFFICIAL |

#### 3.1.1 Outputs

| Output | Dictionary Path | Description |
|--------|-----------------|-------------|
| DV01(par) | RiskEngine.Results.Outputs.Interest rates.Delta.Par.Value | IR Delta Par in native currency. Sensitivity of NPV to 1bp parallel shift in par yield curve. |
| DV01(par) USD | RiskEngine.Results.Outputs.Interest rates.Delta.Par.Value | IR Delta Par in USD. Uses zero day FX spot for conversion. |
| DV01(par) ZAR | RiskEngine.Results.Outputs.Interest rates.Delta.Par.Value | IR Delta Par in ZAR. **[DEPRECATED - should be decommissioned]** |

#### 3.1.2 Breakdowns

| Breakdown | Dictionary Path | Description |
|-----------|-----------------|-------------|
| Date | RiskEngine.Results.Outputs.Interest rates.Delta.Par.Date | Pillar date from maturity set LNOFFICIAL |
| Curve Name | RiskEngine.Results.Outputs.Interest rates.Delta.Par.Curve key.Curve name | Interest rate curve label |
| Currency | RiskEngine.Results.Outputs.Interest rates.Delta.Par.Curve key.Currency | Currency of the interest rate curve |
| Portfolio | Data.Trade.Portfolio | Trading portfolio |
| Trade Number | Data.Trade.Trade number | Unique trade identifier |
| Legal Entity | Data.Trade.Legal entity | Legal entity code |
| Closing Entity | Data.Trade.Closing entity | Closing entity (for ZAR flag) |
| Family | Data.Trade.Family | Product family |
| Group | Data.Trade.Group | Product group |
| Type | Data.Trade.Type | Product type |
| PL Instrument | Data.Trade.PL Instrument | P&L instrument |
| Sec Code | Data.Trade.Sec code | Security code |
| Sec Currency | Data.Trade.Sec currency | Security currency |
| Status | Data.Trade.Status | Trade status |
| Generator | RiskEngine.Results.Outputs.Interest rates.Delta.Par.Curve key.Generator | Rate generator |
| Typology | Data.Trade.Typology | Product classification |

#### 3.1.3 Maturity Set: LNOFFICIAL

| Label | Example Date (Ref: 02-Jun-2023) |
|-------|--------------------------------|
| O/N | 05 Jun 2023 |
| T/N | 06 Jun 2023 |
| 1W | 09 Jun 2023 |
| 2W | 16 Jun 2023 |
| 1M | 02 Jul 2023 |
| 2M | 02 Aug 2023 |
| 3M | 02 Sep 2023 |
| 6M | 02 Dec 2023 |
| 9M | 02 Mar 2024 |
| 1Y | 02 Jun 2024 |
| 2Y | 02 Jun 2025 |
| 3Y | 02 Jun 2026 |
| 5Y | 02 Jun 2028 |
| 7Y | 02 Jun 2030 |
| 10Y | 02 Jun 2033 |
| 15Y | 02 Jun 2038 |
| 20Y | 02 Jun 2043 |
| 30Y | 02 Jun 2053 |

### 3.2 IRPV02_GAMMAS (IR Gamma)

| Property | Value |
|----------|-------|
| **View Name** | IRPV02_GAMMAS |
| **Purpose** | IR Gamma (Convexity) Sensitivities |
| **Outputs** | 6 (3 Zero + 3 Par) |
| **Breakdowns** | 15 |
| **Maturity Set** | LNOFFICIAL |

**Important Note**: This simulation view produces both zero rate and par rate gamma outputs. The PDG extraction selects only the PAR outputs. The Market Risk IR Delta & Gamma feed extracts only the ZERO outputs from the same view.

#### 3.2.1 Outputs

| Output | Type | Description |
|--------|------|-------------|
| GAMMA_ZERO_CCY | Zero Rate | IR Gamma Zero in native currency - **NOT used in PDG** |
| GAMMA_ZERO_USD | Zero Rate | IR Gamma Zero in USD - **NOT used in PDG** |
| GAMMA_ZERO_ZAR | Zero Rate | IR Gamma Zero in ZAR - **NOT used in PDG** |
| GAMMA_PAR_CCY | Par Rate | IR Gamma Par in native currency - **Used in PDG** |
| GAMMA_PAR_USD | Par Rate | IR Gamma Par in USD - **Used in PDG** |
| GAMMA_PAR_ZAR | Par Rate | IR Gamma Par in ZAR - **Used in PDG (Deprecated)** |

#### 3.2.2 Breakdowns

| Breakdown | Description |
|-----------|-------------|
| Portfolio | Trading portfolio |
| Closing Entity | Closing entity code |
| Legal Entity | Legal entity code |
| Currency | Curve currency |
| Curve name | Interest rate curve |
| Trade Number | Trade identifier |
| Sec Code | Security code |
| Family | Product family |
| Group | Product group |
| Type | Product type |
| Generator | Rate generator |
| PL Instrument | P&L instrument |
| DatePar | Pillar date (Par) |
| Date | Pillar date |
| Typology | Product classification |

---

## 4. Feeders

### 4.1 IR Delta Feeders

The IR Delta feeders populate the A_IRD_PV01_TTL.REP datamart table.

#### 4.1.1 HKG Region

| Component | Value |
|-----------|-------|
| **Processing Script** | HK_IRPDG_FDR |
| **Batches of Feeders** | B_A_IRDPVTTLHKG |
| **Global Filter** | B_IRDPV01OHKG_ARC |
| **Portfolio Nodes** | FXHKSBL, LMHKSBL, PMSG |
| **Expression Filter** | .NOT.(TRN_GRP="CS".AND.(INSTRUMENT="SGD/USD F/F 6M".OR.INSTRUMENT="SGD/USD F/V 3M".OR.INSTRUMENT="SGD/USD V/V 6M")) |
| **Feeder** | A_IRD_PV01_TTL |
| **Dynamic Table** | A_IRD_IRPV01_TTL |
| **Simulation View** | MDS_IRPV01TTL |

**Additional HKG Feeders:**

| Feeder | Global Filter | Portfolio | Dynamic Table | Purpose |
|--------|---------------|-----------|---------------|---------|
| A_IRD_PV01_TTL1 | RBC_FILTER | STB_DUMMY_PTF | A_IRD_IRPV01_TTL | STB dummy portfolios |
| A_BOND_NOTIONAL | B_IRDPV01OHKG_ARC | FXHKSBL, LMHKSBL, PMSG | A_BOND_NOTIONAL | Bond notional data |

#### 4.1.2 LDN Region

| Component | Value |
|-----------|-------|
| **Processing Script** | LN_IRPDG_FDR |
| **Batches of Feeders** | B_A_IRDPVTTLLDN |
| **Global Filter** | B_IRDPV01OLDN_ARC |
| **Portfolio Nodes** | FXDLNSBL, FXLNSBL, IRLNSBL, JBSBSA, LMLNSBL, PMLNSBL |
| **Feeder** | A_IRD_PV01_TTL1 |
| **Dynamic Table** | A_IRD_IRPV01_TTL |
| **Simulation View** | MDS_IRPV01TTL |

**Additional LDN Feeders:**

| Feeder | Global Filter | Portfolio | Dynamic Table | Purpose |
|--------|---------------|-----------|---------------|---------|
| A_IRD_PV01_TTL2 | B_IRDPV01OLDN | FXDLNSBL, FXLNSBL, IFXMMLNIC, IFXMMLNLH, IRLNSBL, JBSBSA, LMLNSBL, PMLN | A_BOND_NOTIONAL | Bond notional data |
| A_IRD_PV01_TTL1 | RBC_FILTER | STB_DUMMY_PTF | A_IRD_IRPV01_TTL | STB dummy portfolios |

**Note**: The Bond Notional feeder includes IFXMMLNIC and IFXMMLNLH portfolios which are no longer used.

#### 4.1.3 NYK Region

| Component | Value |
|-----------|-------|
| **Processing Script** | NY_IRPDG_FDR |
| **Batches of Feeders** | B_A_IRDPVTTLNYK |
| **Global Filter** | B_IRDPV01ONYK_ARC |
| **Portfolio Nodes** | FXNYSBL, LMNYSBL, PMNY |
| **Feeder** | A_IRD_PV01_TTL1 |
| **Dynamic Table** | A_IRD_IRPV01_TTL |
| **Simulation View** | MDS_IRPV01TTL |

**Additional NYK Feeders:**

| Feeder | Global Filter | Portfolio | Dynamic Table | Purpose |
|--------|---------------|-----------|---------------|---------|
| A_IRD_PV01_TTL1 | RBC_FILTER | STB_DUMMY_PTF | A_IRD_IRPV01_TTL | STB dummy portfolios |
| A_BOND_NOTIONAL | B_IRDPV01ONYK_ARC | FXNYSBL, LMNYSBL, PMNY | A_BOND_NOTIONAL | Bond notional data |

#### 4.1.4 SAO Region

| Component | Value |
|-----------|-------|
| **Processing Script** | SP_IRPDG_FDR |
| **Batches of Feeders** | B_A_IRDPVTTLSAO |
| **Global Filter** | B_IRDPV01OSAO_ARC |
| **Portfolio Nodes** | LMSPBSI, LMSPFIA, LMSPFND, LMSPSBL |
| **Feeder** | A_IRD_PV01_TTL |
| **Dynamic Table** | A_IRD_IRPV01_TTL |
| **Simulation View** | MDS_IRPV01TTL |

**Additional SAO Feeders:**

| Feeder | Global Filter | Portfolio | Dynamic Table | Purpose |
|--------|---------------|-----------|---------------|---------|
| A_IRD_PV01_TTL1 | RBC_FILTER | STB_DUMMY_PTF | A_IRD_IRPV01_TTL | STB dummy portfolios |
| A_BOND_NOTIONAL | B_IRDPV01OSAO_ARC | LMSPBSI, LMSPFIA, LMSPFND, LMSPSBL | A_BOND_NOTIONAL | Bond notional data |

### 4.2 IR Gamma Feeders

The IR Gamma feeders populate the A_IRPV02_GAMMA.REP datamart table. Product filtering restricts to Caps/Floors (IRD|CF|) and Swaptions (IRD|OSWP|).

| Region | Processing Script | Batches | Global Filter | Portfolio Nodes | Feeder |
|--------|-------------------|---------|---------------|-----------------|--------|
| HKG | BF_PRVIRGAM_HK | BF_PRVIRGAM_HK | GF_PRVIRGAM_HK | LMHK, PMSG | TF_IRPV02_GAMMA |
| LDN | BF_PRVIRGAM_LN | BF_PRVIRGAM_LN | GF_PRVIRGAM_LN | FXDLN, IRLN, LMLN, PMLN | TF_IRPV02_GAMMA |
| NYK | BF_PRVIRGAM_NY | BF_PRVIRGAM_NY | GF_PRVIRGAM_NY | LMNY, PMNY | TF_IRPV02_GAMMA |
| SAO | BF_PRVIRGAM_SP | BF_PRVIRGAM_SP | GF_PRVIRGAM_SP | LMSP | TF_IRPV02_GAMMA |

**Product Filter**: All global filters include Family/Group/Type filter for:
- IRD|CF| (Caps/Floors)
- IRD|OSWP| (Swaptions)

---

## 5. Datamart Tables

### 5.1 A_IRD_PV01_TTL.REP

| Property | Value |
|----------|-------|
| **Table Name** | A_IRD_PV01_TTL.REP |
| **Source View** | MDS_IRPV01TTL |
| **Dynamic Table** | A_IRD_IRPV01_TTL |
| **Expression Filter** | DV01__PA1<>0.OR.DV01__PAR<>0 |

#### Key Columns

| Column | Description |
|--------|-------------|
| M_PORTFOLIO | Trading portfolio |
| M_TRN_FMLY | Product family |
| M_TRN_GRP | Product group |
| M_TRN_TYPE | Product type |
| M_PL_INSTRU | P&L instrument |
| M_SEC_CD | Security code |
| M_NB | Trade number |
| M_CURRENCY | Curve currency |
| M_CURVE_NAM | Curve name |
| M_DATE | Pillar date |
| DV01__PAR | Delta Par (native currency) |
| DV01__PA1 | Delta Par (USD) |
| DV01__PA2 | Delta Par (ZAR) - Deprecated |
| M_LEGAL_ENT | Legal entity |
| M_CLOS_ENT | Closing entity |
| M_TYPOLOGY | Product typology |

### 5.2 A_IRPV02_GAMMA.REP

| Property | Value |
|----------|-------|
| **Table Name** | A_IRPV02_GAMMA.REP |
| **Source View** | IRPV02_GAMMAS |
| **Dynamic Table** | A_IRPV02_GAMMA |

#### Key Columns

| Column | Description |
|--------|-------------|
| M_PORTFOLIO | Trading portfolio |
| M_NB | Trade number |
| M_CURVE_NAM | Curve name |
| M_DATE_PAR | Pillar date (Par) |
| GAMMA_PAR_CCY | Gamma Par (native currency) |
| GAMMA_PAR_USD | Gamma Par (USD) |
| GAMMA_PAR_ZAR | Gamma Par (ZAR) - Deprecated |

### 5.3 A_BOND_NOTIONAL.REP

| Property | Value |
|----------|-------|
| **Table Name** | A_BOND_NOTIONAL.REP |
| **Source** | TRN_PL table for TRN_GRP="BOND" |
| **Dynamic Table** | A_BOND_NOTIONAL |

#### Key Columns

| Column | Description |
|--------|-------------|
| M_NB | Trade number |
| M_TP_RTCCP02 | Bond notional |
| M_TP_RTCAPI0 | Alternative notional field |
| M_TP_SECLOT | Security lot size |

---

## 6. Reference Tables

### 6.1 A_RTCT_REP (Curve Definition)

| Column | Description |
|--------|-------------|
| M_LABEL | Curve label |
| M_TYPE | Generator type (e.g., "Swap", "Bond") |
| M_D_GEN | Generator name |
| M_BID_S | Spread indicator |

### 6.2 A_RATES_REP (Rate Definition)

| Column | Description |
|--------|-------------|
| M_LABEL | Rate label |
| M_GENINTNB | Generator internal number |
| M_S_BID1 | Convexity spread indicator |

### 6.3 TBL_BOND_MKTDATA_REP (Bond Market Data)

| Column | Description |
|--------|-------------|
| M_LABEL | Bond label |
| M_EVAL_MODE | Evaluation mode (e.g., "MTM.CR" for Mark to Market) |

### 6.4 SB_SE_RBC_REP (Risk Basket Composition)

| Column | Description |
|--------|-------------|
| M_SE_LABEL | Security label |
| M_SE_BOND | Flag identifying dummy bonds in STB deals |

### 6.5 SB_TP_REP / SB_TP_BD_REP (Trade Parameters)

| Column | Description |
|--------|-------------|
| M_NB | Trade number |
| M_TP_RTCCP02 | Notional for bonds |
| M_TP_RTCAPI0 | Alternative notional |
| M_TP_SECLOT | Security lot |

---

## 7. Extraction

### 7.1 Extraction Configuration

| Region | Processing Script | Batch | Extraction | Request |
|--------|-------------------|-------|------------|---------|
| HKG | HK_VSPA_IRPDG_RPT | BE_IRD_PV01TTHK | DE_IRD_PV01_TTL | IRD_PV01_Par_Delta_Gamma_TLZAR |
| LDN | LN_VSPA_IRPDG_RPT | BE_IRD_PV01TTLD | DE_IRD_PV01_TTL | IRD_PV01_Par_Delta_Gamma_TLZAR |
| NYK | NY_VSPA_IRPDG_RPT | BE_IRD_PV01TTNY | DE_IRD_PV01_TTL | IRD_PV01_Par_Delta_Gamma_TLZAR |
| SAO | SP_VSPA_IRPDG_RPT | BE_IRD_PV01TTSP | DE_IRD_PV01_TTL | IRD_PV01_Par_Delta_Gamma_TLZAR |

### 7.2 Extraction SQL Structure

The extraction request uses a complex 4-block UNION ALL structure to handle Structured Bond (STB) deals:

```sql
-- Block 1: Non-dummy STB bonds with generator = -1
SELECT [fields]
FROM A_IRD_PV01_TTL.REP PV01
LEFT JOIN A_IRPV02_GAMMA.REP GAMMA ON ...
LEFT JOIN A_BOND_NOTIONAL.REP BOND ON ...
LEFT JOIN TBL_BOND_MKTDATA_REP MKTDATA ON ...
LEFT JOIN A_RTCT_REP RTCT ON ...
LEFT JOIN A_RATES_REP RATES ON ...
WHERE NOT EXISTS (SELECT 1 FROM SB_SE_RBC_REP WHERE ...)  -- Not dummy bond
  AND RATES.M_GENINTNB = -1

UNION ALL

-- Block 2: Non-dummy STB bonds with generator ≠ -1
SELECT [fields]
FROM A_IRD_PV01_TTL.REP PV01
LEFT JOIN A_IRPV02_GAMMA.REP GAMMA ON ...
LEFT JOIN A_BOND_NOTIONAL.REP BOND ON ...
LEFT JOIN TBL_BOND_MKTDATA_REP MKTDATA ON ...
LEFT JOIN A_RTCT_REP RTCT ON ...
LEFT JOIN A_RATES_REP RATES ON ...
WHERE NOT EXISTS (SELECT 1 FROM SB_SE_RBC_REP WHERE ...)  -- Not dummy bond
  AND RATES.M_GENINTNB <> -1

UNION ALL

-- Block 3: Dummy STB bonds with generator = -1
SELECT [fields]
FROM A_IRD_PV01_TTL.REP PV01
LEFT JOIN A_IRPV02_GAMMA.REP GAMMA ON ...
LEFT JOIN A_BOND_NOTIONAL.REP BOND ON ...
LEFT JOIN TBL_BOND_MKTDATA_REP MKTDATA ON ...
LEFT JOIN A_RTCT_REP RTCT ON ...
LEFT JOIN A_RATES_REP RATES ON ...
WHERE EXISTS (SELECT 1 FROM SB_SE_RBC_REP WHERE ...)  -- Is dummy bond
  AND RATES.M_GENINTNB = -1

UNION ALL

-- Block 4: Dummy STB bonds with generator ≠ -1
SELECT [fields]
FROM A_IRD_PV01_TTL.REP PV01
LEFT JOIN A_IRPV02_GAMMA.REP GAMMA ON ...
LEFT JOIN A_BOND_NOTIONAL.REP BOND ON ...
LEFT JOIN TBL_BOND_MKTDATA_REP MKTDATA ON ...
LEFT JOIN A_RTCT_REP RTCT ON ...
LEFT JOIN A_RATES_REP RATES ON ...
WHERE EXISTS (SELECT 1 FROM SB_SE_RBC_REP WHERE ...)  -- Is dummy bond
  AND RATES.M_GENINTNB <> -1
```

### 7.3 Key Extraction Logic

#### SBSA Exclusion

```sql
-- MxSQLExpression parameter at batch level
A_IRD_PV01_TTL.M_LEGAL_ENT <> 'SBSA'
```

#### Gamma Join

```sql
-- Join Delta and Gamma on trade, curve, and pillar
LEFT JOIN A_IRPV02_GAMMA.REP GAMMA
ON PV01.M_NB = GAMMA.M_NB
   AND PV01.M_CURVE_NAM = GAMMA.M_CURVE_NAM
   AND PV01.M_DATE = GAMMA.M_DATE_PAR
```

#### Curve Type Default

```sql
-- Default to 'Bond' if M_TYPE is null
CASE WHEN RTCT.M_TYPE IS NULL THEN 'Bond' ELSE RTCT.M_TYPE END AS CurveType
```

#### Spread Flags

```sql
-- Curve Spread flag
CASE WHEN RTCT.M_BID_S IS NULL OR PV01.M_TRN_GRP = 'FUTURE' THEN 'N' ELSE 'Y' END AS Curve_Spread

-- Convexity Spread flag
CASE WHEN RATES.M_S_BID1 IS NULL OR PV01.M_TRN_GRP = 'FUTURE' THEN 'N' ELSE 'Y' END AS Convexity_Spread
```

#### Notional Calculation

```sql
-- Bond notional logic
CASE
  WHEN PV01.M_TRN_GRP = 'BOND' THEN BOND.M_TP_RTCCP02
  WHEN PV01.M_TRN_TYPE = 'RTRN' THEN BOND.M_TP_RTCAPI0 * BOND.M_TP_SECLOT
  ELSE 0
END AS act_Notional
```

#### Evaluation Mode

```sql
-- Bond evaluation mode
CASE
  WHEN PV01.M_TRN_GRP NOT IN ('BOND', 'RTRN') THEN 'XXX'
  WHEN MKTDATA.M_LABEL IS NULL THEN 'Zero coupon spread'
  WHEN MKTDATA.M_EVAL_MODE = 'MTM.CR' THEN 'Mark to Market'
  -- ... other modes
  ELSE MKTDATA.M_EVAL_MODE
END AS Evaluation_Bond
```

---

## 8. Output File

### 8.1 File Specification

| Property | Value |
|----------|-------|
| **File Pattern** | `MxMGB_MR_Rates_PDG_{Region}_{YYYYMMDD}.csv` |
| **Delimiter** | Semicolon (;) |
| **Header** | Yes |
| **Encoding** | UTF-8 |
| **Output Path** | ./reports/today/eod |

### 8.2 Output Fields (26 Fields)

| # | Field | Type | Length | Source |
|---|-------|------|--------|--------|
| 1 | PORTFOLIO | VarChar | 16 | MDS_IRPV01TTL.Portfolio |
| 2 | Family | VarChar | 16 | MDS_IRPV01TTL.Family |
| 3 | Group | VarChar | 5 | MDS_IRPV01TTL.Group |
| 4 | Type | VarChar | 16 | MDS_IRPV01TTL.Type |
| 5 | Instrument | VarChar | 50 | MDS_IRPV01TTL.PL Instrument |
| 6 | Sec_code | VarChar | 16 | MDS_IRPV01TTL.Sec Code |
| 7 | Trade Number | Numeric | 16 | MDS_IRPV01TTL.Trade Number (0 if DEAD) |
| 8 | CURRENCY | VarChar | 4 | MDS_IRPV01TTL.Currency / Sec Currency for Bonds |
| 9 | CURVE_NAM | VarChar | 35 | MDS_IRPV01TTL.Curve Name |
| 10 | CurveType | VarChar | 10 | A_RTCT_REP.M_TYPE ('Bond' if null) |
| 11 | Generat | VarChar | 10 | MDS_IRPV01TTL.Generator |
| 12 | DATE | VarChar | 64 | MDS_IRPV01TTL.Date |
| 13 | Delta Par | American | 16,2 | MDS_IRPV01TTL.DV01(par) |
| 14 | Delta Par(USD) | American | 16,2 | MDS_IRPV01TTL.DV01(par) USD |
| 15 | Gamma Par | American | 16,2 | IRPV02_GAMMAS.GAMMA_PAR_CCY (0 if no match) |
| 16 | Gamma Par(USD) | American | 16,2 | IRPV02_GAMMAS.GAMMA_PAR_USD (0 if no match) |
| 17 | act. Notional | American | 25,8 | A_BOND_NOTIONAL.REP (0 if not bond) |
| 18 | Evaluation(Bond) | VarChar | - | TBL_BOND_MKTDATA_REP.M_EVAL_MODE ('XXX' if not bond) |
| 19 | ZAR_PROCESSING | VarChar | 1 | 'Y' if Closing Entity = JBSBSA, else 'N' |
| 20 | Delta Par(ZAR) | American | 12,2 | MDS_IRPV01TTL.DV01(par) ZAR |
| 21 | Gamma Par(ZAR) | American | 16,2 | IRPV02_GAMMAS.GAMMA_PAR_ZAR (0 if no match) |
| 22 | Typology | VarChar | 21 | MDS_IRPV01TTL.Typology |
| 23 | Curve_Spread | VarChar | 1 | 'Y' if M_BID_S not null, else 'N' |
| 24 | Convexity_Spread | VarChar | 1 | 'Y' if M_S_BID1 not null, else 'N' |
| 25 | RBC_FMLY | VarChar | - | '' (blank) |
| 26 | RBC_GRP | VarChar | - | '' (blank) |
| 27 | RBC_TYPE | VarChar | - | '' (blank) |
| 28 | RBC_INSTRUMENT | VarChar | - | '' (blank) |

### 8.3 Sample Output

```
PORTFOLIO;Family;Group;Type;Instrument;Sec_code;Trade Number;CURRENCY;CURVE_NAM;CurveType;Generat;DATE;Delta Par;Delta Par(USD);Gamma Par;Gamma Par(USD);act. Notional;Evaluation(Bond);ZAR_PROCESSING;Delta Par(ZAR);Gamma Par(ZAR);Typology;Curve_Spread;Convexity_Spread;RBC_FMLY;RBC_GRP;RBC_TYPE;RBC_INSTRUMENT
PMLNSBPDSF;COM;SPOT;;XPD;;28249787;USD;USD_SOFR_ANFUTS;Swap;USD SOFR;1M;0.00;0.00;0.00;0.00;0.00000000;XXX;N;-0.01;0.00;PM - FWD UA;N;N;;;;
PMLNSBPDSF;COM;SPOT;;XPD;;28249787;USD;USD_SOFR_ANFUTS;Swap;USD SOFR;6M;1.17;1.17;0.00;0.00;0.00000000;XXX;N;20.69;0.00;PM - FWD UA;N;N;;;;
```

---

## 9. File Packaging and Delivery

### 9.1 Packaging

| Property | Value |
|----------|-------|
| **Script** | process_reports.sh |
| **ZIP Pattern** | MxMGB_MR_Sensitivities_{Region}_{YYYYMMDD}.zip |
| **Contents** | PDG file + other market risk sensitivity reports |

### 9.2 Delivery

| Target | MFT ID |
|--------|--------|
| Plato | MurexMGBSensitivitiesToPlato_{Region} |
| RDS | MurexMGBSensitivitiesToRDS_{Region} |

---

## 10. Processing Schedule

| Time (GMT) | Event |
|------------|-------|
| 18:00 | Market data close (LN) |
| 21:00 | Valuation batch complete |
| 02:00 | IR Delta feeder batch start (**_IRPDG_FDR) |
| 02:30 | IR Gamma feeder batch start (BF_PRVIRGAM_**) |
| 03:30 | All feeder batches complete |
| 04:00 | Extraction batch start (**_VSPA_IRPDG_RPT) |
| 04:30 | Extraction complete |
| 05:00 | File packaging (process_reports.sh) |
| 05:30 | MFT delivery |

---

## 11. Recommendations

### 11.1 Portfolio Filter Standardization

**Current State**: Mix of Level 4 and Level 5 portfolio nodes selected.

**Recommendation**: Standardize to Level 4 nodes only:
- LDN: FXDLN, IRLN, LMLN, PMLN
- HKG: LMHK, PMSG
- NYK: LMNY, PMNY
- SAO: LMSP

### 11.2 Unused Portfolio Cleanup

**Current State**: Bond Notional feeder for LDN includes IFXMMLNIC and IFXMMLNLH.

**Recommendation**: Remove these inactive portfolios.

### 11.3 HKG Expression Filter Review

**Current State**: Filter excludes SGD/USD XCCY swaps.

**Recommendation**: Review if deals still exist; remove filter if expired.

### 11.4 Deprecated Fields Decommissioning

**Current State**: ZAR fields still calculated but not used.

**Recommendation**: Remove DV01(par) ZAR, Gamma Par(ZAR), and ZAR_PROCESSING from simulation views and extraction.

---

## 12. Document Control

### 12.1 Version History

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | 2025-01-03 | Initial version | Risk Technology |

### 12.2 Approval

| Role | Name | Date |
|------|------|------|
| Business Owner | Head of Product Control | |
| Technical Owner | Head of Risk Technology | |
| Approver | Risk Technology Change Board | |

---

*End of Document*
