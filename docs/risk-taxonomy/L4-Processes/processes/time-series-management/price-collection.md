---
# Process Metadata
process_id: MR-L4-005c
process_name: Price Collection
version: 1.0
effective_date: 2025-01-15
next_review_date: 2026-01-15
owner: Head of Reporting, Analysis & Validation (RAV)
approving_committee: MLRC

# Taxonomy Linkages
parent_process: MR-L4-005  # Time Series Management
l1_requirements:
  - REQ-L1-001  # CRR
  - REQ-L1-022  # BCBS 239
l2_risk_types:
  - MR-L2-001   # Market Risk
l7_systems:
  - SYS-MR-010  # Time Series Service
  - SYS-MR-006  # Market Data ODS
---

# Price Collection Process

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Process ID** | MR-L4-005c |
| **Version** | 1.0 |
| **Effective Date** | 15 January 2025 |
| **Parent Process** | Time Series Management (MR-L4-005) |
| **Owner** | Head of Reporting, Analysis & Validation (RAV) |

---

## 1. Purpose

The Price Collection process ensures that daily end-of-day (EOD) market observations are collected from all configured sources for every active risk factor. This process is the first step in the daily time series operations, feeding into cleaning, validation, curve stripping, and ultimately VaR calculation.

---

## 2. Scope

### 2.1 Collection Scope

| Source Type | Examples | Collection Method |
|-------------|----------|-------------------|
| **External - Real-time feeds** | Bloomberg, Reuters | API snapshot at EOD |
| **External - Batch files** | Markit, exchange files | File transfer (SFTP) |
| **Internal - Trader marks** | OTC desks, structured products | Post-IPV extraction |
| **Internal - Curves** | MDC-built curves | Market Data ODS extraction |

### 2.2 Data Types Collected

- Interest rates (par rates, zero rates, discount factors)
- Credit spreads (CDS spreads, bond spreads, index levels)
- FX rates (spot, forward points)
- Equity prices (stocks, indices)
- Commodity prices (spot, futures)
- Volatility surfaces (swaption, FX, equity)

---

## 3. Process Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           PRICE COLLECTION PROCESS                                      │
│                           (Daily - London Time)                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘

17:30 GMT ───────────────────────────────────────────────────────────────────────────────
          │
          │  ┌─────────────────────────────────────────────────────────────────────────┐
          │  │                 TRIGGER: EOD SNAPSHOT COMPLETED                         │
          │  │                                                                         │
          │  │  • MDC confirms EOD curves/prices approved (4-eyes)                     │
          │  │  • Finance confirms IPV complete for internal marks                     │
          │  │  • External source EOD snapshots available                              │
          │  └─────────────────────────────────────────────────────────────────────────┘
          │
18:30 GMT ───────────────────────────────────────────────────────────────────────────────
          │
          │  ┌─────────────────────────────────────────────────────────────────────────┐
          │  │                 1. SOURCE READINESS CHECK                               │
          │  │                                                                         │
          │  │  For each configured source:                                            │
          │  │  • Check connectivity                                                   │
          │  │  • Verify EOD snapshot available                                        │
          │  │  • Log readiness status                                                 │
          │  │                                                                         │
          │  │  If source unavailable → flag for exception handling                    │
          │  └─────────────────────────────────────────────────────────────────────────┘
          │
19:00 GMT ───────────────────────────────────────────────────────────────────────────────
          │
          │  ┌─────────────────────────────────────────────────────────────────────────┐
          │  │                 2. PARALLEL COLLECTION                                  │
          │  │                                                                         │
          │  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐       │
          │  │  │ EXTERNAL FEEDS   │  │ INTERNAL CURVES  │  │ INTERNAL MARKS   │       │
          │  │  │                  │  │                  │  │                  │       │
          │  │  │ Bloomberg API    │  │ Market Data ODS  │  │ Trading Systems  │       │
          │  │  │ Reuters API      │  │ extraction       │  │ (post-IPV)       │       │
          │  │  │ Markit batch     │  │                  │  │                  │       │
          │  │  │ Exchange files   │  │                  │  │                  │       │
          │  │  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘       │
          │  │           │                     │                     │                 │
          │  │           └─────────────────────┴─────────────────────┘                 │
          │  │                                 │                                       │
          │  │                                 ▼                                       │
          │  │                    ┌─────────────────────────┐                          │
          │  │                    │     STAGING AREA        │                          │
          │  │                    │                         │                          │
          │  │                    │  Raw observations with  │                          │
          │  │                    │  source metadata        │                          │
          │  │                    └─────────────────────────┘                          │
          │  └─────────────────────────────────────────────────────────────────────────┘
          │
