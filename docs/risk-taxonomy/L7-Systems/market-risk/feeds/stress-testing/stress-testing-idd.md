# Stress Testing Feed - Interface Design Document

**Meridian Global Bank - Market Risk Technology**

---

## 1. Interface Overview

| Attribute | Value |
|-----------|-------|
| **Feed Name** | Stress Testing Feed |
| **Source System** | Murex Market Risk Engine |
| **Target System** | VESPA |
| **Feed Type** | Daily batch |
| **Format** | Pipe-delimited text (with headers) |
| **Delivery** | Managed File Transfer (MFT) |

---

## 2. Datamart Tables

### 2.1 Export Tables by Region

| Region | Revaluation Run | Datamart Table |
|--------|-----------------|----------------|
| HKG | HKG_StressTesting | MRA_EXPORT_HKG_STRESSTESTING_REP |
| LDN | LDN_StressTesting | MRA_EXPORT_LDN_STRESSTESTING_REP |
| NYK | NYK_StressTesting | MRA_EXPORT_NYK_STRESSTESTING_REP |
| SAO | SAO_StressTesting | MRA_EXPORT_SAO_STRESSTESTING_REP |

---

## 3. Extraction Configuration

### 3.1 Extraction Details by Region

| Region | Processing Script | Batch Extraction | Single Extraction | Extraction Request |
|--------|-------------------|------------------|-------------------|-------------------|
| HKG | HK_StressTesting_RPT | BE_ST_HK | DE_StressTesting_SB | ER_StressTesting_SB |
| LDN | LN_StressTesting_RPT | BE_ST_LN | DE_StressTesting_SB | ER_StressTesting_SB |
| NYK | NYK_StressTesting_RPT | BE_ST_NY | DE_StressTesting_SB | ER_StressTesting_SB |
| SAO | SP_StressTesting_RPT | BE_ST_SP | DE_StressTesting_SB | ER_StressTesting_SB |

### 3.2 Extraction Request Description

**ER_StressTesting_SB** performs the following:

1. **Data Aggregation**: Fetches P&L Vectors from all 4 regional datamart tables
2. **Filtering by Output**: Fetches relevant P&L vectors by output results and revalRun (defined in batch)
3. **Field Selection**: Extracts portfolio, currency, family, group, type, PL key, risk section, CIF_ID, GLOBUS_ID, country, security code, scenario container label, and P&L vector
4. **Grouping**: Groups results by same outputs (except PL currency)
5. **Exclusions**: Excludes central point (scenario=-1) and P&L vectors below 0.000001
6. **Static Data Joins**: Joins to SB_SE_HEAD_REP (security) and SB_CP_REP (counterparty)

---

## 4. Output File Specification

### 4.1 File Naming Convention

| ZIP File Pattern | Description |
|------------------|-------------|
| StressTest_MxGts_***_All_yyyymmdd.zip | All risk class files per region |

**Note**: *** is replaced by region code (LDN, HKG, NYK, SAO)

### 4.2 Risk Class Files per ZIP

| ZIP Contains | Report Name | Risk Class |
|--------------|-------------|------------|
| 8 files | StressTest_MxGts_***_Commodities_yyyymmdd.txt | StrCommodity |
| | StressTest_MxGts_***_FX_yyyymmdd.txt | GenFX |
| | StressTest_MxGts_***_IR_yyyymmdd.txt | GenIR |
| | StressTest_MxGts_***_Recovery_yyyymmdd.txt | RR |
| | StressTest_MxGts_***_Credit_yyyymmdd.txt | CRD |
| | StressTest_MxGts_***_Bond_Basi_yyyymmdd.txt | BCS |
| | StressTest_MxGts_***_IR_FX_Com_yyyymmdd.txt | TotalStr |
| | StressTest_MxGts_***_Total_yyyymmdd.txt | TotalStrCRD |

---

## 5. Field Specifications

### 5.1 Total Report Fields

