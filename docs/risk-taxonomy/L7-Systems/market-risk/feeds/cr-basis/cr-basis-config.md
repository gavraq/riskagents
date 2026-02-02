---
# Document Metadata
document_id: CR-BAS-CFG-001
document_name: CR Basis Rate Feed - IT Configuration Document
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Risk Technology
approving_committee: Risk Technology Steering Committee

# Parent Reference
parent_document: CR-BAS-BRD-001
feed_id: CR-BAS-001
---

# CR Basis Rate Feed - IT Configuration Document

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Document ID** | CR-BAS-CFG-001 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Risk Technology |
| **Related BRD** | CR-BAS-BRD-001 |

---

## 1. Configuration Overview

This document specifies the technical configuration for the CR Basis Rate feed within the Murex Global Operating Model (GOM). The feed extracts recovery rate sensitivities (BASIS) **without propagation** using the M_RECOVERY1 field.

### 1.1 Component Summary

| Component Type | Name | Purpose |
|---------------|------|---------|
| Simulation Views | VW_Vespa_Sensitivities, VW_Vespa_Sensitivities_CRDI | Source sensitivity data |
| Datamart Tables | TBL_VESPA_SENS_REP, TBL_VESPA_SENSCI_REP | Staging for extraction |
| Feeders | FD_VESPA_SENS, FD_VESPA_SENSCI | Populate datamart tables |
| Data Extractors | DE_VESPA_CR_BASIS | Extract to CSV |
| Extraction Requests | ER_VESPA_CR_BASIS | Execute extraction |
| Processing Scripts | **_MR_VESPA_BAS_RPT | Post-processing |
| Batch Events | BE_VESPA_BAS_** | Scheduled execution |

---

## 2. Murex GOM Configuration

### 2.1 Simulation Views

#### 2.1.1 Non-CRDI: VW_Vespa_Sensitivities

| Property | Value |
|----------|-------|
| **View Name** | VW_Vespa_Sensitivities |
| **Purpose** | Credit sensitivities for single-name products |
| **Key Sensitivity Field** | M_RECOVERY1 (Recovery Rate 2) |
| **Output** | BASIS - Recovery rate sensitivity without propagation |

**Filter Criteria**:
```sql
STP_STATUS IN ('RELE', 'VERI', 'STTL')
AND LEGAL_ENTITY = 'MGB'
AND CREDIT_DELTA_DATE IS NOT NULL
AND ISSUER IS NOT NULL
AND FAMILY IN ('CRD', 'IRD', 'EQD')
```

#### 2.1.2 CRDI: VW_Vespa_Sensitivities_CRDI

| Property | Value |
|----------|-------|
| **View Name** | VW_Vespa_Sensitivities_CRDI |
| **Purpose** | Credit sensitivities for credit index products |
| **Key Sensitivity Field** | M_RECOVERY1 (Recovery Rate 2) |
| **Output** | BASIS - Index-level recovery rate sensitivity |

**Filter Criteria**:
```sql
STP_STATUS IN ('RELE', 'VERI', 'STTL')
AND LEGAL_ENTITY = 'MGB'
AND GROUP = 'CRDI'
```

### 2.2 Sensitivity Calculation

#### 2.2.1 BASIS Calculation Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| **Sensitivity Type** | M_RECOVERY1 | Recovery Rate 2 in Simulation |
| **Propagation** | OFF | No propagation to credit spread curve |
| **Bump Size** | 1% | Recovery rate shock |
| **Calculation** | Full Revaluation | Complete MTM recalculation |

**Key Distinction from RR01**:
- **RR01** uses M_RECOVERY (Recovery Rate 1) WITH propagation
- **BASIS** uses M_RECOVERY1 (Recovery Rate 2) WITHOUT propagation

### 2.3 Datamart Tables

#### 2.3.1 TBL_VESPA_SENS_REP (Non-CRDI)

| Property | Value |
|----------|-------|
| **Table Name** | TBL_VESPA_SENS_REP |
| **Schema** | DATAMART |
| **Refresh Mode** | Truncate and Load |
| **Partition** | By ASOF_DATE |

#### 2.3.2 TBL_VESPA_SENSCI_REP (CRDI)

| Property | Value |
|----------|-------|
| **Table Name** | TBL_VESPA_SENSCI_REP |
| **Schema** | DATAMART |
| **Refresh Mode** | Truncate and Load |
| **Partition** | By ASOF_DATE |

### 2.4 Feeders

#### 2.4.1 FD_VESPA_SENS (Non-CRDI)

| Property | Value |
|----------|-------|
| **Feeder Name** | FD_VESPA_SENS |
| **Source** | VW_Vespa_Sensitivities |
| **Target** | TBL_VESPA_SENS_REP |
| **Mode** | Full Refresh |

#### 2.4.2 FD_VESPA_SENSCI (CRDI)

| Property | Value |
|----------|-------|
| **Feeder Name** | FD_VESPA_SENSCI |
| **Source** | VW_Vespa_Sensitivities_CRDI |
| **Target** | TBL_VESPA_SENSCI_REP |
| **Mode** | Full Refresh |

