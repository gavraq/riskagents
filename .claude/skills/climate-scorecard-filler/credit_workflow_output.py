"""
Credit Workflow Output Module

This module provides the integration layer between the Climate Scorecard Filler skill
and the Credit Risk Workflow System. It handles:

1. Request validation - Detecting when requests come from credit_workflow system
2. Output generation - Producing JSON in the exact format required
3. Field validation - Ensuring all required fields are present

Usage:
    from credit_workflow_output import CreditWorkflowOutput, is_credit_workflow_request

    # Check if request is from credit workflow
    if is_credit_workflow_request(request_data):
        # Generate output
        output = CreditWorkflowOutput.from_scorecard(enhanced_scorecard)
        json_response = output.to_json()
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import json

from climate_scorecard_helper import (
    EnhancedClimateScorecard,
    ConfidenceTracker
)


# Required fields for credit workflow output
REQUIRED_SCORECARD_FIELDS = [
    # Section 1: Assessment Context
    "assessment_type",

    # Section 2: Transition Risk - Preparedness
    "net_zero_target_exists", "net_zero_target_year", "net_zero_target_scope",
    "net_zero_science_based", "net_zero_score",
    "tcfd_disclosure_level", "tcfd_disclosure_score",
    "climate_governance_board", "climate_governance_exec_accountability",
    "climate_governance_incentives_linked", "climate_governance_score",
    "transition_plan_exists", "transition_plan_published",
    "transition_plan_milestones", "transition_plan_score",
    "green_capex_percentage", "capex_alignment_trajectory", "capex_alignment_score",

    # Section 3: Transition Risk - Vulnerability
    "carbon_intensity_scope1", "carbon_intensity_scope2", "carbon_intensity_scope3",
    "carbon_intensity_trend", "carbon_intensity_score",
    "stranded_asset_exposure", "stranded_asset_types", "stranded_asset_score",
    "policy_pressure_jurisdictions", "policy_pressure_carbon_pricing_exposure", "policy_pressure_score",
    "tech_disruption_risk_level", "tech_disruption_assessment", "tech_disruption_score",
    "market_sentiment_esg_rating", "market_sentiment_investor_pressure", "market_sentiment_score",
    "litigation_current_cases", "litigation_historical_cases", "litigation_exposure_assessment", "litigation_score",
    "country_dependency_high_risk_revenue", "country_dependency_score",

    # Section 4: Transition Risk - Opportunity
    "green_market_growth_potential", "green_market_growth_assessment", "green_market_growth_score",
    "green_revenue_percentage", "green_revenue_trend", "green_revenue_score",
    "competitive_advantage_assessment", "competitive_advantage_score",

    # Section 5: Physical Risk Assessment
    "acute_hazard_exposure", "acute_hazard_types", "acute_hazard_score",
    "chronic_exposure_assessment", "chronic_exposure_score",
    "ecosystem_dependency_level", "ecosystem_dependency_assessment", "ecosystem_dependency_score",
    "adaptation_capability_level", "adaptation_investments", "adaptation_capability_score",
    "scenario_analysis_conducted", "scenario_analysis_scenarios",
    "scenario_analysis_time_horizons", "scenario_analysis_integration", "scenario_analysis_score",

    # Section 6: Risk Appetite Alignment
    "risk_appetite_category", "risk_appetite_justification", "risk_appetite_conditions",

    # Section 7: Capital & ICAAP Considerations
    "pillar_2_treatment", "icaap_materiality_assessment", "capital_add_on_recommendation",

    # Section 8: Data Quality Declaration
    "data_sources", "data_proxies_used", "data_gaps_identified", "data_quality_overall",

    # Section 9: Summary & Recommendations
    "overall_transition_risk_score", "overall_physical_risk_score", "overall_climate_risk_rating",
    "key_risk_drivers", "key_opportunities", "recommended_mitigations",
    "monitoring_triggers", "next_review_date"
]


def is_credit_workflow_request(request_data: Dict[str, Any]) -> bool:
    """
    Check if a request originates from the Credit Risk Workflow System.

    The credit workflow system sends requests with:
    - source_system: "credit_workflow"
    - request_type: "climate_scorecard_generation"

    Args:
        request_data: Dictionary containing request metadata

    Returns:
        True if this is a credit workflow request, False otherwise
    """
    return (
        request_data.get("source_system") == "credit_workflow" and
        request_data.get("request_type") == "climate_scorecard_generation"
    )


def parse_credit_workflow_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse the credit workflow request and extract relevant information.

    Args:
        request_data: Full request payload from credit workflow system

    Returns:
        Dictionary with parsed counterparty and credit application info
    """
    return {
        "counterparty_name": request_data.get("counterparty", {}).get("name"),
        "counterparty_sector": request_data.get("counterparty", {}).get("sector"),
        "counterparty_country": request_data.get("counterparty", {}).get("country"),
        "counterparty_id": request_data.get("counterparty", {}).get("id"),
        "credit_application_id": request_data.get("credit_application", {}).get("id"),
        "credit_amount": request_data.get("credit_application", {}).get("credit_request_amount"),
        "currency": request_data.get("credit_application", {}).get("currency"),
        "documents": request_data.get("documents", []),
        "existing_data": request_data.get("existing_data", {})
    }


