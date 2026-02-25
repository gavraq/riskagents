---
name: stress-scenario-approver
description: Approves a stress scenario into the official library by updating all 3 data stores (risk_factor_shocks_library.json, stress-inventory.ts, LIBRARY_SCENARIOS). Use when user says "approve scenario", "add to approved", "add to stress library", "MLRC approved", "include in official stress tests", "add scenario to library", "promote scenario".
---

# Stress Scenario Approver

You are the **Stress Scenario Approval Workflow Agent** responsible for promoting a draft/research stress scenario into the official approved stress library. This requires updating **3 separate data stores** in a specific order, and critically, ensuring **full coverage** across all 442 rate curves and 227 FX pairs.

## When to Use This Skill

Trigger on keywords like:
- "approve scenario", "approve this stress"
- "add to approved", "add to stress library"
- "MLRC approved", "include in official stress tests"
- "add scenario to library", "promote scenario"
- "add the new stress to the approved library"

## The 3 Data Stores

Approving a scenario requires updating ALL of the following:

### 1. Risk Factor Shocks Library (JSON)
**Primary path**: `.claude/skills/pillar-stress-generator/data/risk_factor_shocks_library.json`
**UI copy path**: `riskagents-ui/public/data/risk_factor_shocks_library.json` (at `/Volumes/DockSSD/projects/riskagents-ui/public/data/risk_factor_shocks_library.json`)

Contains shock parameters for all 7 asset classes:
- `rates` - **442 interest rate curves** (167 `:Std` + 275 secondary: bonds, repos, basis swaps, RFR, etc.)
- `fx` - **227 FX pairs** (spot + NDF pairs for all currencies)
- `credit` - Credit spread widening by region with sector betas (10 regions)
- `energy` - Energy commodity price and volatility shocks (6 products)
- `precious_metals` - Precious metal price, vol, and lease rate shocks (5 metals)
- `base_metals` - Base metal price and volatility shocks (8 metals)
- `equities` - Equity index (14), sector (11), and volatility shocks

### 2. Stress Inventory TypeScript (UI)
**Path**: `/Volumes/DockSSD/projects/riskagents-ui/src/lib/stress-inventory.ts`

Contains:
- `APPROVED_SCENARIOS` array - Scenario cards for the Scenarios tab
- `LIBRARY_SCENARIOS` array - Dropdown options for the Parameters tab
- `UNCOVERED_DOMAINS` array - Domains without coverage (update if applicable)

### 3. Scenario Source Document
**Path**: `output/stress tests/<scenario_filename>.md`

The source markdown document with full parameter tables.

## Workflow Steps

### Step 1: Identify the Source Document

Find the scenario markdown in `output/stress tests/`. Read it to extract all parameter data from the tables.

### Step 2: Create a Python Build Script

Create a file `data/build_<scenario_slug>_shocks.py` following the pattern in `data/build_approved_scenarios.py`.

The build script defines **explicit shocks** for:
- Major `:Std` rate curves (USD, EUR, GBP, JPY, CHF + key EM currencies mentioned in the document)
- Major FX pairs explicitly mentioned in the scenario document
- All 7 non-rates asset classes (credit, energy, precious, base metals, equities) in full

**Important**: The build script only needs to define the **explicitly documented** rate curves and FX pairs. The remaining 400+ rate curves and 190+ FX pairs are filled by the propagation script (Step 4).

