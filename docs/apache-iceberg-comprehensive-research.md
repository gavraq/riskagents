# Apache Iceberg: Comprehensive Research for Trading & Risk Data Lakehouse Architecture

**Research Date:** December 11, 2025
**Context:** Adapting a traditional ODS/Data Warehouse architecture for trading and risk data to an Apache Iceberg-based Data Lakehouse, with focus on FpML trade messages converted to Parquet format.

---

## Table of Contents

1. [What is Apache Iceberg?](#what-is-apache-iceberg)
2. [Core Architecture](#core-architecture)
3. [Key Features](#key-features)
4. [File Format Support](#file-format-support)
5. [Query Engine Integration](#query-engine-integration)
6. [Data Lakehouse Pattern](#data-lakehouse-pattern)
7. [Comparison with Alternatives](#comparison-with-alternatives)
8. [Financial Services Applications](#financial-services-applications)
9. [Best Practices for Financial Data](#best-practices-for-financial-data)
10. [Migration from ODS/DWH to Iceberg](#migration-from-odsdwh-to-iceberg)
11. [Recommendations](#recommendations)

---

## 1. What is Apache Iceberg?

Apache Iceberg is an **open table format** for large-scale analytics on data lakes, originally developed at Netflix to address limitations in Apache Hive's architecture. It provides:

- **ACID transactions** for data consistency and reliability
- **Schema and partition evolution** without costly data rewrites
- **Time travel** capabilities for querying historical data
- **Hidden partitioning** that abstracts partitioning complexity from users
- **Snapshot isolation** for consistent concurrent reads and writes

### Key Innovation

Iceberg emerged to solve fundamental data lake challenges:
- Slow data evolution
- Inefficient reads/writes
- Lack of ACID transaction support
- Complex partition management
- Inability to perform row-level updates/deletes efficiently

> "Apache Iceberg is the missing layer that turned 'dump it in the lake' into 'query reliable tables.' It brings back the guarantees we loved in warehouses—ACID, schema control, and consistent views—without giving up cloud-scale storage and engine choice."

### Version History

- **Version 1**: Core spec for managing large analytic tables using immutable file formats (Parquet, Avro, ORC)
- **Version 2**: Adds row-level updates and deletes via delete files
- **Version 3**: Extends data types (nanosecond timestamps, variant, geometry, geography)
- **Version 4**: Currently under active development

---

## 2. Core Architecture

Apache Iceberg uses a **three-layer architecture** that separates concerns and enables its powerful features:

### 2.1 Data Layer

The data layer stores actual data in **immutable file formats**:
- **Parquet** (default, columnar format for analytics)
- **Avro** (row-based, optimized for streaming/writes)
- **ORC** (columnar, Hadoop-optimized)

**Key Concept: Immutability**
- Instead of modifying existing files, Iceberg creates new data files
- Updates use delete files (positional, equality, or deletion vectors)
- Enables consistent snapshots and time travel

### 2.2 Metadata Layer

The metadata layer manages table structure and file tracking using JSON metadata files:

- **Metadata Files**: Track table schema, partitions, snapshots, and properties
- **Manifest Files**: Contain file-level information (location, size, partition, row/column stats)
- **Manifest Lists**: Act as directories for manifest files, enabling quick table scans

This layer enables:
- Efficient query planning through file-level statistics
- Partition pruning without reading data
- Schema evolution tracking
- Snapshot history management

### 2.3 Catalog Layer

The catalog layer maintains pointers to the current metadata file:

- **Atomic Updates**: Pointer updates ensure ACID compliance
- **Multiple Catalog Types**: Hive Metastore, AWS Glue, REST-based catalogs, Nessie
- **Transaction Coordination**: Ongoing changes invisible until committed

Supported catalog implementations:
- Hive Metastore (traditional)
- AWS Glue Catalog
- REST Catalog
- Nessie (Git-like versioning)
- Custom implementations

---

## 3. Key Features

### 3.1 Schema Evolution

**Native schema evolution without data rewrites:**
- Add, drop, rename, reorder columns
- Widen column types (e.g., INT to BIGINT)
- Support for nested structures
- Backward compatibility maintained in metadata

**Financial Data Benefits:**
- Adapt to regulatory changes (new reporting fields)
- Evolve trade schemas as products become more complex
- Add risk metrics incrementally without disruption
- Historical data remains queryable after schema changes

### 3.2 Partition Evolution

**In-place partition strategy changes:**
- Update partitioning without rewriting data
- Old and new partition schemes coexist
- Metadata tracks multiple partition versions

**Example Use Case:**
```
# Initial: Partition trades by month (2023 data)
partition_spec = [month(trade_date)]

# Later: Switch to daily partitions (2024+ data)
partition_spec = [day(trade_date)]

# Both coexist seamlessly in the same table
```

### 3.3 Hidden Partitioning

**User-friendly partitioning abstraction:**
- Users query natural columns (e.g., `trade_date`)
- Iceberg automatically applies partition transforms
- No need to reference partition columns explicitly

**Supported Transforms:**
- `identity` - Use column value as-is
- `year`, `month`, `day`, `hour` - Extract time components
- `bucket[N]` - Hash-based bucketing
- `truncate[W]` - Truncate strings/numbers
- `void` - Hidden partition (no physical partitioning)

**Example:**
```sql
-- Partition by month, but users query by date
CREATE TABLE trades (
  trade_id STRING,
  trade_date DATE,
  notional DECIMAL
)
PARTITIONED BY (month(trade_date));

-- Users query naturally - Iceberg handles partition pruning
SELECT * FROM trades
WHERE trade_date BETWEEN '2025-01-15' AND '2025-02-15';
```

### 3.4 Time Travel & Versioning

**Query historical data via snapshots:**
- Each write creates a new snapshot
- Snapshots retained until explicitly expired
- Query any historical version by timestamp or snapshot ID

**Use Cases:**
- **Regulatory Compliance**: "What did our risk report show at EOD last quarter?"
- **Audit Trails**: Compare positions between two points in time
- **Error Recovery**: Rollback to previous version after bad data ingestion
- **Testing**: Use production snapshot for testing without copying data

**Query Syntax (Spark):**
```sql
-- Query as of specific timestamp
SELECT * FROM trades TIMESTAMP AS OF '2025-01-31 23:59:59';

-- Query specific snapshot
SELECT * FROM trades VERSION AS OF 123456789;

-- Query using branch/tag
SELECT * FROM trades VERSION AS OF 'eod-2025-01-31';
```

### 3.5 ACID Transactions

**Full ACID guarantees for data lake operations:**

- **Atomicity**: Operations complete fully or not at all
- **Consistency**: Tables always in valid state
- **Isolation**: Concurrent operations don't interfere (snapshot isolation)
- **Durability**: Committed changes persist

**Concurrency Model:**
- **Readers** never block writers (snapshot isolation)
- **Writers** use optimistic concurrency control
- **No locks** for read operations
- **Atomic pointer updates** for commits

**Financial Data Benefits:**
- Multiple processes can safely write to the same table
- End-of-day processing doesn't block intraday queries
- Risk calculations can run concurrently with trade ingestion

### 3.6 Row-Level Operations

**Efficient updates and deletes without full rewrites:**

**Delete Files (V2 Spec):**
- **Positional Deletes**: Identify rows by file path and position
- **Equality Deletes**: Identify rows by column values
- **Deletion Vectors** (V3): Optimized positional deletes

**Write Strategies:**
- **Copy-on-Write (CoW)**: Rewrite data files immediately (faster reads)
- **Merge-on-Read (MoR)**: Write deltas separately (faster writes, merge on read)

**Trade-offs:**
```
Copy-on-Write:
✓ Faster queries (no merge overhead)
✗ Slower updates (file rewrites)
✓ Best for read-heavy workloads

Merge-on-Read:
✓ Faster updates (append-only)
✗ Slower queries (merge overhead)
✓ Best for streaming/high-frequency updates
```

---

## 4. File Format Support

Apache Iceberg supports three columnar/row-based formats with different trade-offs:

### 4.1 Apache Parquet (Recommended Default)

**Columnar format optimized for analytics:**

**Strengths:**
- Excellent compression ratios
- Efficient column pruning
- Built-in column statistics
- Best for analytical queries
- Wide ecosystem support

**Best For:**
- Analytical/OLAP workloads
- Read-heavy patterns
- Wide tables with selective column access
- Complex aggregations

**Trade Data Usage:**
- Historical trade repositories
- Risk metric tables (VaR, Greeks)
- Market data time series
- Position snapshots

### 4.2 Apache Avro

**Row-based format with schema evolution:**

**Strengths:**
- Fast write performance
- Excellent schema evolution
- Compact binary encoding
- Native Kafka integration
- Self-describing format

**Best For:**
- Streaming workloads (Kafka, Flink)
- Write-heavy patterns
- CDC (Change Data Capture)
- Schema evolution requirements

**Trade Data Usage:**
- Real-time trade capture
- FpML message ingestion (initial landing)
- Streaming market data
- CDC from transactional systems

**Compaction Pattern:**
```
1. Ingest: Write streaming data as Avro (fast writes)
2. Compact: Periodically convert to Parquet (optimized reads)
3. Result: Best of both worlds
```

### 4.3 Apache ORC

**Columnar format optimized for Hadoop:**

**Strengths:**
- Native ACID support in Hive
- Lightweight indexing
- Aggressive compression
- Predicate pushdown optimization

**Best For:**
- Hive-centric ecosystems
- Hadoop/HDFS environments
- ACID requirements within Hive

**Trade Data Usage:**
- Legacy Hadoop migrations
- Hive-based data pipelines
- Organizations standardized on ORC

### 4.4 File Format Selection Matrix

| Dimension | Parquet | Avro | ORC |
|-----------|---------|------|-----|
| **Read Performance** | Excellent | Good | Excellent |
| **Write Performance** | Good | Excellent | Good |
| **Compression** | Excellent | Good | Excellent |
| **Analytics** | Best | Fair | Best |
| **Streaming** | Fair | Best | Fair |
| **Schema Evolution** | Good | Excellent | Good |
| **Ecosystem Support** | Widest | Wide | Hadoop-focused |
| **Default Choice** | Yes | Streaming only | Legacy only |

### 4.5 Best Practice: Hybrid Approach

**For high-volume trading systems:**

```
┌─────────────────┐
│ Real-time Layer │ → Avro (fast ingestion)
└────────┬────────┘
         │
         ↓ Compaction (hourly/daily)
┌─────────────────┐
│ Analytical Layer│ → Parquet (optimized queries)
└─────────────────┘
```

**AWS S3 Tables** (2025) supports automatic compaction across formats with 12-40% performance improvement.

---

## 5. Query Engine Integration

Apache Iceberg's **engine-agnostic design** enables multi-engine access to the same tables without data duplication.

### 5.1 Supported Engines (2025)

**Production-Ready:**
- Apache Spark
- Apache Flink
- Trino (Presto)
- Dremio
- Snowflake
- AWS Athena
- DuckDB
- StarRocks
- Google BigQuery
- Databricks

**Emerging/Experimental:**
- ClickHouse
- PostgreSQL (via pg_lake extension)

### 5.2 Engine Comparison

#### Apache Spark

**Strengths:**
- Most mature Iceberg integration
- Full read/write support
- DataFrames + SQL support
- Extensive optimization features
- Horizontal scalability

**Best For:**
- Large-scale batch processing
- Complex transformations
- ETL/ELT pipelines
- Machine learning workloads

**Trading Use Case:**
```python
# End-of-day risk aggregation
spark.sql("""
  INSERT INTO risk_metrics_daily
  SELECT
    trade_date,
    portfolio_id,
    SUM(notional) as total_notional,
    calculate_var(positions) as var_95
  FROM trades
  WHERE trade_date = current_date()
  GROUP BY trade_date, portfolio_id
""")
```

#### Trino (formerly Presto)

**Strengths:**
- Blazing-fast interactive queries
- MPP (massively parallel processing)
- In-memory processing
- Multi-source federation (join across systems)
- Lightweight compared to Spark

**Best For:**
- Ad-hoc analytics
- Business intelligence queries
- Interactive dashboards
- Cross-system joins (Iceberg + PostgreSQL + MySQL)

**Trading Use Case:**
```sql
-- Real-time risk dashboard
SELECT
  p.portfolio_name,
  t.trade_count,
  r.current_var
FROM iceberg.prod.portfolios p
JOIN iceberg.prod.trade_summary t ON p.portfolio_id = t.portfolio_id
JOIN postgres.risk.latest_metrics r ON p.portfolio_id = r.portfolio_id
WHERE t.trade_date = current_date();
```

**Performance Note:** Trino often outperforms Spark for query speed due to specialized query execution optimization.

#### Apache Flink

**Strengths:**
- True streaming engine
- Low-latency processing (<200ms)
- Exactly-once semantics
- Native CDC support
- Real-time analytics

**Best For:**
- Real-time data ingestion
- Streaming ETL
- CDC from databases
- Real-time risk monitoring

**Trading Use Case:**
```python
# Real-time trade ingestion with enrichment
flink_env.from_source(kafka_source)
  .map(parse_fpml)
  .key_by(lambda t: t.trade_id)
  .window(TumblingEventTimeWindows.of(Time.seconds(10)))
  .aggregate(trade_aggregator)
  .sink_to(iceberg_sink)
```

#### DuckDB

**Strengths:**
- Embedded analytics engine
- Zero configuration
- Excellent single-node performance
- Native Iceberg support (2025)
- Perfect for local analysis

**Best For:**
- Local data analysis
- Prototyping
- Small-to-medium datasets
- Python/Jupyter notebooks
- Development/testing

**Trading Use Case:**
```python
import duckdb

# Quick analysis on laptop
conn = duckdb.connect()
conn.execute("""
  SELECT
    asset_class,
    COUNT(*) as trade_count,
    SUM(notional) as total_notional
  FROM iceberg_scan('s3://trades/prod.db/trades')
  WHERE trade_date = '2025-12-11'
  GROUP BY asset_class
""").df()
```

**AWS Collaboration (2025):** DuckDB now has seamless integration with S3 Tables for Iceberg access.

#### Dremio

**Strengths:**
- Semantic layer over Iceberg
- Self-service data access
- Query acceleration/caching
- Data virtualization
- Columnar Cloud Cache

**Best For:**
- Self-service analytics
- Business user access
- Multi-source data access
- Performance acceleration

**Trading Use Case:** Enable business users to query trading data without deep technical knowledge.

### 5.3 Multi-Engine Architecture Pattern

**Common Financial Services Pattern:**

```
┌────────────────────────────────────────────────┐
│         Apache Iceberg Tables (S3/ADLS)        │
│    (Single source of truth - no duplication)   │
└───┬────────────┬─────────────┬─────────────┬───┘
    │            │             │             │
┌───▼────┐  ┌───▼────┐   ┌────▼────┐   ┌────▼────┐
│  Flink │  │  Spark │   │  Trino  │   │ DuckDB  │
│        │  │        │   │         │   │         │
│Ingest  │  │  Batch │   │ Queries │   │  Local  │
│ (CDC)  │  │  ETL   │   │   BI    │   │Analysis │
└────────┘  └────────┘   └─────────┘   └─────────┘
```

**Key Advantage:** Each engine optimized for its purpose, all accessing the same data.

### 5.4 Query Optimization Features

**Iceberg provides engines with rich metadata for optimization:**

- **Partition Pruning**: Skip irrelevant partitions using metadata
- **File Pruning**: Skip files using min/max statistics
- **Column Pruning**: Read only required columns (Parquet/ORC)
- **Predicate Pushdown**: Filter at storage layer
- **Metadata Caching**: Cache manifest files for faster planning

**Example Impact:**
```
Query: SELECT * FROM trades WHERE trade_date = '2025-12-11'

Without Iceberg: Scan 10TB, 100,000 files
With Iceberg: Scan 10GB, 100 files (1000x reduction)
```

---

## 6. Data Lakehouse Pattern

### 6.1 What is a Data Lakehouse?

A **data lakehouse** combines the best of data lakes and data warehouses:

**From Data Lakes:**
- Low-cost object storage (S3, ADLS, GCS)
- Scalability to petabyte scale
- Open formats (Parquet, Avro)
- Multi-engine support
- Flexibility for unstructured/semi-structured data

**From Data Warehouses:**
- ACID transactions
- SQL query performance
- Schema enforcement
- Governance and security
- BI tool integration

**Iceberg's Role:** Iceberg is the table format layer that enables lakehouse architecture by bringing warehouse-like capabilities to data lakes.

### 6.2 Lakehouse Architecture Layers

```
┌─────────────────────────────────────────────────┐
│   Consumption Layer (BI, ML, Applications)      │
├─────────────────────────────────────────────────┤
│   Query Engines (Spark, Trino, Flink, DuckDB)  │
├─────────────────────────────────────────────────┤
│   Governance (Catalog, Access Control, Audit)  │
├─────────────────────────────────────────────────┤
│   Table Format (Apache Iceberg)                 │
│   • Metadata Layer (snapshots, manifests)      │
│   • Schema & Partition Management              │
│   • ACID Transaction Coordination              │
├─────────────────────────────────────────────────┤
│   Storage Layer (S3, ADLS, GCS)                │
│   • Data Files (Parquet, Avro, ORC)           │
│   • Cost-effective Object Storage              │
└─────────────────────────────────────────────────┘
```

### 6.3 Medallion Architecture (Bronze/Silver/Gold)

**Recommended pattern for data organization:**

#### Bronze Layer (Raw Data)
- **Purpose**: Land raw data with minimal transformation
- **Format**: Avro or Parquet
- **Pattern**: Append-only, preserves source fidelity
- **Iceberg Benefit**: Schema evolution without rewrites

**Trading Example:**
```
bronze/
  fpml_messages/      # Raw FpML as Avro
  market_data_feeds/  # Raw market data
  confirmations/      # Trade confirmations
```

#### Silver Layer (Cleansed & Conformed)
- **Purpose**: Standardized, validated, enriched data
- **Format**: Parquet
- **Pattern**: SCD Type 2, deduplication, quality checks
- **Iceberg Benefit**: Efficient updates via delete files

**Trading Example:**
```
silver/
  trades/            # Parsed & validated trades
  positions/         # Aggregated positions
  reference_data/    # Enriched reference data
```

#### Gold Layer (Business Aggregates)
- **Purpose**: Business-ready datasets, pre-aggregated
- **Format**: Parquet
- **Pattern**: Star schema, aggregates, metrics
- **Iceberg Benefit**: Time travel for historical analysis

**Trading Example:**
```
gold/
  risk_metrics_daily/     # Daily VaR, Greeks
  pnl_by_portfolio/       # P&L aggregations
  trade_summary_monthly/  # Management reports
```

### 6.4 Streaming + Batch Unification

**Modern pattern: Single architecture for both paradigms**

```
┌──────────────────────────────────────────────┐
│ Streaming Data (Kafka/Flink) ───┐            │
│                                  │            │
│ Batch Data (Spark/ETL) ──────────┤            │
│                                  ↓            │
│                        ┌─────────────────┐   │
│                        │ Iceberg Tables  │   │
│                        └─────────────────┘   │
│                                  │            │
│                                  ├─→ Real-time Queries (Trino)
│                                  ├─→ Batch Analytics (Spark)
│                                  └─→ ML Training (Python)
└──────────────────────────────────────────────┘
```

**Key Benefits:**
- No separate systems for streaming vs. batch
- Unified governance and metadata
- Reduced operational complexity
- Lower infrastructure costs

### 6.5 Real-World Scale: Salesforce Case Study (2025)

**Enterprise-scale implementation:**
- **4 million** Iceberg tables
- **50 petabytes** of data
- **~90% metadata cache hit rate**

**Key Architectural Decisions:**
1. **Event-Driven Processing**: Storage Native Change Events (SNCE) trigger optimization
2. **Incremental Processing**: Avoid schedule-based full scans
3. **Shared Metadata Cache**: All microservices use common cache
4. **Reactive Optimization**: Storage Optimizer responds to changes

**Lesson:** Iceberg scales to massive enterprise deployments with proper architecture.

---

## 7. Comparison with Alternatives

### 7.1 The "Big Three" Table Formats

| Feature | Apache Iceberg | Delta Lake | Apache Hudi |
|---------|----------------|------------|-------------|
| **Origin** | Netflix | Databricks | Uber |
| **Primary Focus** | Multi-engine lakehouse | Spark-centric lakehouse | Streaming data lake |
| **Governance** | Apache Foundation | Linux Foundation (2024) | Apache Foundation |
| **License** | Apache 2.0 | Apache 2.0 | Apache 2.0 |

### 7.2 Feature Comparison

#### Schema Evolution
- **Iceberg**: Most flexible, supports complex nested schema changes
- **Delta Lake**: Good, emphasizes schema enforcement for quality
- **Hudi**: Good, schema evolution supported

#### Partition Evolution
- **Iceberg**: Excellent, true in-place evolution without rewrites
- **Delta Lake**: Limited, requires rewriting for major changes
- **Hudi**: Good, supports partition changes

#### Time Travel
- **Iceberg**: Excellent, unlimited snapshots (until expired)
- **Delta Lake**: Good, retention policies apply
- **Hudi**: Good, savepoint-based

#### Engine Support
- **Iceberg**: Widest ecosystem (Spark, Flink, Trino, Dremio, DuckDB, Snowflake, BigQuery, etc.)
- **Delta Lake**: Spark-optimized, growing ecosystem (Trino, Flink, etc.)
- **Hudi**: Strong with Spark and Flink, growing support

#### Write Performance
- **Iceberg**: Good, optimized for batch and streaming
- **Delta Lake**: Good, Spark-optimized
- **Hudi**: Excellent, designed for high-frequency updates (MoR mode)

#### Read Performance
- **Iceberg**: Good-Excellent (depends on maintenance)
- **Delta Lake**: Good-Excellent
- **Hudi**: Good (CoW mode), Fair (MoR mode - merge overhead)

#### CDC Support
- **Iceberg**: Good, via Flink CDC + delete files
- **Delta Lake**: Good, via Delta Change Data Feed
- **Hudi**: Excellent, native CDC focus, built-in indexing

#### Vendor Lock-in
- **Iceberg**: Lowest, true multi-engine by design
- **Delta Lake**: Medium, Databricks-optimized but increasingly open
- **Hudi**: Low, Apache governance

### 7.3 2025 Industry Trends

**Iceberg is becoming the de facto standard:**
- Major cloud providers (AWS, GCP, Azure) prioritize Iceberg
- Snowflake native Iceberg support (2024+)
- Google BigQuery native Iceberg (2024+)
- Apache XTable enables interoperability between formats

**Format Wars Are Over (2025 Perspective):**
> "The Hudi community has moved on from format wars as it recently introduced native Apache Iceberg format support. In 2025 it's no longer about what 'table format' you should be using, and now it's a question of how are you managing your 'database on the lake.'"

**Apache XTable (Incubating):** Provides seamless interoperability between Hudi, Delta, and Iceberg—no need to choose just one.

### 7.4 Recommendation Matrix

| Scenario | Recommended Format |
|----------|-------------------|
| Multi-engine access critical | **Iceberg** |
| Avoid vendor lock-in | **Iceberg** |
| Spark-only environment | Delta Lake or Iceberg |
| High-frequency updates/CDC | Hudi or Iceberg |
| Complex schema evolution | **Iceberg** |
| Financial services (flexible queries) | **Iceberg** |
| Regulatory compliance (time travel) | **Iceberg** or Delta Lake |
| Streaming-first architecture | Hudi or Iceberg + Flink |

### 7.5 Performance Benchmarks (General Trends)

**TPC-DS Benchmarks:**
- Delta Lake and Hudi show comparable performance
- Iceberg trails slightly in raw performance
- **BUT:** Performance differences are marginal compared to architectural flexibility

**Key Consideration:**
- Default Hudi settings optimize for mutable workloads (upsert)
- Default Iceberg/Delta optimize for append-only
- Fair comparison requires matching workload patterns

**Real-World Insight:** Architectural flexibility, ecosystem support, and operational simplicity often matter more than micro-benchmark differences.

---

## 8. Financial Services Applications

### 8.1 Key Use Cases

#### Trade Data Management
- **Challenge**: High volume, complex schemas (FpML), frequent updates
- **Iceberg Solution**:
  - Schema evolution handles product complexity
  - Hidden partitioning by trade_date, asset_class, counterparty
  - Time travel for trade reconstruction
  - CDC patterns for ODS synchronization

#### Market Data Storage
- **Challenge**: Massive time-series data, high ingestion rates
- **Iceberg Solution**:
  - Avro for fast ingestion → Parquet for analytics
  - Partition by day/hour using hidden partitioning
  - Snapshot isolation for consistent views during market hours
  - Efficient column pruning for symbol-specific queries

#### Risk Metrics & Calculations
- **Challenge**: Computed data, point-in-time accuracy, regulatory reporting
- **Iceberg Solution**:
  - Store calculations as separate tables (VaR, Greeks, stress tests)
  - Time travel: "What was VaR at EOD 2024-12-31?"
  - Partition by calculation_date + portfolio_id
  - Snapshot tags for regulatory submission versions

#### Position Snapshots
- **Challenge**: EOD positions, historical comparison, audit requirements
- **Iceberg Solution**:
  - Daily snapshot tables with full ACID guarantees
  - Branch/tag snapshots for month-end, quarter-end
  - Efficient storage via Parquet compression
  - Time travel eliminates need for separate historical tables

### 8.2 Regulatory & Compliance Benefits

**Audit Trails:**
- Complete history via snapshot log
- Immutable data files (tamper-proof)
- Metadata tracks all changes (who, when, what)

**Point-in-Time Reporting:**
```sql
-- Generate Q4 2024 regulatory report (run in 2025)
SELECT
  portfolio_id,
  SUM(market_value) as total_exposure,
  MAX(var_95) as max_var
FROM trades TIMESTAMP AS OF '2024-12-31 17:00:00'
WHERE booking_entity = 'EU_ENTITY'
GROUP BY portfolio_id;
```

**Data Lineage:**
- Snapshot metadata provides full lineage
- Track data provenance through layers
- Support BCBS 239 requirements (Risk Data Aggregation)

**Retention & Archival:**
- Expire old snapshots per policy
- Metadata compaction for long-term storage
- Separate hot/cold storage tiers

### 8.3 Financial Institution Reference Architecture

```
┌─────────────────────────────────────────────────┐
│        Front Office / Trading Systems           │
│    (Trade capture, OMS, Risk engines)           │
└───────────┬─────────────────────────────────────┘
            │ FpML, FIX, Proprietary formats
            ↓
┌───────────────────────────────────────────────┐
│    Ingestion Layer (Kafka + Flink)            │
│    • Parse FpML → structured events           │
│    • Validation & enrichment                  │
│    • CDC from transactional databases         │
└───────────┬───────────────────────────────────┘
            │
            ↓
┌─────────────────────────────────────────────────┐
│         Apache Iceberg Lakehouse (S3)           │
│                                                 │
│  Bronze: Raw trades, messages, market data     │
│  Silver: Validated trades, positions, ref data │
│  Gold: Risk metrics, P&L, aggregates           │
│                                                 │
│  Tables:                                        │
│  • trades (partitioned by date, asset_class)   │
│  • positions (snapshot per EOD)                │
│  • market_data (time-series, symbol-based)     │
│  • risk_metrics (VaR, Greeks, stress results)  │
│  • reference_data (counterparties, products)   │
└───────────┬─────────────────────────────────────┘
            │
            ↓ Multi-engine access
┌────────────────────────────────────────────────┐
│           Consumption Layer                     │
│                                                 │
│  Trino: Interactive queries, BI dashboards     │
│  Spark: Batch risk calculations, EOD processing│
│  DuckDB: Analyst ad-hoc queries, notebooks     │
│  Python: ML models, custom analytics           │
│                                                 │
│  Use Cases:                                     │
│  • Real-time risk dashboards                   │
│  • Regulatory reporting (MiFID II, Dodd-Frank)│
│  • Stress testing & scenario analysis          │
│  • P&L attribution & analysis                  │
│  • Trade lifecycle management                  │
└────────────────────────────────────────────────┘
```

### 8.4 Real-World Financial Services Implementations

**Large Financial Institution (Anonymous):**
- Adopted Iceberg to preserve years of investment in custom risk calculation engines
- Uses Iceberg metadata layer alongside existing data pipelines
- Time travel critical for compliance and regulatory reporting
- Multi-engine access enables different teams to use preferred tools

**Benefits Realized:**
- Reduced storage costs (vs. traditional DWH)
- Faster time-to-insight for analysts
- Simplified compliance (time travel, audit trails)
- Eliminated data duplication across systems
- Improved data freshness (streaming CDC)

**Typical ROI Drivers:**
1. **Storage Cost Reduction**: 60-80% vs. proprietary DWH
2. **Query Performance**: 10-100x for partition-pruned queries
3. **Development Velocity**: Faster schema changes, no migration downtime
4. **Operational Simplicity**: Unified platform vs. fragmented systems

---

## 9. Best Practices for Financial Data

### 9.1 Partitioning Strategies

#### Trade Data

**Recommended Strategy: Multi-dimensional partitioning**

```sql
CREATE TABLE trades (
  trade_id STRING,
  trade_date DATE,
  asset_class STRING,
  counterparty_id STRING,
  notional DECIMAL(18,2),
  product_type STRING,
  ...
)
PARTITIONED BY (
  year(trade_date),    -- Coarse-grained pruning
  month(trade_date),   -- Month-level queries
  bucket(16, asset_class)  -- Handle skew
);
```

**Rationale:**
- **Date partitioning**: 90% of queries filter by date
- **Bucket by asset_class**: Prevents skew (e.g., "IR Swaps" dominating)
- **Three-column split** (year/month/day): Enhanced pruning, Athena compatibility

**Anti-patterns:**
- ❌ High-cardinality: `PARTITIONED BY (trade_id)` → millions of partitions
- ❌ Low-cardinality: `PARTITIONED BY (currency)` → uneven distribution
- ❌ Over-partitioning: More than 3-4 partition columns

**Optimization Guidelines:**
- Target **100-10,000 files per partition**
- Aim for **100MB-1GB per file** (Parquet)
- Total table size **> 1TB** before partitioning
- Use `bucket[N]` for skewed dimensions

#### Market Data (Time Series)

**Recommended Strategy: Time-based partitioning**

```sql
CREATE TABLE market_data_ticks (
  symbol STRING,
  timestamp TIMESTAMP,
  bid DECIMAL(18,6),
  ask DECIMAL(18,6),
  ...
)
PARTITIONED BY (
  day(timestamp),
  hour(timestamp)
);
```

**Rationale:**
- Day-level partitioning for date range queries
- Hour-level for intraday analysis
- No bucketing needed (time naturally distributes)

**Alternative for High-Volume:**
```sql
PARTITIONED BY (
  day(timestamp),
  bucket(32, symbol)  -- Distribute symbols across files
);
```

#### Risk Metrics

**Recommended Strategy: Business-aligned partitioning**

```sql
CREATE TABLE risk_metrics (
  calculation_date DATE,
  portfolio_id STRING,
  risk_type STRING,  -- 'VaR', 'Greeks', 'Stress'
  metric_value DECIMAL(18,4),
  ...
)
PARTITIONED BY (
  year(calculation_date),
  month(calculation_date),
  risk_type
);
```

**Rationale:**
- Regulatory reports typically filter by date + risk_type
- Portfolio-level queries read across partitions (no portfolio partition)

#### Position Snapshots

**Recommended Strategy: Point-in-time partitioning**

```sql
CREATE TABLE positions (
  snapshot_date DATE,
  portfolio_id STRING,
  security_id STRING,
  quantity DECIMAL(18,4),
  market_value DECIMAL(18,2),
  ...
)
PARTITIONED BY (
  year(snapshot_date),
  month(snapshot_date)
);
```

**Alternative: Separate daily snapshot tables with tagging**
```
positions_daily (append-only, partitioned by month)
+ Iceberg tags: 'eod-2025-01-31', 'eod-2025-02-28'
```

### 9.2 Schema Design Principles

#### Flatten vs. Nested Structures

**FpML Trade Example:**

**Option 1: Flattened (Recommended for SQL queries)**
```sql
CREATE TABLE trades (
  trade_id STRING,
  trade_date DATE,
  -- Party fields
  party_a_id STRING,
  party_a_name STRING,
  party_b_id STRING,
  party_b_name STRING,
  -- Product fields
  product_type STRING,
  notional DECIMAL(18,2),
  currency STRING,
  maturity_date DATE,
  -- Pricing fields
  fixed_rate DECIMAL(8,6),
  float_index STRING,
  ...
);
```

**Option 2: Nested (Preserve FpML structure)**
```sql
CREATE TABLE trades (
  trade_id STRING,
  trade_date DATE,
  parties ARRAY<STRUCT<
    party_id: STRING,
    party_role: STRING,
    party_name: STRING
  >>,
  product STRUCT<
    product_type: STRING,
    notional: DECIMAL(18,2),
    currency: STRING,
    terms: STRUCT<
      maturity_date: DATE,
      fixed_rate: DECIMAL(8,6),
      float_index: STRING
    >
  >,
  ...
);
```

**Recommendation:**
- **Silver layer**: Flatten for query performance
- **Bronze layer**: Keep nested for auditability
- Use schema evolution to add fields as needed

#### Separate Fact and Dimension Tables

**Star Schema in Lakehouse:**

```
Fact: trades (high volume, append-mostly)
Dims: counterparties, products, currencies (low volume, SCD Type 2)

Join in query engines (Trino, Spark) - not pre-joined
```

### 9.3 Write Patterns & Ingestion

#### Real-Time Trade Capture

**Pattern: Streaming CDC via Flink**

```python
# Flink CDC from trading system
mysql_cdc = MySqlSource.builder()
  .hostname("trading-db")
  .databaseList("trading")
  .tableList("trading.trades")
  .build()

# Write to Iceberg with exactly-once semantics
iceberg_sink = IcebergSink.forRowData(trades_table)
  .tableLoader(catalog_loader)
  .equalityFieldColumns(["trade_id"])  # Upsert key
  .upsert(True)
  .build()

env.from_source(mysql_cdc, WatermarkStrategy.noWatermarks(), "MySQL CDC")
  .sink_to(iceberg_sink)
```

**Key Configuration:**
- Use `upsert=True` for trade amendments
- Set `equality-delete-columns` for efficient updates
- Consider MoR mode for high-frequency updates

#### Batch Trade Loading

**Pattern: Daily batch from front office systems**

```python
# Spark batch job
df = spark.read.format("avro").load("s3://landing/fpml/2025-12-11/")

df.write \
  .format("iceberg") \
  .mode("append") \
  .option("write.format.default", "parquet") \
  .option("write.distribution-mode", "hash") \
  .partitionBy("year(trade_date)", "month(trade_date)", "asset_class") \
  .saveAsTable("silver.trades")
```

#### Market Data Ingestion

**Pattern: High-throughput streaming with compaction**

```python
# Write as Avro for fast ingestion
market_data_stream.write \
  .format("iceberg") \
  .option("write.format.default", "avro") \
  .option("write.distribution-mode", "none")  # No shuffle
  .option("write.target-file-size-bytes", 134217728)  # 128MB
  .saveAsTable("bronze.market_data_ticks")

# Schedule hourly compaction to Parquet
spark.sql("""
  CALL system.rewrite_data_files(
    table => 'bronze.market_data_ticks',
    strategy => 'binpack',
    options => map('min-input-files', '5')
  )
""")
```

### 9.4 Query Patterns

#### Trade Reporting

```sql
-- Daily trade summary by asset class
SELECT
  asset_class,
  COUNT(*) as trade_count,
  SUM(notional) as total_notional,
  AVG(notional) as avg_notional
FROM trades
WHERE trade_date = '2025-12-11'
  AND booking_entity = 'NYC'
GROUP BY asset_class;

-- Iceberg automatically prunes to single day's files
-- No need to specify partition columns explicitly
```

#### Historical Position Analysis

```sql
-- Compare positions between two dates
WITH positions_start AS (
  SELECT * FROM positions
  TIMESTAMP AS OF '2025-01-01 00:00:00'
),
positions_end AS (
  SELECT * FROM positions
  TIMESTAMP AS OF '2025-12-11 00:00:00'
)
SELECT
  s.portfolio_id,
  s.security_id,
  e.quantity - s.quantity as quantity_change,
  e.market_value - s.market_value as value_change
FROM positions_start s
JOIN positions_end e
  ON s.portfolio_id = e.portfolio_id
  AND s.security_id = e.security_id;
```

#### Risk Metrics with Time Travel

```sql
-- Generate regulatory report for last quarter
SELECT
  portfolio_id,
  AVG(var_95) as avg_var,
  MAX(var_95) as max_var,
  MIN(var_95) as min_var
FROM risk_metrics_daily
TIMESTAMP AS OF '2024-12-31 17:00:00'
WHERE calculation_date BETWEEN '2024-10-01' AND '2024-12-31'
  AND risk_type = 'VaR'
GROUP BY portfolio_id;
```

#### Cross-System Joins (Trino Federation)

```sql
-- Join lakehouse trades with transactional system
SELECT
  t.trade_id,
  t.notional,
  c.credit_rating,
  c.risk_limit
FROM iceberg.prod.trades t
JOIN postgres.reference.counterparties c
  ON t.counterparty_id = c.counterparty_id
WHERE t.trade_date = current_date()
  AND c.credit_rating IN ('BBB', 'BB', 'B');
```

### 9.5 Maintenance & Operations

#### Snapshot Management

**Retention Policy:**
```sql
-- Expire snapshots older than 90 days
CALL system.expire_snapshots(
  table => 'trades',
  older_than => TIMESTAMP '2024-09-12 00:00:00',
  retain_last => 100  -- Keep at least 100 snapshots
);
```

**Snapshot Tagging for Compliance:**
```sql
-- Tag month-end snapshots for regulatory retention
ALTER TABLE trades CREATE TAG 'eod-2025-01-31' AS OF VERSION 123456;
ALTER TABLE trades CREATE TAG 'eod-2025-02-28' AS OF VERSION 234567;

-- Query tagged snapshot 5 years later
SELECT * FROM trades VERSION AS OF 'eod-2025-01-31';
```

#### Compaction Strategy

**File Compaction (Small Files Problem):**
```sql
-- Compact small files created by streaming ingestion
CALL system.rewrite_data_files(
  table => 'trades',
  strategy => 'binpack',
  options => map(
    'target-file-size-bytes', '536870912',  -- 512MB target
    'min-input-files', '10',                -- Compact if 10+ small files
    'max-file-group-size-bytes', '5368709120'  -- 5GB max rewrite
  )
);
```

**Manifest Compaction:**
```sql
-- Compact metadata files for faster query planning
CALL system.rewrite_manifests('trades');
```

**Scheduled Maintenance (Recommended):**
- **Hourly**: Compact streaming tables (if high write volume)
- **Daily**: Expire old snapshots, compact data files
- **Weekly**: Rewrite manifests, analyze statistics

#### Monitoring & Observability

**Key Metrics to Track:**
- **File Size Distribution**: Target 100MB-1GB per file
- **Files per Partition**: Target 100-10,000
- **Snapshot Count**: Expire old snapshots regularly
- **Metadata Size**: Compact manifests when large
- **Query Planning Time**: Should be <5s for well-maintained tables
- **Data Skew**: Monitor partition sizes

**Metadata Queries:**
```sql
-- Check file sizes
SELECT
  partition,
  COUNT(*) as file_count,
  SUM(file_size_in_bytes) / 1024 / 1024 / 1024 as size_gb,
  AVG(file_size_in_bytes) / 1024 / 1024 as avg_file_size_mb
FROM trades.files
GROUP BY partition
ORDER BY size_gb DESC;

-- Check snapshot history
SELECT
  committed_at,
  snapshot_id,
  operation,
  summary
FROM trades.snapshots
ORDER BY committed_at DESC
LIMIT 20;
```

---

## 10. Migration from ODS/DWH to Iceberg

### 10.1 Current State: Traditional ODS/DWH Architecture

**Typical Financial Services Setup:**

```
┌───────────────────────────────────────┐
│   Source Systems (Front Office)       │
│   • Trading systems (FpML messages)   │
│   • Market data feeds                 │
│   • Risk engines                      │
└──────────────┬────────────────────────┘
               │
               ↓ ETL Batch Loads
┌──────────────────────────────────────┐
│   Operational Data Store (ODS)        │
│   • Near real-time staging            │
│   • Normalized schema                 │
│   • Change tracking                   │
└──────────────┬───────────────────────┘
               │
               ↓ Nightly ETL
┌──────────────────────────────────────┐
│   Data Warehouse (DWH)                │
│   • Star schema                       │
│   • Historical data                   │
│   • Aggregations                      │
└──────────────┬───────────────────────┘
               │
               ↓
┌──────────────────────────────────────┐
│   BI Tools / Reports                  │
└──────────────────────────────────────┘
```

**Pain Points:**
- ❌ Expensive proprietary DWH licenses
- ❌ Rigid schema changes (downtime required)
- ❌ Separate systems for batch and streaming
- ❌ Limited query engine flexibility
- ❌ Complex ETL maintenance
- ❌ Data duplication across ODS/DWH
- ❌ Delayed data availability (batch windows)

### 10.2 Target State: Iceberg Lakehouse Architecture

```
┌───────────────────────────────────────┐
│   Source Systems (Front Office)       │
│   • Trading systems (FpML messages)   │
│   • Market data feeds                 │
│   • Risk engines                      │
└──────────────┬────────────────────────┘
               │
               ↓ Streaming + Batch Ingestion
┌──────────────────────────────────────┐
│   Ingestion Layer                     │
│   • Kafka (message bus)               │
│   • Flink (streaming CDC)             │
│   • Spark (batch loads)               │
└──────────────┬───────────────────────┘
               │
               ↓
┌─────────────────────────────────────────────┐
│   Iceberg Lakehouse (S3/ADLS)               │
│                                             │
│   Bronze: Raw data (Avro/Parquet)          │
│   Silver: Cleansed data (Parquet)          │
│   Gold: Business aggregates (Parquet)      │
│                                             │
│   Single source of truth - no duplication  │
└──────────────┬──────────────────────────────┘
               │
               ↓ Multi-engine access
┌──────────────────────────────────────┐
│   Query Engines                       │
│   • Trino (BI, dashboards)            │
│   • Spark (batch analytics)           │
│   • Flink (real-time)                 │
│   • DuckDB (analyst queries)          │
└──────────────┬───────────────────────┘
               │
               ↓
┌──────────────────────────────────────┐
│   BI Tools / Reports / ML             │
└──────────────────────────────────────┘
```

**Benefits:**
- ✅ 60-80% cost reduction (object storage vs. DWH)
- ✅ Schema evolution without downtime
- ✅ Unified batch and streaming
- ✅ Multi-engine flexibility (avoid vendor lock-in)
- ✅ Real-time data availability
- ✅ Single copy of data
- ✅ Time travel for compliance

### 10.3 Migration Strategies

#### Strategy 1: Shadow Migration (CTAS - CREATE TABLE AS)

**Approach:** Rewrite data into new Iceberg tables

**Pros:**
- Opportunity to redesign schema optimally
- Rethink partitioning strategy
- No dependency on source format
- Clean separation (old system continues during migration)

**Cons:**
- Higher initial cost (rewriting all data)
- Longer migration timeline
- Temporary data duplication

**Process:**
```sql
-- Example: Migrate trades from Oracle DWH to Iceberg

-- Step 1: Create optimized Iceberg table
CREATE TABLE iceberg.trades (
  trade_id STRING,
  trade_date DATE,
  asset_class STRING,
  notional DECIMAL(18,2),
  ...
)
USING iceberg
PARTITIONED BY (year(trade_date), month(trade_date), asset_class);

-- Step 2: CTAS from source (via Spark/Trino)
INSERT INTO iceberg.trades
SELECT
  trade_id,
  CAST(trade_date AS DATE),
  asset_class,
  CAST(notional AS DECIMAL(18,2)),
  ...
FROM oracle.dwh.trades;

-- Step 3: Set up incremental sync
-- (Ongoing: capture changes from source)
```

**Timeline:** 3-6 months for large datasets (multi-TB)

#### Strategy 2: In-Place Migration

**Approach:** Convert existing Parquet/ORC/Avro files to Iceberg metadata

**Pros:**
- Fast migration (no data rewrite)
- Lower cost (no data duplication)
- Minimal downtime

**Cons:**
- Must already be in Parquet/ORC/Avro format
- Inherits existing partitioning (may not be optimal)
- Limited redesign opportunity

**Prerequisites:**
- Data already in object storage (S3/ADLS/GCS)
- Files in Parquet, ORC, or Avro format
- Reasonable partitioning scheme

**Process:**
```python
# Example: In-place migration using Spark

from pyspark.sql import SparkSession

spark = SparkSession.builder \
  .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog") \
  .getOrCreate()

# Migrate existing Parquet files to Iceberg
spark.sql("""
  CALL local.system.migrate('local.trades_iceberg',
                            's3://data-lake/trades-parquet/')
""")

# Result: Iceberg metadata created, data files unchanged
```

**Timeline:** Days to weeks

#### Strategy 3: Hybrid (Recommended for Trading Data)

**Approach:** Combine both strategies based on data characteristics

**Decision Matrix:**

| Data Type | Strategy | Rationale |
|-----------|----------|-----------|
| **Historical Trades (>2 years)** | In-place | Already in Parquet, rarely queried, fast migration |
| **Recent Trades (<2 years)** | Shadow | Redesign schema, optimize partitioning for queries |
| **Market Data (time-series)** | In-place | Large volume, good partitioning, no redesign needed |
| **Risk Metrics** | Shadow | Small enough to rewrite, benefit from redesign |
| **Reference Data** | Shadow | Small datasets, can optimize easily |

**Process:**
```
Phase 1 (Month 1-2):
  • Migrate historical data (in-place)
  • Set up lakehouse infrastructure
  • Create Bronze/Silver/Gold layers

Phase 2 (Month 2-4):
  • Migrate recent data (shadow, with redesign)
  • Set up streaming ingestion (Kafka + Flink)
  • Parallel run old + new systems

Phase 3 (Month 4-6):
  • Migrate BI reports to new queries
  • Validate data reconciliation
  • Decommission old DWH
```

### 10.4 Blue/Green Deployment Strategy

**Parallel Operation During Migration:**

```
┌──────────────────────────────────────┐
│         Source Systems                │
└──────────┬───────────────────────────┘
           │
           ├───────────┬───────────────┐
           │           │               │
     ┌─────▼────┐  ┌──▼─────────────┐ │
     │ ODS/DWH  │  │ Iceberg Lake   │ │
     │ (GREEN)  │  │ (BLUE)         │ │
     └─────┬────┘  └──┬─────────────┘ │
           │           │               │
           ↓           ↓               │
     ┌──────────┐ ┌────────────┐      │
     │ BI Tools │ │ BI Tools   │      │
     │ (Old)    │ │ (New)      │      │
     └──────────┘ └────────────┘      │
                                      │
     ↓ Reconciliation & Validation ←──┘
```

**Reconciliation Checks:**
```sql
-- Compare row counts
SELECT COUNT(*) FROM oracle.dwh.trades
WHERE trade_date = '2025-12-11';

SELECT COUNT(*) FROM iceberg.trades
WHERE trade_date = '2025-12-11';

-- Compare aggregates
SELECT
  asset_class,
  SUM(notional) as total_notional
FROM oracle.dwh.trades
WHERE trade_date BETWEEN '2025-01-01' AND '2025-12-11'
GROUP BY asset_class
ORDER BY asset_class;

-- Same query against Iceberg
SELECT
  asset_class,
  SUM(notional) as total_notional
FROM iceberg.trades
WHERE trade_date BETWEEN '2025-01-01' AND '2025-12-11'
GROUP BY asset_class
ORDER BY asset_class;
```

### 10.5 FpML-Specific Migration

**Challenge:** FpML is XML-based, but Iceberg works best with Parquet

#### Bronze Layer: Preserve Raw FpML

**Option 1: Store FpML as Avro with schema**
```python
# Parse FpML, convert to Avro with nested structure
fpml_df = spark.read.format("xml") \
  .option("rowTag", "trade") \
  .load("s3://fpml-landing/")

# Write to Bronze as Avro (preserves structure)
fpml_df.write.format("iceberg") \
  .option("write.format.default", "avro") \
  .mode("append") \
  .saveAsTable("bronze.fpml_messages")
```

**Option 2: Store original XML + extracted fields**
```sql
CREATE TABLE bronze.fpml_messages (
  message_id STRING,
  received_at TIMESTAMP,
  trade_id STRING,
  message_type STRING,
  fpml_xml STRING,  -- Full XML as string
  fpml_parsed STRUCT<...>  -- Parsed key fields
)
USING iceberg;
```

#### Silver Layer: Flatten FpML to Structured Schema

**Extract key fields for analytical queries:**

```python
from pyspark.sql.functions import *

# Parse FpML XML and flatten
fpml_df = spark.table("bronze.fpml_messages")

trades_df = fpml_df.select(
  col("trade_id"),
  col("fpml_parsed.tradeDate").alias("trade_date"),
  col("fpml_parsed.partyA.partyId").alias("party_a_id"),
  col("fpml_parsed.partyB.partyId").alias("party_b_id"),
  col("fpml_parsed.product.productType").alias("product_type"),
  col("fpml_parsed.notional.amount").alias("notional"),
  col("fpml_parsed.notional.currency").alias("currency"),
  # ... extract more fields
)

# Write to Silver as Parquet
trades_df.write.format("iceberg") \
  .option("write.format.default", "parquet") \
  .partitionBy("year(trade_date)", "month(trade_date)", "product_type") \
  .mode("append") \
  .saveAsTable("silver.trades")
```

**Schema Evolution Benefit:**
```python
# Later: Add new FpML 5.12 fields without breaking existing queries
spark.sql("""
  ALTER TABLE silver.trades
  ADD COLUMNS (
    initial_margin DECIMAL(18,2),
    variation_margin DECIMAL(18,2),
    clearing_house STRING
  )
""")

# Old queries still work, new fields NULL for historical data
```

### 10.6 Data Governance During Migration

**Catalog Selection:**
- **AWS Glue**: Native AWS integration, serverless
- **Hive Metastore**: Compatibility with existing Hadoop ecosystem
- **Nessie**: Git-like versioning, multi-table transactions
- **Custom REST Catalog**: Flexibility for custom requirements

**Access Control:**
```sql
-- Use Lake Formation (AWS) or Ranger (on-prem)
GRANT SELECT ON iceberg.trades TO ROLE 'risk_analysts';
GRANT SELECT, INSERT ON iceberg.trades TO ROLE 'data_engineers';

-- Column-level security
GRANT SELECT (trade_id, trade_date, notional)
  ON iceberg.trades TO ROLE 'external_auditors';
```

**Encryption:**
- Enable S3 server-side encryption (SSE-S3, SSE-KMS)
- Set Iceberg table property: `encryption.key.id`

### 10.7 Migration Checklist

**Pre-Migration:**
- [ ] Assess current data volumes and query patterns
- [ ] Select catalog provider (Glue, Hive, Nessie)
- [ ] Choose cloud storage (S3, ADLS, GCS)
- [ ] Design Bronze/Silver/Gold layers
- [ ] Redesign schemas and partitioning strategies
- [ ] Set up Iceberg catalog and infrastructure
- [ ] Provision query engines (Trino, Spark, Flink)

**Migration Phase:**
- [ ] Migrate historical data (in-place or shadow)
- [ ] Set up streaming ingestion (Kafka + Flink)
- [ ] Implement incremental sync from source systems
- [ ] Configure compaction and maintenance jobs
- [ ] Set up snapshot expiration policies
- [ ] Implement data quality checks
- [ ] Run parallel old + new systems

**Validation Phase:**
- [ ] Reconcile row counts and aggregates
- [ ] Validate query performance (vs. old DWH)
- [ ] Test time travel and snapshot queries
- [ ] Migrate BI reports and dashboards
- [ ] User acceptance testing (UAT)
- [ ] Load testing for peak volumes

**Cutover Phase:**
- [ ] Final incremental sync
- [ ] Switch production traffic to Iceberg
- [ ] Monitor for issues (24/7 support)
- [ ] Decommission old ODS/DWH (after grace period)

**Post-Migration:**
- [ ] Establish ongoing maintenance (compaction, snapshots)
- [ ] Set up monitoring and alerting
- [ ] Train teams on Iceberg features
- [ ] Optimize based on usage patterns
- [ ] Document architecture and runbooks

---

## 11. Recommendations

### 11.1 Architecture Recommendations

**For Trading & Risk Data Lakehouse:**

#### 1. Adopt Medallion Architecture (Bronze/Silver/Gold)

**Bronze Layer:**
- **Purpose**: Land raw FpML messages with minimal transformation
- **Format**: Avro (for fast streaming ingestion)
- **Partitioning**: `day(received_at)`
- **Retention**: 90 days (then compact to Silver)

**Silver Layer:**
- **Purpose**: Validated, parsed trades with standardized schema
- **Format**: Parquet (for analytical performance)
- **Partitioning**: `year(trade_date), month(trade_date), bucket(16, asset_class)`
- **Retention**: Indefinite (regulatory requirement)

**Gold Layer:**
- **Purpose**: Pre-aggregated risk metrics, P&L, summaries
- **Format**: Parquet
- **Partitioning**: `year(calculation_date), month(calculation_date), risk_type`
- **Retention**: Indefinite with snapshot tagging

#### 2. Use Multi-Engine Strategy

**Recommended Engine Mix:**

```
Flink     → Real-time ingestion (FpML, market data, CDC)
Spark     → Batch processing (EOD risk, compaction, aggregations)
Trino     → Interactive queries (BI dashboards, analyst ad-hoc)
DuckDB    → Local analysis (notebooks, prototyping)
```

**Why:** Each engine optimized for specific workload, no vendor lock-in

#### 3. Implement Streaming + Batch Hybrid

**Real-Time Path (Latency: <1 minute):**
```
Trading System → Kafka → Flink → Iceberg (Bronze/Silver)
```

**Batch Path (Latency: <1 hour):**
```
Trading System → S3 Landing → Spark → Iceberg (Bronze/Silver)
```

**Aggregation Path (Latency: EOD):**
```
Iceberg (Silver) → Spark (EOD jobs) → Iceberg (Gold)
```

#### 4. Use AWS S3 Tables (2025) or Equivalent

**Benefits:**
- Native Iceberg support
- Automatic compaction (Parquet, Avro, ORC)
- 12-40% query performance improvement
- Simplified operations

**Alternative:** GCP BigLake, Azure Synapse (Iceberg support)

### 11.2 Table Design Recommendations

#### Trade Data

**Schema:**
```sql
CREATE TABLE trades (
  -- Identifiers
  trade_id STRING,
  version INT,  -- For amendments
  trade_date DATE,
  value_date DATE,

  -- Parties
  party_a_id STRING,
  party_b_id STRING,
  counterparty_id STRING,

  -- Product
  asset_class STRING,
  product_type STRING,
  underlying_id STRING,

  -- Economics
  notional DECIMAL(18,2),
  currency STRING,
  direction STRING,  -- 'Buy', 'Sell'

  -- Pricing
  price DECIMAL(18,6),
  accrued_interest DECIMAL(18,2),

  -- Lifecycle
  status STRING,  -- 'Pending', 'Confirmed', 'Settled', 'Cancelled'
  booking_entity STRING,
  portfolio_id STRING,

  -- Audit
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  created_by STRING,

  -- Compliance
  regulatory_regime STRING,
  reportable BOOLEAN
)
USING iceberg
PARTITIONED BY (
  year(trade_date),
  month(trade_date),
  bucket(16, asset_class)
);
```

**Write Strategy:** Upsert via equality deletes (for amendments)
```python
df.writeTo("trades") \
  .option("write.upsert.enabled", "true") \
  .option("equalityDeleteColumns", "trade_id,version") \
  .append()
```

#### Market Data

**Schema:**
```sql
CREATE TABLE market_data (
  symbol STRING,
  timestamp TIMESTAMP,
  bid DECIMAL(18,6),
  ask DECIMAL(18,6),
  last DECIMAL(18,6),
  volume BIGINT,
  data_source STRING
)
USING iceberg
PARTITIONED BY (
  day(timestamp),
  hour(timestamp)
);
```

**Write Strategy:** Streaming append (Avro), hourly compaction (Parquet)

#### Risk Metrics

**Schema:**
```sql
CREATE TABLE risk_metrics (
  calculation_date DATE,
  calculation_time TIMESTAMP,
  portfolio_id STRING,
  risk_type STRING,  -- 'VaR', 'CVaR', 'Greeks', 'Stress'
  risk_metric STRING,  -- 'VaR_95', 'Delta', 'Gamma', etc.
  metric_value DECIMAL(18,6),
  confidence_level DECIMAL(5,4),  -- 0.95, 0.99
  calculation_method STRING,
  metadata MAP<STRING, STRING>
)
USING iceberg
PARTITIONED BY (
  year(calculation_date),
  month(calculation_date),
  risk_type
);
```

**Write Strategy:** Daily batch (replace partition)

#### Position Snapshots

**Schema:**
```sql
CREATE TABLE positions (
  snapshot_date DATE,
  snapshot_time TIMESTAMP,
  portfolio_id STRING,
  security_id STRING,
  quantity DECIMAL(18,6),
  market_value DECIMAL(18,2),
  currency STRING,
  position_type STRING  -- 'Long', 'Short'
)
USING iceberg
PARTITIONED BY (
  year(snapshot_date),
  month(snapshot_date)
);
```

**Write Strategy:** Daily snapshot with Iceberg tagging
```sql
-- After EOD processing
ALTER TABLE positions CREATE TAG 'eod-2025-12-11' AS OF VERSION 123456;
```

### 11.3 Partitioning Recommendations

**Key Principles:**

1. **Date partitioning is essential** for financial time-series data
   - Use `year(trade_date), month(trade_date)` for enhanced pruning
   - Avoid `day(trade_date)` unless data volume is massive (>100GB/day)

2. **Use bucketing for skewed dimensions**
   - Example: `bucket(16, asset_class)` prevents "IR Swaps" partition dominance
   - Target: 16-32 buckets for good distribution

3. **Limit partitioning columns to 2-4**
   - More partitions = more metadata overhead
   - Iceberg's hidden partitioning makes user queries easy regardless

4. **Avoid high-cardinality partitioning**
   - ❌ Never partition by `trade_id`, `counterparty_id` (millions of values)
   - ✅ Use for filtering in queries, not partitioning

5. **Target file sizes: 100MB-1GB**
   - Smaller: Poor query performance (many small files)
   - Larger: Inefficient partition pruning

### 11.4 Maintenance Recommendations

#### Daily Maintenance

```sql
-- Expire old snapshots (keep 90 days of history)
CALL system.expire_snapshots(
  table => 'trades',
  older_than => TIMESTAMP '${90_days_ago}',
  retain_last => 100
);

-- Compact small files from streaming ingestion
CALL system.rewrite_data_files(
  table => 'trades',
  strategy => 'binpack',
  options => map('target-file-size-bytes', '536870912')
);
```

#### Weekly Maintenance

```sql
-- Compact manifests for faster query planning
CALL system.rewrite_manifests('trades');

-- Analyze table statistics (for cost-based optimization)
ANALYZE TABLE trades COMPUTE STATISTICS;
```

#### Monthly Maintenance

```sql
-- Tag month-end snapshots for compliance
ALTER TABLE trades CREATE TAG 'eom-2025-12-31' AS OF VERSION ${snapshot_id};

-- Remove orphan files (failed writes)
CALL system.remove_orphan_files(
  table => 'trades',
  older_than => TIMESTAMP '${7_days_ago}'
);
```

### 11.5 Query Performance Recommendations

#### 1. Always Filter by Partition Columns

**Good:**
```sql
SELECT * FROM trades
WHERE trade_date BETWEEN '2025-01-01' AND '2025-12-31';
-- Iceberg prunes to 12 month partitions
```

**Bad:**
```sql
SELECT * FROM trades
WHERE YEAR(trade_date) = 2025;
-- Function on partition column prevents pruning - scans all partitions!
```

#### 2. Use Iceberg Metadata Tables for Exploration

```sql
-- Understand table structure without scanning data
SELECT * FROM trades.files LIMIT 10;
SELECT * FROM trades.snapshots ORDER BY committed_at DESC;
SELECT * FROM trades.partitions;
```

#### 3. Leverage Time Travel for Debugging

```sql
-- Compare today's data vs. yesterday
SELECT * FROM trades WHERE trade_id = 'TRADE123';  -- Current
SELECT * FROM trades TIMESTAMP AS OF '2025-12-10 23:59:59'
WHERE trade_id = 'TRADE123';  -- Yesterday
```

#### 4. Use Trino for Federation

```sql
-- Join lakehouse with transactional systems
SELECT
  t.trade_id,
  c.credit_limit
FROM iceberg.prod.trades t
JOIN postgres.live.counterparties c ON t.counterparty_id = c.id;
```

### 11.6 Migration Recommendations

**For Traditional ODS/DWH to Iceberg:**

1. **Start with Hybrid Strategy**
   - In-place migration for historical data
   - Shadow migration for recent data with redesign

2. **Use Blue/Green Deployment**
   - Run parallel for 3-6 months
   - Reconcile daily to build confidence
   - Gradual BI report migration

3. **Focus on Streaming First**
   - Set up real-time ingestion (Kafka + Flink)
   - Prove lower latency vs. batch ETL
   - Build momentum for full migration

4. **Invest in Data Quality**
   - Implement checks at Bronze → Silver boundary
   - Use Iceberg's schema evolution for flexibility
   - Monitor data freshness and completeness

5. **Plan for FpML Parsing**
   - Bronze: Store raw FpML (Avro, preserves structure)
   - Silver: Flatten key fields (Parquet, optimized queries)
   - Gold: Business aggregates

### 11.7 Tooling Recommendations

**Catalog:** AWS Glue (if on AWS) or Nessie (for Git-like versioning)

**Query Engines:**
- **Primary**: Trino (BI, dashboards, ad-hoc)
- **Batch**: Spark (EOD processing, aggregations)
- **Streaming**: Flink (real-time ingestion, CDC)
- **Local**: DuckDB (analyst notebooks)

**Orchestration:** Apache Airflow or AWS Step Functions

**Monitoring:**
- Datadog or Prometheus (infrastructure)
- Monte Carlo or Datafold (data observability)

**Data Quality:** Great Expectations or AWS Glue Data Quality

### 11.8 Skills & Training Recommendations

**For Data Engineering Teams:**
- Iceberg fundamentals (snapshots, manifests, metadata)
- Spark/Flink programming for Iceberg
- Partitioning and compaction strategies
- Trino SQL for federation

**For Analysts:**
- Iceberg time travel queries
- Understanding hidden partitioning
- Trino SQL (vs. traditional DWH SQL)

**For Architects:**
- Lakehouse design patterns
- Multi-engine architecture
- Governance and security (Lake Formation, Ranger)

---

## Summary

Apache Iceberg represents a transformative approach to managing large-scale analytical data in financial services. For a trading and risk data architecture transitioning from traditional ODS/Data Warehouse patterns to a modern lakehouse, Iceberg provides:

### Core Value Proposition

1. **Cost Efficiency**: 60-80% reduction vs. proprietary DWH (object storage + open engines)
2. **Flexibility**: Multi-engine access without vendor lock-in (Spark, Trino, Flink, DuckDB)
3. **Agility**: Schema evolution without downtime or data rewrites
4. **Compliance**: Built-in time travel and audit trails for regulatory requirements
5. **Performance**: Partition/file pruning enables sub-second queries on petabyte-scale data
6. **Unification**: Single platform for batch and streaming workloads

### Key Architectural Decisions

**Table Format:** Apache Iceberg (over Delta Lake or Hudi)
- **Rationale**: Widest multi-engine support, flexible schema evolution, no vendor lock-in

**File Format:** Hybrid approach
- **Streaming/Bronze**: Avro (fast writes)
- **Analytics/Silver/Gold**: Parquet (optimized reads)
- **Compaction**: Automatic Avro→Parquet conversion

**Query Engines:**
- **Flink**: Real-time ingestion (FpML, market data, CDC)
- **Spark**: Batch processing (EOD risk, aggregations)
- **Trino**: Interactive queries (BI, dashboards)
- **DuckDB**: Local analysis (notebooks)

**Partitioning Strategy:**
- **Trades**: `year(trade_date), month(trade_date), bucket(16, asset_class)`
- **Market Data**: `day(timestamp), hour(timestamp)`
- **Risk Metrics**: `year(calculation_date), month(calculation_date), risk_type`
- **Positions**: `year(snapshot_date), month(snapshot_date)` + Iceberg tags

**Data Organization:** Medallion architecture (Bronze/Silver/Gold)
- **Bronze**: Raw FpML messages (Avro, 90-day retention)
- **Silver**: Validated trades (Parquet, indefinite)
- **Gold**: Risk aggregates (Parquet, snapshot tagging for compliance)

### Migration Approach

**Hybrid Strategy:**
- **Historical Data**: In-place migration (fast, low-cost)
- **Recent Data**: Shadow migration with redesign (optimal schema)
- **FpML Processing**: Bronze (raw XML) → Silver (flattened Parquet)

**Timeline:** 4-6 months with blue/green deployment

### Critical Success Factors

1. **Maintenance Discipline**: Daily compaction, weekly manifest rewrites, monthly snapshot expiration
2. **Partitioning Design**: Balance between query performance and metadata overhead
3. **Streaming Pipeline**: Kafka + Flink for real-time trade capture and CDC
4. **Data Quality**: Validation at Bronze→Silver boundary
5. **Governance**: Catalog selection (Glue/Nessie), access controls (Lake Formation/Ranger)
6. **Training**: Upskill teams on Iceberg concepts and multi-engine SQL

### Expected Outcomes

- **Query Performance**: 10-100x improvement (via partition pruning) vs. full table scans
- **Data Freshness**: Real-time (<1 min) vs. nightly batch
- **Cost Savings**: 60-80% reduction in storage and compute costs
- **Agility**: Schema changes in minutes vs. days/weeks
- **Compliance**: Time travel queries eliminate need for separate audit tables

---

## Sources

- [Apache Iceberg Architecture: 3 Core Components to Understand](https://atlan.com/know/iceberg/apache-iceberg-architecture/)
- [Apache Iceberg Spec](https://iceberg.apache.org/spec/)
- [Apache Iceberg Deep Dive — Part 2: Technical Architecture Practical Walkthrough](https://medium.com/@jdegbun/apache-iceberg-deep-dive-part-2-technical-architecture-practical-walkthrough-a7193a00c830)
- [The 2025 Comprehensive Guide to Apache Iceberg](https://dev.to/alexmercedcoder/the-2025-comprehensive-guide-to-apache-iceberg-2g22)
- [Apache Iceberg Official Website](https://iceberg.apache.org/)
- [What is Apache Iceberg in Databricks?](https://docs.databricks.com/aws/en/iceberg/)
- [Apache Iceberg: Why This Open Table Format is Taking Over Data Lakehouses](https://olake.io/blog/apache-iceberg-features-benefits/)
- [Why Apache Iceberg? A Guide to Real-Time Data Lakes in 2025](https://streamkap.com/blog/apache-iceberg-guide)
- [Apache Iceberg Evolution](https://iceberg.apache.org/docs/latest/evolution/)
- [What Is Apache Iceberg? How It Works, Benefits, & Use Cases](https://www.montecarlodata.com/blog-are-apache-iceberg-tables-right-for-your-data-lake-6-reasons-why/)
- [Apache Iceberg: A Strong Contender for your 2025 Data Lake Strategy](https://procogia.com/apache-iceberg-2025-data-lake-strategy/)
- [2025 Guide to Architecting an Iceberg Lakehouse](https://medium.com/data-engineering-with-dremio/2025-guide-to-architecting-an-iceberg-lakehouse-9b19ed42c9de)
- [Apache Iceberg vs Delta Lake vs Apache Hudi - Feature Comparison Deep Dive](https://www.onehouse.ai/blog/apache-hudi-vs-delta-lake-vs-apache-iceberg-lakehouse-feature-comparison)
- [Hudi vs Iceberg vs Delta Lake: Detailed Comparison](https://lakefs.io/blog/hudi-iceberg-and-delta-lake-data-lake-table-formats-compared/)
- [Apache Hudi vs. Apache Iceberg: 2025 Evaluation Guide](https://atlan.com/know/iceberg/apache-hudi-vs-iceberg/)
- [Iceberg vs Delta vs Hudi — the most comprehensive comparison](https://medium.com/@kywe665/iceberg-vs-delta-vs-hudi-the-most-comprehensive-comparison-96577fc6dfc5)
- [Apache Hudi vs Delta Lake vs Apache Iceberg](https://hudi.apache.org/blog/2025/01/09/apache-iceberg-vs-delta-lake-vs-apache-hudi/)
- [Top 10 Query Engines for Apache Iceberg: A Complete Comparison](https://estuary.dev/blog/comparison-query-engines-for-apache-iceberg/)
- [Apache Iceberg Trino: Modern Data Lakehouse Explained](https://www.puppygraph.com/blog/apache-iceberg-trino)
- [Trino + Apache Iceberg = Modern Open Data Lake](https://medium.com/@mehakgambhir/trino-apache-iceberg-modern-open-data-lake-c1f51f5004d9)
- [AWS re:Invent 2025 - Best practices for building Apache Iceberg based lakehouse architectures on AWS](https://dev.to/kazuya_dev/aws-reinvent-2025-best-practices-for-building-apache-iceberg-based-lakehouse-architectures-on-aws-1a29)
- [Data Streaming Meets Lakehouse: Apache Iceberg for Unified Real-Time and Batch Analytics](https://www.kai-waehner.de/blog/2025/11/19/data-streaming-meets-lakehouse-apache-iceberg-for-unified-real-time-and-batch-analytics/)
- [Inside Data Cloud's Open Lakehouse: Powered by Apache Iceberg (Salesforce)](https://engineering.salesforce.com/inside-data-clouds-open-lakehouse-4m-tables-and-50pb-powered-by-apache-iceberg/)
- [Optimizing Partition Strategies in Apache Iceberg on AWS](https://geeklogbook.com/optimizing-partition-strategies-in-apache-iceberg-on-aws/)
- [OLake Iceberg Partitioning Guide for Efficient Data Queries](https://olake.io/docs/writers/iceberg/partitioning/)
- [Partitioning with Apache Iceberg: A Deep Dive](https://amdatalakehouse.substack.com/p/partitioning-with-apache-iceberg)
- [Partitioning That Scales: Real Lessons from Apache Iceberg in Production](https://medium.com/art-of-data-engineering/partitioning-that-scales-real-lessons-from-apache-iceberg-in-production-74f3f51bd23b)
- [Iceberg partitioning best practices](https://www.starburst.io/blog/iceberg-partitioning/)
- [Migration Guide for Apache Iceberg Lakehouses](https://www.dremio.com/blog/migration-guide-for-apache-iceberg-lakehouses/)
- [From SQL Server to Lakehouse: A Better Journey to an Apache Iceberg Lakehouse](https://www.dremio.com/blog/from-sql-server-to-lakehouse-a-better-journey-to-an-apache-iceberg-lakehouse/)
- [Migrate an existing data lake to a transactional data lake using Apache Iceberg](https://aws.amazon.com/blogs/big-data/migrate-an-existing-data-lake-to-a-transactional-data-lake-using-apache-iceberg/)
- [Apache Parquet vs AVRO: Open file formats, compute engine](https://www.starburst.io/blog/apache-parquet-vs-avro/)
- [Parquet, ORC, and Avro: The File Format Fundamentals of Big Data](https://www.upsolver.com/blog/the-file-format-fundamentals-of-big-data)
- [The Data Engineer's Guide to File Formats: Parquet vs ORC vs Avro](https://medium.com/towards-data-engineering/the-data-engineers-guide-to-file-formats-parquet-vs-orc-vs-avro-470e1d7f7643)
- [Compaction support for Avro and ORC file formats in Apache Iceberg tables in Amazon S3](https://aws.amazon.com/blogs/big-data/compaction-support-for-avro-and-orc-file-formats-in-apache-iceberg-tables-in-amazon-s3/)
- [Apache Parquet vs. Apache Iceberg: 2025 Evaluation Guide](https://atlan.com/know/iceberg/apache-parquet-vs-apache-iceberg/)
- [Apache Iceberg Hidden Partitioning](https://iceberg.apache.org/docs/latest/partitioning/)
- [Apache Iceberg Hidden Partitioning Reduces Full Scans](https://www.dremio.com/blog/fewer-accidental-full-table-scans-brought-to-you-by-apache-icebergs-hidden-partitioning/)
- [Change Data Capture (CDC) with Apache Iceberg](https://www.dremio.com/blog/cdc-with-apache-iceberg/)
- [Unified CDC Ingestion and Processing with Apache Flink and Iceberg](https://current.confluent.io/post-conference-videos-2025/unified-cdc-ingestion-and-processing-with-apache-flink-and-iceberg-lnd25)
- [Apache Flink 1.18+ & Apache Iceberg CDC Integration](https://olake.io/iceberg/query-engine/flink/)
- [Top Trends for Data Streaming with Apache Kafka and Flink in 2026](https://www.kai-waehner.de/blog/2025/12/10/top-trends-for-data-streaming-with-apache-kafka-and-flink-in-2026/)
- [Replicate changes from databases to Apache Iceberg tables using Amazon Data Firehose](https://aws.amazon.com/blogs/aws/replicate-changes-from-databases-to-apache-iceberg-tables-using-amazon-data-firehose/)
- [Best Practices for Optimizing Apache Iceberg Performance](https://www.starburst.io/blog/best-practices-for-optimizing-apache-iceberg-performance/)
- [What is Apache Iceberg? - Iceberg Tables Explained - AWS](https://aws.amazon.com/what-is/apache-iceberg/)
- [Iceberg, Right Ahead! 7 Apache Iceberg Best Practices For Smooth Data Sailing](https://www.montecarlodata.com/blog-apache-iceberg-best-practices/)
- [Apache Iceberg Time Travel Guide: Snapshots, Queries & Rollbacks](https://estuary.dev/blog/time-travel-apache-iceberg/)
- [Spark Queries - Apache Iceberg](https://iceberg.apache.org/docs/latest/spark-queries/)
- [A Guide to Apache Iceberg Snapshots and Time Travel](https://www.e6data.com/blog/apache-iceberg-snapshots-time-travel)

---

**Document Generated:** December 11, 2025
**Author:** Claude (via Claude Code)
**Purpose:** Research foundation for Trading & Risk Data Lakehouse architecture design
