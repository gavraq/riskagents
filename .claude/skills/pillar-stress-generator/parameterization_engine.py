"""
Parameterization Engine

Suggests risk factor shocks based on scenario narratives, historical precedents,
and typical correlation patterns.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class ScenarioType(Enum):
    """Types of stress scenarios."""
    RECESSION = "recession"
    INFLATION_SHOCK = "inflation_shock"
    SUPPLY_DISRUPTION = "supply_disruption"
    GEOPOLITICAL = "geopolitical"
    FINANCIAL_CRISIS = "financial_crisis"
    POLICY_ERROR = "policy_error"
    CHINA_SLOWDOWN = "china_slowdown"
    SOVEREIGN_CRISIS = "sovereign_crisis"
    PANDEMIC = "pandemic"
    CLIMATE = "climate"

class Severity(Enum):
    """Scenario severity levels."""
    MODERATE = "moderate"  # 60% of historical max
    SEVERE = "severe"      # 100% of historical max (target)
    EXTREME = "extreme"    # 150% of historical max

@dataclass
class RiskFactorShock:
    """A single risk factor shock."""
    factor_name: str
    asset_class: str
    shock_value: float
    shock_unit: str  # "pct", "bps", "absolute"
    rationale: str
    historical_analogue: Optional[str] = None
    confidence: str = "medium"  # "high", "medium", "low"

class ParameterizationEngine:
    """
    Engine for generating risk factor shock suggestions based on scenario characteristics.
    """

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.risk_factor_library = self._load_risk_factor_library()
        self.historical_crises = self._load_historical_crises()

    def _load_risk_factor_library(self) -> Dict:
        """Load the comprehensive risk factor library."""
        library_path = self.data_dir / "risk_factor_shocks_library.json"
        with open(library_path, 'r') as f:
            return json.load(f)

    def _load_historical_crises(self) -> Dict:
        """Load historical crisis database."""
        crises_path = self.data_dir / "historical_crises.json"
        with open(crises_path, 'r') as f:
            return json.load(f)

    def suggest_scenario_shocks(
        self,
        scenario_type: ScenarioType,
        severity: Severity,
        primary_geography: str,  # "global", "EUR", "US", "EM_Asia", etc.
        narrative_elements: List[str],
        custom_adjustments: Optional[Dict] = None
    ) -> Dict[str, List[RiskFactorShock]]:
        """
        Generate comprehensive risk factor shock suggestions for a scenario.

        Args:
            scenario_type: Type of scenario
            severity: Severity level
            primary_geography: Main geographic focus
            narrative_elements: Key narrative elements (e.g., ["oil_supply_shock", "inflation_spike"])
            custom_adjustments: Optional manual adjustments to default shocks

        Returns:
            Dictionary mapping asset classes to lists of risk factor shocks
        """
        shocks = {}

        # Get base template based on scenario type
        template = self._get_scenario_template(scenario_type)

        # Apply severity scaling
        scaled_template = self._scale_by_severity(template, severity)

        # Apply geographic focus
        geo_adjusted = self._apply_geographic_focus(scaled_template, primary_geography)

        # Apply narrative-specific adjustments
        for element in narrative_elements:
            geo_adjusted = self._apply_narrative_adjustment(geo_adjusted, element)

        # Apply custom adjustments if provided
        if custom_adjustments:
            geo_adjusted = self._apply_custom_adjustments(geo_adjusted, custom_adjustments)

        # Convert to RiskFactorShock objects with rationale
        shocks = self._create_shock_objects(geo_adjusted, scenario_type, severity)

        return shocks

    def _get_scenario_template(self, scenario_type: ScenarioType) -> Dict:
        """Get base shock template for scenario type."""
        templates = {
            ScenarioType.RECESSION: {
                "description": "Global or regional recession scenario",
                "equities": {"global": -25, "DM": -20, "EM": -30},
                "credit_spreads": {"IG": 120, "HY": 400},
                "rates_DM": -100,  # bps (flight to quality)
                "rates_EM": 200,   # bps (risk premium)
                "USD": 10,  # % strength
                "EM_FX": -15,  # % depreciation
                "oil": -25,  # % (demand destruction)
                "base_metals": -20,  # %
                "gold": 5,  # % (safe haven)
                "correlation_pattern": "risk_off"
            },

            ScenarioType.INFLATION_SHOCK: {
                "description": "Inflation surprise scenario",
                "equities": {"global": -15, "DM": -12, "EM": -18},
                "credit_spreads": {"IG": 80, "HY": 250},
                "rates_DM": 150,  # bps (CB tightening)
                "rates_EM": 250,  # bps
                "USD": 5,  # % (rate advantage)
                "EM_FX": -10,  # %
                "oil": 20,  # % (inflation component)
                "base_metals": 10,  # %
                "gold": 8,  # % (inflation hedge)
                "correlation_pattern": "inflation_shock"
            },

            ScenarioType.SUPPLY_DISRUPTION: {
                "description": "Commodity supply disruption (geopolitical)",
                "equities": {"global": -15, "affected_region": -25},
                "credit_spreads": {"IG": 60, "HY": 180},
                "rates_DM": 50,  # bps (inflation concerns)
                "rates_EM": 150,  # bps
                "affected_commodity": 50,  # % (supply cut)
                "related_commodities": 15,  # %
                "consumer_equities": -20,  # % (margin pressure)
                "correlation_pattern": "supply_disruption"
            },

            ScenarioType.FINANCIAL_CRISIS: {
                "description": "Systemic financial crisis (2008-style)",
                "equities": {"global": -35, "DM": -30, "EM": -45},
                "credit_spreads": {"IG": 300, "HY": 1000},
                "rates_DM": -150,  # bps (aggressive easing)
                "rates_EM": 250,  # bps (credit freeze)
                "USD": 15,  # % (flight to safety)
                "EM_FX": -25,  # %
                "oil": -40,  # % (demand collapse)
                "base_metals": -30,  # %
                "gold": 10,  # % (safe haven)
                "volatility": {"VIX": 70, "FX_vol": 20},
                "correlation_pattern": "risk_off"
            },

            ScenarioType.CHINA_SLOWDOWN: {
                "description": "China hard landing scenario",
                "equities": {"China": -30, "EM_Asia": -20, "global": -15},
                "credit_spreads": {"China_HY": 600, "EM_Asia_IG": 180, "EM_Asia_HY": 450},
                "rates_DM": -50,  # bps (global growth concerns)
                "CNY": 8,  # % depreciation
                "EM_Asia_FX": -12,  # %
                "oil": -20,  # % (China demand)
                "copper": -25,  # %
                "iron_ore": -35,  # %
                "base_metals": -20,  # %
                "correlation_pattern": "recession"
            },

            ScenarioType.GEOPOLITICAL: {
                "description": "Geopolitical crisis / conflict",
                "equities": {"affected_region": -25, "global": -12},
                "credit_spreads": {"affected_region": 250, "global_IG": 60},
                "rates_DM": -25,  # bps (safe haven)
                "affected_region_FX": -20,  # %
                "oil": 30,  # % (risk premium)
                "gold": 12,  # % (safe haven)
                "defense_equities": 15,  # % (sector specific)
                "correlation_pattern": "supply_disruption"
            }
        }

        return templates.get(scenario_type, templates[ScenarioType.RECESSION])

    def _scale_by_severity(self, template: Dict, severity: Severity) -> Dict:
        """Scale shock magnitudes by severity level."""
        scaling_factors = {
            Severity.MODERATE: 0.6,
            Severity.SEVERE: 1.0,
            Severity.EXTREME: 1.5
        }

        factor = scaling_factors[severity]
        scaled = template.copy()

        # Scale all numeric values
        for key, value in template.items():
            if isinstance(value, (int, float)):
                scaled[key] = value * factor
            elif isinstance(value, dict):
                scaled[key] = {k: v * factor if isinstance(v, (int, float)) else v
                              for k, v in value.items()}

        return scaled

    def _apply_geographic_focus(self, template: Dict, geography: str) -> Dict:
        """Apply geographic-specific adjustments."""
        # This would contain logic to adjust shocks based on primary geography
        # For now, return template as-is
        return template

    def _apply_narrative_adjustment(self, template: Dict, element: str) -> Dict:
        """Apply adjustments based on specific narrative elements."""
        adjustments = {
            "oil_supply_shock": {
                "oil": 1.5,  # 50% increase to oil shock
                "gas": 1.8,  # 80% increase to gas shock
                "inflation_expectations": 1.3
            },
            "policy_error": {
                "rates_DM": 1.2,  # Rates move more in policy error
                "credit_spreads": 1.3,  # Credit stress amplified
                "curve_inversion": True
            },
            "banking_stress": {
                "financials_credit": 2.0,  # Double credit spread for financials
                "deposit_flight": True
            }
        }

        if element in adjustments:
            adj = adjustments[element]
            for key, multiplier in adj.items():
                if isinstance(multiplier, (int, float)) and key in template:
                    if isinstance(template[key], (int, float)):
                        template[key] *= multiplier

        return template

    def _apply_custom_adjustments(self, template: Dict, custom: Dict) -> Dict:
        """Apply user-specified custom adjustments."""
        for key, value in custom.items():
            template[key] = value
        return template

    def _create_shock_objects(
        self,
        template: Dict,
        scenario_type: ScenarioType,
        severity: Severity
    ) -> Dict[str, List[RiskFactorShock]]:
        """Convert template to structured RiskFactorShock objects."""
        shocks_by_asset_class = {
            "rates": [],
            "fx": [],
            "credit": [],
            "energy": [],
            "precious_metals": [],
            "base_metals": []
        }

        # This is a simplified version - full implementation would map all template
        # values to specific risk factors with detailed rationale

        # Example for equities/credit
        if "credit_spreads" in template:
            cs = template["credit_spreads"]
            if "IG" in cs:
                shocks_by_asset_class["credit"].append(
                    RiskFactorShock(
                        factor_name="IG_Credit_Spreads",
                        asset_class="credit",
                        shock_value=cs["IG"],
                        shock_unit="bps",
                        rationale=f"{scenario_type.value} scenario: Investment grade spreads widen due to credit risk repricing",
                        historical_analogue=self._get_historical_analogue(scenario_type),
                        confidence="high"
                    )
                )

        return shocks_by_asset_class

    def _get_historical_analogue(self, scenario_type: ScenarioType) -> str:
        """Get relevant historical crisis for this scenario type."""
        analogues = {
            ScenarioType.RECESSION: "2008 Global Financial Crisis",
            ScenarioType.INFLATION_SHOCK: "2022 Ukraine War (stagflation)",
            ScenarioType.SUPPLY_DISRUPTION: "2022 Ukraine War",
            ScenarioType.FINANCIAL_CRISIS: "2008 Global Financial Crisis",
            ScenarioType.CHINA_SLOWDOWN: "2015-2016 China Slowdown",
            ScenarioType.GEOPOLITICAL: "2022 Ukraine War"
        }
        return analogues.get(scenario_type, "Historical precedent")

    def get_historical_crisis_data(self, crisis_id: str) -> Optional[Dict]:
        """Retrieve detailed data for a specific historical crisis."""
        for crisis in self.historical_crises.get("crises", []):
            if crisis["id"] == crisis_id:
                return crisis
        return None

    def calibrate_to_historical(
        self,
        target_scenario_type: ScenarioType,
        severity: Severity
    ) -> Dict:
        """
        Calibrate scenario shocks to historical crisis precedents.

        Returns detailed shock specifications with historical justification.
        """
        # Find relevant historical crisis
        crisis_mapping = {
            ScenarioType.FINANCIAL_CRISIS: "financial_crisis_2008",
            ScenarioType.INFLATION_SHOCK: "ukraine_war_2022",
            ScenarioType.CHINA_SLOWDOWN: "china_slowdown_2015",
            ScenarioType.GEOPOLITICAL: "ukraine_war_2022"
        }

        crisis_id = crisis_mapping.get(target_scenario_type)
        if not crisis_id:
            return {}

        crisis_data = self.get_historical_crisis_data(crisis_id)
        if not crisis_data:
            return {}

        # Extract risk factors and scale by severity
        severity_multiplier = {
            Severity.MODERATE: 0.6,
            Severity.SEVERE: 1.0,
            Severity.EXTREME: 1.5
        }[severity]

        calibrated = {
            "historical_reference": crisis_data["name"],
            "period": crisis_data["period"],
            "severity_calibration": severity.value,
            "shocks": {}
        }

        # Extract and scale risk factors
        if "risk_factors" in crisis_data:
            calibrated["shocks"] = self._scale_historical_shocks(
                crisis_data["risk_factors"],
                severity_multiplier
            )

        return calibrated

    def _scale_historical_shocks(self, risk_factors: Dict, multiplier: float) -> Dict:
        """Scale historical shock magnitudes by severity multiplier."""
        scaled = {}

        for asset_class, factors in risk_factors.items():
            scaled[asset_class] = {}
            for factor, data in factors.items():
                if isinstance(data, dict):
                    scaled[asset_class][factor] = {}
                    for key, value in data.items():
                        if isinstance(value, (int, float)) and "pct" in key or "bps" in key:
                            scaled[asset_class][factor][key] = value * multiplier
                        else:
                            scaled[asset_class][factor][key] = value
                else:
                    scaled[asset_class][factor] = data

        return scaled