---

## 3. Data Extraction Configuration

### 3.1 Data Extractor: DE_VESPA_CR_BASIS

| Property | Value |
|----------|-------|
| **Extractor Name** | DE_VESPA_CR_BASIS |
| **Type** | SQL-based Extraction |
| **Output Format** | CSV |
| **Delimiter** | Comma (,) |
| **Header** | Yes |
| **Encoding** | UTF-8 |

### 3.2 Extraction SQL

```sql
-- Non-CRDI Credit Sensitivities (BASIS)
SELECT
    TRADE_NUMBER,
    PORTFOLIO,
    FAMILY,
    GRP,
    TYPE,
    TYPOLOGY,
    ISSUER,
    CURVE_NAME,
    CIF,
    GLOBUS_ID,
    COUNTRY,
    ISIN,
    BASIS,           -- Recovery sensitivity (local currency)
    BASIS_USD,       -- Recovery sensitivity (USD)
    CURRENCY,
    MATURITY,
    MDS,
    UNDERLYING,
    RESTRUCTURING,
    ASOF_DATE
FROM TBL_VESPA_SENS_REP
WHERE ASOF_DATE = :BUSINESS_DATE
  AND BASIS IS NOT NULL

UNION ALL

-- CRDI Credit Index Sensitivities (BASIS)
SELECT
    TRADE_NUMBER,
    PORTFOLIO,
    FAMILY,
    GRP,
    TYPE,
    TYPOLOGY,
    CRDI_LABEL AS ISSUER,      -- Index label as issuer
    CRDI_LABEL AS CURVE_NAME,  -- Index label as curve
    0 AS CIF,                   -- Not applicable for indices
    '' AS GLOBUS_ID,            -- Not applicable for indices
    '' AS COUNTRY,              -- Multi-country indices
    '' AS ISIN,                 -- Not applicable for indices
    BASIS,
    BASIS_USD,
    CURRENCY,
    MATURITY,
    MDS,
    UNDERLYING,
    RESTRUCTURING,
    ASOF_DATE
FROM TBL_VESPA_SENSCI_REP
WHERE ASOF_DATE = :BUSINESS_DATE
  AND BASIS IS NOT NULL
ORDER BY TRADE_NUMBER, CURVE_NAME
```

### 3.3 Extraction Request: ER_VESPA_CR_BASIS

| Property | Value |
|----------|-------|
| **Request Name** | ER_VESPA_CR_BASIS |
| **Data Extractor** | DE_VESPA_CR_BASIS |
| **Output Directory** | /data/feeds/vespa/cr_basis/ |
| **File Pattern** | MxMGB_MR_Credit_Basis_Rate_{REGION}_{YYYYMMDD}.csv |

### 3.4 Output File Configuration

| Property | Value |
|----------|-------|
| **File Name Pattern** | MxMGB_MR_Credit_Basis_Rate_{REGION}_{YYYYMMDD}.csv |
| **Example** | MxMGB_MR_Credit_Basis_Rate_LN_20250102.csv |
| **Field Count** | 20 |
| **Record Terminator** | LF |
| **Quoting** | Double quotes for text fields |

---

## 4. Processing Scripts

### 4.1 Regional Processing Scripts

| Region | Script Name | Purpose |
|--------|-------------|---------|
| London | LN_MR_VESPA_BAS_RPT | Process LN credit basis |
| Hong Kong | HK_MR_VESPA_BAS_RPT | Process HK credit basis |
| New York | NY_MR_VESPA_BAS_RPT | Process NY credit basis |
| Singapore | SP_MR_VESPA_BAS_RPT | Process SP credit basis |

### 4.2 Script Functionality

```bash
#!/bin/bash
# **_MR_VESPA_BAS_RPT Processing Script Template

# 1. Validate input files
validate_input_files()

# 2. Apply data quality checks
check_mandatory_fields()
validate_basis_values()
check_currency_codes()

# 3. Apply FX conversion (if needed)
apply_fx_rates()

# 4. Generate output file
generate_output_file()

# 5. Archive source files
archive_processed_files()

# 6. Trigger downstream notifications
notify_downstream_systems()
```

### 4.3 Data Quality Checks

| Check | Rule | Action |
|-------|------|--------|
| Mandatory Fields | All required fields populated | Reject record |
| BASIS Range | BASIS within reasonable bounds | Flag for review |
| Currency Validation | Valid ISO currency code | Reject record |
| Issuer Check | Non-CRDI must have issuer | Reject record |
| Duplicate Check | No duplicate trade/curve combinations | Take latest |

---

## 5. Batch Configuration

### 5.1 Batch Events

| Batch Event | Region | Schedule | Dependencies |
|-------------|--------|----------|--------------|
| BE_VESPA_BAS_LN | London | 04:30 GMT | BE_VALUATION_LN |
| BE_VESPA_BAS_HK | Hong Kong | 20:30 GMT (T) | BE_VALUATION_HK |
| BE_VESPA_BAS_NY | New York | 02:30 GMT | BE_VALUATION_NY |
| BE_VESPA_BAS_SP | Singapore | 21:30 GMT (T) | BE_VALUATION_SP |