19:15 GMT ───────────────────────────────────────────────────────────────────────────────
          │
          │  ┌─────────────────────────────────────────────────────────────────────────┐
          │  │                 3. INITIAL COMPLETENESS CHECK                           │
          │  │                                                                         │
          │  │  For each active risk factor:                                           │
          │  │  • Check observation received from configured source                    │
          │  │  • Log coverage metrics                                                 │
          │  │  • Flag missing observations                                            │
          │  │                                                                         │
          │  │  Missing observations → queue for backup source or proxy                │
          │  └─────────────────────────────────────────────────────────────────────────┘
          │
19:30 GMT ───────────────────────────────────────────────────────────────────────────────
          │
          │  ┌─────────────────────────────────────────────────────────────────────────┐
          │  │                 4. BACKUP SOURCE FALLBACK                               │
          │  │                                                                         │
          │  │  For missing observations with backup source configured:                │
          │  │  • Attempt collection from backup                                       │
          │  │  • Log fallback event for audit                                         │
          │  │  • Update source metadata on observation                                │
          │  └─────────────────────────────────────────────────────────────────────────┘
          │
19:45 GMT ───────────────────────────────────────────────────────────────────────────────
          │
          │  ┌─────────────────────────────────────────────────────────────────────────┐
          │  │                 5. COLLECTION COMPLETE                                  │
          │  │                                                                         │
          │  │  • Generate collection report                                           │
          │  │  • Pass to Cleaning & Validation process (MR-L4-005d)                    │
          │  │  • Any still-missing observations flagged for proxy consideration       │
          │  └─────────────────────────────────────────────────────────────────────────┘
          │
          ▼
    [To Cleaning & Validation Process]
