---
# Policy Metadata
policy_id: MR-L3-006
policy_name: Trading Book Boundary Policy
version: 1.0
effective_date: 2025-01-17
next_review_date: 2026-01-17
owner: Head of Market Risk
approving_committee: RMC
document_classification: Internal
supersedes: null

# Taxonomy Linkages
parent_policy: MR-L3-001  # Market Risk Policy
l1_requirements:
  - REQ-L1-001  # CRR/CRR III (Art 104)
  - REQ-L1-003  # FRTB
  - REQ-L1-004  # SS13/13 Market Risk
l2_risk_types:
  - MR-L2-001   # Market Risk (General)
l3_governance:
  - MR-L3-001   # Market Risk Policy
  - MR-L3-002   # MLRC Terms of Reference
l4_processes:
  - MR-L4-001   # Market Risk Process Orchestration
  - MR-L4-002   # Trade Capture Controls
  - MR-L4-014   # Aged Inventory Monitoring
l5_controls:
  - MR-L5-005   # Concentration Limits Controls
l7_systems:
  - SYS-MR-001  # Murex (Trading System)
  - SYS-MR-005  # Trade ODS
---

# Trading Book Boundary Policy

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Policy ID** | MR-L3-006 |
| **Version** | 1.0 |
| **Effective Date** | 17 January 2025 |
| **Next Review** | 17 January 2026 |
| **Parent Policy** | Market Risk Policy (MR-L3-001) |
| **Owner** | Head of Market Risk |
| **Approving Committee** | Risk Management Committee (RMC) |

---

## 1. Introduction

### 1.1 Purpose

This Trading Book Boundary Policy establishes the governance framework for maintaining a clear and robust boundary between the Trading Book and Banking Book at Meridian Global Bank ("the Bank"). The boundary is fundamental to ensuring appropriate risk measurement, regulatory capital treatment, and risk management.

This Policy supplements the Market Risk Policy (MR-L3-001) with detailed requirements for boundary definition, designation, monitoring, and reclassification governance.

### 1.2 Regulatory Context

The trading book boundary is a core regulatory requirement under CRR and FRTB:

| Regulation | Reference | Key Requirements |
|------------|-----------|------------------|
| **CRR Article 104** | Trading book definition | Positions held with trading intent; capable of being traded |
| **CRR Article 104a** | Trading intent | Short-term resale; profit from price movements; locking in arbitrage |
| **CRR Article 104b** | Boundary requirements | Clear policies; designation at inception; internal transfers |
| **CRR Article 104c** | Presumption of trading book | Listed equities, net short credit/equity positions, underwriting |
| **FRTB** | Boundary tightening | Stricter boundary; reduced arbitrage opportunities |
| **PRA SS13/13** | Market risk management | Boundary governance expectations |

### 1.3 Scope

This Policy applies to:
- All positions across all legal entities within Meridian Global Bank Group
- All asset classes (rates, credit, FX, equities, commodities)
- All desks and business units
- All staff involved in trade booking, risk management, and finance

---

## 2. Trading Book Definition

### 2.1 Trading Book Criteria

A position is assigned to the **Trading Book** if it meets the following criteria:

| Criterion | Definition | Evidence Required |
|-----------|------------|-------------------|
| **Trading Intent** | Position held for short-term resale, profiting from price movements, or locking in arbitrage | Trading mandate; desk strategy documentation |
| **Tradability** | Position can be traded or hedged in an orderly manner | Market liquidity assessment; exit strategy |
| **Market Risk Exposure** | Position exposes the Bank to market risk that should be managed under trading book framework | Risk factor identification |
| **Not Excluded** | Position not explicitly required to be in Banking Book | Regulatory classification check |

### 2.2 Trading Intent

Positions are deemed to have **trading intent** if held for any of the following purposes:

1. **Short-term resale**: Intent to sell in the near term
2. **Price movement profit**: Benefiting from actual or expected short-term price differences
3. **Arbitrage locking**: Locking in profits from price discrepancies
4. **Market-making**: Inventory held to facilitate client business
5. **Hedging trading book**: Positions hedging other trading book items

### 2.3 Presumption of Trading Book

The following positions are **presumed to be in the Trading Book** unless the Bank can demonstrate otherwise:

| Position Type | Presumption Basis |
|---------------|-------------------|
| Listed equity instruments | CRR Art 104c(a) |
| Net short credit positions | CRR Art 104c(b) |
| Net short equity positions | CRR Art 104c(b) |
| Underwriting positions | CRR Art 104c(c) |
| Positions from market-making | CRR Art 104c(d) |
| Collective investment undertakings (trading) | CRR Art 104c(e) |
| Exchange-traded derivatives | CRR Art 104c(f) |

Rebuttal of presumption requires documented evidence and RMC approval.

---

## 3. Banking Book Definition

### 3.1 Banking Book Criteria

A position is assigned to the **Banking Book** if it meets the following criteria:

| Criterion | Definition | Examples |
|-----------|------------|----------|
| **Non-trading Intent** | Position not held for trading purposes | Held to maturity; contractual term |
| **Strategic Holding** | Investment held for strategic purposes | Equity stakes in subsidiaries |
| **Structural Position** | Position arising from structural balance sheet management | ALM hedges; liquidity portfolio |
| **Regulatory Requirement** | Position required by regulation to be in Banking Book | Securitisation positions (certain) |

### 3.2 Banking Book Position Types

| Category | Description | Capital Treatment |
|----------|-------------|-------------------|
| **Held to Maturity** | Debt instruments held to contractual maturity | Credit risk (SA or IRB) |
| **Available for Sale** | Instruments not actively traded but may be sold | Credit risk + CSRBB where applicable |
| **Loans and Receivables** | Originated loans | Credit risk |
| **Strategic Equities** | Equity holdings not for trading | Equity risk in Banking Book |
| **Structural FX** | FX positions from structural investments | May be exempt from FX risk |
| **ALM Hedges** | Derivatives hedging Banking Book exposures | Hedge accounting treatment |

---

## 4. Boundary Governance

### 4.1 Designation at Inception

**Requirement**: All positions must be designated to Trading Book or Banking Book **at inception** (point of trade execution or acquisition).

| Responsibility | Owner |
|----------------|-------|
| Initial designation in booking system | Front Office |
| Validation of designation | Product Control |
| Ongoing boundary compliance | Market Risk + Finance |
| Policy oversight | RMC |

### 4.2 Designation Documentation

For each position, the following must be documented:

| Element | Requirement |
|---------|-------------|
| **Book Designation** | Trading Book or Banking Book |
| **Trading Intent** | Documented rationale for trading book positions |
| **Desk Assignment** | Trading desk responsible |
| **Mandate Compliance** | Confirmation position within desk mandate |
| **Exit Strategy** | For trading book: how position will be managed/exited |

### 4.3 Desk Mandates

Each trading desk operates under a documented **Trading Mandate** that specifies:

- Permitted products and instruments
- Permitted markets and currencies
- Position limits and risk limits
- Trading strategies and intent
- Holding period expectations

Positions outside desk mandate require escalation and approval before booking.

### 4.4 Boundary Controls

| Control | Frequency | Owner | Purpose |
|---------|-----------|-------|---------|
| Trade booking validation | Real-time | Systems/Product Control | Ensure correct designation |
| Boundary reconciliation | Daily | Finance | Trading vs Banking book alignment |
| Mandate compliance check | Daily | Market Risk | Positions within mandate |
| Aged inventory review | Quarterly | Market Risk | Identify positions with changed intent |
| Boundary attestation | Annual | Desk Heads | Confirm trading intent maintained |

---

## 5. Reclassification Governance

### 5.1 Principle of No Reclassification

**General Rule**: Once a position is designated to Trading Book or Banking Book, it **cannot be reclassified** except in limited, pre-defined circumstances. This prevents regulatory arbitrage.

### 5.2 Permitted Reclassifications

Reclassification may only occur under the following circumstances:

| Circumstance | Direction | Approval Required |
|--------------|-----------|-------------------|
| **Market Event** | TB → BB | Extraordinary market conditions preventing trading; RMC approval |
| **Business Strategy Change** | TB → BB | Documented change in business strategy; RMC + PRA notification |
| **Regulatory Change** | Either | Change in regulatory requirements; RMC approval |
| **Error Correction** | Either | Booking error identified; CFO + CRO approval |
| **Group Restructuring** | Either | Entity merger/demerger; Board approval |

### 5.3 Reclassification Process

