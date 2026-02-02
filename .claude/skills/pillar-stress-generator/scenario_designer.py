"""
Scenario Designer

Creates new pillar stress scenarios with economic narratives, risk factor parameterization,
and validation. Produces structured output for MLRC documentation.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

from parameterization_engine import (
    ParameterizationEngine,
    ScenarioType,
    Severity,
    RiskFactorShock
)
from validators import ScenarioValidator, ValidationResult

@dataclass
class ScenarioMetadata:
    """Metadata for a stress scenario."""
    scenario_id: str
    scenario_name: str
    created_date: str
    created_by: str
    version: str
    scenario_type: str
    severity: str
    primary_geography: str
    status: str  # "draft", "consultation", "mlrc_approved"

@dataclass
class EconomicNarrative:
    """Economic narrative for the scenario."""
    trigger_event: str
    transmission_channels: List[str]
    timeline: Dict[str, str]  # {"onset": "Q1 2025", "peak": "Q2 2025", "recovery": "Q4 2025"}
    key_assumptions: List[str]
    probability_assessment: str  # "plausible", "unlikely_but_possible", "tail_risk"
    narrative_text: str

@dataclass
class AssetClassShocks:
    """Shocks for a specific asset class."""
    asset_class: str
    description: str
    shocks: Dict[str, Any]  # Flexible structure for different asset classes
    rationale: str
    historical_analogue: Optional[str] = None

@dataclass
class StressScenario:
    """Complete stress scenario specification."""
    metadata: ScenarioMetadata
    narrative: EconomicNarrative
    asset_class_shocks: List[AssetClassShocks]
    validation_results: List[ValidationResult]
    confidence_score: float  # 0-100
    consultation_prompts: Dict[str, List[str]]  # For Front Office consultation
    next_steps: List[str]

class ScenarioDesigner:
    """
    Orchestrates the creation of new pillar stress scenarios.
    """

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.param_engine = ParameterizationEngine(data_dir)
        self.validator = ScenarioValidator()
        self.risk_factor_library = self._load_risk_factor_library()

    def _load_risk_factor_library(self) -> Dict:
        """Load risk factor library."""
        with open(self.data_dir / "risk_factor_shocks_library.json", 'r') as f:
            return json.load(f)

    def create_scenario(
        self,
        scenario_name: str,
        trigger_event: str,
        scenario_type: ScenarioType,
        severity: Severity,
        primary_geography: str,
        narrative_elements: List[str],
        transmission_channels: List[str],
        key_assumptions: List[str],
        timeline: Optional[Dict[str, str]] = None,
        created_by: str = "Market Risk",
        custom_shocks: Optional[Dict] = None
    ) -> StressScenario:
        """
        Create a complete stress scenario.

        Args:
            scenario_name: Name of the scenario
            trigger_event: What triggers the stress
            scenario_type: Type of scenario (recession, inflation shock, etc.)
            severity: Severity level (moderate, severe, extreme)
            primary_geography: Main geographic focus
            narrative_elements: Key narrative components
            transmission_channels: How shock transmits through markets
            key_assumptions: Critical assumptions underlying scenario
            timeline: Event timeline (onset, peak, recovery)
            created_by: Scenario creator
            custom_shocks: Optional manual shock adjustments

        Returns:
            Complete StressScenario object ready for MLRC documentation
        """
        # Generate scenario ID
        scenario_id = self._generate_scenario_id(scenario_name)

        # Create metadata
        metadata = ScenarioMetadata(
            scenario_id=scenario_id,
            scenario_name=scenario_name,
            created_date=datetime.now().strftime("%Y-%m-%d"),
            created_by=created_by,
            version="1.0",
            scenario_type=scenario_type.value,
            severity=severity.value,
            primary_geography=primary_geography,
            status="draft"
        )

        # Generate economic narrative
        narrative_text = self._generate_narrative_text(
            trigger_event=trigger_event,
            scenario_type=scenario_type,
            severity=severity,
            transmission_channels=transmission_channels,
            timeline=timeline or {}
        )

        narrative = EconomicNarrative(
            trigger_event=trigger_event,
            transmission_channels=transmission_channels,
            timeline=timeline or {
                "onset": "Immediate",
                "peak": "1-3 months",
                "recovery": "6-12 months"
            },
            key_assumptions=key_assumptions,
            probability_assessment=self._assess_probability(scenario_type, severity),
            narrative_text=narrative_text
        )

        # Generate risk factor shocks using parameterization engine
        shock_suggestions = self.param_engine.suggest_scenario_shocks(
            scenario_type=scenario_type,
            severity=severity,
            primary_geography=primary_geography,
            narrative_elements=narrative_elements,
            custom_adjustments=custom_shocks
        )

        # Convert to AssetClassShocks objects with detailed specifications
        asset_class_shocks = self._build_asset_class_shocks(
            shock_suggestions=shock_suggestions,
            scenario_type=scenario_type,
            severity=severity
        )

        # Validate scenario
        validation_results = self._validate_scenario(
            asset_class_shocks=asset_class_shocks,
            scenario_type=scenario_type.value,
            severity=severity.value
        )

        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(
            scenario_type=scenario_type,
            severity=severity,
            validation_results=validation_results
        )

        # Generate Front Office consultation prompts
        consultation_prompts = self._generate_consultation_prompts(
            scenario_name=scenario_name,
            asset_class_shocks=asset_class_shocks,
            scenario_type=scenario_type
        )

        # Determine next steps
        next_steps = self._determine_next_steps(
            validation_results=validation_results,
            confidence_score=confidence_score
        )

        # Assemble complete scenario
        scenario = StressScenario(
            metadata=metadata,
            narrative=narrative,
            asset_class_shocks=asset_class_shocks,
            validation_results=validation_results,
            confidence_score=confidence_score,
            consultation_prompts=consultation_prompts,
            next_steps=next_steps
        )

        return scenario

    def _generate_scenario_id(self, scenario_name: str) -> str:
        """Generate unique scenario ID."""
        # Convert name to ID format: "US Recession 2025" -> "us_recession_2025"
        scenario_id = scenario_name.lower().replace(" ", "_").replace("-", "_")
        # Add timestamp for uniqueness
        timestamp = datetime.now().strftime("%Y%m%d")
        return f"{scenario_id}_{timestamp}"

    def _generate_narrative_text(
        self,
        trigger_event: str,
        scenario_type: ScenarioType,
        severity: Severity,
        transmission_channels: List[str],
        timeline: Dict[str, str]
    ) -> str:
        """Generate comprehensive narrative text."""
        severity_desc = {
            Severity.MODERATE: "moderate stress",
            Severity.SEVERE: "severe stress",
            Severity.EXTREME: "extreme stress"
        }

        narrative_parts = [
            f"**Trigger Event**: {trigger_event}",
            "",
            f"**Scenario Type**: {scenario_type.value.replace('_', ' ').title()}",
            f"**Severity**: {severity_desc[severity].title()}",
            "",
            "**Transmission Channels**:"
        ]

        for i, channel in enumerate(transmission_channels, 1):
            narrative_parts.append(f"{i}. {channel}")

        narrative_parts.extend([
            "",
            "**Timeline**:"
        ])

        for phase, description in timeline.items():
            narrative_parts.append(f"- **{phase.title()}**: {description}")

        return "\n".join(narrative_parts)

    def _assess_probability(self, scenario_type: ScenarioType, severity: Severity) -> str:
        """Assess probability class for scenario."""
        # Moderate scenarios are more plausible
        if severity == Severity.MODERATE:
            return "plausible"
        elif severity == Severity.SEVERE:
            return "unlikely_but_possible"
        else:  # EXTREME
            return "tail_risk"

    def _build_asset_class_shocks(
        self,
        shock_suggestions: Dict[str, List[RiskFactorShock]],
        scenario_type: ScenarioType,
        severity: Severity
    ) -> List[AssetClassShocks]:
        """Build detailed asset class shock specifications."""
        asset_class_shocks = []

        # Get calibration to historical crisis
        historical_calibration = self.param_engine.calibrate_to_historical(
            target_scenario_type=scenario_type,
            severity=severity
        )

        historical_ref = historical_calibration.get("historical_reference", "Historical precedent")

        # Rates & FX
        rates_fx_shocks = self._build_rates_fx_shocks(scenario_type, severity, historical_ref)
        if rates_fx_shocks:
            asset_class_shocks.append(rates_fx_shocks)

        # Credit
        credit_shocks = self._build_credit_shocks(scenario_type, severity, historical_ref)
        if credit_shocks:
            asset_class_shocks.append(credit_shocks)

        # Energy
        energy_shocks = self._build_energy_shocks(scenario_type, severity, historical_ref)
        if energy_shocks:
            asset_class_shocks.append(energy_shocks)

        # Precious Metals
        pm_shocks = self._build_precious_metals_shocks(scenario_type, severity, historical_ref)
        if pm_shocks:
            asset_class_shocks.append(pm_shocks)

        # Base Metals
        bm_shocks = self._build_base_metals_shocks(scenario_type, severity, historical_ref)
        if bm_shocks:
            asset_class_shocks.append(bm_shocks)

        return asset_class_shocks

    def _build_rates_fx_shocks(
        self,
        scenario_type: ScenarioType,
        severity: Severity,
        historical_ref: str
    ) -> AssetClassShocks:
        """Build Rates & FX shock specifications."""
        # Get typical shocks from templates
        template = self.param_engine._get_scenario_template(scenario_type)
        scaled = self.param_engine._scale_by_severity(template, severity)

        # Build region-specific shocks
        regions = ["China", "Europe", "Emerging Europe", "North America", "EM Asia", "Africa Sub Sahara"]
        tenors = ["3M", "2Y", "10Y"]  # Simplified for initial version

        shocks_data = {
            "regions": {},
            "fx_moves": {}
        }

        # Rates shocks by region
        for region in regions:
            shocks_data["regions"][region] = {
                tenor: scaled.get(f"rates_{'DM' if region in ['Europe', 'North America'] else 'EM'}", 0)
                for tenor in tenors
            }

        # FX shocks
        if "USD" in scaled:
            shocks_data["fx_moves"]["USD_Index"] = scaled["USD"]
        if "EM_FX" in scaled:
            shocks_data["fx_moves"]["EM_FX_Avg"] = scaled["EM_FX"]

        rationale = self._generate_rates_rationale(scenario_type, severity)

        return AssetClassShocks(
            asset_class="Rates & FX",
            description="Interest rate curve shocks (bps) and FX movements (% change in value of 1 USD)",
            shocks=shocks_data,
            rationale=rationale,
            historical_analogue=historical_ref
        )

    def _build_credit_shocks(
        self,
        scenario_type: ScenarioType,
        severity: Severity,
        historical_ref: str
    ) -> AssetClassShocks:
        """Build Credit spread shock specifications."""
        template = self.param_engine._get_scenario_template(scenario_type)
        scaled = self.param_engine._scale_by_severity(template, severity)

        # Get credit shock template from library
        credit_data = self.risk_factor_library["asset_classes"]["credit"]

        shocks_data = {
            "base_spreads": {},
            "sector_betas": credit_data["example_scenario"]["region_spreads"]
        }

        # Base spread moves by region
        if "credit_spreads" in scaled:
            for grade, spread_bps in scaled["credit_spreads"].items():
                shocks_data["base_spreads"][grade] = spread_bps

        rationale = self._generate_credit_rationale(scenario_type, severity)

        return AssetClassShocks(
            asset_class="Credit Trading",
            description="Credit spread relative moves by sector and region with beta multipliers",
            shocks=shocks_data,
            rationale=rationale,
            historical_analogue=historical_ref
        )

    def _build_energy_shocks(
        self,
        scenario_type: ScenarioType,
        severity: Severity,
        historical_ref: str
    ) -> AssetClassShocks:
        """Build Energy commodity shock specifications."""
        template = self.param_engine._get_scenario_template(scenario_type)
        scaled = self.param_engine._scale_by_severity(template, severity)

        energy_data = self.risk_factor_library["asset_classes"]["energy"]

        shocks_data = {}

        # Oil shocks
        if "oil" in scaled:
            shocks_data["WTI"] = {
                "price_shock_pct": scaled["oil"],
                "vol_shock_abs": 20 if abs(scaled["oil"]) > 20 else 15
            }
            shocks_data["Brent"] = {
                "price_shock_pct": scaled["oil"] * 0.9,  # Brent slightly less than WTI
                "vol_shock_abs": 20 if abs(scaled["oil"]) > 20 else 15
            }

        # Distillates follow oil
        for product in ["Heavy Distillates", "Medium Distillates", "Light Distillates"]:
            if "oil" in scaled:
                shocks_data[product] = {
                    "price_shock_pct": scaled["oil"],
                    "vol_shock_abs": 20
                }

        rationale = self._generate_energy_rationale(scenario_type, severity)

        return AssetClassShocks(
            asset_class="Energy",
            description="Energy commodity shocks as relative price moves and absolute volatility shocks",
            shocks=shocks_data,
            rationale=rationale,
            historical_analogue=historical_ref
        )

    def _build_precious_metals_shocks(
        self,
        scenario_type: ScenarioType,
        severity: Severity,
        historical_ref: str
    ) -> AssetClassShocks:
        """Build Precious Metals shock specifications."""
        template = self.param_engine._get_scenario_template(scenario_type)
        scaled = self.param_engine._scale_by_severity(template, severity)

        shocks_data = {}

        # Gold - safe haven in risk-off
        if "gold" in scaled:
            shocks_data["Gold"] = {
                "price_shock_pct": scaled["gold"],
                "vol_shock_pct": 60 if scaled["gold"] > 0 else 30,
                "lease_rate_bps": -140 if scaled["gold"] > 0 else -50
            }

        # Silver follows gold but more volatile
        if "gold" in scaled:
            shocks_data["Silver"] = {
                "price_shock_pct": scaled["gold"] * 1.5,
                "vol_shock_pct": 30,
                "lease_rate_bps": -190 if scaled["gold"] > 0 else -80
            }

        # Industrial PMs (Platinum, Palladium) - follow broader recession/growth
        if "base_metals" in scaled:
            shocks_data["Platinum"] = {
                "price_shock_pct": scaled["base_metals"] * 0.6,
                "vol_shock_pct": 15,
                "lease_rate_bps": -140
            }
            shocks_data["Palladium"] = {
                "price_shock_pct": scaled["base_metals"] * 0.8,
                "vol_shock_pct": 30,
                "lease_rate_bps": -130
            }

        rationale = self._generate_pm_rationale(scenario_type, severity)

        return AssetClassShocks(
            asset_class="Precious Metals",
            description="Precious metals shocks: relative price, relative volatility, absolute lease rate (bps)",
            shocks=shocks_data,
            rationale=rationale,
            historical_analogue=historical_ref
        )

    def _build_base_metals_shocks(
        self,
        scenario_type: ScenarioType,
        severity: Severity,
        historical_ref: str
    ) -> AssetClassShocks:
        """Build Base Metals shock specifications."""
        template = self.param_engine._get_scenario_template(scenario_type)
        scaled = self.param_engine._scale_by_severity(template, severity)

        shocks_data = {}

        # Default base metals shock
        base_shock = scaled.get("base_metals", -20)

        # Copper - bellwether for global growth
        copper_shock = scaled.get("copper", base_shock)
        shocks_data["Copper"] = {
            "price_shock_pct": copper_shock,
            "vol_shock_abs": 25
        }

        # Aluminium
        shocks_data["Aluminium"] = {
            "price_shock_pct": base_shock * 0.75,
            "vol_shock_abs": 10
        }

        # Nickel
        shocks_data["Nickel"] = {
            "price_shock_pct": base_shock,
            "vol_shock_abs": 25
        }

        # Zinc, Lead
        for metal in ["Zinc", "Lead", "Tin"]:
            shocks_data[metal] = {
                "price_shock_pct": base_shock,
                "vol_shock_abs": 20
            }

        rationale = self._generate_bm_rationale(scenario_type, severity)

        return AssetClassShocks(
            asset_class="Base Metals",
            description="Base metals shocks: relative price and absolute volatility",
            shocks=shocks_data,
            rationale=rationale,
            historical_analogue=historical_ref
        )

    def _generate_rates_rationale(self, scenario_type: ScenarioType, severity: Severity) -> str:
        """Generate rationale for rates & FX shocks."""
        rationales = {
            ScenarioType.RECESSION: "Flight to quality drives DM rates down; EM rates up on risk premium. USD strengthens as safe haven.",
            ScenarioType.INFLATION_SHOCK: "Central banks tighten aggressively; rates rise across all regions. USD benefits from rate advantage.",
            ScenarioType.GEOPOLITICAL: "Risk-off flows into DM government bonds; affected region rates spike. Flight to USD and CHF."
        }
        return rationales.get(scenario_type, "Rate movements calibrated to scenario type and severity.")

    def _generate_credit_rationale(self, scenario_type: ScenarioType, severity: Severity) -> str:
        """Generate rationale for credit shocks."""
        return f"{scenario_type.value.replace('_', ' ').title()} scenario drives credit risk repricing. Spreads widen due to default risk and liquidity premium. High yield particularly affected. Cyclical sectors (Energy, Materials) see elevated betas."

    def _generate_energy_rationale(self, scenario_type: ScenarioType, severity: Severity) -> str:
        """Generate rationale for energy shocks."""
        if scenario_type == ScenarioType.SUPPLY_DISRUPTION:
            return "Supply disruption from geopolitical event drives oil prices sharply higher. Volatility spikes as market reprices supply risk."
        elif scenario_type == ScenarioType.RECESSION:
            return "Demand destruction from economic contraction drives oil prices lower. OPEC+ production cuts insufficient to offset demand weakness."
        return "Oil price moves driven by scenario dynamics. Distillates follow crude movements."

    def _generate_pm_rationale(self, scenario_type: ScenarioType, severity: Severity) -> str:
        """Generate rationale for precious metals shocks."""
        return "Gold and silver benefit from safe haven demand in risk-off scenario. Industrial PMs (Platinum, Palladium) decline with broader industrial demand weakness. Lease rates fall reflecting lower cost of carry."

    def _generate_bm_rationale(self, scenario_type: ScenarioType, severity: Severity) -> str:
        """Generate rationale for base metals shocks."""
        if scenario_type == ScenarioType.CHINA_SLOWDOWN:
            return "China hard landing drives sharp decline in industrial metals demand. Copper particularly affected as bellwether for global growth. Volatility rises as market reprices growth outlook."
        return "Industrial metals decline on weaker global growth expectations. Copper acts as economic bellwether. Volatility increases reflecting uncertainty."

    def _validate_scenario(
        self,
        asset_class_shocks: List[AssetClassShocks],
        scenario_type: str,
        severity: str
    ) -> List[ValidationResult]:
        """Validate scenario using ScenarioValidator."""
        # Convert asset_class_shocks to format expected by validator
        shocks_dict = {}
        for ac_shock in asset_class_shocks:
            shocks_dict[ac_shock.asset_class.lower().replace(" & ", "_").replace(" ", "_")] = ac_shock.shocks

        return self.validator.validate_scenario(
            scenario_shocks=shocks_dict,
            scenario_type=scenario_type,
            severity=severity
        )

    def _calculate_confidence_score(
        self,
        scenario_type: ScenarioType,
        severity: Severity,
        validation_results: List[ValidationResult]
    ) -> float:
        """Calculate confidence score (0-100)."""
        # Start with base score based on scenario type
        base_scores = {
            ScenarioType.RECESSION: 85,  # Well-understood
            ScenarioType.FINANCIAL_CRISIS: 80,  # Historical precedent (2008)
            ScenarioType.INFLATION_SHOCK: 75,  # Recent precedent (2022)
            ScenarioType.GEOPOLITICAL: 70,  # Variable outcomes
            ScenarioType.SUPPLY_DISRUPTION: 75,  # Historical examples
            ScenarioType.CHINA_SLOWDOWN: 70,  # 2015 precedent
            ScenarioType.POLICY_ERROR: 65,  # Harder to model
            ScenarioType.PANDEMIC: 60,  # Rare events
            ScenarioType.CLIMATE: 55  # Limited precedent
        }

        score = base_scores.get(scenario_type, 70)

        # Adjust for severity
        severity_adjustments = {
            Severity.MODERATE: 10,  # More plausible
            Severity.SEVERE: 0,  # Baseline
            Severity.EXTREME: -15  # Less plausible
        }
        score += severity_adjustments.get(severity, 0)

        # Penalize for validation errors
        from validators import ValidationLevel
        errors = sum(1 for v in validation_results if v.level == ValidationLevel.ERROR)
        warnings = sum(1 for v in validation_results if v.level == ValidationLevel.WARNING)

        score -= errors * 15
        score -= warnings * 5

        # Clamp to 0-100
        return max(0, min(100, score))

    def _generate_consultation_prompts(
        self,
        scenario_name: str,
        asset_class_shocks: List[AssetClassShocks],
        scenario_type: ScenarioType
    ) -> Dict[str, List[str]]:
        """Generate prompts for Front Office consultation."""
        prompts = {}

        # Energy desk
        if any(ac.asset_class == "Energy" for ac in asset_class_shocks):
            prompts["Energy Trading"] = [
                f"Review {scenario_name} oil price shocks vs current positioning",
                "Confirm relevance to key trading strategies (calendar spreads, crack spreads)",
                "Identify any basis risks (Brent-WTI, physical vs futures) needing explicit shocks",
                "Validate vol shock magnitudes vs current market conditions"
            ]

        # Metals desks
        if any(ac.asset_class == "Precious Metals" for ac in asset_class_shocks):
            prompts["Precious Metals"] = [
                "Review precious metals shocks vs inventory positions",
                "Confirm lease rate assumptions align with financing strategies",
                "Identify any cross-commodity risks not captured"
            ]

        if any(ac.asset_class == "Base Metals" for ac in asset_class_shocks):
            prompts["Base Metals"] = [
                "Validate base metals shocks vs key positions (especially copper)",
                "Confirm calendar spread impacts captured (pending Murex migration)",
                "Review any specific contract types (LME, SHFE) needing separate shocks"
            ]

        # Credit Trading
        if any(ac.asset_class == "Credit Trading" for ac in asset_class_shocks):
            prompts["Credit Trading"] = [
                "Review sector beta assumptions vs current portfolio composition",
                "Validate regional spread differentiation",
                "Identify any specific issuer concentrations requiring attention",
                "Confirm alignment with issuer risk exposures"
            ]

        return prompts

    def _determine_next_steps(
        self,
        validation_results: List[ValidationResult],
        confidence_score: float
    ) -> List[str]:
        """Determine recommended next steps."""
        from validators import ValidationLevel

        steps = []

        errors = [v for v in validation_results if v.level == ValidationLevel.ERROR]
        warnings = [v for v in validation_results if v.level == ValidationLevel.WARNING]

        if errors:
            steps.append("🔴 CRITICAL: Address validation errors before proceeding")
            steps.append("Review shock magnitudes and correlation consistency")

        if warnings:
            steps.append("⚠️  Review validation warnings with Market Risk SME")

        if confidence_score < 60:
            steps.append("⚠️  Low confidence score - extensive expert validation required")
            steps.append("Consider historical calibration adjustments")

        steps.append("Conduct Front Office consultation (use prompts provided)")
        steps.append("Present to Market Risk team for technical review")
        steps.append("Prepare MLRC presentation materials")
        steps.append("Schedule MLRC approval discussion")

        return steps

    def save_scenario(self, scenario: StressScenario, output_dir: Path) -> Path:
        """Save scenario to JSON file."""
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{scenario.metadata.scenario_id}.json"

        # Convert to dictionary (handling dataclasses and enums)
        scenario_dict = self._scenario_to_dict(scenario)

        with open(output_file, 'w') as f:
            json.dump(scenario_dict, f, indent=2)

        return output_file

    def _scenario_to_dict(self, scenario: StressScenario) -> Dict:
        """Convert StressScenario to dictionary for JSON serialization."""
        seen = set()

        def convert_value(v, path="root"):
            # Handle circular references
            obj_id = id(v)
            if obj_id in seen and hasattr(v, '__dict__'):
                return f"<circular reference to {path}>"

            if hasattr(v, '__dict__'):
                seen.add(obj_id)
                try:
                    result = {}
                    for k, val in v.__dict__.items():
                        # Skip private attributes and non-serializable objects
                        if k.startswith('_'):
                            continue
                        try:
                            result[k] = convert_value(val, f"{path}.{k}")
                        except (TypeError, RecursionError):
                            result[k] = str(val)
                    return result
                finally:
                    seen.discard(obj_id)
            elif isinstance(v, list):
                return [convert_value(item, f"{path}[{i}]") for i, item in enumerate(v)]
            elif isinstance(v, dict):
                return {k: convert_value(val, f"{path}.{k}") for k, val in v.items()}
            elif isinstance(v, Enum):
                return v.value
            elif isinstance(v, (str, int, float, bool, type(None))):
                return v
            else:
                # For other types, convert to string
                return str(v)

        return convert_value(scenario)

    def load_scenario(self, scenario_file: Path) -> StressScenario:
        """Load scenario from JSON file."""
        with open(scenario_file, 'r') as f:
            data = json.load(f)

        # Reconstruct StressScenario object
        # This is simplified - full implementation would properly reconstruct all dataclass objects
        return data  # Return dict for now