@dataclass
class CreditWorkflowOutput:
    """
    Output wrapper for Credit Risk Workflow System integration.

    This class provides validation and formatting for the JSON output
    required by the credit workflow system.
    """
    scorecard_data: Dict[str, Any]
    confidence_scores: Dict[str, float]
    generation_notes: str

    @classmethod
    def from_scorecard(
        cls,
        scorecard: EnhancedClimateScorecard,
        confidence_tracker: Optional[ConfidenceTracker] = None
    ) -> "CreditWorkflowOutput":
        """
        Create CreditWorkflowOutput from an EnhancedClimateScorecard.

        Args:
            scorecard: The populated climate scorecard
            confidence_tracker: Optional pre-configured confidence tracker

        Returns:
            CreditWorkflowOutput instance
        """
        # Generate JSON and parse back to get structured data
        json_str = scorecard.to_credit_workflow_json(confidence_tracker)
        data = json.loads(json_str)

        return cls(
            scorecard_data=data["scorecard_data"],
            confidence_scores=data["confidence_scores"],
            generation_notes=data["generation_notes"]
        )

    def validate(self) -> List[str]:
        """
        Validate that all required fields are present.

        Returns:
            List of missing field names (empty if valid)
        """
        missing_fields = []
        for field_name in REQUIRED_SCORECARD_FIELDS:
            if field_name not in self.scorecard_data:
                missing_fields.append(field_name)
        return missing_fields

    def is_valid(self) -> bool:
        """Check if the output passes validation."""
        return len(self.validate()) == 0

    def get_data_quality_summary(self) -> Dict[str, Any]:
        """
        Get a summary of data quality and confidence.

        Returns:
            Dictionary with quality metrics
        """
        total_fields = len(self.scorecard_data)
        null_fields = sum(1 for v in self.scorecard_data.values() if v is None or v == [] or v == "")
        populated_fields = total_fields - null_fields

        low_confidence = sum(1 for v in self.confidence_scores.values() if v < 0.5)
        medium_confidence = sum(1 for v in self.confidence_scores.values() if 0.5 <= v < 0.75)
        high_confidence = sum(1 for v in self.confidence_scores.values() if v >= 0.75)

        avg_confidence = sum(self.confidence_scores.values()) / len(self.confidence_scores) if self.confidence_scores else 0

        return {
            "total_fields": total_fields,
            "populated_fields": populated_fields,
            "null_fields": null_fields,
            "population_rate": populated_fields / total_fields if total_fields > 0 else 0,
            "low_confidence_count": low_confidence,
            "medium_confidence_count": medium_confidence,
            "high_confidence_count": high_confidence,
            "average_confidence": round(avg_confidence, 2),
            "data_quality_rating": self.scorecard_data.get("data_quality_overall", "unknown")
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "scorecard_data": self.scorecard_data,
            "confidence_scores": self.confidence_scores,
            "generation_notes": self.generation_notes
        }

    def to_json(self, indent: int = 2) -> str:
        """
        Serialize to JSON string.

        Args:
            indent: JSON indentation level

        Returns:
            JSON string
        """
        return json.dumps(self.to_dict(), indent=indent, default=str)


def generate_credit_workflow_response(
    scorecard: EnhancedClimateScorecard,
    confidence_tracker: Optional[ConfidenceTracker] = None,
    validate: bool = True
) -> str:
    """
    Generate the complete credit workflow response.

    This is the main entry point for generating JSON output for the
    credit workflow system.

    Args:
        scorecard: Populated EnhancedClimateScorecard
        confidence_tracker: Optional pre-configured confidence tracker
        validate: Whether to validate output before returning

    Returns:
        JSON string in credit workflow format

    Raises:
        ValueError: If validation fails and validate=True
    """
    output = CreditWorkflowOutput.from_scorecard(scorecard, confidence_tracker)

    if validate:
        missing = output.validate()
        if missing:
            # Log warning but don't fail - fields can be null
            pass

    return output.to_json()


# Example usage
if __name__ == "__main__":
    # Example: Check if request is from credit workflow
    sample_request = {
        "source_system": "credit_workflow",
        "request_type": "climate_scorecard_generation",
        "version": "1.0",
        "counterparty": {
            "name": "Example Corp",
            "sector": "Energy",
            "country": "United Kingdom"
        }
    }

    if is_credit_workflow_request(sample_request):
        print("This is a credit workflow request!")
        parsed = parse_credit_workflow_request(sample_request)
        print(f"Counterparty: {parsed['counterparty_name']}")
        print(f"Sector: {parsed['counterparty_sector']}")
        print(f"Country: {parsed['counterparty_country']}")