| Column | Field Name | Type | Length | Source |
|--------|------------|------|--------|--------|
| 1 | ENTITY | VarChar | - | Set by format script (Entity+Run+Riskfactor) |
| 2 | LABEL | VarChar | - | Set to 'contStress' by format script |
| 3 | PARAM | VarChar | - | Risk factor (set by format script) |
| 4 | BACK | VarChar | - | Set to 'N' (not backtesting) |
| 5 | IS_BENCH | VarChar | - | Set to 'N' (not benchmark) |
| 6 | HOR_DAYS | Numeric | - | Set to '1' by format script |
| 7 | DATE | Date | - | Run date (set by format script) |
| 8 | SCENARIO | Numeric | - | Scenario ID from MRA_EXPORT |
| 9 | OLABEL | VarChar | - | Set to 'P&L(i)' by format script |
| 10 | RESULT | Number | 32,10 | P&L Vector from MRA_EXPORT |
| 11 | RESULTV | Number | 32,10 | P&L Vector Diff (scenario vs central point) |
| 12 | CUR | VarChar | 255 | Trade currency |
| 13 | PL_CUR | VarChar | - | Set to 'USD' by format script |
| 14 | PTFOLIO | VarChar | 255 | Portfolio |
| 15 | TRN_FMLY | VarChar | 255 | Trade Family |
| 16 | TRN_GRP | VarChar | 255 | Trade Group |
| 17 | TRN_TYPE | VarChar | 255 | Trade Type |
| 18 | INSTRUMENT | VarChar | 255 | P&L Instrument |
| 19 | PL_KEY1 | VarChar | 255 | P&L Key |
| 20 | RSKSECTION | VarChar | 255 | Risk Section |
| 21 | DEALNUM | - | - | Set to blank by format script |
| 22 | DLDRAFT | - | - | Set to blank by format script |
| 23 | ISSUER | VarChar | 255 | Issuer (from MRA_EXPORT or SB_CP_REP for SCF) |
| 24 | CIF | Numeric | 38 | CIF ID (M_ADDINFONUM1) |
| 25 | GLOBUS_ID | VarChar | 255 | GLOBUS ID (M_RISKLABEL2) |
| 26 | COUNTRY | VarChar | 255 | Counterparty country (from MRA_EXPORT or SB_CP_REP) |
| 27 | ISIN | VarChar | 255 | Security ISIN (from MRA_EXPORT or SB_SE_HEAD_REP) |

---

## 6. Extraction SQL

### 6.1 ER_StressTesting_SB Query