```python
#!/usr/bin/env python3
"""Build <Scenario Name> into the risk_factor_shocks_library.json."""

import json
from pathlib import Path
from datetime import date

LIBRARY_PATH = Path(__file__).parent.parent / ".claude/skills/pillar-stress-generator/data/risk_factor_shocks_library.json"
UI_PATH = Path("/Volumes/DockSSD/projects/riskagents-ui/public/data/risk_factor_shocks_library.json")

TENORS = ["O/N", "TN", "1W", "2W", "1M", "2M", "3M", "6M", "9M", "1Y", "18M", "2Y", "3Y", "5Y", "7Y", "10Y", "15Y", "20Y", "30Y"]

SCENARIO_NAME = "<Exact Scenario Name>"  # Must match stress-inventory.ts libraryScenario


def build_rate_curve(shocks_dict: dict) -> dict:
    """Build a tenor->bps dict from sparse input."""
    return {t: v for t, v in shocks_dict.items() if t in TENORS}


def build_scenario():
    """Return (rates, fx, credit, energy, precious, base_metals, equities) dicts."""
    rates = {}
    # Define :Std curves for major currencies mentioned in document
    rates["USD :Std"] = build_rate_curve({...})
    rates["EUR :Std"] = build_rate_curve({...})
    # ... etc for all explicitly documented currencies

    fx = {
        "EUR": 0.10,  # Convention: positive = depreciation vs USD
        # ... all explicitly documented pairs
    }

    credit = { ... }  # Full 10 regions with sector betas
    energy = { ... }   # 6 standard products
    precious = { ... } # 5 metals
    base_metals = { ... } # 8 metals
    equities = { ... }  # 14 indices, 11 sectors, VIX

    return rates, fx, credit, energy, precious, base_metals, equities


def main():
    with open(LIBRARY_PATH) as f:
        library = json.load(f)

    rates, fx, credit, energy, precious, base_metals, equities = build_scenario()

    # Add rates (individual curves, preserving any existing)
    if SCENARIO_NAME not in library["asset_classes"]["rates"]["scenarios"]:
        library["asset_classes"]["rates"]["scenarios"][SCENARIO_NAME] = {}
    for curve, shocks in rates.items():
        library["asset_classes"]["rates"]["scenarios"][SCENARIO_NAME][curve] = shocks

    # Add other asset classes (full replacement)
    library["asset_classes"]["fx"]["scenarios"][SCENARIO_NAME] = fx
    library["asset_classes"]["credit"]["scenarios"][SCENARIO_NAME] = {"region_spreads": credit}
    library["asset_classes"]["energy"]["scenarios"][SCENARIO_NAME] = {"shocks": energy}
    library["asset_classes"]["precious_metals"]["scenarios"][SCENARIO_NAME] = {"shocks": precious}
    library["asset_classes"]["base_metals"]["scenarios"][SCENARIO_NAME] = {"shocks": base_metals}
    if "equities" in library["asset_classes"]:
        library["asset_classes"]["equities"]["scenarios"][SCENARIO_NAME] = equities

    # Update metadata
    all_names = sorted(set(
        list(library["asset_classes"]["rates"]["scenarios"].keys()) +
        list(library["asset_classes"]["fx"]["scenarios"].keys()) +
        [SCENARIO_NAME]
    ))
    library["metadata"]["total_scenarios"] = len(all_names)
    library["metadata"]["scenario_names"] = all_names
    library["metadata"]["last_updated"] = str(date.today())

    # Write to both paths
    with open(LIBRARY_PATH, "w") as f:
        json.dump(library, f, indent=2)
    if UI_PATH.parent.exists():
        with open(UI_PATH, "w") as f:
            json.dump(library, f, indent=2)


if __name__ == "__main__":
    main()
```

### Step 3: Run the Build Script

```bash
uv run python data/build_<scenario_slug>_shocks.py
```

This adds explicit shocks (~20 rate curves, ~33 FX pairs + all commodity/credit/equity data).

### Step 4: Propagate Regional Shocks (CRITICAL - Full Coverage)

**This is the step that ensures full coverage across all 442 rate curves and 227 FX pairs.**

The library has 442 rate curves (167 standard `:Std` + 275 secondary: bonds, repos, cross-currency basis, RFR, etc.) and 227 FX pairs (spot + NDF). The build script only defines the ~15-20 major curves from the document. The propagation script fills the remaining ~420 curves and ~190 pairs using **regional mapping**.

#### 4a. Add regional shocks to `data/propagate_regional_shocks.py`

Add an entry to the `REGIONAL_SHOCKS` dict for the new scenario. The regions are:

| Region | Description | Example Currencies |
|--------|-------------|-------------------|
| `DM_USD` | US Dollar | USD |
| `DM_EUR` | Euro | EUR |
| `DM_GBP` | Sterling | GBP |
| `DM_JPY` | Japanese Yen | JPY |
| `DM_CHF` | Swiss Franc | CHF |
| `DM_COMM` | Commodity DM | AUD, NZD, CAD |
| `DM_SCANDI` | Scandinavian | NOK, SEK, DKK |
| `EM_ASIA` | EM Asia | CNY, INR, KRW, IDR, THB, PHP, VND, etc. |
| `EM_LATAM` | Latin America | BRL, MXN, CLP, COP, PEN, ARS, etc. |
| `EM_CEE` | Central & Eastern Europe | PLN, HUF, CZK, RON, BGN, etc. |
| `EM_RUSSIA` | Russia / CIS | RUB, UAH, KZT, UZS, etc. |
| `EM_TURKEY` | Turkey | TRY |
| `MENA` | Middle East & North Africa | AED, SAR, QAR, EGP, MAD, ILS, etc. |
| `AFRICA` | Sub-Saharan Africa | ZAR, NGN, GHS, KES, TZS, UGX, etc. |
| `GOLD` | Gold | XAU |

Each region needs:
- **`fx`**: FX shock as decimal (positive = depreciation vs USD)
- **`rates`**: Sparse tenor→bps dict (will be interpolated to all 19 tenors)

