---
# Process Metadata
process_id: MR-L4-004
process_name: Regional EOD Management
version: 2.0
effective_date: 2025-01-15
next_review_date: 2026-01-15
owner: Head of Market Risk
approving_committee: MLRC

# Taxonomy Linkages
parent_process: MR-L4-001  # Market Risk Process Orchestration (orchestration)
l1_requirements:
  - REQ-L1-001  # CRR
l2_risk_types:
  - MR-L2-001   # Market Risk
l3_governance:
  - MR-L3-001   # Market Risk Policy
l7_systems:
  - SYS-MR-006  # Market Data ODS
  - SYS-MR-009  # P&L ODS
  - SYS-MR-012  # Snapshot Service
---

# Regional EOD Management Process

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Process ID** | MR-L4-004 |
| **Version** | 2.0 |
| **Effective Date** | 15 January 2025 |
| **Parent Process** | Market Risk Process Orchestration (MR-L4-001) |
| **Owner** | Head of Market Risk |

---

## 1. Purpose

The Regional EOD Management process addresses the complexities of operating across multiple time zones. Each regional trading desk values its positions using **local EOD market data snapshots**, ensuring traders see P&L that reflects their actual execution quality relative to their local market close.

However, **intercompany trades** between books in different regions create **fictitious P&L** at the firm-wide level because the same trade is valued using different regional snapshots. This process:

- Ensures each region uses appropriate local market data for regional P&L
- Identifies intercompany trades that span regional snapshots
- Calculates and quantifies fictitious P&L arising from snapshot timing differences
- Enables Product Control to assess whether material adjustments are required
- Maintains a consistent global view for VaR and regulatory reporting

---

## 2. Regional Valuation Approach

### 2.1 Local Snapshot Principle

Each region values its trading books using its **own local EOD market data snapshot**:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     REGIONAL VALUATION - LOCAL SNAPSHOTS                                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ASIA (HK)                  LONDON (HQ)                NEW YORK                         │
│  17:30 HKT                  17:30 GMT                  17:30 EST                        │
│                                                                                         │
│  ┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐          │
│  │   ASIA SNAPSHOT     │    │   LONDON SNAPSHOT   │    │     NY SNAPSHOT     │          │
│  │                     │    │                     │    │                     │          │
│  │  • Asia FX rates    │    │  • EUR FX rates     │    │  • USD FX rates     │          │
│  │  • Asian IR curves  │    │  • EUR IR curves    │    │  • USD IR curves    │          │
│  │  • Asian equities   │    │  • European equities│    │  • US equities      │          │
│  │  • Commodity (Asia) │    │  • Global reference │    │  • Commodity (US)   │          │
│  └──────────┬──────────┘    └──────────┬──────────┘    └──────────┬──────────┘          │
│             │                          │                          │                     │
│             ▼                          ▼                          ▼                     │
│  ┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐          │
│  │   ASIA BOOKS        │    │   LONDON BOOKS      │    │     NY BOOKS        │          │
│  │                     │    │                     │    │                     │          │
│  │  Valued at ASIA     │    │  Valued at LONDON   │    │  Valued at NY       │          │
│  │  snapshot prices    │    │  snapshot prices    │    │  snapshot prices    │          │
│  │                     │    │                     │    │                     │          │
│  │  Traders see P&L    │    │  Traders see P&L    │    │  Traders see P&L    │          │
│  │  vs. local close    │    │  vs. local close    │    │  vs. local close    │          │
│  └─────────────────────┘    └─────────────────────┘    └─────────────────────┘          │
│                                                                                         │
│  RATIONALE: Traders should see P&L that reflects their execution quality relative       │
│  to the market conditions when they finished trading for the day.                       │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Benefits of Local Snapshots

| Benefit | Description |
|---------|-------------|
| **Trader P&L Attribution** | Traders see P&L reflecting their actual trading decisions |
| **Execution Quality** | Performance measured against prices available at close |
| **Accountability** | Regional desks accountable for regional market moves |
| **Simplicity** | Each region owns its data quality |

---

## 3. The Intercompany Fictitious P&L Problem