Any proposed reclassification must follow this process:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     RECLASSIFICATION PROCESS                            │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. IDENTIFICATION                                                       │
│    - Position identified for potential reclassification                 │
│    - Requestor documents rationale                                      │
│    - Initial assessment by Market Risk                                  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. IMPACT ASSESSMENT                                                    │
│    - Capital impact quantified (Market Risk + Finance)                  │
│    - Risk measurement impact assessed                                   │
│    - P&L impact evaluated                                               │
│    - Regulatory notification requirement determined                     │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 3. APPROVAL                                                             │
│    - MLRC review (all cases)                                            │
│    - RMC approval (TB ↔ BB transfers)                                   │
│    - Board notification (material transfers)                            │
│    - PRA notification (where required)                                  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 4. EXECUTION                                                            │
│    - System booking updated                                             │
│    - Capital recalculated                                               │
│    - Risk limits adjusted                                               │
│    - Documentation archived                                             │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 5. MONITORING                                                           │
│    - Post-transfer monitoring period (6 months)                         │
│    - Any subsequent transfer requires enhanced scrutiny                 │
│    - Quarterly reporting to MLRC                                        │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.4 Capital Impact on Reclassification

When reclassification results in reduced capital requirements:
- Day 1 capital benefit is **not recognised**
- Capital charge remains at higher of pre/post transfer for **12 months**
- PRA notification required for material capital reduction

This prevents gaming through strategic reclassifications.

### 5.5 Regulatory Notification

The PRA must be notified of:
- Any Trading Book → Banking Book transfer
- Any transfer resulting in capital reduction >$6m
- Any pattern of transfers suggesting arbitrage
- Changes to boundary policy

---

## 6. Internal Transfers

### 6.1 Internal Risk Transfers (IRT)

Internal Risk Transfers between Trading Book and Banking Book are subject to specific governance:

| Transfer Type | Treatment | Requirements |
|---------------|-----------|--------------|
| **TB → TB** | Permitted | Normal booking; no special approval |
| **BB → TB** (hedging) | Conditional | Must meet hedge criteria; documented |
| **TB → BB** | Restricted | RMC approval; capital floor applies |

### 6.2 Internal Hedging

Where Trading Book hedges Banking Book exposures:
- The hedge must be documented as Internal Risk Transfer
- Banking Book continues to hold original risk for capital
- Trading Book hedge is a separate position with its own capital treatment
- No double-counting of risk reduction

### 6.3 Third-Party Hedging

Where the Bank externally hedges an internal position:
- External hedge recognised in book where originally booked
- Capital benefit only in book holding external hedge
- Documentation must clearly identify hedge relationship

---

## 7. Aged Inventory and Trading Intent

### 7.1 Aged Inventory Definition

Positions in the Trading Book that have been held for extended periods raise questions about trading intent:

| Category | Definition | Action Required |
|----------|------------|-----------------|
| **Watch List** | Held >3 months with <25% turnover | Heightened monitoring |
| **Aged** | Held >6 months with <10% turnover | Trading intent attestation |
| **Stale** | Held >12 months with <2% turnover | Exit strategy or reclassification review |

### 7.2 Quarterly Attestation

For aged inventory positions, Desk Heads must **quarterly attest**:
- Trading intent is maintained
- Position is capable of being traded/hedged
- Exit strategy exists and is viable
- Position remains appropriate for Trading Book

### 7.3 Trading Intent Challenges

If trading intent cannot be demonstrated:
- Position escalated to MLRC
- Assessment of continued Trading Book eligibility
- If ineligible: reclassification process initiated
- Capital impact crystallised at point of reclassification

> **Process Reference**: For detailed aged inventory procedures, see [Aged Inventory Monitoring (MR-L4-014)](../../L4-Processes/processes/aged-inventory-monitoring.md).

---

## 8. FRTB Boundary Considerations

### 8.1 FRTB Boundary Tightening

Under FRTB (applicable from implementation date), the boundary rules are strengthened:

| FRTB Requirement | Impact |
|------------------|--------|
| **Stricter Trading Intent** | Enhanced documentation requirements |
| **Desk-Level Assignment** | Positions assigned to defined trading desks |
| **Desk Attestation** | Annual attestation of desk scope and intent |
| **Boundary Permeability** | Tighter controls on internal transfers |
| **P&L Attribution** | Must demonstrate desk-level P&L alignment with risk |

### 8.2 Trading Desk Definition

Under FRTB, each **Trading Desk** must be clearly defined with:
- Documented business strategy
- Coherent risk management approach
- Defined products and markets
- Named desk head with P&L responsibility
- Capital allocated at desk level

