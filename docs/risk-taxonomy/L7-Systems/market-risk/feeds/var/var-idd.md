# Value at Risk (VaR) P&L Strips Feed - Interface Design Document

**Meridian Global Bank - Market Risk Technology**

---

## 1. Interface Overview

| Attribute | Value |
|-----------|-------|
| **Feed Name** | VaR P&L Strips Feed |
| **Source System** | Murex Market Risk Engine |
| **Target System** | VESPA |
| **Feed Type** | Daily batch |
| **Format** | Pipe-delimited text (no headers) |
| **Delivery** | Managed File Transfer (MFT) |

---

## 2. Datamart Tables

### 2.1 Export Tables by Region and VaR Type

| Region | VaR Type | Revaluation Run | Datamart Table |
|--------|----------|-----------------|----------------|
| HKG | 1DVAR | HKG_1DVAR | MRA_EXPORT_HKG_1DVAR_REP |
| HKG | 10DVAR | HKG_10DVAR | MRA_EXPORT_HKG_10DVAR_REP |
| HKG | 10DSVAR | HKG_10DSVAR | MRA_EXPORT_HKG_10DSVAR_REP |
| HKG | 10DESVAR | HKG_10DESVAR | MRA_EXPORT_HKG_10DESVAR_REP |
| LDN | 1DVAR | LDN_1DVAR | MRA_EXPORT_LDN_1DVAR_REP |
| LDN | 10DVAR | LDN_10DVAR | MRA_EXPORT_LDN_10DVAR_REP |
| LDN | 10DSVAR | LDN_10DSVAR | MRA_EXPORT_LDN_10DSVAR_REP |
| LDN | 10DESVAR | LDN_10DESVAR | MRA_EXPORT_LDN_10DESVAR_REP |
| NYK | 1DVAR | NYK_1DVAR | MRA_EXPORT_NYK_1DVAR_REP |
| NYK | 10DVAR | NYK_10DVAR | MRA_EXPORT_NYK_10DVAR_REP |
| NYK | 10DSVAR | NYK_10DSVAR | MRA_EXPORT_NYK_10DSVAR_REP |
| NYK | 10DESVAR | NYK_10DESVAR | MRA_EXPORT_NYK_10DESVAR_REP |
| SAO | 1DVAR | SAO_1DVAR | MRA_EXPORT_SAO_1DVAR_REP |
| SAO | 10DVAR | SAO_10DVAR | MRA_EXPORT_SAO_10DVAR_REP |
| SAO | 10DSVAR | SAO_10DSVAR | MRA_EXPORT_SAO_10DSVAR_REP |
| SAO | 10DESVAR | SAO_10DESVAR | MRA_EXPORT_SAO_10DESVAR_REP |

---

## 3. Extraction Configuration

### 3.1 Extraction Requests by VaR Type

| Region | VaR Type | Processing Script | Batch Extraction | Single Extractions | Extraction Requests |
|--------|----------|-------------------|------------------|--------------------|--------------------|
| HKG | 1DVAR | HK_1DVAR_RPT | BE_1DVAR_HK | DE_1DVAR_SB, DE_1DVAR_D_SB | ER_1DVAR_SB, ER_1DVAR_D_SB |
| HKG | 10DVAR | HK_10DVAR_RPT | BE_10DVAR_HK | DE_10DVAR_SB, DE_10DVAR_D_SB | ER_10DVAR_SB, ER_10DVAR_D_SB |
| HKG | 10DSVAR | HK_10DSVAR_RPT | BE_10DSVAR_HK | DE_10DSVAR_SB, DE_10DSVAR_D_SB | ER_10DSVAR_SB, ER_10DSVAR_D_SB |
| LDN | 1DVAR | LN_1DVAR_RPT | BE_1DVAR_LN | DE_1DVAR_SB, DE_1DVAR_D_SB | ER_1DVAR_SB, ER_1DVAR_D_SB |
| LDN | 10DVAR | LN_10DVAR_RPT | BE_10DVAR_LN | DE_10DVAR_SB, DE_10DVAR_D_SB | ER_10DVAR_SB, ER_10DVAR_D_SB |
| LDN | 10DSVAR | LN_10DSVAR_RPT | BE_10DSVAR_LN | DE_10DSVAR_SB, DE_10DSVAR_D_SB | ER_10DSVAR_SB, ER_10DSVAR_D_SB |
| NYK | 1DVAR | NY_1DVAR_RPT | BE_1DVAR_NY | DE_1DVAR_SB, DE_1DVAR_D_SB | ER_1DVAR_SB, ER_1DVAR_D_SB |
| NYK | 10DVAR | NY_10DVAR_RPT | BE_10DVAR_NY | DE_10DVAR_SB, DE_10DVAR_D_SB | ER_10DVAR_SB, ER_10DVAR_D_SB |
| NYK | 10DSVAR | NY_10DSVAR_RPT | BE_10DSVAR_NY | DE_10DSVAR_SB, DE_10DSVAR_D_SB | ER_10DSVAR_SB, ER_10DSVAR_D_SB |
| SAO | 1DVAR | SP_1DVAR_RPT | BE_1DVAR_SP | DE_1DVAR_SB, DE_1DVAR_D_SB | ER_1DVAR_SB, ER_1DVAR_D_SB |
| SAO | 10DVAR | SP_10DVAR_RPT | BE_10DVAR_SP | DE_10DVAR_SB, DE_10DVAR_D_SB | ER_10DVAR_SB, ER_10DVAR_D_SB |
| SAO | 10DSVAR | SP_10DSVAR_RPT | BE_10DSVAR_SP | DE_10DSVAR_SB, DE_10DSVAR_D_SB | ER_10DSVAR_SB, ER_10DSVAR_D_SB |

