"""
Pillar Stress Scenario Generator Skill

Generates and reviews top-down pillar stress scenarios for market risk management.
Supports new scenario creation and annual reviews with MLRC-ready documentation.
"""

__version__ = "1.0.0"
__author__ = "Risk Agent Platform"

from pathlib import Path

# Skill directory structure
SKILL_DIR = Path(__file__).parent
DATA_DIR = SKILL_DIR / "data"
RISK_FACTOR_LIBRARY = DATA_DIR / "risk_factor_shocks_library.json"
HISTORICAL_CRISES = DATA_DIR / "historical_crises.json"
EXISTING_SCENARIOS_DIR = DATA_DIR / "existing_scenarios"