**How it works**:
1. For each currency/curve NOT already defined by the build script
2. Look up the currency's region in `REGION_MAP`
3. Apply the regional FX shock or interpolated rate curve
4. Explicit values from the build script are NEVER overwritten

#### 4b. Run the propagation script

```bash
uv run python data/propagate_regional_shocks.py
```

**Expected output**: The new scenario should go from ~20 rates / ~33 FX to **442 rates / 227 FX**.

#### 4c. Verify coverage

```bash
uv run python -c "
import json
lib = json.load(open('.claude/skills/pillar-stress-generator/data/risk_factor_shocks_library.json'))
name = '<SCENARIO_NAME>'
rates = len(lib['asset_classes']['rates']['scenarios'][name])
fx = len(lib['asset_classes']['fx']['scenarios'][name])
print(f'{name}: {rates} rate curves, {fx} FX pairs')
assert rates >= 440, f'FAIL: Only {rates} rate curves (expected ~442)'
assert fx >= 225, f'FAIL: Only {fx} FX pairs (expected ~227)'
print('PASS: Full coverage achieved')
"
```

### Step 5: Update stress-inventory.ts

Add an entry to the `APPROVED_SCENARIOS` array:

```typescript
{
  id: "<kebab-case-id>",
  name: "<Full Scenario Name>",
  domain: "<Domain Category>",
  trigger: "<Trigger description>",
  riskFactors: ["Factor 1", "Factor 2", "Factor 3", "Factor 4"],
  assetClasses: ["Energy", "FX", "Rates", "Credit", "Equities"],
  severity: "Severe" | "Extreme" | "Moderate",
  status: "Approved",
  lastReviewed: "<Month Year>",
  file: "<filename>.md",
  libraryScenario: "<Exact name matching SCENARIO_NAME in build script>",
}
```

Add the scenario name to the `LIBRARY_SCENARIOS` array (in the "Approved pillar stress scenarios" section).

Update `UNCOVERED_DOMAINS` if this scenario covers a previously uncovered domain.

### Step 6: Final Verification

```bash
cd /Volumes/DockSSD/projects/riskagents-ui && npm run build
```

Check that:
- Build completes without errors
- Scenario count increased by 1
- All 7 asset class tabs show data for the new scenario
- Rate curves = 442 and FX pairs = 227 (matching other approved scenarios)

## Data Mapping Reference

### Rates Structure
```json
{
  "SCENARIO_NAME": {
    "USD :Std": {"O/N": 25, "1W": 30, "1M": 40, ...},
    "EUR :Std": {"O/N": 35, "1M": 40, ...},
    "USD_GOVBND_SA": {"O/N": 25, ...},
    "USD_SOFR_ANFUTS": {"O/N": 25, ...},
    ...
  }
}
```
- **Standard curves** (`CCY :Std`): The main swap curve for each currency. Defined explicitly in the build script.
- **Secondary curves** (e.g., `USD_GOVBND_SA`, `EUR_RFR_ISDA`, `CNH_REPO_COLLAT_MED_GRADE`): Government bonds, RFR, repo, cross-currency basis. Populated by propagation script using the same regional shocks.
- Currency format: `"CCY :Std"` (note the space before colon)
- Values are basis points (positive = rates up, negative = rates down)
- All 19 standard tenors: O/N, TN, 1W, 2W, 1M, 2M, 3M, 6M, 9M, 1Y, 18M, 2Y, 3Y, 5Y, 7Y, 10Y, 15Y, 20Y, 30Y

### FX Structure
```json
{
  "EUR": 0.10,    // 10% depreciation vs USD
  "JPY": -0.08,   // 8% appreciation vs USD (safe haven)
  "AE1": 0.08,    // NDF pair for AED
  ...
}
```
- **Convention**: Positive = depreciation vs USD (currency weakens)
- Safe havens (JPY, CHF) that appreciate have **negative** values
- NDF pairs (3-letter codes ending in digit, e.g., `AE1` for AED, `CN1` for CNY) are populated by the propagation script to match regional averages

### Credit Structure
```json
{
  "region_spreads": {
    "North America": {
      "base_spread_move_pct": 40,
      "sectors": {
        "Materials": 1.2,
        "Energy": 0.8,
        ...
      }
    },
    ...
  }
}
```
- `base_spread_move_pct`: Percentage spread widening for the region
- `sectors`: Beta multipliers (1.0 = base move, >1 = higher stress, <1 = lower stress)
- Standard 10 regions: North America, Europe, Emerging Asia, Middle East and North Africa, Africa Sub Sahara, South America, Central America, Emerging Europe, Australasia and Low Risk Asia, Offshore
- Standard 13 sectors: Materials, Energy, Oil & Gas, Utilities, Health Care, Consumer Cyclical, Consumer Goods, Consumer Services, Consumer Stable, Telecommunications, Diversified, Financials, Unclassified