### 3.1 When Fictitious P&L Arises

Fictitious P&L arises specifically from **intercompany trades** - trades between books in different regions. Because each leg of the trade is valued using a different regional snapshot, the valuations do not match, creating artificial P&L at the firm level.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     INTERCOMPANY FICTITIOUS P&L - EXAMPLE                               │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  SCENARIO: Asia Commodity Trader Hedges FX Exposure with London FX Desk                 │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  Asia commodity trader has a JPY-denominated copper position and wants to hedge         │
│  the USD/JPY FX exposure. Enters an internal FX forward with London FX desk.            │
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │                                                                                 │    │
│  │   ASIA BOOK (Commodities)              LONDON BOOK (FX Desk)                    │    │
│  │   ─────────────────────────            ─────────────────────                    │    │
│  │                                                                                 │    │
│  │   Trade: BUY USD 10M                   Trade: SELL USD 10M                      │    │
│  │          vs. JPY @ 148.50                     vs. JPY @ 148.50                  │    │
│  │          (internal trade)                     (internal trade)                  │    │
│  │                                                                                 │    │
│  │   Valued at: ASIA SNAPSHOT             Valued at: LONDON SNAPSHOT               │    │
│  │   USD/JPY = 148.50                     USD/JPY = 149.00                         │    │
│  │                                                                                 │    │
│  │   MTM: $0 (at trade rate)              MTM: +$33,557                            │    │
│  │                                        (149.00 vs. 148.50)                      │    │
│  │                                                                                 │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │                                                                                 │    │
│  │   FIRM-LEVEL VIEW                                                               │    │
│  │   ───────────────────                                                           │    │
│  │                                                                                 │    │
│  │   Asia Book MTM:     $0                                                         │    │
│  │   London Book MTM:   +$33,557                                                   │    │
│  │   ─────────────────────────                                                     │    │
│  │   Firm Total:        +$33,557   ← FICTITIOUS P&L                                │    │
│  │                                                                                 │    │
│  │   This P&L is fictitious because:                                               │    │
│  │   • The trades are internal - they should NET TO ZERO at firm level             │    │
│  │   • The difference arises ONLY because of different valuation snapshots         │    │
│  │   • It will reverse tomorrow when both books use updated snapshots              │    │
│  │                                                                                 │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Types of Internal Trades Affected

| Trade Type | Example | Regions Involved | Typical Size |
|------------|---------|------------------|--------------|
| **FX Hedges** | Commodity desk hedges FX exposure | Asia ↔ London, NY ↔ London | Significant |
| **Internal Funding** | Regional desk borrows USD from Treasury | Any region ↔ Treasury (London) | Large notional |
| **Risk Transfer** | Regional desk transfers position to central book | Asia/NY ↔ London | Variable |
| **Intercompany Swaps** | IR swap between regional entities | Any cross-regional | Material |
| **Cross-regional Hedges** | NY hedge of Asia exposure | Asia ↔ NY | Variable |

### 3.3 Why This Matters

| Scenario | Impact |
|----------|--------|
| **Large market move between snapshots** | Fictitious P&L can be material (>$1M) |
| **Many internal trades** | Aggregate effect can be significant |
| **Volatile FX pairs** | USD/JPY, emerging market FX especially affected |
| **End of month/quarter** | May affect reported results if not identified |

---

