"""
Validators

Checks for correlation consistency, shock reasonableness, and scenario plausibility.
"""

from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import Enum

class ValidationLevel(Enum):
    """Validation severity levels."""
    ERROR = "error"        # Must fix - scenario is invalid
    WARNING = "warning"    # Should review - potential issue
    INFO = "info"          # Informational - worth noting

@dataclass
class ValidationResult:
    """Result of a validation check."""
    level: ValidationLevel
    category: str  # "correlation", "magnitude", "consistency"
    message: str
    affected_factors: List[str]
    suggestion: str = ""

class ScenarioValidator:
    """
    Validates stress scenarios for consistency, plausibility, and correlation logic.
    """

    def __init__(self):
        # Define typical correlation patterns
        self.correlation_rules = self._define_correlation_rules()
        self.magnitude_limits = self._define_magnitude_limits()

    def _define_correlation_rules(self) -> Dict:
        """Define expected correlation patterns between risk factors."""
        return {
            "risk_off": {
                "description": "Flight to quality scenario",
                "rules": [
                    {
                        "condition": "equities_down",
                        "expects": [
                            {"factor": "DM_rates", "direction": "down", "rationale": "Flight to quality"},
                            {"factor": "credit_spreads", "direction": "up", "rationale": "Credit risk repricing"},
                            {"factor": "USD", "direction": "up", "rationale": "Safe haven demand"},
                            {"factor": "EM_FX", "direction": "down", "rationale": "Capital flight"}
                        ]
                    }
                ]
            },
            "inflation_shock": {
                "description": "Inflation surprise scenario",
                "rules": [
                    {
                        "condition": "rates_up_sharply",
                        "expects": [
                            {"factor": "credit_spreads", "direction": "up", "rationale": "Discount rate + default risk"},
                            {"factor": "equities", "direction": "down", "rationale": "Higher discount rates"},
                            {"factor": "commodities", "direction": "up", "rationale": "Inflation hedge"}
                        ]
                    }
                ]
            },
            "commodity_links": {
                "rules": [
                    {
                        "factor_pair": ["USD", "commodities"],
                        "typical_correlation": "negative",
                        "exceptions": ["supply_disruption"]
                    },
                    {
                        "factor_pair": ["oil", "EM_FX"],
                        "typical_correlation": "positive_for_exporters",
                        "note": "Commodity exporters (RUB, BRL, NOK) benefit from oil rise"
                    }
                ]
            },
            "rates_credit_link": {
                "rules": [
                    {
                        "condition": "DM_rates_down",
                        "if_also": "credit_spreads_tightening",
                        "flag": "WARNING",
                        "message": "Rates falling (risk-off) but credit tightening (risk-on) - inconsistent"
                    }
                ]
            }
        }

    def _define_magnitude_limits(self) -> Dict:
        """Define reasonable magnitude limits for shock sizes."""
        return {
            "equities": {
                "moderate_decline": (-5, -15),
                "severe_decline": (-15, -35),
                "extreme_decline": (-35, -60),
                "max_historical": -54,  # MSCI EM in 2008
                "warning_threshold": -70
            },
            "credit_spreads": {
                "IG": {
                    "moderate": (50, 120),
                    "severe": (120, 400),
                    "extreme": (400, 600),
                    "max_historical": 600,  # 2008
                    "warning_threshold": 800
                },
                "HY": {
                    "moderate": (150, 400),
                    "severe": (400, 1000),
                    "extreme": (1000, 1500),
                    "max_historical": 2000,  # 2008
                    "warning_threshold": 2500
                }
            },
            "rates": {
                "DM": {
                    "moderate_move": (-150, 150),
                    "severe_move": (-200, 200),
                    "max_historical_down": -200,  # 2008
                    "max_historical_up": 300,  # 1970s-80s inflation
                    "warning_threshold": 400
                },
                "EM": {
                    "moderate_move": (100, 250),
                    "severe_move": (250, 500),
                    "max_historical": 1000,
                    "warning_threshold": 1500
                }
            },
            "fx": {
                "DM_pairs": {
                    "moderate_move": (-10, 10),
                    "severe_move": (-15, 15),
                    "max_historical": 20,
                    "warning_threshold": 30
                },
                "EM_FX": {
                    "moderate_move": (-15, 15),
                    "severe_move": (-25, 25),
                    "max_historical": 50,  # RUB 2022 with capital controls
                    "warning_threshold": 60
                }
            },
            "commodities": {
                "oil": {
                    "moderate_move": (-30, 30),
                    "severe_move": (-50, 50),
                    "max_historical_down": -65,  # COVID 2020
                    "max_historical_up": 100,  # 2008
                    "warning_threshold": 150
                },
                "base_metals": {
                    "moderate_move": (-20, 20),
                    "severe_move": (-30, 30),
                    "max_historical": 54,  # Copper 2008
                    "warning_threshold": 80
                }
            },
            "VIX": {
                "elevated": (25, 35),
                "high_stress": (35, 60),
                "extreme_stress": (60, 85),
                "max_historical": 85,  # COVID 2020
                "warning_threshold": 100
            }
        }

    def validate_scenario(
        self,
        scenario_shocks: Dict[str, Any],
        scenario_type: str,
        severity: str
    ) -> List[ValidationResult]:
        """
        Comprehensive validation of a stress scenario.

        Args:
            scenario_shocks: Dictionary of risk factor shocks
            scenario_type: Type of scenario
            severity: Severity level

        Returns:
            List of validation results (errors, warnings, info)
        """
        results = []

        # 1. Validate shock magnitudes
        results.extend(self._validate_magnitudes(scenario_shocks, severity))

        # 2. Check correlation consistency
        results.extend(self._validate_correlations(scenario_shocks, scenario_type))

        # 3. Check tenor structure logic (rates)
        if "rates" in scenario_shocks:
            results.extend(self._validate_tenor_structure(scenario_shocks["rates"]))

        # 4. Check regional differentiation
        results.extend(self._validate_regional_logic(scenario_shocks))

        # 5. Validate completeness
        results.extend(self._validate_completeness(scenario_shocks))

        return results

    def _validate_magnitudes(
        self,
        shocks: Dict,
        severity: str
    ) -> List[ValidationResult]:
        """Check if shock magnitudes are reasonable vs historical precedents."""
        results = []

        # Check equity shocks
        if "equities" in shocks:
            for region, shock_pct in shocks["equities"].items():
                if shock_pct < -70:
                    results.append(ValidationResult(
                        level=ValidationLevel.ERROR,
                        category="magnitude",
                        message=f"Equity shock for {region} ({shock_pct}%) exceeds historical maximum (-54% MSCI EM 2008)",
                        affected_factors=[f"equities_{region}"],
                        suggestion="Consider reducing to -50% to -60% range or provide strong justification"
                    ))
                elif shock_pct < -60:
                    results.append(ValidationResult(
                        level=ValidationLevel.WARNING,
                        category="magnitude",
                        message=f"Equity shock for {region} ({shock_pct}%) is more extreme than 2008 crisis",
                        affected_factors=[f"equities_{region}"],
                        suggestion="This exceeds 2008 levels (-42% S&P, -54% EM). Justify if intended."
                    ))

        # Check credit spreads
        if "credit_spreads" in shocks:
            if "IG" in shocks["credit_spreads"]:
                ig_spread = shocks["credit_spreads"]["IG"]
                if ig_spread > 800:
                    results.append(ValidationResult(
                        level=ValidationLevel.ERROR,
                        category="magnitude",
                        message=f"IG spread widening ({ig_spread}bps) exceeds reasonable limit (2008 max: 600bps)",
                        affected_factors=["IG_credit_spreads"],
                        suggestion="Consider 300-600bps range for severe scenarios"
                    ))

        # Check FX moves
        if "fx" in shocks:
            for pair, move_pct in shocks["fx"].items():
                if abs(move_pct) > 60:
                    results.append(ValidationResult(
                        level=ValidationLevel.ERROR,
                        category="magnitude",
                        message=f"FX move for {pair} ({move_pct}%) is extremely large",
                        affected_factors=[pair],
                        suggestion="Even RUB in 2022 with capital controls was ~50%. Review this magnitude."
                    ))

        return results

    def _validate_correlations(
        self,
        shocks: Dict,
        scenario_type: str
    ) -> List[ValidationResult]:
        """Check if risk factor movements are correlated appropriately."""
        results = []

        # Risk-off consistency check
        equity_direction = self._get_direction(shocks.get("equities", {}))
        rates_dm_direction = self._get_direction(shocks.get("rates_DM", 0))
        credit_direction = self._get_direction(shocks.get("credit_spreads", {}).get("IG", 0))

        if equity_direction == "down" and credit_direction == "down":
            results.append(ValidationResult(
                level=ValidationLevel.ERROR,
                category="correlation",
                message="Equities down but credit spreads tightening - inconsistent (should widen in stress)",
                affected_factors=["equities", "credit_spreads"],
                suggestion="Credit spreads should widen when equities decline"
            ))

        if equity_direction == "down" and rates_dm_direction == "up":
            # Could be valid in stagflation, but flag for review
            if scenario_type not in ["inflation_shock", "stagflation"]:
                results.append(ValidationResult(
                    level=ValidationLevel.WARNING,
                    category="correlation",
                    message="Equities down but DM rates up - unusual pattern (only valid in stagflation)",
                    affected_factors=["equities", "rates_DM"],
                    suggestion="Confirm this is stagflation scenario. Typically rates fall in equity stress (flight to quality)."
                ))

        # USD vs EM FX check
        usd_direction = self._get_direction(shocks.get("USD", 0))
        em_fx_direction = self._get_direction(shocks.get("EM_FX", 0))

        if usd_direction == "up" and em_fx_direction == "up":
            results.append(ValidationResult(
                level=ValidationLevel.ERROR,
                category="correlation",
                message="USD strengthening and EM FX strengthening - inconsistent",
                affected_factors=["USD", "EM_FX"],
                suggestion="USD strength typically means EM FX weakness (negative correlation)"
            ))

        return results

    def _validate_tenor_structure(self, rates_shocks: Dict) -> List[ValidationResult]:
        """Validate that rate curve shocks have logical tenor structure."""
        results = []

        # Check if short/long rates have plausible relationship
        # This would require more detailed tenor-by-tenor data
        # For now, placeholder

        return results

    def _validate_regional_logic(self, shocks: Dict) -> List[ValidationResult]:
        """Check if regional differentiation makes sense."""
        results = []

        # DM vs EM differentiation
        if "equities" in shocks:
            equities = shocks["equities"]
            dm_avg = (equities.get("US", 0) + equities.get("EUR", 0)) / 2
            em_avg = equities.get("EM", 0)

            if em_avg > dm_avg:  # EM should typically be worse than DM in stress
                results.append(ValidationResult(
                    level=ValidationLevel.WARNING,
                    category="consistency",
                    message="EM equities declining less than DM - unusual (EM typically more volatile)",
                    affected_factors=["equities_DM", "equities_EM"],
                    suggestion="In most stress scenarios, EM suffers more than DM. Confirm if this is intended."
                ))

        return results

    def _validate_completeness(self, shocks: Dict) -> List[ValidationResult]:
        """Check if all major asset classes are covered."""
        results = []

        required_asset_classes = ["rates", "fx", "credit", "commodities"]
        missing = [ac for ac in required_asset_classes if ac not in shocks]

        if missing:
            results.append(ValidationResult(
                level=ValidationLevel.WARNING,
                category="completeness",
                message=f"Missing asset classes: {', '.join(missing)}",
                affected_factors=missing,
                suggestion="Complete scenarios should cover all major asset classes"
            ))

        return results

    def _get_direction(self, value: Any) -> str:
        """Determine direction of movement from shock value."""
        if isinstance(value, dict):
            # Average over dictionary values
            values = [v for v in value.values() if isinstance(v, (int, float))]
            if not values:
                return "neutral"
            avg = sum(values) / len(values)
            return "up" if avg > 0 else "down" if avg < 0 else "neutral"
        elif isinstance(value, (int, float)):
            return "up" if value > 0 else "down" if value < 0 else "neutral"
        return "neutral"

    def generate_validation_report(
        self,
        validation_results: List[ValidationResult]
    ) -> str:
        """Generate human-readable validation report."""
        report = []

        errors = [r for r in validation_results if r.level == ValidationLevel.ERROR]
        warnings = [r for r in validation_results if r.level == ValidationLevel.WARNING]
        info = [r for r in validation_results if r.level == ValidationLevel.INFO]

        report.append("# Scenario Validation Report\n")

        if errors:
            report.append(f"## ❌ ERRORS ({len(errors)})\n")
            for i, error in enumerate(errors, 1):
                report.append(f"### {i}. {error.message}")
                report.append(f"**Affected**: {', '.join(error.affected_factors)}")
                report.append(f"**Suggestion**: {error.suggestion}\n")

        if warnings:
            report.append(f"## ⚠️  WARNINGS ({len(warnings)})\n")
            for i, warning in enumerate(warnings, 1):
                report.append(f"### {i}. {warning.message}")
                report.append(f"**Affected**: {', '.join(warning.affected_factors)}")
                report.append(f"**Suggestion**: {warning.suggestion}\n")

        if info:
            report.append(f"## ℹ️  INFO ({len(info)})\n")
            for i, item in enumerate(info, 1):
                report.append(f"### {i}. {item.message}\n")

        if not errors and not warnings:
            report.append("## ✅ VALIDATION PASSED\n")
            report.append("No errors or warnings detected. Scenario is consistent and plausible.\n")

        return "\n".join(report)
