"""
Scenario Reviewer

Conducts annual reviews of existing pillar stress scenarios, assessing continued relevance
and proposing parameter updates with clear rationale.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class ChangeType(Enum):
    """Types of changes in annual review."""
    NO_CHANGE = "no_change"
    PARAMETER_UPDATE = "parameter_update"
    PRODUCT_REMOVED = "product_removed"
    PRODUCT_ADDED = "product_added"
    METHODOLOGY_CHANGE = "methodology_change"
    MARKET_RECALIBRATION = "market_recalibration"

@dataclass
class AssetClassReview:
    """Review results for a single asset class."""
    asset_class: str
    change_type: ChangeType
    current_parameters: Dict[str, Any]
    proposed_parameters: Optional[Dict[str, Any]]
    rationale: str
    affected_products: List[str]

@dataclass
class ScenarioReviewResult:
    """Complete annual review results."""
    scenario_name: str
    scenario_id: str
    review_date: str
    reviewer: str
    previous_review_date: Optional[str]

    asset_class_reviews: List[AssetClassReview]

    # Overall assessment
    scenario_still_relevant: bool
    relevance_assessment: str

    # Market context
    market_changes_since_last_review: List[str]
    regulatory_changes: List[str]
    system_changes: List[str]

    # Conclusions
    recommended_action: str  # "approve_as_is", "approve_with_changes", "major_revision_needed"
    next_review_date: str

class ScenarioReviewer:
    """
    Conducts annual reviews of existing pillar stress scenarios.
    """

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.risk_factor_library = self._load_risk_factor_library()

    def _load_risk_factor_library(self) -> Dict:
        """Load risk factor library with existing scenarios."""
        with open(self.data_dir / "risk_factor_shocks_library.json", 'r') as f:
            return json.load(f)

    def review_scenario(
        self,
        scenario_name: str,
        reviewer: str = "Market Risk",
        market_changes: Optional[List[str]] = None,
        system_changes: Optional[List[str]] = None,
        trading_changes: Optional[Dict[str, List[str]]] = None
    ) -> ScenarioReviewResult:
        """
        Conduct comprehensive annual review of a scenario.

        Args:
            scenario_name: Name of scenario to review (e.g., "Financial Crisis 2025")
            reviewer: Name of reviewer
            market_changes: Notable market developments since last review
            system_changes: System/platform changes (e.g., "Base Metals to Murex")
            trading_changes: Changes to trading activities by desk

        Returns:
            Complete review results with recommendations
        """
        # Find scenario in library
        existing_scenario = self._find_scenario_in_library(scenario_name)

        if not existing_scenario:
            raise ValueError(f"Scenario '{scenario_name}' not found in library")

        # Initialize review
        review_date = datetime.now().strftime("%Y-%m-%d")

        # Review each asset class
        asset_class_reviews = []

        # Rates & FX
        rates_review = self._review_rates_fx(
            existing_scenario=existing_scenario,
            market_changes=market_changes or []
        )
        asset_class_reviews.append(rates_review)

        # Credit
        credit_review = self._review_credit(
            existing_scenario=existing_scenario,
            market_changes=market_changes or []
        )
        asset_class_reviews.append(credit_review)

        # Energy
        energy_review = self._review_energy(
            existing_scenario=existing_scenario,
            market_changes=market_changes or [],
            trading_changes=trading_changes or {}
        )
        asset_class_reviews.append(energy_review)

        # Precious Metals
        pm_review = self._review_precious_metals(
            existing_scenario=existing_scenario,
            system_changes=system_changes or []
        )
        asset_class_reviews.append(pm_review)

        # Base Metals
        bm_review = self._review_base_metals(
            existing_scenario=existing_scenario,
            system_changes=system_changes or [],
            trading_changes=trading_changes or {}
        )
        asset_class_reviews.append(bm_review)

        # Assess overall relevance
        scenario_still_relevant = self._assess_overall_relevance(
            scenario_name=scenario_name,
            asset_class_reviews=asset_class_reviews,
            market_changes=market_changes or []
        )

        relevance_assessment = self._generate_relevance_assessment(
            scenario_name=scenario_name,
            still_relevant=scenario_still_relevant,
            market_changes=market_changes or []
        )

        # Determine recommended action
        recommended_action = self._determine_recommended_action(asset_class_reviews)

        # Calculate next review date (1 year from now)
        next_review = datetime.now().replace(year=datetime.now().year + 1).strftime("%Y-%m-%d")

        return ScenarioReviewResult(
            scenario_name=scenario_name,
            scenario_id=existing_scenario.get("id", scenario_name.lower().replace(" ", "_")),
            review_date=review_date,
            reviewer=reviewer,
            previous_review_date=existing_scenario.get("last_review_date"),
            asset_class_reviews=asset_class_reviews,
            scenario_still_relevant=scenario_still_relevant,
            relevance_assessment=relevance_assessment,
            market_changes_since_last_review=market_changes or [],
            regulatory_changes=[],  # Would be populated from inputs
            system_changes=system_changes or [],
            recommended_action=recommended_action,
            next_review_date=next_review
        )

    def _find_scenario_in_library(self, scenario_name: str) -> Optional[Dict]:
        """Find scenario in risk factor library."""
        # Check if scenario exists in library
        scenarios = self.risk_factor_library.get("metadata", {}).get("scenario_names", [])

        # Normalize scenario name
        normalized_name = scenario_name.replace("_", " ").title()

        for scenario in scenarios:
            if scenario.replace("_", " ").title() == normalized_name:
                # Return scenario data
                return {
                    "name": scenario,
                    "id": scenario.lower().replace(" ", "_"),
                    "rates": self.risk_factor_library["asset_classes"]["rates"]["scenarios"].get(scenario),
                    "fx": self.risk_factor_library["asset_classes"]["fx"]["scenarios"].get(scenario),
                    "credit": self.risk_factor_library["asset_classes"]["credit"],
                    "energy": self.risk_factor_library["asset_classes"]["energy"],
                    "precious_metals": self.risk_factor_library["asset_classes"]["precious_metals"],
                    "base_metals": self.risk_factor_library["asset_classes"]["base_metals"]
                }

        return None

    def _review_rates_fx(
        self,
        existing_scenario: Dict,
        market_changes: List[str]
    ) -> AssetClassReview:
        """Review Rates & FX parameters."""
        # In most cases, rate/FX parameters remain appropriate unless major structural changes

        # Check if market volatility has significantly changed
        significant_volatility_change = any(
            "volatility" in change.lower() or "vol" in change.lower()
            for change in market_changes
        )

        if significant_volatility_change:
            return AssetClassReview(
                asset_class="Rates & FX",
                change_type=ChangeType.MARKET_RECALIBRATION,
                current_parameters=existing_scenario.get("rates", {}),
                proposed_parameters=None,  # Would calculate adjusted parameters
                rationale="Market volatility patterns have changed since last review. Consider recalibrating shock magnitudes to current vol regime.",
                affected_products=["All rate curves", "All FX pairs"]
            )

        return AssetClassReview(
            asset_class="Rates & FX",
            change_type=ChangeType.NO_CHANGE,
            current_parameters=existing_scenario.get("rates", {}),
            proposed_parameters=None,
            rationale="No proposed changes. Rate and FX shock parameters remain appropriate for the scenario specification.",
            affected_products=[]
        )

    def _review_credit(
        self,
        existing_scenario: Dict,
        market_changes: List[str]
    ) -> AssetClassReview:
        """Review Credit spread parameters."""
        # Credit parameters typically stable unless major changes to sector composition

        return AssetClassReview(
            asset_class="Credit Trading",
            change_type=ChangeType.NO_CHANGE,
            current_parameters=existing_scenario.get("credit", {}),
            proposed_parameters=None,
            rationale="No proposed changes. Credit spread shocks and sector beta factors remain appropriate.",
            affected_products=[]
        )

    def _review_energy(
        self,
        existing_scenario: Dict,
        market_changes: List[str],
        trading_changes: Dict[str, List[str]]
    ) -> AssetClassReview:
        """Review Energy commodity parameters."""
        # Check for product changes
        energy_changes = trading_changes.get("Energy Trading", [])

        if energy_changes:
            return AssetClassReview(
                asset_class="Energy",
                change_type=ChangeType.PARAMETER_UPDATE,
                current_parameters=existing_scenario.get("energy", {}),
                proposed_parameters=None,
                rationale=f"Trading desk changes noted: {'; '.join(energy_changes)}. Review shock specifications accordingly.",
                affected_products=energy_changes
            )

        return AssetClassReview(
            asset_class="Energy",
            change_type=ChangeType.NO_CHANGE,
            current_parameters=existing_scenario.get("energy", {}),
            proposed_parameters=None,
            rationale="No proposed changes. Energy product shocks remain appropriate.",
            affected_products=[]
        )

    def _review_precious_metals(
        self,
        existing_scenario: Dict,
        system_changes: List[str]
    ) -> AssetClassReview:
        """Review Precious Metals parameters."""
        # Check for Murex migration (volatility shock type change)
        murex_migration = any("murex" in change.lower() for change in system_changes)

        if murex_migration and "precious" in " ".join(system_changes).lower():
            return AssetClassReview(
                asset_class="Precious Metals",
                change_type=ChangeType.METHODOLOGY_CHANGE,
                current_parameters=existing_scenario.get("precious_metals", {}),
                proposed_parameters={
                    "volatility_shock_type": "relative",
                    "note": "Changed from Absolute to Relative per Murex migration"
                },
                rationale="Vol shock type update from Absolute to Relative, adjusting the size of the shocks accordingly informed by current market levels and existing shock sizes. This change aligns with the Precious Metals to Murex migration.",
                affected_products=["Gold", "Silver", "Platinum", "Palladium"]
            )

        return AssetClassReview(
            asset_class="Precious Metals",
            change_type=ChangeType.NO_CHANGE,
            current_parameters=existing_scenario.get("precious_metals", {}),
            proposed_parameters=None,
            rationale="No proposed changes.",
            affected_products=[]
        )

    def _review_base_metals(
        self,
        existing_scenario: Dict,
        system_changes: List[str],
        trading_changes: Dict[str, List[str]]
    ) -> AssetClassReview:
        """Review Base Metals parameters."""
        changes_list = []
        proposed_params = {}

        # Check for Murex migration
        murex_migration = any("murex" in change.lower() and "base" in change.lower()
                              for change in system_changes)

        # Check if desk stopped trading certain products
        bm_trading_changes = trading_changes.get("Base Metals", [])

        iron_ore_removed = any("iron ore" in change.lower() and "removed" in change.lower()
                               for change in bm_trading_changes)
        cobalt_added = any("cobalt" in change.lower() for change in bm_trading_changes)

        if iron_ore_removed:
            changes_list.append("Remove Iron Ore shock (desk no longer trades this product)")
            proposed_params["Iron_Ore"] = "REMOVED"

        if cobalt_added:
            changes_list.append("Explicitly define Cobalt shock (currently falls under 'Other')")
            proposed_params["Cobalt"] = {"price_shock_pct": -25, "vol_shock_abs": 25}

        if murex_migration:
            changes_list.append("Note: Full term structure upgrade deferred pending Murex migration completion in 2025")

        if changes_list:
            return AssetClassReview(
                asset_class="Base Metals",
                change_type=ChangeType.PRODUCT_REMOVED if iron_ore_removed else ChangeType.PARAMETER_UPDATE,
                current_parameters=existing_scenario.get("base_metals", {}),
                proposed_parameters=proposed_params,
                rationale="\n".join(changes_list),
                affected_products=["Iron Ore"] if iron_ore_removed else ["Cobalt"]
            )

        return AssetClassReview(
            asset_class="Base Metals",
            change_type=ChangeType.NO_CHANGE,
            current_parameters=existing_scenario.get("base_metals", {}),
            proposed_parameters=None,
            rationale="No proposed changes.",
            affected_products=[]
        )

    def _assess_overall_relevance(
        self,
        scenario_name: str,
        asset_class_reviews: List[AssetClassReview],
        market_changes: List[str]
    ) -> bool:
        """Assess if scenario is still relevant."""
        # Scenario is relevant unless major changes make it obsolete
        major_changes = sum(
            1 for review in asset_class_reviews
            if review.change_type != ChangeType.NO_CHANGE
        )

        # If fewer than half asset classes need changes, scenario is still relevant
        return major_changes < len(asset_class_reviews) / 2

    def _generate_relevance_assessment(
        self,
        scenario_name: str,
        still_relevant: bool,
        market_changes: List[str]
    ) -> str:
        """Generate relevance assessment text."""
        if still_relevant:
            return f"The '{scenario_name}' scenario remains relevant for stress testing purposes. The underlying economic narrative and transmission channels continue to represent plausible stress conditions."
        else:
            return f"The '{scenario_name}' scenario requires significant revision due to material changes in market structure, trading activities, or economic conditions."

    def _determine_recommended_action(
        self,
        asset_class_reviews: List[AssetClassReview]
    ) -> str:
        """Determine recommended action based on review results."""
        changes = [r for r in asset_class_reviews if r.change_type != ChangeType.NO_CHANGE]

        if not changes:
            return "approve_as_is"
        elif len(changes) <= 2:
            return "approve_with_changes"
        else:
            return "major_revision_needed"

    def generate_review_memo(
        self,
        review_result: ScenarioReviewResult
    ) -> str:
        """Generate annual review memo in MLRC format."""
        memo_parts = []

        # Header
        memo_parts.append(f"# {review_result.scenario_name} - Annual Review {datetime.now().year}")
        memo_parts.append("")

        # Cover Sheet
        memo_parts.append("## Board Report Cover Sheet")
        memo_parts.append(f"**Document Name**: {review_result.scenario_name} - Annual Review {datetime.now().year}")
        memo_parts.append(f"**Meeting Date**: MLRC - {review_result.review_date}")
        memo_parts.append(f"**Presenter**: {review_result.reviewer}")
        memo_parts.append(f"**Context**: Memo for noting - Annual Review for the \"{review_result.scenario_name}\" Scenario")
        memo_parts.append(f"**Purpose**: Annual review of \"{review_result.scenario_name}\" scenario shocks applied to various asset classes")
        memo_parts.append("")

        # Background
        memo_parts.append("## Background")
        memo_parts.append(f"The below are the shocks approved for the \"{review_result.scenario_name}\" scenario as per the Example Bank Stress Testing Parameterisation document.")
        memo_parts.append("")

        # Market Context (if provided)
        if review_result.market_changes_since_last_review:
            memo_parts.append("### Market Developments Since Last Review")
            for change in review_result.market_changes_since_last_review:
                memo_parts.append(f"- {change}")
            memo_parts.append("")

        # System Changes (if provided)
        if review_result.system_changes:
            memo_parts.append("### System and Platform Changes")
            for change in review_result.system_changes:
                memo_parts.append(f"- {change}")
            memo_parts.append("")

        # Asset Class Reviews
        for review in review_result.asset_class_reviews:
            memo_parts.append(f"## {review.asset_class}")

            if review.change_type == ChangeType.NO_CHANGE:
                memo_parts.append("**No proposed changes**")
                memo_parts.append("")
                memo_parts.append("**Current Applied Shocks**")
                memo_parts.append("*(See attached parameterization document)*")
            else:
                memo_parts.append(f"**{review.change_type.value.replace('_', ' ').title()}**")
                memo_parts.append("")
                memo_parts.append(f"**Rationale**: {review.rationale}")
                memo_parts.append("")

                if review.proposed_parameters:
                    memo_parts.append("**Proposed Changes**:")
                    for param, value in review.proposed_parameters.items():
                        memo_parts.append(f"- {param}: {value}")

                if review.affected_products:
                    memo_parts.append(f"**Affected Products**: {', '.join(review.affected_products)}")

            memo_parts.append("")

        # Conclusions
        memo_parts.append("## Conclusions and Recommended Actions")

        action_text = {
            "approve_as_is": "Memo submitted for approval. No changes to scenario parameters proposed.",
            "approve_with_changes": "Memo submitted for approval with proposed parameter updates as detailed above.",
            "major_revision_needed": "Significant revision required. Recommend scheduling detailed scenario redesign discussion."
        }

        memo_parts.append(action_text[review_result.recommended_action])
        memo_parts.append("")

        # References
        memo_parts.append("## References")
        memo_parts.append("[1] Example Bank Stress Testing Parameterisation")
        memo_parts.append("")

        # Document History
        memo_parts.append("## Document History")
        memo_parts.append(f"**Prepared by**: {review_result.reviewer}")
        memo_parts.append(f"**Date**: {review_result.review_date}")
        memo_parts.append("**Reviewed by 2nd line of defence**: N/A")
        memo_parts.append("**Matters raised by 2nd line of defence**: N/A")
        memo_parts.append("")

        # Formal Governance
        memo_parts.append("## Formal Document Governance")
        memo_parts.append("**Reviewing committee and meeting date**: MLRC")
        memo_parts.append("**Outcome and key rationale for decision**: *(To be completed post-MLRC)*")
        memo_parts.append("**Significant matters raised and associated actions**: *(To be completed post-MLRC)*")
        memo_parts.append("")

        return "\n".join(memo_parts)