### Energy Structure
```json
{
  "shocks": {
    "Brent Crude": {"price_shock_pct": 50, "vol_shock_abs": 70},
    "WTI": {"price_shock_pct": 35, "vol_shock_abs": 60},
    "Heating Oil": {"price_shock_pct": 55, "vol_shock_abs": 55},
    "Gasoil": {"price_shock_pct": 65, "vol_shock_abs": 55},
    "Natural Gas (TTF)": {"price_shock_pct": 35, "vol_shock_abs": 50},
    "Natural Gas (Henry Hub)": {"price_shock_pct": 20, "vol_shock_abs": 40}
  }
}
```

### Precious Metals Structure
```json
{
  "shocks": {
    "Gold": {"price_shock_pct": 25, "vol_shock_pct": 40, "lease_rate_bps": -30},
    "Silver": {"price_shock_pct": 30, "vol_shock_pct": 45, "lease_rate_bps": -20},
    "Platinum": {"price_shock_pct": 15, "vol_shock_pct": 30, "lease_rate_bps": 0},
    "Palladium": {"price_shock_pct": 20, "vol_shock_pct": 35, "lease_rate_bps": 10},
    "Rhodium": {"price_shock_pct": 10, "vol_shock_pct": null, "lease_rate_bps": 0}
  }
}
```

### Base Metals Structure
```json
{
  "shocks": {
    "Copper": {"price_shock_pct": -10, "vol_shock_abs": 30},
    "Aluminium": {"price_shock_pct": -8, "vol_shock_abs": 25},
    "Nickel": {"price_shock_pct": -12, "vol_shock_abs": 35},
    "Zinc": {"price_shock_pct": -10, "vol_shock_abs": 25},
    "Lead": {"price_shock_pct": -8, "vol_shock_abs": 20},
    "Tin": {"price_shock_pct": -10, "vol_shock_abs": 25},
    "Cobalt": {"price_shock_pct": -5, "vol_shock_abs": 20},
    "Iron Ore": {"price_shock_pct": -15, "vol_shock_abs": 30}
  }
}
```

### Equities Structure
```json
{
  "index_shocks": {
    "S&P 500": -15,
    "NASDAQ": -15,
    "Dow Jones": -12,
    "Russell 2000": -18,
    "Euro Stoxx 50": -20,
    "FTSE 100": -10,
    "DAX": -18,
    "Nikkei 225": -15,
    "Hang Seng": -15,
    "KOSPI": -12,
    "TAIEX": -10,
    "ASX 200": -12,
    "MSCI EM": -20,
    "JSE Top 40": -18
  },
  "sector_shocks": {
    "Technology": -15,
    "Financials": -12,
    "Energy": 20,
    "Materials": 15,
    ...
  },
  "volatility": {
    "VIX": 38
  }
}
```

## Reference Files

- **Build script pattern**: `data/build_approved_scenarios.py` (defines explicit shocks for ~12 curves per scenario)
- **Propagation script**: `data/propagate_regional_shocks.py` (fills remaining ~420 curves using regional mapping)
- **Region/currency mapping**: `REGION_MAP` in `data/propagate_regional_shocks.py`
- **Equity shocks pattern**: `data/build_equity_shocks.py`
- **Current library**: `.claude/skills/pillar-stress-generator/data/risk_factor_shocks_library.json`
- **UI inventory**: `riskagents-ui/src/lib/stress-inventory.ts`
- **Scenario documents**: `output/stress tests/*.md`

## Coverage Requirements

Every approved scenario MUST have:

| Asset Class | Expected Count | Tolerance |
|---|---|---|
| Rate curves | 442 | >= 440 |
| FX pairs | 227 | >= 225 |
| Credit regions | 10 | Exact |
| Energy products | 6 | Exact (standard set) |
| Precious metals | 5 | Exact (Gold, Silver, Platinum, Palladium, Rhodium) |
| Base metals | 8 | Exact (Cu, Al, Ni, Zn, Pb, Sn, Co, Fe) |
| Equity indices | 14 | Exact |
| Equity sectors | 11 | Exact |

If the propagation step results in fewer than 440 rate curves or 225 FX pairs, investigate whether the `REGION_MAP` in `propagate_regional_shocks.py` is missing any currencies and add them.

## Important Notes

- Always run the build script THEN the propagation script (in that order)
- The build script defines explicit shocks; the propagation script fills the rest - never the reverse
- Explicit values from the build script are NEVER overwritten by propagation
- The propagation script uses linear interpolation to fill all 19 tenors from sparse inputs
- Scenario names must match exactly across all 3 data stores
- Run `npm run build` in the UI project to verify TypeScript compiles
- Both JSON copies (skill data + UI public) must be identical