```sql
SELECT ST.M_PORTFOLIO,
       ST.M_CURRENCY,
       ST.M_FAMILY,
       ST.M_GROUP,
       ST.M_TYPE,
       ST.M_INSTRUMENT,
       ST.M_PLKEY,
       ST.M_RISKSECTION,
       ST.M_ADDINFONUM1,
       ST.M_RISKLABEL2,
       CASE WHEN ST.M_ISSUER IS NOT NULL
            THEN ST.M_ISSUER
            WHEN (ST.M_ISSUER IS NULL AND ST.M_GROUP = 'SCF')
            THEN CP.M_DSP_LABEL END AS M_ISSUER,
       CASE WHEN ST.M_COUNTRY IS NOT NULL
            THEN ST.M_COUNTRY
            WHEN (ST.M_COUNTRY IS NULL AND ST.M_GROUP = 'SCF')
            THEN CP.M_H_CNT_CODE END AS M_COUNTRY,
       CASE WHEN ST.M_SECURITYCODE IS NOT NULL
            THEN ST.M_SECURITYCODE
            WHEN (ST.M_SECURITYCODE IS NULL AND ST.M_GROUP = 'SCF')
            THEN SE_HEAD.M_SE_CODE END AS M_SECURITYCODE,
       ST.M_CONTAINER,
       ST.M_SCENARIOID,
       SUM(CASE @outputResult:C
           WHEN 'BCS' THEN ST.M_PL_BCS_
           WHEN 'CRD' THEN ST.M_PL_CRD_
           WHEN 'GenFX' THEN ST.M_PL_GenFX_
           WHEN 'GenIR' THEN ST.M_PL_GenIR_
           WHEN 'TotalStr' THEN ST.M_PL_TOTALSTR_
           WHEN 'RR' THEN ST.M_PL_RR_
           WHEN 'StrCommodity' THEN ST.M_PL_STRCOMMODITY_
           WHEN 'TotalStrCRD' THEN ST.M_PL_TotalStrCRD_ END) M_RESULT,
       SUM(CASE @outputResult:C
           WHEN 'BCS' THEN ST.M_PL_BCS_DIFF
           WHEN 'CRD' THEN ST.M_PL_CRD_DIFF
           WHEN 'GenFX' THEN ST.M_PL_GenFX_DIFF
           WHEN 'GenIR' THEN ST.M_PL_GenIR_DIFF
           WHEN 'TotalStr' THEN ST.M_PL_TOTALSTR_DIFF
           WHEN 'RR' THEN ST.M_PL_RR_DIFF
           WHEN 'StrCommodity' THEN ST.M_PL_STRCOM_DIFF
           WHEN 'TotalStrCRD' THEN ST.M_PL_TotalStrCRD_DIFF END) M_RESULTV
FROM (SELECT * FROM MRA_EXPORT_NYK_STRESSTESTING_REP
      WHERE M_DESCRIPTION = @revalRun:C AND M_SCENARIOID <> -1
      UNION ALL
      SELECT * FROM MRA_EXPORT_HKG_STRESSTESTING_REP
      WHERE M_DESCRIPTION = @revalRun:C AND M_SCENARIOID <> -1
      UNION ALL
      SELECT * FROM MRA_EXPORT_LDN_STRESSTESTING_REP
      WHERE M_DESCRIPTION = @revalRun:C AND M_SCENARIOID <> -1
      UNION ALL
      SELECT * FROM MRA_EXPORT_SAO_STRESSTESTING_REP
      WHERE M_DESCRIPTION = @revalRun:C AND M_SCENARIOID <> -1) ST
LEFT JOIN SB_SE_HEAD_REP SE_HEAD
  ON SE_HEAD.M_SE_D_LABEL = ST.M_INSTRUMENT
  AND SE_HEAD.M_REF_DATA = @MxDataSetKey:N
LEFT JOIN SB_CP_REP CP
  ON SE_HEAD.M_SE_ISS = CP.M_LABEL
  AND CP.M_REF_DATA = @MxDataSetKey:N
HAVING ABS(SUM(CASE @outputResult:C
           WHEN 'BCS' THEN ST.M_PL_BCS_DIFF
           WHEN 'CRD' THEN ST.M_PL_CRD_DIFF
           WHEN 'GenFX' THEN ST.M_PL_GenFX_DIFF
           WHEN 'GenIR' THEN ST.M_PL_GenIR_DIFF
           WHEN 'TotalStr' THEN ST.M_PL_TOTALSTR_DIFF
           WHEN 'RR' THEN ST.M_PL_RR_DIFF
           WHEN 'StrCommodity' THEN ST.M_PL_STRCOM_DIFF
           WHEN 'TotalStrCRD' THEN ST.M_PL_TotalStrCRD_DIFF END)) > 0.000001
GROUP BY ST.M_PORTFOLIO, ST.M_CURRENCY, ST.M_FAMILY, ST.M_GROUP, ST.M_TYPE,
         ST.M_INSTRUMENT, ST.M_PLKEY, ST.M_RISKSECTION, ST.M_ADDINFONUM1,
         ST.M_RISKLABEL2, M_ISSUER, M_COUNTRY, M_SECURITYCODE,
         ST.M_CONTAINER, ST.M_SCENARIOID
ORDER BY ST.M_PORTFOLIO, ST.M_CURRENCY, ST.M_FAMILY, ST.M_GROUP, ST.M_TYPE,
         ST.M_INSTRUMENT, ST.M_PLKEY, ST.M_RISKSECTION, ST.M_ADDINFONUM1,
         ST.M_RISKLABEL2, M_ISSUER, M_COUNTRY, M_SECURITYCODE,
         ST.M_CONTAINER, ST.M_SCENARIOID ASC
```

---

## 7. Sample Data

### 7.1 Recovery Rate (RR) Report Sample

```
ENTITY|LABEL|PARAM|BACK|IS_BENCH|HOR_DAYS|DATE|SCENARIO|OLABEL|RESULT|RESULTV|CUR|PL_CUR|PTFOLIO|TRN_FMLY|TRN_GRP|TRN_TYPE|INSTRUMENT|PL_KEY1|RSKSECTION|DEALNUM|DLDRAFT|ISSUER|CIF|GLOBUS_ID|COUNTRY|ISIN
LDN_STRRR|contStress|RR|N|N|1|20230420|61|P&L(i)|-410.28229|-112.33162|USD|USD|CTLNSBLALCOFRT|IRD|BOND||ARGENT 12/15/35 VAR| USD CORP|3798|||THE REPUBLIC OF ARGENTINA|100075554|101119|AR|US040114GM64
```

### 7.2 Field Values Explanation