### 8.3 P&L Attribution Test

FRTB requires that hypothetical P&L (from risk model) aligns with actual P&L. Material misalignment may indicate:
- Risk not properly captured
- Booking in wrong desk/book
- Potential boundary issues

---

## 9. Monitoring and Reporting

### 9.1 Ongoing Monitoring

| Metric | Frequency | Owner | Escalation |
|--------|-----------|-------|------------|
| Boundary reconciliation breaks | Daily | Finance | CFO if unresolved >3 days |
| New positions outside mandate | Real-time | Systems | Market Risk immediately |
| Aged inventory (>6 months) | Monthly | Market Risk | MLRC quarterly |
| Internal transfers | Weekly | Market Risk | MLRC if material |
| Reclassification requests | Ad hoc | Market Risk | RMC |

### 9.2 Regular Reporting

| Report | Frequency | Content | Audience |
|--------|-----------|---------|----------|
| Boundary Status Report | Monthly | Reconciliation status; open items | MLRC |
| Aged Inventory Report | Quarterly | Aged positions; attestation status | MLRC/RMC |
| Reclassification Report | Quarterly | Transfers in period; capital impact | RMC |
| Annual Boundary Review | Annual | Policy effectiveness; regulatory updates | RMC/Board |

### 9.3 Annual Review

Market Risk, in conjunction with Finance, conducts an annual review of:
- Boundary policy effectiveness
- Reclassification patterns
- Aged inventory trends
- FRTB readiness (until full implementation)
- Regulatory developments

Results presented to RMC with recommendations for policy updates.

---

## 10. Roles and Responsibilities

| Role | Responsibilities |
|------|------------------|
| **Front Office** | Correct designation at inception; mandate compliance; trading intent attestation |
| **Product Control** | Booking validation; P&L verification; boundary reconciliation |
| **Market Risk** | Policy oversight; boundary monitoring; aged inventory review; reclassification assessment |
| **Finance** | Capital calculation; regulatory reporting; boundary reconciliation |
| **Risk Methodology & Analytics** | FRTB desk definition support; P&L attribution methodology |
| **Internal Audit** | Independent assurance over boundary controls |
| **RMC** | Policy approval; reclassification approval; boundary oversight |

---

## 11. Related Documents

### 11.1 Parent and Sibling Policies

| Document | Relationship |
|----------|--------------|
| [Market Risk Policy (MR-L3-001)](./market-risk-policy.md) | Parent policy |
| [VaR Policy (MR-L3-004)](./var-policy.md) | Sibling policy; risk measurement |
| [Stress Testing Policy (MR-L3-005)](./stress-testing-policy.md) | Sibling policy; stress framework |

### 11.2 Supporting Processes

| Process | Reference |
|---------|-----------|
| Trade Capture Controls | MR-L4-002 |
| Aged Inventory Monitoring | MR-L4-014 |

### 11.3 Related Policies

| Policy | Relationship |
|--------|--------------|
| Non-Traded Market Risk Policy | Banking Book risk management |
| Hedge Accounting Policy | Internal transfer treatment |
| Capital Policy | Capital treatment across books |

---

## 12. Exceptions

There are no exceptions to this Policy. Any deviations require RMC approval and PRA notification where required.

---

## 13. Definitions

| Term | Definition |
|------|------------|
| **Trading Book** | Positions held with trading intent subject to market risk capital |
| **Banking Book** | Positions not held for trading subject to credit risk capital |
| **Trading Intent** | Purpose of short-term resale, price profit, or arbitrage |
| **Reclassification** | Moving position between Trading and Banking Book |
| **Internal Risk Transfer** | Moving risk exposure between internal books |
| **Aged Inventory** | Trading book positions held >6 months with low turnover |
| **FRTB** | Fundamental Review of Trading Book (Basel framework) |
| **Desk Mandate** | Documented scope of permitted trading activity |

---

## 14. Policy Contact

| Field | Details |
|-------|---------|
| **Policy Owner** | Head of Market Risk |
| **Finance Queries** | Group Financial Controller |
| **Regulatory Queries** | Head of Regulatory Affairs |

---

## 15. Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-17 | Initial version | RMC |

---

*This policy is the property of Meridian Global Bank. Unauthorised distribution is prohibited.*

*End of Document*
