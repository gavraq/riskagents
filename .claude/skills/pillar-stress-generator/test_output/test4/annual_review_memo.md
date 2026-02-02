# Financial Crisis 2025 - Annual Review 2025

## Board Report Cover Sheet
**Document Name**: Financial Crisis 2025 - Annual Review 2025
**Meeting Date**: MLRC - 2025-11-12
**Presenter**: Market Risk
**Context**: Memo for noting - Annual Review for the "Financial Crisis 2025" Scenario
**Purpose**: Annual review of "Financial Crisis 2025" scenario shocks applied to various asset classes

## Background
The below are the shocks approved for the "Financial Crisis 2025" scenario as per the ICBCS Stress Testing Parameterisation document.

### Market Developments Since Last Review
- Volatility regime has shifted higher vs 2024
- EM spreads have compressed significantly

### System and Platform Changes
- Base Metals migrating to Murex (in progress, target 2025)
- Precious Metals vol shocks changed to relative (Murex)

## Rates & FX
**Market Recalibration**

**Rationale**: Market volatility patterns have changed since last review. Consider recalibrating shock magnitudes to current vol regime.

**Affected Products**: All rate curves, All FX pairs

## Credit Trading
**No proposed changes**

**Current Applied Shocks**
*(See attached parameterization document)*

## Energy
**No proposed changes**

**Current Applied Shocks**
*(See attached parameterization document)*

## Precious Metals
**Methodology Change**

**Rationale**: Vol shock type update from Absolute to Relative, adjusting the size of the shocks accordingly informed by current market levels and existing shock sizes. This change aligns with the Precious Metals to Murex migration.

**Proposed Changes**:
- volatility_shock_type: relative
- note: Changed from Absolute to Relative per Murex migration
**Affected Products**: Gold, Silver, Platinum, Palladium

## Base Metals
**Parameter Update**

**Rationale**: Explicitly define Cobalt shock (currently falls under 'Other')
Note: Full term structure upgrade deferred pending Murex migration completion in 2025

**Proposed Changes**:
- Cobalt: {'price_shock_pct': -25, 'vol_shock_abs': 25}
**Affected Products**: Cobalt

## Conclusions and Recommended Actions
Significant revision required. Recommend scheduling detailed scenario redesign discussion.

## References
[1] ICBCS Stress Testing Parameterisation

## Document History
**Prepared by**: Market Risk
**Date**: 2025-11-12
**Reviewed by 2nd line of defence**: N/A
**Matters raised by 2nd line of defence**: N/A

## Formal Document Governance
**Reviewing committee and meeting date**: MLRC
**Outcome and key rationale for decision**: *(To be completed post-MLRC)*
**Significant matters raised and associated actions**: *(To be completed post-MLRC)*