## 4. Process Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     REGIONAL EOD MANAGEMENT PROCESS                                     │
│                     (Daily)                                                             │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         1. REGIONAL SNAPSHOT CAPTURE                                     │
│                                                                                          │
│  Each region captures local EOD prices at market close:                                  │
│                                                                                          │
│  • Asia (HK): 17:30 HKT → SNAP-YYYYMMDD-ASIA                                             │
│  • London:    17:30 GMT → SNAP-YYYYMMDD-LONDON                                           │
│  • New York:  17:30 EST → SNAP-YYYYMMDD-NY                                               │
│                                                                                          │
│  Owner: Regional MDC teams                                                               │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         2. REGIONAL P&L CALCULATION                                      │
│                                                                                          │
│  Each region values its books using its LOCAL snapshot:                                  │
│                                                                                          │
│  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐                  │
│  │ ASIA BOOKS         │  │ LONDON BOOKS       │  │ NY BOOKS           │                  │
│  │ × ASIA SNAPSHOT    │  │ × LONDON SNAPSHOT  │  │ × NY SNAPSHOT      │                  │
│  │ = ASIA P&L         │  │ = LONDON P&L       │  │ = NY P&L           │                  │
│  └────────────────────┘  └────────────────────┘  └────────────────────┘                  │
│                                                                                          │
│  This is the P&L traders see and are accountable for                                     │
│                                                                                          │
│  Owner: Regional Product Control                                                         │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         3. IDENTIFY INTERCOMPANY TRADES                                  │
│                                                                                          │
│  The Snapshot Service identifies internal trades that span regional snapshots:           │
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  INTERCOMPANY TRADE DETECTION                                                       │ │
│  │                                                                                     │ │
│  │  Query: SELECT trades WHERE counterparty_type = 'INTERNAL'                          │ │
│  │                        AND book_region != counterparty_book_region                  │ │
│  │                                                                                     │ │
│  │  Output:                                                                            │ │
│  │  ┌──────────┬─────────────┬────────────┬─────────────┬────────────┬───────────┐     │ │
│  │  │ Trade ID │ Asia Book   │ Asia Snap  │ London Book │ London Snap│ Notional  │     │ │
│  │  ├──────────┼─────────────┼────────────┼─────────────┼────────────┼───────────┤     │ │
│  │  │ IC-001   │ ASIA-COMM-1 │ 148.50     │ LON-FX-1    │ 149.00     │ $10M      │     │ │
│  │  │ IC-002   │ ASIA-RATES-1│ 3.45%      │ LON-TREAS   │ 3.47%      │ $50M      │     │ │
│  │  │ IC-003   │ NY-EQ-1     │ 4250       │ LON-EQ-1    │ 4255       │ $5M       │     │ │
│  │  └──────────┴─────────────┴────────────┴─────────────┴────────────┴───────────┘     │ │
│  │                                                                                     │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
│  Owner: Trade ODS / Snapshot Service                                                     │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         4. CALCULATE FICTITIOUS P&L                                      │
│                                                                                          │
│  For each intercompany trade, calculate the P&L difference arising from snapshot timing: │
│                                                                                          │
│  Fictitious_P&L = MTM(Book_A, Snapshot_A) + MTM(Book_B, Snapshot_B)                      │
│                                                                                          │
│  (Should be zero if same prices used; difference = fictitious P&L)                       │
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  FICTITIOUS P&L CALCULATION                                                         │ │
│  │                                                                                     │ │
│  │  Trade IC-001: Internal FX Forward USD/JPY                                          │ │
│  │  ─────────────────────────────────────────                                          │ │
│  │  Asia Book (ASIA-COMM-1):                                                           │ │
│  │    Position: BUY USD 10M @ 148.50                                                   │ │
│  │    Snapshot: USD/JPY = 148.50                                                       │ │
│  │    MTM: $0                                                                          │ │
│  │                                                                                     │ │
│  │  London Book (LON-FX-1):                                                            │ │
│  │    Position: SELL USD 10M @ 148.50                                                  │ │
│  │    Snapshot: USD/JPY = 149.00                                                       │ │
│  │    MTM: +$33,557 (London values at higher rate)                                     │ │
│  │                                                                                     │ │
│  │  Firm Level: $0 + $33,557 = $33,557 FICTITIOUS P&L                                  │ │
│  │                                                                                     │ │
│  │  Alternative Calculation:                                                           │ │
│  │  = Notional × |Snapshot_A_Price - Snapshot_B_Price| / Snapshot_B_Price              │ │
│  │  = $10M × |148.50 - 149.00| / 149.00                                                │ │
│  │  = $33,557                                                                          │ │
│  │                                                                                     │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
│  Owner: Product Control                                                                  │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         5. AGGREGATE AND REPORT FICTITIOUS P&L                           │
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  DAILY FICTITIOUS P&L REPORT                                                        │ │
│  │  Date: 2025-01-15                                                                   │ │
│  │                                                                                     │ │
│  │  ┌───────────────────────────────────────────────────────────────────────────────┐  │ │
│  │  │ Region Pair     │ # Trades │ Gross Notional │ Fictitious P&L │ Status         │  │ │
│  │  ├─────────────────┼──────────┼────────────────┼────────────────┼────────────────┤  │ │
│  │  │ Asia ↔ London   │    45    │   $2.3B        │   +$156,234    │ ⚠ Review       │  │ │
│  │  │ NY ↔ London     │    23    │   $1.1B        │   -$45,678     │ ✓ Immaterial   │  │ │
│  │  │ Asia ↔ NY       │     8    │   $450M        │   +$12,345     │ ✓ Immaterial   │  │ │
│  │  ├─────────────────┼──────────┼────────────────┼────────────────┼────────────────┤  │ │
│  │  │ TOTAL           │    76    │   $3.85B       │   +$122,901    │                │  │ │
│  │  └───────────────────────────────────────────────────────────────────────────────┘  │ │
│  │                                                                                     │ │
│  │  Largest Contributors:                                                              │ │
│  │  1. IC-001: FX Forward USD/JPY Asia→London: +$33,557                                │ │
│  │  2. IC-015: IR Swap USD Asia→Treasury: +$28,900                                     │ │
│  │  3. IC-022: FX Forward EUR/USD NY→London: -$21,456                                  │ │
│  │                                                                                     │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
│  Owner: Product Control                                                                  │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         6. PRODUCT CONTROL REVIEW                                        │
│                                                                                          │
│  Product Control reviews fictitious P&L and determines if adjustment is warranted:       │
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  ADJUSTMENT DECISION FRAMEWORK                                                      │ │
│  │                                                                                     │ │
│  │  Given this is a TIMING DIFFERENCE that will reverse the next day,                  │ │
│  │  adjustments are typically only made if:                                            │ │
│  │                                                                                     │ │
│  │  1. VERY MATERIAL to daily P&L (>$500K or >10% of desk P&L)                         │ │
│  │  2. End of month/quarter and affects reported results                               │ │
│  │  3. Persistent pattern suggesting systematic issue                                  │ │
│  │                                                                                     │ │
│  │  Standard Treatment:                                                                │ │
│  │  ─────────────────────────────────────────────────────────────────────────────────  │ │
│  │  │ Total Fictitious P&L │ Action                                                 │  │ │
│  │  ├──────────────────────┼────────────────────────────────────────────────────────│  │ │
│  │  │ < $100K              │ No action - include in P&L explain only                │  │ │
│  │  │ $100K - $500K        │ Document and monitor - no adjustment                   │  │ │
│  │  │ $500K - $1M          │ Review with Desk Head - adjustment discretionary       │  │ │
│  │  │ > $1M                │ Escalate to Finance - likely adjustment required       │  │ │
│  │  └──────────────────────┴────────────────────────────────────────────────────────┘  │ │
│  │                                                                                     │ │
│  │  If adjustment made: Post reserve/release to neutralise fictitious P&L              │ │
│  │  Reverse next day when snapshots align                                              │ │
│  │                                                                                     │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
│  Owner: Product Control / Finance                                                        │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Regional Snapshot Details