| Field | Sample Value | Description |
|-------|-------------|-------------|
| ENTITY | LDN_STRRR | London + Stress + Recovery Rate |
| LABEL | contStress | Legacy scenario container name |
| PARAM | RR | Risk factor (Recovery Rate) |
| BACK | N | Not backtesting result |
| IS_BENCH | N | Not benchmark VaR |
| HOR_DAYS | 1 | 1-day horizon |
| DATE | 20230420 | Run date (20 Apr 2023) |
| SCENARIO | 61 | Scenario identifier |
| OLABEL | P&L(i) | Type of result |
| RESULT | -410.28229 | Scenario P&L value |
| RESULTV | -112.33162 | P&L difference from central point |
| CUR | USD | Trade currency |
| PL_CUR | USD | P&L currency |
| PTFOLIO | CTLNSBLALCOFRT | Portfolio |
| TRN_FMLY | IRD | Interest Rate Derivatives |
| TRN_GRP | BOND | Bond group |
| TRN_TYPE | (blank) | Trade type |
| INSTRUMENT | ARGENT 12/15/35 VAR | Argentine bond |
| PL_KEY1 | USD CORP | P&L key |
| RSKSECTION | 3798 | Risk section |
| ISSUER | THE REPUBLIC OF ARGENTINA | Issuer name |
| CIF | 100075554 | CIF identifier |
| GLOBUS_ID | 101119 | GLOBUS identifier |
| COUNTRY | AR | Argentina |
| ISIN | US040114GM64 | Security ISIN |

---

## 8. Data Quality Rules

### 8.1 Exclusion Rules

| Rule ID | Description |
|---------|-------------|
| DQ-ST-001 | Exclude central point (scenario = -1) |
| DQ-ST-002 | Exclude P&L vectors with absolute value below 0.000001 |

### 8.2 Validation Rules

| Rule ID | Description | Action |
|---------|-------------|--------|
| VR-ST-001 | All risk classes present in output | Alert if missing |
| VR-ST-002 | Static data joins successful | Alert if null enrichment |
| VR-ST-003 | Scenario IDs match expected scenarios | Alert if mismatch |

---

## 9. Processing Scripts

### 9.1 Report Formatting

**Script**: `/apps/murex/client/scripts/var/eod/formatriskreport.sh`

**Function**: Formats extracted reports to VESPA standards and creates ZIP packages

**Output Path**: `[App directory]/reports/today/eod/`

### 9.2 Export Configuration

**File**: `/apps/murex/mx/fs/public/mxres/mxmarketrisk_service/scripts/ant-targets-sources-EOD.mxres`

**Target**: `exportEODRun`

---

## 10. Delivery Specification

### 10.1 MFT Configuration

| Component | Value |
|-----------|-------|
| Protocol | MFT (Managed File Transfer) |
| Target System | VESPA (via RDS) |
| Frequency | Daily |

### 10.2 MFT IDs by Region

| Region | MFT ID |
|--------|--------|
| London | MurexGTSStressToVespa_LDN |
| Hong Kong | MurexGTSStressToVespa_HKG |
| New York | MurexGTSStressToVespa_NYK |
| São Paulo | MurexGTSStressToVespa_SAO |

---

## 11. Static Data Joins

### 11.1 Security Definition Join (SB_SE_HEAD_REP)

| Join Condition | Purpose |
|----------------|---------|
| SE_HEAD.M_SE_D_LABEL = ST.M_INSTRUMENT | Match by instrument label |
| SE_HEAD.M_REF_DATA = @MxDataSetKey:N | Match by data set |

**Fields Retrieved**: M_SE_CODE (Security Code/ISIN)

### 11.2 Counterparty Definition Join (SB_CP_REP)

| Join Condition | Purpose |
|----------------|---------|
| SE_HEAD.M_SE_ISS = CP.M_LABEL | Match by issuer label |
| CP.M_REF_DATA = @MxDataSetKey:N | Match by data set |

**Fields Retrieved**: M_DSP_LABEL (Issuer Name), M_H_CNT_CODE (Country Code)

### 11.3 SCF Special Handling

For SCF (Structured Credit Facility) trades where M_GROUP = 'SCF':
- If M_ISSUER is null, use CP.M_DSP_LABEL
- If M_COUNTRY is null, use CP.M_H_CNT_CODE
- If M_SECURITYCODE is null, use SE_HEAD.M_SE_CODE

---

## 12. Related Documentation

| Document | Description |
|----------|-------------|
| [stress-testing-overview.md](stress-testing-overview.md) | Architecture overview |
| [stress-testing-brd.md](stress-testing-brd.md) | Business requirements |
| [stress-testing-config.md](stress-testing-config.md) | Murex configuration |

---

*Document Version: 1.0 | Last Updated: 2025-01-13*