### 5.2 Batch Sequence

```
BE_CREDIT_CURVES_** (Credit curve calibration)
    ↓
BE_VALUATION_** (Valuation batch)
    ↓
FD_VESPA_SENS / FD_VESPA_SENSCI (Feeder execution)
    ↓
BE_VESPA_BAS_** (BASIS extraction batch)
    ↓
**_MR_VESPA_BAS_RPT (Processing script)
    ↓
File delivery to VESPA
```

### 5.3 Batch Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| BUSINESS_DATE | :SYSDATE-1 | Previous business day |
| MDS_SET | {REGION}CLOSE | Regional market data set |
| LEGAL_ENTITY | MGB | Meridian Global Bank |
| TIMEOUT | 120 mins | Maximum batch runtime |
| RETRY_COUNT | 3 | Number of retry attempts |

---

## 6. Environment Configuration

### 6.1 Environment Details

| Environment | Purpose | Database | Schedule |
|-------------|---------|----------|----------|
| DEV | Development testing | MXDEV | On-demand |
| UAT | User acceptance testing | MXUAT | Daily (delayed) |
| PROD | Production | MXPROD | Daily (live) |

### 6.2 File System Paths

| Environment | Path |
|-------------|------|
| DEV | /data/dev/feeds/vespa/cr_basis/ |
| UAT | /data/uat/feeds/vespa/cr_basis/ |
| PROD | /data/prod/feeds/vespa/cr_basis/ |

### 6.3 Connection Details

| System | Connection | Protocol |
|--------|------------|----------|
| Murex → Datamart | JDBC | TNS |
| Datamart → File System | Direct | Local FS |
| File System → VESPA | SFTP | SSH |

---

## 7. Monitoring and Alerting

### 7.1 Monitoring Points

| Monitor | Threshold | Alert |
|---------|-----------|-------|
| Batch completion | >06:00 GMT | L2 Support |
| Record count variance | >10% vs T-1 | L2 Support |
| BASIS outliers | >10 std dev | RAV Team |
| Missing issuers | Any | Credit Data Team |
| File delivery | >06:30 GMT | L2 Support |

### 7.2 Alert Configuration

| Alert Type | Recipient | Channel |
|------------|-----------|---------|
| Batch failure | Risk Technology | Email, SMS |
| SLA breach | Risk Technology, RAV | Email, SMS |
| Data quality issue | RAV Team | Email |
| Downstream delay | VESPA Support | Email |

---

## 8. Recovery Procedures

### 8.1 Batch Failure Recovery

| Failure Type | Recovery Action |
|--------------|-----------------|
| Credit curve failure | Use T-1 curves, flag positions |
| Feeder failure | Rerun feeder, check source data |
| Extraction failure | Rerun extraction, check SQL |
| File transfer failure | Retry SFTP, check connectivity |
| Valuation failure | Escalate to L2, use T-1 values |

### 8.2 Data Recovery

| Scenario | Recovery Steps |
|----------|----------------|
| Missing positions | 1. Check feeder logs 2. Verify source view 3. Rerun feeder |
| Incorrect BASIS | 1. Verify M_RECOVERY1 source 2. Check propagation setting 3. Rerun calculation |
| Duplicate records | 1. Check UNION logic 2. Apply deduplication 3. Regenerate file |

---

## 9. Change Control

### 9.1 Configuration Changes

| Change Type | Approval Required | Lead Time |
|-------------|-------------------|-----------|
| Field addition | Risk Technology + RAV | 2 weeks |
| Filter change | Risk Technology | 1 week |
| Schedule change | Risk Technology | 3 days |
| New region | Risk Technology + MLRC | 4 weeks |

### 9.2 Version Control

| Component | Repository | Branch Strategy |
|-----------|------------|-----------------|
| SQL scripts | GitLab | Feature branches |
| Shell scripts | GitLab | Feature branches |
| Batch config | Murex Workflow | Change tickets |
| Documentation | Confluence | Version history |

---

## 10. Related Documentation

| Document | ID | Relationship |
|----------|-----|--------------|
| [CR Basis BRD](./cr-basis-brd.md) | CR-BAS-BRD-001 | Business requirements |
| [CR Basis IDD](./cr-basis-idd.md) | CR-BAS-IDD-001 | Interface specification |
| [CR Delta Zero Config](../cr-delta-zero/cr-delta-zero-config.md) | CR-DZ-CFG-001 | Related CR01 config |
| [Murex GOM Guide](../../murex-gom-guide.md) | MR-L7-GOM | GOM reference |
| [Batch Operations Guide](../../batch-operations.md) | MR-L7-BATCH | Batch procedures |

---

## 11. Document Control

### 11.1 Version History

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | 2025-01-02 | Initial version | Risk Technology |

### 11.2 Review Schedule

| Review Type | Frequency | Next Due |
|-------------|-----------|----------|
| Technical review | Annual | January 2026 |
| Performance review | Quarterly | April 2025 |
| Security review | Annual | January 2026 |

---

*End of Document*