### 5.1 Asia EOD Snapshot (Hong Kong)

| Attribute | Detail |
|-----------|--------|
| **Snapshot Time** | 17:30 HKT |
| **Markets Covered** | HK, Singapore, Tokyo, Sydney |
| **Key Instruments** | USD/JPY, AUD/USD, Asian IR curves, Asian equities |
| **Used For** | Asia book P&L, Asia trader performance |
| **Validation** | Asia MDC validates before publication |

### 5.2 London EOD Snapshot

| Attribute | Detail |
|-----------|--------|
| **Snapshot Time** | 17:30 GMT |
| **Markets Covered** | All European markets |
| **Key Instruments** | EUR, GBP, CHF rates; European equities; major FX |
| **Used For** | London book P&L, Global reference for VaR/regulatory |
| **Validation** | Global MDC validates before publication |

### 5.3 New York EOD Snapshot

| Attribute | Detail |
|-----------|--------|
| **Snapshot Time** | 17:30 EST |
| **Markets Covered** | US, Canada, Latin America |
| **Key Instruments** | USD rates, US equities, CAD, MXN |
| **Used For** | NY book P&L, Americas trader performance |
| **Validation** | NY MDC validates before publication |

---

## 6. VaR and Regulatory Reporting

### 6.1 Global VaR Calculation

