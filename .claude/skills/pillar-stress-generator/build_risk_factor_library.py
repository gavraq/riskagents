"""
Build comprehensive risk factor shock library from Bank stress testing data.
Extracts data from Excel file and structures it for use by the pillar stress generator skill.
"""

import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Any

# Paths
EXCEL_FILE = Path("data/example_bank/Processes/Market_Risk/Stress Testing/Stress testing shocks - detailed breakdown.xlsx")
OUTPUT_DIR = Path(".claude/skills/pillar-stress-generator/data")

def extract_rates_data(excel_file: Path) -> Dict[str, Any]:
    """Extract rate curve shock data from all scenarios."""
    xls = pd.ExcelFile(excel_file)

    # Get all rate sheets
    rate_sheets = [s for s in xls.sheet_names if s.endswith('_rates')]

    scenarios = {}
    all_curves = set()
    tenors = ['O/N', 'T/N', '1W', '2W', '1M', '2M', '3M', '6M', '9M', '1Y', '2Y', '3Y', '5Y', '7Y', '10Y', '15Y', '20Y', '30Y']

    for sheet in rate_sheets:
        scenario_name = sheet.replace('_rates', '')
        df = pd.read_excel(excel_file, sheet_name=sheet)

        # Extract curve data
        curve_data = {}
        for _, row in df.iterrows():
            curve_name = row.iloc[0]
            if pd.isna(curve_name) or not isinstance(curve_name, str):
                continue

            all_curves.add(curve_name)

            # Extract shocks for all tenors
            shocks = {}
            for i, tenor in enumerate(tenors, start=1):  # Start at 1 to skip first column (curve name)
                try:
                    shock_value = row.iloc[i]
                    if not pd.isna(shock_value):
                        shocks[tenor] = float(shock_value)
                except (IndexError, ValueError):
                    pass

            curve_data[curve_name] = shocks

        scenarios[scenario_name] = curve_data

    return {
        "asset_class": "Rates",
        "description": "Interest rate curve shocks in basis points across all tenors",
        "tenors": tenors,
        "total_curves": len(all_curves),
        "all_curve_names": sorted(list(all_curves)),
        "scenarios": scenarios
    }

def extract_fx_data(excel_file: Path) -> Dict[str, Any]:
    """Extract FX shock data from all scenarios."""
    xls = pd.ExcelFile(excel_file)

    # Get all FX sheets
    fx_sheets = [s for s in xls.sheet_names if s.endswith('_fx')]

    scenarios = {}
    all_currencies = set()

    for sheet in fx_sheets:
        scenario_name = sheet.replace('_fx', '')
        df = pd.read_excel(excel_file, sheet_name=sheet)

        # Extract FX data
        fx_data = {}
        for _, row in df.iterrows():
            currency = row.iloc[0]
            if pd.isna(currency) or not isinstance(currency, str):
                continue

            all_currencies.add(currency)

            try:
                shock_value = row.iloc[1]  # "(change in value of 1 USD)" column
                if not pd.isna(shock_value):
                    fx_data[currency] = float(shock_value)
            except (IndexError, ValueError):
                pass

        scenarios[scenario_name] = fx_data

    return {
        "asset_class": "FX",
        "description": "FX shock as change in value of 1 USD (decimal format, e.g., 0.14 = 14% depreciation)",
        "total_currencies": len(all_currencies),
        "all_currencies": sorted(list(all_currencies)),
        "scenarios": scenarios
    }

def extract_credit_data() -> Dict[str, Any]:
    """
    Extract credit spread shock data from policy documents.
    Based on the Word document analysis showing sector/region beta factors.
    """
    # From the "Commodity price collapse with Global double dip" document
    credit_data = {
        "asset_class": "Credit Trading",
        "description": "Credit spread relative moves by sector and region with beta multipliers",
        "regions": [
            "Europe",
            "Emerging Europe",
            "North America",
            "South America",
            "Central America",
            "Offshore",
            "Middle East and North Africa",
            "Africa Sub Sahara",
            "Emerging Asia",
            "Australasia and Low Risk Asia"
        ],
        "sectors": [
            "Materials",
            "Energy",
            "Oil & Gas",
            "Utilities",
            "Health Care",
            "Consumer Cyclical",
            "Consumer Goods",
            "Consumer Services",
            "Consumer Stable",
            "Telecommunications",
            "Diversified",
            "Financials",
            "Unclassified"
        ],
        "structure": {
            "description": "Each region has a base credit spread move, multiplied by sector-specific beta",
            "formula": "Total Spread Move = Base Spread Move (%) × Sector Beta"
        },
        "example_scenario": {
            "name": "Commodity Price Collapse & Global Double Dip",
            "region_spreads": {
                "Europe": {"base_spread_move_pct": 45, "sectors": {"Energy": 1.5, "Materials": 1.5, "Financials": 1.0}},
                "Emerging Europe": {"base_spread_move_pct": 75, "sectors": {"Energy": 1.5, "Materials": 1.5, "Financials": 1.0}},
                "North America": {"base_spread_move_pct": 45, "sectors": {"Energy": 1.5, "Materials": 1.5, "Financials": 1.0}},
                "South America": {"base_spread_move_pct": 75, "sectors": {"Energy": 1.5, "Materials": 1.5, "Financials": 1.0}},
                "Africa Sub Sahara": {"base_spread_move_pct": 75, "sectors": {"Energy": 1.5, "Materials": 1.5, "Financials": 1.0}},
                "Emerging Asia": {"base_spread_move_pct": 75, "sectors": {"Energy": 1.5, "Materials": 1.5, "Financials": 1.0}}
            }
        },
        "note": "Specific sector betas vary by scenario. Energy/Materials typically have higher betas (1.5) in commodity-related scenarios."
    }

    return credit_data