### 3.2 Extraction Types

#### Detailed Extraction (TotalCRD Reports)

Used for: `ER_1DVAR_D_SB`, `ER_10DVAR_D_SB`, `ER_10DSVAR_D_SB`

**Functionality**:
1. Aggregates four regional data sets, outputting based on revalRun parameter
2. Fetches P&L strips by output results including: portfolio, PL instrument, currency, scenario description, scenario dates, scenario ID
3. Groups results by same outputs
4. Excludes central point (scenario=-1) and P&L strips below 0.5

#### Non-Detailed Extraction (All Other Risk Classes)

Used for: `ER_1DVAR_SB`, `ER_10DVAR_SB`, `ER_10DSVAR_SB`

**Functionality**:
1. Aggregates four regional data sets, outputting based on revalRun parameter
2. Fetches P&L strips by output results including: portfolio, currency, scenario description, scenario dates, scenario ID
3. Groups results by same outputs
4. Excludes central point (scenario=-1) and P&L strips below 0.5

---

## 4. Output File Specification

### 4.1 File Naming Convention

| VaR Type | ZIP File Pattern | Report File Pattern |
|----------|------------------|---------------------|
| 1D VaR | P&LStrips_MxGts_***_1D_VAR_All_yyyymmdd.zip | P&LStrips_MxGts_***_1D_VAR_{RiskClass}_yyyymmdd.txt |
| 10D VaR | P&LStrips_MxGts_***_10D_VAR_All_yyyymmdd.zip | P&LStrips_MxGts_***_10D_VAR_{RiskClass}_yyyymmdd.txt |
| 10D SVaR | P&LStrips_MxGts_***_10D_SVAR_All_yyyymmdd.zip | P&LStrips_MxGts_***_10D_SVAR_{RiskClass}_yyyymmdd.txt |

**Note**: *** is replaced by region code (LDN, HKG, NYK, SAO)

### 4.2 Risk Class Files per ZIP

| ZIP Contains | Report Name | Risk Class |
|--------------|-------------|------------|
| 10 files | P&LStrips_MxGts_***_{Type}_Com_yyyymmdd.txt | Commodities |
| | P&LStrips_MxGts_***_{Type}_Credit_Curve_yyyymmdd.txt | CRD |
| | P&LStrips_MxGts_***_{Type}_FX_yyyymmdd.txt | FX |
| | P&LStrips_MxGts_***_{Type}_FXVol_yyyymmdd.txt | FXVol |
| | P&LStrips_MxGts_***_{Type}_GenFX_yyyymmdd.txt | GenFX |
| | P&LStrips_MxGts_***_{Type}_GenIR_yyyymmdd.txt | GenIR |
| | P&LStrips_MxGts_***_{Type}_IR_yyyymmdd.txt | IR |
| | P&LStrips_MxGts_***_{Type}_IRVol_yyyymmdd.txt | IRVol |
| | P&LStrips_MxGts_***_{Type}_IR_FX_Com_yyyymmdd.txt | Total |
| | P&LStrips_MxGts_detail_***_{Type}_Total_yyyymmdd.txt | TotalCRD |

---

## 5. Field Specifications

### 5.1 TotalCRD Report Fields (Detailed Extraction)

| Column | Field Name | Type | Length | Source |
|--------|------------|------|--------|--------|
| 1 | Portfolio | VarChar | 255 | MRA_EXPORT VAR Table |
| 2 | PL Instrument | VarChar | 255 | MRA_EXPORT VAR Table |
| 3 | Trade Currency | VarChar | 255 | MRA_EXPORT VAR Table |
| 4 | Constant (1) | Numeric | 1 | Inserted by format script |
| 5 | Constant (1) | Numeric | 1 | Inserted by format script |
| 6 | Time Window | Numeric | 2 | Set in format script (1 or 10) |
| 7 | Risk Class | VarChar | 12 | MRA_EXPORT VAR Table |
| 8 | Scenario Date | Date | - | MRA_EXPORT VAR Table |
| 9 | Scenario ID | Numeric | 38 | MRA_EXPORT VAR Table |
| 10 | PL Strip Value | Number | 32,10 | MRA_EXPORT VAR Table |

### 5.2 Other Risk Class Report Fields (Non-Detailed Extraction)