For **VaR and regulatory capital** purposes, a single consistent snapshot must be used:

| Purpose | Snapshot Used | Rationale |
|---------|---------------|-----------|
| **Regulatory VaR** | London EOD | Consistent global view; aligned with regulatory reporting |
| **Internal Limit Monitoring** | London EOD | Consistent with regulatory; facilitates comparison |
| **Time Series Construction** | London EOD | Consistent observation times across history |

**Note:** Regional P&L uses local snapshots for trader accountability, but VaR uses a single global snapshot for consistency.

### 6.2 Reconciliation to VaR

The sum of regional P&L (using local snapshots) may differ from the global P&L (using London snapshot for all positions). This difference is explained by:

1. **Non-intercompany positions**: Market moves between regional close and London close
2. **Intercompany positions**: Fictitious P&L (calculated above)

This reconciliation is performed daily and documented in the P&L explain.

---

## 7. Controls

| Control ID | Control | Type | Owner |
|------------|---------|------|-------|
| REO-C01 | Regional snapshots captured by scheduled time | Preventive | Regional MDC |
| REO-C02 | Each region values books using local snapshot | Preventive | Product Control |
| REO-C03 | Intercompany trades identified daily via Snapshot Service | Detective | Trade ODS |
| REO-C04 | Fictitious P&L calculated for all cross-regional internal trades | Detective | Product Control |
| REO-C05 | Material fictitious P&L (>$500K) escalated to Finance | Detective | Product Control |
| REO-C06 | Adjustment decision documented with rationale | Detective | Finance |
| REO-C07 | Regional vs. global P&L reconciled daily | Detective | Product Control |

---

## 8. Service Levels

| Metric | Target | Escalation |
|--------|--------|------------|
| Asia snapshot published | 18:00 HKT | Asia MDC Manager |
| London snapshot published | 18:30 GMT | Global MDC Manager |
| NY snapshot published | 18:00 EST | NY MDC Manager |
| Intercompany trades identified | T+1 06:00 GMT | Trade ODS |
| Fictitious P&L calculated | T+1 07:00 GMT | Product Control |
| Adjustment decision made | T+1 08:00 GMT | Finance |

---

## 9. Special Scenarios

### 9.1 Market Holidays

| Scenario | Handling |
|----------|----------|
| **Asia holiday, London open** | Asia books use T-1 Asia snapshot; no new fictitious P&L for Asia trades |
| **London holiday, Asia/NY open** | Regional books valued at local snapshots; no global snapshot produced |
| **Partial holiday** | Each region uses own snapshot for open markets |

### 9.2 Large Market Moves

When significant market moves occur between regional closes:
- Fictitious P&L likely to be material
- Product Control pre-warned by Market Risk
- Finance prepared for potential adjustment
- Extra scrutiny on intercompany book activity

---

## 10. Related Documents

| Document | Relationship |
|----------|--------------|
| [Market Risk Process Orchestration](./market-risk-process-orchestration.md) | Parent orchestration |
| [EOD Market Data Snapshot](./eod-market-data-snapshot.md) | Provides regional snapshots |
| [Trade Capture Controls](./trade-capture-controls.md) | Identifies internal trades |
| [Market Risk Policy](../L3-Governance/policies/market-risk-policy.md) | Governance framework |

---

## 11. Document Control

### 11.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-15 | Initial version | MLRC |
| 2.0 | 2025-01-15 | Corrected to reflect local snapshot valuation; added intercompany fictitious P&L process | MLRC |

---

*End of Document*