def extract_energy_data() -> Dict[str, Any]:
    """Extract energy commodity shock data from policy documents."""
    energy_data = {
        "asset_class": "Energy",
        "description": "Energy commodity shocks as relative price moves and absolute volatility shocks",
        "products": ["WTI", "Brent", "Heavy Distillates", "Medium Distillates", "Light Distillates", "Emissions"],
        "shock_types": {
            "price": "Relative shock (percentage)",
            "volatility": "Absolute shock (percentage points)"
        },
        "example_scenario": {
            "name": "Commodity Price Collapse & Global Double Dip",
            "shocks": {
                "WTI": {"price_shock_pct": -25, "vol_shock_abs": 20},
                "Brent": {"price_shock_pct": -20, "vol_shock_abs": 20},
                "Heavy Distillates": {"price_shock_pct": -25, "vol_shock_abs": 25},
                "Medium Distillates": {"price_shock_pct": -20, "vol_shock_abs": 20},
                "Light Distillates": {"price_shock_pct": -20, "vol_shock_abs": 25},
                "Emissions": {"price_shock_pct": 0, "vol_shock_abs": 0}
            }
        },
        "typical_ranges": {
            "supply_disruption": {"price": "+40% to +80%", "vol": "+20% to +40%"},
            "demand_collapse": {"price": "-30% to -50%", "vol": "+15% to +30%"},
            "normal_stress": {"price": "-20% to +25%", "vol": "+15% to +25%"}
        }
    }

    return energy_data

def extract_precious_metals_data() -> Dict[str, Any]:
    """Extract precious metals shock data from policy documents."""
    pm_data = {
        "asset_class": "Precious Metals",
        "description": "Precious metals shocks: relative price, relative volatility, absolute lease rate (bps)",
        "products": ["Gold", "Silver", "Palladium", "Platinum", "Other"],
        "shock_types": {
            "price": "Relative shock (percentage)",
            "volatility": "Relative shock (percentage) - NOTE: Changed from absolute to relative per 2024 review",
            "lease_rate": "Absolute shock (basis points)"
        },
        "example_scenario": {
            "name": "Commodity Price Collapse & Global Double Dip",
            "shocks": {
                "Gold": {"price_shock_pct": 7, "vol_shock_pct": 60, "lease_rate_bps": -140},
                "Silver": {"price_shock_pct": 14, "vol_shock_pct": 30, "lease_rate_bps": -190},
                "Palladium": {"price_shock_pct": 16, "vol_shock_pct": 30, "lease_rate_bps": -130},
                "Platinum": {"price_shock_pct": 11, "vol_shock_pct": 15, "lease_rate_bps": -140},
                "Other": {"price_shock_pct": 16, "vol_shock_pct": None, "lease_rate_bps": -130}
            }
        },
        "typical_patterns": {
            "safe_haven_bid": {"Gold": "+5% to +15%", "Silver": "+10% to +20%"},
            "industrial_demand_collapse": {"Palladium": "-15% to -25%", "Platinum": "-10% to -20%"},
            "risk_off": {"lease_rates": "-100bps to -200bps (lower cost of carry)"}
        },
        "historical_note": "Vol shocks changed from Absolute to Relative in annual review per Murex migration"
    }

    return pm_data