| Column | Field Name | Type | Length | Source |
|--------|------------|------|--------|--------|
| 1 | Portfolio | VarChar | 255 | MRA_EXPORT VAR Table |
| 2 | Trade Currency | VarChar | 255 | MRA_EXPORT VAR Table |
| 3 | PL Strip Currency | VarChar | 4 | Set to USD in format script |
| 4 | Constant (1) | Numeric | 1 | Inserted by format script |
| 5 | Constant (1) | Numeric | 1 | Inserted by format script |
| 6 | Time Window | Numeric | 2 | Set in format script (1 or 10) |
| 7 | Risk Class | VarChar | 12 | MRA_EXPORT VAR Table |
| 8 | Scenario Date | Date | - | MRA_EXPORT VAR Table |
| 9 | Scenario ID | Numeric | 38 | MRA_EXPORT VAR Table |
| 10 | PL Strip Value | Number | 32,10 | MRA_EXPORT VAR Table |

---

## 6. Sample Data

### 6.1 TotalCRD Report Sample (Total)

```
CTSPSBLBRCTG|USD/BRL|USD|1|1|10|Total|13/01/2023|165|-17.52900
CTSPSBLBRCTG|USD/BRL|USD|1|1|10|Total|13/02/2023|186|9.831890
CTSPSBLBRCTG|USD/BRL|USD|1|1|10|Total|13/03/2023|206|7.350160
CTSPSBLBRCTG|USD/BRL|USD|1|1|10|Total|13/04/2023|229|-27.84730
```

### 6.2 Risk Class Report Sample (FX)

```
CTSPSBLBRCTG|BRL|USD|1|1|1|FX|01/02/2023|178|2.50407
CTSPSBLBRCTG|BRL|USD|1|1|1|FX|01/03/2023|198|1.37668
CTSPSBLBRCTG|BRL|USD|1|1|1|FX|01/05/2023|241|0.00000
CTSPSBLBRCTG|BRL|USD|1|1|1|FX|01/06/2022|3|-6.4765300
```

---

## 7. Data Quality Rules

### 7.1 Exclusion Rules

| Rule ID | Description |
|---------|-------------|
| DQ-VAR-001 | Exclude central point (scenario = -1) |
| DQ-VAR-002 | Exclude P&L strips with absolute value below 0.5 |
| DQ-VAR-003 | Ensure scenario dates within expected range |

### 7.2 Validation Rules

| Rule ID | Description | Action |
|---------|-------------|--------|
| VR-VAR-001 | Scenario count equals expected (250 for VaR/SVaR) | Alert if mismatch |
| VR-VAR-002 | All risk classes present in output | Alert if missing |
| VR-VAR-003 | P&L values in reasonable range | Alert if outliers |

---

## 8. Processing Scripts

### 8.1 Report Formatting

**Script**: `/apps/murex/client/scripts/var/eod/formatriskreport.sh`

**Function**: Formats extracted reports to VESPA standards and creates ZIP packages

**Output Path**: `[App directory]/reports/today/eod/`

### 8.2 Export Configuration

**File**: `/apps/murex/mx/fs/public/mxres/mxmarketrisk_service/scripts/ant-targets-sources-EOD.mxres`

**Target**: `exportEODRun`

---

## 9. Delivery Specification

### 9.1 MFT Configuration

| Component | Value |
|-----------|-------|
| Protocol | MFT (Managed File Transfer) |
| Target System | VESPA |
| Frequency | Daily |

### 9.2 MFT IDs by Region

| Region | MFT ID Pattern |
|--------|----------------|
| London | MurexGTSSVAR10DToVespa_LDN |
| Hong Kong | MurexGTSSVAR10DToVespa_HKG |
| New York | MurexGTSSVAR10DToVespa_NYK |
| São Paulo | MurexGTSSVAR10DToVespa_SAO |

---

## 10. ESVaR Special Handling

### 10.1 ESVaR Characteristics

| Attribute | Value |
|-----------|-------|
| Observation Start | 02 January 2007 |
| Observation End | Current date (growing) |
| Generation Frequency | Weekly |
| Scenario Count | Growing (not fixed at 250) |
| Purpose | Stress period identification for SVaR |

### 10.2 ESVaR Output Files

| Region | VaR Type | ZIP File |
|--------|----------|----------|
| HKG | 10DESVAR | P&LStrips_MxGts_HKG_10D_ESVAR_All_yyyymmdd.zip |
| LDN | 10DESVAR | P&LStrips_MxGts_LDN_10D_ESVAR_All_yyyymmdd.zip |
| NYK | 10DESVAR | P&LStrips_MxGts_NYK_10D_ESVAR_All_yyyymmdd.zip |
| SAO | 10DESVAR | P&LStrips_MxGts_SAO_10D_ESVAR_All_yyyymmdd.zip |

---

## 11. Related Documentation

| Document | Description |
|----------|-------------|
| [var-overview.md](var-overview.md) | Architecture overview |
| [var-brd.md](var-brd.md) | Business requirements |
| [var-config.md](var-config.md) | Murex configuration |

---

*Document Version: 1.0 | Last Updated: 2025-01-13*