```

---

## 4. Source Configuration

### 4.1 Source Types and Characteristics

| Source | Protocol | Latency | Coverage | Reliability |
|--------|----------|---------|----------|-------------|
| **Bloomberg** | B-PIPE / SFTP | Real-time | Broad | High |
| **Reuters** | Eikon API | Real-time | Broad | High |
| **Markit** | SFTP batch | T+1 morning | Credit specialist | High |
| **Exchanges** | Direct feed / SFTP | EOD | Listed instruments | High |
| **Internal MDC** | Database extract | Post-EOD | Full curve coverage | High |
| **Internal Trading** | Database extract | Post-IPV | Trader marks | Medium |

### 4.2 Source Selection per Risk Factor Type

| Risk Factor Type | Primary Source | Typical Backup |
|------------------|----------------|----------------|
| **Interest Rate Curves** | Internal MDC (post-strip) | Bloomberg |
| **FX Spot** | Bloomberg | Reuters |
| **FX Forward Points** | Bloomberg | Internal Trading |
| **Credit CDS** | Markit | Bloomberg |
| **Credit Indices** | Markit | Internal Trading |
| **Equity Spot** | Exchange | Bloomberg |
| **Commodity** | Exchange / Bloomberg | Reuters |
| **Volatility Surfaces** | Bloomberg / Internal | Reuters / Broker |

---

## 5. Collected Data Structure

### 5.1 Raw Observation Record

| Field | Description | Example |
|-------|-------------|---------|
| `collection_id` | Unique collection batch ID | COL-20250115-001 |
| `risk_factor_id` | Target risk factor | EUR_OIS_10Y |
| `observation_date` | Business date | 2025-01-15 |
| `observation_time` | Actual collection timestamp | 2025-01-15T19:05:32Z |
| `observation_value` | Raw value | 2.3456 |
| `source_system` | Data source | Bloomberg |
| `source_ticker` | Vendor identifier | EUSA10 Curncy |
| `collection_status` | Success / Failed / Backup | Success |
| `backup_used` | Whether backup source used | No |
| `ipv_status` | IPV approval (if internal) | Approved |

---

## 6. Controls

| Control ID | Control | Type | Owner |
|------------|---------|------|-------|
| PC-C01 | All active risk factors must have configured source | Preventive | RAV |
| PC-C02 | Collection batch must complete before T+1 cutoff | Preventive | RAV |
| PC-C03 | Source unavailability logged and alerted | Detective | RAV |
| PC-C04 | Backup source attempts logged | Detective | RAV |
| PC-C05 | Internal marks require IPV status check | Preventive | RAV |
| PC-C06 | Collection completeness report generated | Detective | RAV |

---

## 7. Exception Handling

### 7.1 Source Unavailability

| Scenario | Response | Escalation |
|----------|----------|------------|
| **Bloomberg down** | Switch to Reuters; alert RAV | RAV Team Lead |
| **Markit file delayed** | Wait until T+1 08:00; use previous day with flag | RAV Manager |
| **Exchange feed failure** | Use Bloomberg closing price | RAV Team |
| **Internal MDC not ready** | Wait; escalate if >1 hour delay | MDC Manager |
| **IPV not complete** | Cannot use internal marks; escalate to Finance | Product Control |

### 7.2 Missing Observations

| Coverage Level | Response |
|----------------|----------|
| **>99% collected** | Proceed; missing handled by proxy process |
| **95-99% collected** | Investigate; likely source issue |
| **<95% collected** | Halt collection; major issue - escalate immediately |

---

## 8. Service Levels

| Metric | Target | Threshold | Escalation |
|--------|--------|-----------|------------|
| Collection batch start | 19:00 GMT | 19:15 GMT | RAV Manager |
| Collection batch complete | 19:45 GMT | 20:00 GMT | RAV Manager |
| Coverage rate | 99.5% | 99.0% | Market Risk |
| Source fallback rate | <1% | <2% | RAV Team Lead |

---

## 9. Monitoring and Reporting

### 9.1 Real-Time Monitoring

- **Collection Dashboard**: Shows progress by source and risk factor type
- **Source Health**: Connectivity and response time metrics
- **Coverage Meter**: Live coverage percentage

### 9.2 Daily Reports

| Report | Recipients | Content |
|--------|------------|---------|
| **Collection Summary** | RAV, Market Risk | Coverage %, source usage, exceptions |
| **Source Performance** | RAV, IT | Availability, latency, fallback events |
| **Missing Observations** | RAV, Market Risk | List for proxy/investigation |

---

## 10. Integration Points

### 10.1 Upstream Dependencies

| System/Process | Dependency | Impact if Delayed |
|----------------|------------|-------------------|
| **EOD Market Data Snapshot** | MDC curves ready | Collection delayed |
| **IPV Process** | Internal marks approved | Cannot use trader marks |
| **External Feeds** | API/file available | Backup source or missing |

### 10.2 Downstream Consumers

| Process | Data Provided |
|---------|---------------|
| **Cleaning & Validation** | Raw observations for validation |
| **Curve Stripping** | Par rates for conversion |
| **Proxying Process** | Gap list for proxy application |

---

## 11. Related Documents

| Document | Relationship |
|----------|--------------|
| [Time Series Management](./time-series-overview.md) | Parent process |
| [Risk Factor Setup](./risk-factor-setup.md) | Upstream - defines what to collect |
| [Cleaning & Validation](./cleaning-validation.md) | Downstream - validates collected data |
| [EOD Market Data Snapshot](../eod-market-data-snapshot.md) | Upstream - provides internal curves |

---

## 12. Document Control

### 12.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-15 | Initial version | MLRC |

---

*End of Document*