def extract_base_metals_data() -> Dict[str, Any]:
    """Extract base metals shock data from policy documents."""
    bm_data = {
        "asset_class": "Base Metals",
        "description": "Base metals shocks: relative price and absolute volatility",
        "products": ["Aluminium", "Copper", "Nickel", "Lead", "Zinc", "Tin", "Other", "Iron Ore"],
        "shock_types": {
            "price": "Relative shock (percentage)",
            "volatility": "Absolute shock (percentage points)"
        },
        "example_scenario": {
            "name": "Commodity Price Collapse & Global Double Dip",
            "shocks": {
                "Aluminium": {"price_shock_pct": -15, "vol_shock_abs": 10},
                "Copper": {"price_shock_pct": -20, "vol_shock_abs": 25},
                "Nickel": {"price_shock_pct": -20, "vol_shock_abs": 25},
                "Lead": {"price_shock_pct": -25, "vol_shock_abs": 15},
                "Zinc": {"price_shock_pct": -20, "vol_shock_abs": 20},
                "Tin": {"price_shock_pct": -20, "vol_shock_abs": 20},
                "Other": {"price_shock_pct": -25, "vol_shock_abs": 25},
                "Iron Ore": {"price_shock_pct": -20, "vol_shock_abs": 15, "note": "Removed from scenarios - desk no longer trades"}
            }
        },
        "typical_patterns": {
            "recession": {"price": "-20% to -30%", "vol": "+15% to +30%"},
            "supply_disruption": {"price": "+25% to +50%", "vol": "+20% to +35%"},
            "china_slowdown": {"Copper": "-25% to -35%", "Iron Ore": "-30% to -40%"}
        },
        "ongoing_projects": {
            "murex_migration": {
                "description": "Base Metals moving to Murex will enable term structure shocks and vol surface granularity",
                "target": "2025",
                "enhancements": [
                    "Tenor-specific shocks to capture calendar spread stress",
                    "Volatility surface shocks (vs current parallel shocks)",
                    "Explicit Cobalt shock (currently falls under 'Other')"
                ]
            }
        }
    }

    return bm_data

def build_complete_library():
    """Build the complete risk factor shock library."""
    print("Building comprehensive risk factor shock library...")
    print(f"Reading from: {EXCEL_FILE}")

    # Extract data from all sources
    print("\n1. Extracting Rates data from Excel...")
    rates_data = extract_rates_data(EXCEL_FILE)
    print(f"   ✓ Extracted {rates_data['total_curves']} rate curves across {len(rates_data['scenarios'])} scenarios")

    print("\n2. Extracting FX data from Excel...")
    fx_data = extract_fx_data(EXCEL_FILE)
    print(f"   ✓ Extracted {fx_data['total_currencies']} currencies across {len(fx_data['scenarios'])} scenarios")

    print("\n3. Extracting Credit data from policy documents...")
    credit_data = extract_credit_data()
    print(f"   ✓ Extracted {len(credit_data['regions'])} regions × {len(credit_data['sectors'])} sectors")

    print("\n4. Extracting Energy data from policy documents...")
    energy_data = extract_energy_data()
    print(f"   ✓ Extracted {len(energy_data['products'])} energy products")

    print("\n5. Extracting Precious Metals data from policy documents...")
    pm_data = extract_precious_metals_data()
    print(f"   ✓ Extracted {len(pm_data['products'])} precious metals")

    print("\n6. Extracting Base Metals data from policy documents...")
    bm_data = extract_base_metals_data()
    print(f"   ✓ Extracted {len(bm_data['products'])} base metals")

    # Build complete library structure
    library = {
        "metadata": {
            "version": "1.0",
            "source": "Example Bank Market Risk Stress Testing Framework",
            "last_updated": "2025-01-12",
            "description": "Comprehensive risk factor shock library for pillar stress scenario generation",
            "total_scenarios": len(rates_data['scenarios']),
            "scenario_names": list(rates_data['scenarios'].keys())
        },
        "asset_classes": {
            "rates": rates_data,
            "fx": fx_data,
            "credit": credit_data,
            "energy": energy_data,
            "precious_metals": pm_data,
            "base_metals": bm_data
        }
    }

    # Save to JSON file
    output_file = OUTPUT_DIR / "risk_factor_shocks_library.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(library, f, indent=2)

    print(f"\n✅ Complete library saved to: {output_file}")
    print(f"\nLibrary Summary:")
    print(f"  - Rates: {rates_data['total_curves']} curves")
    print(f"  - FX: {fx_data['total_currencies']} currencies")
    print(f"  - Credit: {len(credit_data['regions'])} regions × {len(credit_data['sectors'])} sectors")
    print(f"  - Energy: {len(energy_data['products'])} products")
    print(f"  - Precious Metals: {len(pm_data['products'])} products")
    print(f"  - Base Metals: {len(bm_data['products'])} products")
    print(f"  - Total Scenarios: {len(rates_data['scenarios'])}")

    return library

if __name__ == "__main__":
    library = build_complete_library()
    print("\n✅ Risk factor library build complete!")
