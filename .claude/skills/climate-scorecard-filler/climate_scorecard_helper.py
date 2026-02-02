"""
Climate Scorecard Helper - Enhanced Generic Framework (SS5/25 Aligned)

Updated December 2025 to align with PRA SS5/25 requirements:
- Risk Appetite alignment section
- ICAAP/Capital considerations for banks
- Enhanced litigation risk treatment (distinct channel option)
- Enhanced scenario analysis quality assessment
- Data quality declaration

Original enhancements from ICBC Standard Bank template:
1. Structured question-based approach within categories
2. Intent/Preparedness vs Vulnerability split for transition risk
3. Transition benefit/opportunity assessment
4. Country-level sovereign risk transmission
5. Counterparty climate risk management capability assessment

Regulatory References:
- PRA SS5/25 (December 2025) - Replaces SS3/19
- BCBS Principles for climate-related financial risks
- ISSB IFRS S2 Climate-related Disclosures

Usage:
    from climate_scorecard_helper import EnhancedClimateScorecard

    scorecard = EnhancedClimateScorecard(
        counterparty="GCB Bank Ltd",
        country="Ghana",
        sector="Financial Institutions"
    )

    # Assess with specific sub-questions
    scorecard.assess_transition_preparedness(
        net_zero_target=2,
        tcfd_disclosure=1,
        governance_structure=3,
        rationale="Limited climate governance..."
    )

    # SS5/25: Set risk appetite alignment
    scorecard.set_risk_appetite_alignment(
        category="Manage",
        justification="Within monitored sector appetite",
        escalation_required=False
    )

    # SS5/25: Set ICAAP considerations (banks only)
    scorecard.set_icaap_considerations(
        capital_relevance="Medium",
        icaap_treatment="Stress Testing",
        materiality_justification="Material exposure through portfolio"
    )

    scorecard.generate_enhanced_scorecard()
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
import json


# =============================================================================
# CREDIT WORKFLOW HELPER FUNCTIONS
# =============================================================================

def score_to_enum_exposure(score: Optional[int]) -> Optional[str]:
    """Convert 1-5 score to none|low|medium|high enum."""
    if score is None:
        return None
    mapping = {1: "none", 2: "low", 3: "medium", 4: "high", 5: "high"}
    return mapping.get(score, "medium")


def score_to_enum_risk(score: Optional[float]) -> Optional[str]:
    """Convert float score to low|medium|high|critical enum."""
    if score is None:
        return None
    if score <= 1.5:
        return "low"
    elif score <= 2.5:
        return "medium"
    elif score <= 3.5:
        return "high"
    else:
        return "critical"


def score_to_rating(score: Optional[float]) -> Optional[str]:
    """Convert overall score to A-E climate rating."""
    if score is None:
        return None
    if score <= 1.5:
        return "A"
    elif score <= 2.5:
        return "B"
    elif score <= 3.0:
        return "C"
    elif score <= 4.0:
        return "D"
    else:
        return "E"


def score_to_tcfd_level(score: Optional[int]) -> Optional[str]:
    """Convert TCFD disclosure score to level enum."""
    if score is None:
        return None
    mapping = {1: "verified", 2: "full", 3: "partial", 4: "partial", 5: "none"}
    return mapping.get(score, "partial")


def score_to_growth_potential(score: Optional[int]) -> Optional[str]:
    """Convert opportunity score to growth potential enum."""
    if score is None:
        return None
    mapping = {1: "transformative", 2: "high", 3: "medium", 4: "low", 5: "none"}
    return mapping.get(score, "medium")


def score_to_revenue_trend(score: Optional[int]) -> Optional[str]:
    """Convert green revenue score to trend enum."""
    if score is None:
        return None
    mapping = {1: "rapidly_growing", 2: "growing", 3: "stable", 4: "stable", 5: "declining"}
    return mapping.get(score, "stable")


def score_to_adaptation_level(score: Optional[int]) -> Optional[str]:
    """Convert adaptation capability score to level enum."""
    if score is None:
        return None
    mapping = {1: "mature", 2: "developing", 3: "developing", 4: "limited", 5: "none"}
    return mapping.get(score, "limited")


def score_to_pillar2_treatment(score: Optional[float]) -> Optional[str]:
    """Convert overall score to Pillar 2 treatment enum."""
    if score is None:
        return None
    if score <= 2.0:
        return "not_material"
    elif score <= 3.0:
        return "low_add_on"
    elif score <= 4.0:
        return "medium_add_on"
    else:
        return "high_add_on"


# =============================================================================
# CONFIDENCE TRACKER
# =============================================================================

@dataclass
class ConfidenceTracker:
    """
    Tracks confidence scores for each field during assessment.

    Confidence levels (0.0-1.0):
    - 0.90-1.00: Very High - Directly from verified company disclosures
    - 0.75-0.89: High - From multiple corroborating sources
    - 0.60-0.74: Medium - From single unverified source or inference
    - 0.40-0.59: Low - Estimated/proxy data used
    - 0.00-0.39: Very Low - Limited data, high uncertainty
    """
    scores: Dict[str, float] = field(default_factory=dict)

    # Default confidence by source type
    SOURCE_CONFIDENCE = {
        "company_disclosure": 0.90,
        "verified_disclosure": 0.95,
        "esg_rating": 0.85,
        "multiple_sources": 0.80,
        "industry_proxy": 0.60,
        "sector_average": 0.55,
        "estimate": 0.50,
        "derived": 0.75,
        "user_provided": 0.95,
        "default": 0.30,
        "null": 0.30,
    }

    def set_confidence(self, field: str, score: float, reason: str = "") -> None:
        """Set confidence for a field (0.0-1.0)."""
        self.scores[field] = max(0.0, min(1.0, score))

    def set_from_source(self, field: str, source_type: str) -> None:
        """Set confidence based on source type."""
        confidence = self.SOURCE_CONFIDENCE.get(source_type, 0.40)
        self.scores[field] = confidence

    def get_confidence(self, field: str) -> float:
        """Get confidence for a field, defaulting to 0.3 if not set."""
        return self.scores.get(field, 0.30)

    def set_null_confidence(self, field: str) -> None:
        """Set confidence for a null/missing field."""
        self.scores[field] = 0.30

    def to_dict(self) -> Dict[str, float]:
        """Return all confidence scores as dictionary."""
        return dict(self.scores)


# =============================================================================
# SS5/25 NEW DATACLASSES
# =============================================================================

@dataclass
class RiskAppetiteAlignment:
    """
    SS5/25 Requirement: Explicit alignment with firm's climate risk appetite framework.

    The PRA expects boards to establish quantified climate risk appetite cascaded
    across business lines. This section documents how the counterparty assessment
    aligns with the firm's risk appetite framework.
    """
    category: str = ""  # "Accept" | "Manage" | "Avoid"
    justification: str = ""
    portfolio_limit_impact: str = ""
    escalation_required: bool = False
    escalation_reason: str = ""

    # Credit Workflow Extended Fields
    risk_appetite_category: Optional[str] = None  # "avoid" | "manage" | "monitor" | "acceptable"
    risk_appetite_justification: Optional[str] = None  # Justification for category
    risk_appetite_conditions: Optional[str] = None  # Conditions for continued engagement


@dataclass
class ICaapConsiderations:
    """
    SS5/25 Requirement: Integration of climate risk into ICAAP for banks.

    Banks must evidence how climate-related risks are assessed for capital
    adequacy materiality in their ICAAPs.
    """
    capital_relevance: str = ""  # "High" | "Medium" | "Low" | "Not Material"
    icaap_treatment: str = ""  # "Pillar 2A" | "Stress Testing" | "Not Material"
    materiality_justification: str = ""

    # Credit Workflow Extended Fields
    pillar_2_treatment: Optional[str] = None  # "not_material" | "low_add_on" | "medium_add_on" | "high_add_on"
    icaap_materiality_assessment: Optional[str] = None  # ICAAP materiality assessment
    capital_add_on_recommendation: Optional[float] = None  # Recommended capital add-on %


@dataclass
class LitigationRiskAssessment:
    """
    SS5/25 Requirement: Flexible treatment of litigation risk.

    The PRA allows firms to treat climate-related litigation as either:
    - A subset of physical and/or transition risks, OR
    - A distinct transmission channel

    This assessment captures the chosen treatment and detailed evaluation.
    """
    treatment: str = "subset"  # "subset" | "distinct_channel"
    score: Optional[int] = None  # 1-5 if assessed separately
    litigation_type: str = ""  # "climate_disclosure" | "greenwashing" | "physical_damage" | "duty_of_care" | "other"
    rationale: str = ""
    sources: List[str] = field(default_factory=list)


@dataclass
class ScenarioAnalysisQuality:
    """
    SS5/25 Requirement: Scenario analysis must inform actual decision-making.

    Enhanced assessment of counterparty's climate scenario analysis quality,
    not just existence. The PRA expects firms to document how CSA results
    have informed actual business decisions.
    """
    # Core scores (1-5 scale)
    analysis_conducted: Optional[int] = None  # 1-5: Has CP conducted CSA?
    results_integrated: Optional[int] = None  # 1-5: Are results used in strategy?
    horizons_appropriate: Optional[int] = None  # 1-5: Are time horizons suitable?
    documentation_quality: Optional[int] = None  # 1-5: Quality of documentation

    # Credit Workflow Extended Fields
    scenario_analysis_conducted: Optional[bool] = None  # Has scenario analysis been done
    scenario_analysis_scenarios: Optional[List[str]] = None  # e.g., ["IEA Net Zero 2050", "NGFS Orderly Transition"]
    scenario_analysis_time_horizons: Optional[List[str]] = None  # e.g., ["2030", "2040", "2050"]
    scenario_analysis_integration: Optional[str] = None  # How scenarios integrate into strategy

    rationale: str = ""
    sources: List[str] = field(default_factory=list)

    def calculate_score(self) -> float:
        """Calculate average scenario analysis quality score"""
        scores = [
            self.analysis_conducted,
            self.results_integrated,
            self.horizons_appropriate,
            self.documentation_quality
        ]
        valid = [s for s in scores if s is not None]
        return sum(valid) / len(valid) if valid else 0.0


@dataclass
class DataQualityDeclaration:
    """
    SS5/25 Requirement: Document data sources, proxies, and limitations.

    Firms must understand data uncertainty, document proxies used, and
    actively work to close data gaps. This provides an audit trail.
    """
    primary_sources: List[str] = field(default_factory=list)
    proxies_used: List[Dict[str, str]] = field(default_factory=list)  # [{"data_point": "...", "proxy": "...", "limitation": "..."}]
    data_gaps: List[str] = field(default_factory=list)
    uncertainty_acknowledgment: str = ""


# =============================================================================
# ORIGINAL DATACLASSES (unchanged)
# =============================================================================


@dataclass
class TransitionPreparedness:
    """Assessment of counterparty's preparedness and intent to transition"""
    # Core scores (1-5 scale)
    net_zero_target: Optional[int] = None  # 1-5: Has credible net-zero target?
    tcfd_disclosure: Optional[int] = None  # 1-5: Quality of climate disclosure (TCFD/CDP)
    governance_structure: Optional[int] = None  # 1-5: Climate governance (board, committees)
    transition_plan: Optional[int] = None  # 1-5: Credibility of transition/decarbonization plan
    capex_alignment: Optional[int] = None  # 1-5: Capex aligned with Paris goals?

    # Credit Workflow Extended Fields
    net_zero_target_exists: Optional[bool] = None  # Has net-zero target
    net_zero_target_year: Optional[int] = None  # Target year (e.g., 2050)
    net_zero_target_scope: Optional[str] = None  # "scope_1" | "scope_1_2" | "scope_1_2_3"
    net_zero_science_based: Optional[bool] = None  # SBTi validated
    tcfd_disclosure_level: Optional[str] = None  # "none" | "partial" | "full" | "verified"
    climate_governance_board: Optional[bool] = None  # Board-level oversight
    climate_governance_exec_accountability: Optional[bool] = None  # Executive accountability
    climate_governance_incentives_linked: Optional[bool] = None  # Compensation linked to climate
    transition_plan_exists: Optional[bool] = None  # Formal transition plan exists
    transition_plan_published: Optional[bool] = None  # Plan publicly available
    transition_plan_milestones: Optional[str] = None  # Key milestones with years and targets
    green_capex_percentage: Optional[float] = None  # Percentage of capex aligned with Paris goals
    capex_alignment_trajectory: Optional[str] = None  # "increasing" | "stable" | "decreasing"

    rationale: str = ""
    sources: List[str] = field(default_factory=list)

    def calculate_score(self) -> float:
        """Calculate average preparedness score"""
        scores = [
            self.net_zero_target,
            self.tcfd_disclosure,
            self.governance_structure,
            self.transition_plan,
            self.capex_alignment
        ]
        valid = [s for s in scores if s is not None]
        return sum(valid) / len(valid) if valid else 0.0


@dataclass
class TransitionVulnerability:
    """Assessment of counterparty's vulnerability to transition risks"""
    # Core scores (1-5 scale)
    sector_carbon_intensity: Optional[int] = None  # 1-5: How carbon-intensive is the sector?
    stranded_asset_risk: Optional[int] = None  # 1-5: Risk of assets becoming stranded
    policy_regulatory_risk: Optional[int] = None  # 1-5: Exposure to carbon pricing, regulations
    technology_disruption: Optional[int] = None  # 1-5: Vulnerability to clean tech disruption
    market_sentiment_risk: Optional[int] = None  # 1-5: Investor/consumer sentiment shifts
    legal_litigation_risk: Optional[int] = None  # 1-5: Climate litigation exposure
    country_transition_dependency: Optional[int] = None  # 1-5: Country fiscal dependency on carbon-intensive sectors

    # Credit Workflow Extended Fields
    carbon_intensity_scope1: Optional[float] = None  # tCO2e per unit revenue
    carbon_intensity_scope2: Optional[float] = None  # tCO2e per unit revenue
    carbon_intensity_scope3: Optional[float] = None  # tCO2e per unit revenue
    carbon_intensity_trend: Optional[str] = None  # "declining" | "stable" | "increasing"
    stranded_asset_exposure: Optional[str] = None  # "none" | "low" | "medium" | "high"
    stranded_asset_types: Optional[str] = None  # Types of assets at risk
    policy_pressure_jurisdictions: Optional[str] = None  # Key jurisdictions with regulatory pressure
    policy_pressure_carbon_pricing_exposure: Optional[bool] = None  # Exposed to carbon pricing
    tech_disruption_risk_level: Optional[str] = None  # "low" | "medium" | "high" | "critical"
    tech_disruption_assessment: Optional[str] = None  # Assessment of technology disruption risks
    market_sentiment_esg_rating: Optional[str] = None  # e.g., "Sustainalytics 38.6 (Severe Risk), MSCI BB"
    market_sentiment_investor_pressure: Optional[str] = None  # "low" | "medium" | "high"
    litigation_current_cases: Optional[int] = None  # Number of current climate litigation cases
    litigation_historical_cases: Optional[int] = None  # Number of historical cases
    litigation_exposure_assessment: Optional[str] = None  # Assessment of litigation exposure
    country_dependency_high_risk_revenue: Optional[float] = None  # % revenue from high-risk jurisdictions

    rationale: str = ""
    sources: List[str] = field(default_factory=list)

    def calculate_score(self) -> float:
        """Calculate average vulnerability score"""
        scores = [
            self.sector_carbon_intensity,
            self.stranded_asset_risk,
            self.policy_regulatory_risk,
            self.technology_disruption,
            self.market_sentiment_risk,
            self.legal_litigation_risk,
            self.country_transition_dependency
        ]
        valid = [s for s in scores if s is not None]
        return sum(valid) / len(valid) if valid else 0.0


@dataclass
class TransitionOpportunity:
    """Assessment of opportunities from climate transition"""
    # Core scores (1-5 scale, where 1 = best positioned)
    market_growth_potential: Optional[int] = None  # 1-5: Growth in low-carbon markets (reverse: 1=high opportunity)
    green_revenue_share: Optional[int] = None  # 1-5: Share of revenue from green products/services
    competitive_advantage: Optional[int] = None  # 1-5: Early mover advantage in transition

    # Credit Workflow Extended Fields
    green_market_growth_potential: Optional[str] = None  # "none" | "low" | "medium" | "high" | "transformative"
    green_market_growth_assessment: Optional[str] = None  # Assessment of green market opportunities
    green_revenue_percentage: Optional[float] = None  # % revenue from green products/services
    green_revenue_trend: Optional[str] = None  # "declining" | "stable" | "growing" | "rapidly_growing"
    competitive_advantage_assessment: Optional[str] = None  # Competitive positioning assessment

    rationale: str = ""
    sources: List[str] = field(default_factory=list)

    def calculate_score(self) -> float:
        """Calculate opportunity score (lower = better positioned)"""
        scores = [
            self.market_growth_potential,
            self.green_revenue_share,
            self.competitive_advantage
        ]
        valid = [s for s in scores if s is not None]
        return sum(valid) / len(valid) if valid else 0.0


@dataclass
class PhysicalRiskExposure:
    """Assessment of physical climate risk exposure"""
    # Core scores (1-5 scale)
    acute_hazard_exposure: Optional[int] = None  # 1-5: Geographic exposure to acute events
    chronic_climate_exposure: Optional[int] = None  # 1-5: Exposure to chronic climate changes
    ecosystem_dependency: Optional[int] = None  # 1-5: Dependency on vulnerable ecosystems
    adaptation_capability: Optional[int] = None  # 1-5: Ability to adapt to physical risks
    scenario_analysis_done: Optional[int] = None  # 1-5: Has CP done physical risk scenario analysis?

    # Credit Workflow Extended Fields
    acute_hazard_exposure_level: Optional[str] = None  # "low" | "medium" | "high" | "critical"
    acute_hazard_types: Optional[List[str]] = None  # e.g., ["floods", "storms", "water_stress", "extreme_heat"]
    chronic_exposure_assessment: Optional[str] = None  # Chronic climate risks assessment
    ecosystem_dependency_level: Optional[str] = None  # "none" | "low" | "medium" | "high"
    ecosystem_dependency_assessment: Optional[str] = None  # Ecosystem dependencies assessment
    adaptation_capability_level: Optional[str] = None  # "none" | "limited" | "developing" | "mature"
    adaptation_investments: Optional[str] = None  # Adaptation investments description

    rationale: str = ""
    sources: List[str] = field(default_factory=list)

    def calculate_score(self) -> float:
        """Calculate physical risk score"""
        scores = [
            self.acute_hazard_exposure,
            self.chronic_climate_exposure,
            self.ecosystem_dependency,
            self.adaptation_capability,
            self.scenario_analysis_done
        ]
        valid = [s for s in scores if s is not None]
        return sum(valid) / len(valid) if valid else 0.0


@dataclass
class EnhancedClimateScorecard:
    """
    Enhanced Climate & Environmental Risk Scorecard (SS5/25 Aligned)

    Incorporates ICBC template learnings while maintaining generic framework flexibility.
    Updated December 2025 to align with PRA SS5/25 requirements.

    SS5/25 Enhancements:
    - Risk Appetite alignment section
    - ICAAP/Capital considerations for banks
    - Enhanced litigation risk treatment (distinct channel option)
    - Enhanced scenario analysis quality assessment
    - Data quality declaration
    """
    counterparty: str
    country: str
    sector: str
    assessment_date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    prepared_by: str = ""

    # Enhanced risk assessments
    transition_preparedness: Optional[TransitionPreparedness] = None
    transition_vulnerability: Optional[TransitionVulnerability] = None
    transition_opportunity: Optional[TransitionOpportunity] = None
    physical_risk: Optional[PhysicalRiskExposure] = None

    # SS5/25 NEW: Enhanced assessments
    litigation_risk: Optional[LitigationRiskAssessment] = None
    scenario_analysis_quality: Optional[ScenarioAnalysisQuality] = None
    risk_appetite_alignment: Optional[RiskAppetiteAlignment] = None
    icaap_considerations: Optional[ICaapConsiderations] = None
    data_quality: Optional[DataQualityDeclaration] = None

    # Legacy support - overall category scores
    policy_risk_score: Optional[float] = None
    technology_risk_score: Optional[float] = None
    market_risk_score: Optional[float] = None
    legal_risk_score: Optional[float] = None

    # Additional fields
    sector_classification: str = ""
    mitigation_measures: List[str] = field(default_factory=list)
    key_risk_drivers: List[str] = field(default_factory=list)
    key_opportunities: List[str] = field(default_factory=list)
    monitoring_triggers: List[str] = field(default_factory=list)
    summary: str = ""

    # Credit Workflow Extended Fields
    assessment_type: Optional[str] = None  # "initial" | "annual_review" | "event_triggered" | "material_change"
    overall_transition_risk_score: Optional[str] = None  # "low" | "medium" | "high" | "critical"
    overall_physical_risk_score: Optional[str] = None  # "low" | "medium" | "high" | "critical"
    overall_climate_risk_rating: Optional[str] = None  # "A" | "B" | "C" | "D" | "E"
    recommended_mitigations: Optional[str] = None  # Structured mitigation text
    next_review_date: Optional[str] = None  # "YYYY-MM-DD"

    def assess_transition_preparedness(
        self,
        net_zero_target: Optional[int] = None,
        tcfd_disclosure: Optional[int] = None,
        governance_structure: Optional[int] = None,
        transition_plan: Optional[int] = None,
        capex_alignment: Optional[int] = None,
        rationale: str = "",
        sources: List[str] = None
    ) -> None:
        """
        Assess counterparty's preparedness and intent to transition

        Scoring (1-5 where 5 = worst):
        1 = Excellent (comprehensive, credible, leading practice)
        2 = Good (solid plans and governance)
        3 = Adequate (basic structures in place)
        4 = Weak (limited or aspirational only)
        5 = None (no plans, no governance, no disclosure)
        """
        self.transition_preparedness = TransitionPreparedness(
            net_zero_target=net_zero_target,
            tcfd_disclosure=tcfd_disclosure,
            governance_structure=governance_structure,
            transition_plan=transition_plan,
            capex_alignment=capex_alignment,
            rationale=rationale,
            sources=sources or []
        )

    def assess_transition_vulnerability(
        self,
        sector_carbon_intensity: Optional[int] = None,
        stranded_asset_risk: Optional[int] = None,
        policy_regulatory_risk: Optional[int] = None,
        technology_disruption: Optional[int] = None,
        market_sentiment_risk: Optional[int] = None,
        legal_litigation_risk: Optional[int] = None,
        country_transition_dependency: Optional[int] = None,
        rationale: str = "",
        sources: List[str] = None
    ) -> None:
        """
        Assess counterparty's vulnerability to transition risks

        Scoring (1-5 where 5 = worst):
        1 = Negligible (no exposure, well-positioned)
        2 = Low (minor exposure, good mitigation)
        3 = Moderate (some exposure, mitigation developing)
        4 = High (significant exposure, limited mitigation)
        5 = Critical (severe exposure, inadequate response)
        """
        self.transition_vulnerability = TransitionVulnerability(
            sector_carbon_intensity=sector_carbon_intensity,
            stranded_asset_risk=stranded_asset_risk,
            policy_regulatory_risk=policy_regulatory_risk,
            technology_disruption=technology_disruption,
            market_sentiment_risk=market_sentiment_risk,
            legal_litigation_risk=legal_litigation_risk,
            country_transition_dependency=country_transition_dependency,
            rationale=rationale,
            sources=sources or []
        )

    def assess_transition_opportunity(
        self,
        market_growth_potential: Optional[int] = None,
        green_revenue_share: Optional[int] = None,
        competitive_advantage: Optional[int] = None,
        rationale: str = "",
        sources: List[str] = None
    ) -> None:
        """
        Assess opportunities from climate transition (NEW from ICBC learning)

        Scoring (1-5 where 1 = best positioned):
        1 = Strong beneficiary (renewable energy, green tech, etc.)
        2 = Some benefit (transition enablers)
        3 = Neutral (limited impact either way)
        4 = Minor headwinds (some transition costs)
        5 = No benefit or negative (carbon-intensive, no transition path)
        """
        self.transition_opportunity = TransitionOpportunity(
            market_growth_potential=market_growth_potential,
            green_revenue_share=green_revenue_share,
            competitive_advantage=competitive_advantage,
            rationale=rationale,
            sources=sources or []
        )

    def assess_physical_risk(
        self,
        acute_hazard_exposure: Optional[int] = None,
        chronic_climate_exposure: Optional[int] = None,
        ecosystem_dependency: Optional[int] = None,
        adaptation_capability: Optional[int] = None,
        scenario_analysis_done: Optional[int] = None,
        rationale: str = "",
        sources: List[str] = None
    ) -> None:
        """
        Assess physical climate risk exposure

        Scoring (1-5 where 5 = worst):
        1 = Negligible (no exposure or excellent adaptation)
        2 = Low (minor exposure, good resilience)
        3 = Moderate (some exposure, adaptation plans)
        4 = High (significant exposure, limited adaptation)
        5 = Critical (severe exposure, no adaptation)
        """
        self.physical_risk = PhysicalRiskExposure(
            acute_hazard_exposure=acute_hazard_exposure,
            chronic_climate_exposure=chronic_climate_exposure,
            ecosystem_dependency=ecosystem_dependency,
            adaptation_capability=adaptation_capability,
            scenario_analysis_done=scenario_analysis_done,
            rationale=rationale,
            sources=sources or []
        )

    # =========================================================================
    # SS5/25 NEW ASSESSMENT METHODS
    # =========================================================================

    def set_risk_appetite_alignment(
        self,
        category: str,
        justification: str,
        portfolio_limit_impact: str = "",
        escalation_required: bool = False,
        escalation_reason: str = ""
    ) -> None:
        """
        SS5/25 Requirement: Set risk appetite alignment.

        Args:
            category: "Accept" | "Manage" | "Avoid"
            justification: Why this category is appropriate
            portfolio_limit_impact: Impact on sector/portfolio limits
            escalation_required: Whether escalation to senior management needed
            escalation_reason: Reason for escalation if required
        """
        self.risk_appetite_alignment = RiskAppetiteAlignment(
            category=category,
            justification=justification,
            portfolio_limit_impact=portfolio_limit_impact,
            escalation_required=escalation_required,
            escalation_reason=escalation_reason
        )

    def set_icaap_considerations(
        self,
        capital_relevance: str,
        icaap_treatment: str,
        materiality_justification: str
    ) -> None:
        """
        SS5/25 Requirement: Set ICAAP/capital considerations (banks only).

        Args:
            capital_relevance: "High" | "Medium" | "Low" | "Not Material"
            icaap_treatment: "Pillar 2A" | "Stress Testing" | "Not Material"
            materiality_justification: Why this treatment is appropriate
        """
        self.icaap_considerations = ICaapConsiderations(
            capital_relevance=capital_relevance,
            icaap_treatment=icaap_treatment,
            materiality_justification=materiality_justification
        )

    def assess_litigation_risk(
        self,
        treatment: str = "subset",
        score: Optional[int] = None,
        litigation_type: str = "",
        rationale: str = "",
        sources: List[str] = None
    ) -> None:
        """
        SS5/25 Requirement: Assess litigation risk with flexible treatment.

        The PRA allows firms to treat litigation as either a subset of transition
        risk OR as a distinct transmission channel.

        Args:
            treatment: "subset" (within transition vulnerability) or "distinct_channel"
            score: 1-5 if assessed as distinct channel
            litigation_type: "climate_disclosure" | "greenwashing" | "physical_damage" | "duty_of_care" | "other"
            rationale: Assessment rationale
            sources: Data sources used
        """
        self.litigation_risk = LitigationRiskAssessment(
            treatment=treatment,
            score=score,
            litigation_type=litigation_type,
            rationale=rationale,
            sources=sources or []
        )

    def assess_scenario_analysis_quality(
        self,
        analysis_conducted: Optional[int] = None,
        results_integrated: Optional[int] = None,
        horizons_appropriate: Optional[int] = None,
        documentation_quality: Optional[int] = None,
        rationale: str = "",
        sources: List[str] = None
    ) -> None:
        """
        SS5/25 Requirement: Enhanced scenario analysis quality assessment.

        Assesses not just whether counterparty conducts CSA, but quality and usage.

        Scoring (1-5 where 5 = worst):
        1 = Excellent (comprehensive analysis informing strategy)
        2 = Good (solid analysis with clear strategic linkage)
        3 = Adequate (basic analysis conducted)
        4 = Weak (limited or superficial analysis)
        5 = None (no scenario analysis conducted)
        """
        self.scenario_analysis_quality = ScenarioAnalysisQuality(
            analysis_conducted=analysis_conducted,
            results_integrated=results_integrated,
            horizons_appropriate=horizons_appropriate,
            documentation_quality=documentation_quality,
            rationale=rationale,
            sources=sources or []
        )

    def set_data_quality_declaration(
        self,
        primary_sources: List[str],
        proxies_used: List[Dict[str, str]] = None,
        data_gaps: List[str] = None,
        uncertainty_acknowledgment: str = ""
    ) -> None:
        """
        SS5/25 Requirement: Document data quality and limitations.

        Args:
            primary_sources: List of primary data sources used
            proxies_used: List of proxies [{"data_point": "...", "proxy": "...", "limitation": "..."}]
            data_gaps: List of identified data gaps
            uncertainty_acknowledgment: Statement acknowledging data uncertainty
        """
        self.data_quality = DataQualityDeclaration(
            primary_sources=primary_sources,
            proxies_used=proxies_used or [],
            data_gaps=data_gaps or [],
            uncertainty_acknowledgment=uncertainty_acknowledgment
        )

    # =========================================================================
    # CALCULATION METHODS
    # =========================================================================

    def calculate_transition_score(self) -> float:
        """
        Calculate overall transition risk score

        Combines preparedness (weight 30%), vulnerability (60%), opportunity (10%)
        """
        prep_score = self.transition_preparedness.calculate_score() if self.transition_preparedness else 3.0
        vuln_score = self.transition_vulnerability.calculate_score() if self.transition_vulnerability else 3.0
        opp_score = self.transition_opportunity.calculate_score() if self.transition_opportunity else 3.0

        # Preparedness: lower = better prepared = lower risk
        # Vulnerability: higher = more vulnerable = higher risk
        # Opportunity: lower = more opportunity = offsets some risk

        # Weight: 30% prep, 60% vuln, 10% opportunity offset
        weighted_score = (0.3 * prep_score) + (0.6 * vuln_score) - (0.1 * (5 - opp_score))

        return max(1.0, min(5.0, weighted_score))  # Clamp to 1-5 range

    def calculate_physical_score(self) -> float:
        """Calculate overall physical risk score"""
        return self.physical_risk.calculate_score() if self.physical_risk else 3.0

    def calculate_overall_score(self) -> float:
        """
        Calculate overall climate risk score
        Default: 60% transition, 40% physical (0-5 year horizon)
        """
        transition = self.calculate_transition_score()
        physical = self.calculate_physical_score()

        # Sector-based weighting (from original framework)
        if self.sector.lower() in ["financial institutions", "services"]:
            return 0.7 * transition + 0.3 * physical
        elif self.sector.lower() in ["agriculture", "real estate", "infrastructure"]:
            return 0.4 * transition + 0.6 * physical
        else:
            return 0.6 * transition + 0.4 * physical

    def requires_rating_override(self) -> Tuple[bool, str, int]:
        """Determine if rating override required (from original framework)"""
        overall_score = self.calculate_overall_score()

        # Check prohibited sectors
        if self.sector_classification == "Prohibited":
            return (True, "Downward", 3)

        if overall_score > 3.5:
            notches = 2 if overall_score > 4.0 else 1
            return (True, "Downward", notches)

        if overall_score > 2.5 and self.sector_classification == "Restricted":
            return (True, "Downward", 1)

        return (False, "None", 0)

    def generate_enhanced_scorecard(self) -> str:
        """Generate enhanced scorecard incorporating ICBC learnings and SS5/25 requirements"""

        transition_score = self.calculate_transition_score()
        physical_score = self.calculate_physical_score()
        overall_score = self.calculate_overall_score()
        override_req, override_dir, override_notches = self.requires_rating_override()

        output = f"""# ENHANCED CLIMATE & ENVIRONMENTAL RISK SCORECARD
## PRA SS5/25 Aligned (December 2025)

**Counterparty:** {self.counterparty}
**Country:** {self.country}
**Sector:** {self.sector}
**Assessment Date:** {self.assessment_date}
**Prepared By:** {self.prepared_by}

---

## TRANSITION RISK ASSESSMENT

### 1. Transition Preparedness (Intent & Capability)

*Assesses the counterparty's preparedness and intent to transition to a low-carbon economy*

"""

        if self.transition_preparedness:
            prep = self.transition_preparedness
            output += f"""
| Assessment Factor | Score | Status |
|-------------------|-------|--------|
| Net-Zero Target & Credibility | {prep.net_zero_target or 'N/A'}/5 | {self._score_label(prep.net_zero_target)} |
| Climate Disclosure Quality (TCFD/CDP) | {prep.tcfd_disclosure or 'N/A'}/5 | {self._score_label(prep.tcfd_disclosure)} |
| Governance Structure | {prep.governance_structure or 'N/A'}/5 | {self._score_label(prep.governance_structure)} |
| Transition Plan Credibility | {prep.transition_plan or 'N/A'}/5 | {self._score_label(prep.transition_plan)} |
| Capex Alignment with Paris Goals | {prep.capex_alignment or 'N/A'}/5 | {self._score_label(prep.capex_alignment)} |

**Preparedness Score:** {prep.calculate_score():.1f}/5

**Rationale:** {prep.rationale}
"""

        output += "\n### 2. Transition Vulnerability (Exposure & Risk)\n\n"
        output += "*Assesses exposure to transition risks regardless of preparedness*\n\n"

        if self.transition_vulnerability:
            vuln = self.transition_vulnerability
            output += f"""
| Risk Factor | Score | Level |
|-------------|-------|-------|
| Sector Carbon Intensity | {vuln.sector_carbon_intensity or 'N/A'}/5 | {self._score_label(vuln.sector_carbon_intensity)} |
| Stranded Asset Risk | {vuln.stranded_asset_risk or 'N/A'}/5 | {self._score_label(vuln.stranded_asset_risk)} |
| Policy & Regulatory Pressure | {vuln.policy_regulatory_risk or 'N/A'}/5 | {self._score_label(vuln.policy_regulatory_risk)} |
| Technology Disruption Vulnerability | {vuln.technology_disruption or 'N/A'}/5 | {self._score_label(vuln.technology_disruption)} |
| Market & Investor Sentiment Risk | {vuln.market_sentiment_risk or 'N/A'}/5 | {self._score_label(vuln.market_sentiment_risk)} |
| Legal & Litigation Risk | {vuln.legal_litigation_risk or 'N/A'}/5 | {self._score_label(vuln.legal_litigation_risk)} |
| Country Transition Dependency | {vuln.country_transition_dependency or 'N/A'}/5 | {self._score_label(vuln.country_transition_dependency)} |

**Vulnerability Score:** {vuln.calculate_score():.1f}/5

**Rationale:** {vuln.rationale}
"""

        output += "\n### 3. Transition Opportunity Assessment\n\n"
        output += "*Assesses potential benefits from climate transition (offsets risk)*\n\n"

        if self.transition_opportunity:
            opp = self.transition_opportunity
            output += f"""
| Opportunity Factor | Score | Positioning |
|-------------------|-------|-------------|
| Low-Carbon Market Growth Potential | {opp.market_growth_potential or 'N/A'}/5 | {self._opportunity_label(opp.market_growth_potential)} |
| Green Revenue Share | {opp.green_revenue_share or 'N/A'}/5 | {self._opportunity_label(opp.green_revenue_share)} |
| Competitive Advantage in Transition | {opp.competitive_advantage or 'N/A'}/5 | {self._opportunity_label(opp.competitive_advantage)} |

**Opportunity Score:** {opp.calculate_score():.1f}/5 (lower = better positioned)

**Rationale:** {opp.rationale}
"""

        output += f"""
**OVERALL TRANSITION RISK SCORE:** **{transition_score:.1f}/5**

*Calculation: 30% Preparedness + 60% Vulnerability - 10% Opportunity Offset*

---

## PHYSICAL RISK ASSESSMENT

*Assesses exposure to physical climate events and adaptation capability*

"""

        if self.physical_risk:
            phys = self.physical_risk
            output += f"""
| Risk Factor | Score | Level |
|-------------|-------|-------|
| Acute Climate Hazard Exposure | {phys.acute_hazard_exposure or 'N/A'}/5 | {self._score_label(phys.acute_hazard_exposure)} |
| Chronic Climate Change Exposure | {phys.chronic_climate_exposure or 'N/A'}/5 | {self._score_label(phys.chronic_climate_exposure)} |
| Ecosystem Dependency & Vulnerability | {phys.ecosystem_dependency or 'N/A'}/5 | {self._score_label(phys.ecosystem_dependency)} |
| Adaptation Capability | {phys.adaptation_capability or 'N/A'}/5 | {self._score_label(phys.adaptation_capability)} |
| Physical Risk Scenario Analysis | {phys.scenario_analysis_done or 'N/A'}/5 | {self._score_label(phys.scenario_analysis_done)} |

**Rationale:** {phys.rationale}
"""

        output += f"""
**OVERALL PHYSICAL RISK SCORE:** **{physical_score:.1f}/5**

---

## COMBINED ASSESSMENT

| Metric | Score |
|--------|-------|
| **Transition Risk Score** | **{transition_score:.1f}/5** |
| **Physical Risk Score** | **{physical_score:.1f}/5** |
| **Overall Climate Risk Score** | **{overall_score:.1f}/5** |
| Sector Classification | {self.sector_classification or 'None'} |
| Rating Override Required | {'**Yes**' if override_req else 'No'} |
| Override Direction | {override_dir} |
| Override Notches | {override_notches if override_req else 'N/A'} |

"""

        # SS5/25: Litigation Risk (if assessed as distinct channel)
        if self.litigation_risk and self.litigation_risk.treatment == "distinct_channel":
            lit = self.litigation_risk
            output += f"""
---

## LITIGATION RISK ASSESSMENT (SS5/25 Distinct Channel)

*Per SS5/25, litigation risk assessed as distinct transmission channel*

| Factor | Assessment |
|--------|------------|
| Treatment | Distinct Channel |
| Litigation Type | {lit.litigation_type or 'Not specified'} |
| Score | {lit.score or 'N/A'}/5 |

**Rationale:** {lit.rationale}

"""

        # SS5/25: Enhanced Scenario Analysis Quality
        if self.scenario_analysis_quality:
            saq = self.scenario_analysis_quality
            output += f"""
---

## SCENARIO ANALYSIS QUALITY (SS5/25 Enhanced)

*SS5/25 requires assessment of how CSA results inform actual decision-making*

| Factor | Score | Assessment |
|--------|-------|------------|
| Analysis Conducted | {saq.analysis_conducted or 'N/A'}/5 | {self._score_label(saq.analysis_conducted)} |
| Results Integrated into Strategy | {saq.results_integrated or 'N/A'}/5 | {self._score_label(saq.results_integrated)} |
| Time Horizons Appropriate | {saq.horizons_appropriate or 'N/A'}/5 | {self._score_label(saq.horizons_appropriate)} |
| Documentation Quality | {saq.documentation_quality or 'N/A'}/5 | {self._score_label(saq.documentation_quality)} |

**CSA Quality Score:** {saq.calculate_score():.1f}/5

**Rationale:** {saq.rationale}

"""

        # SS5/25: Risk Appetite Alignment
        if self.risk_appetite_alignment:
            ra = self.risk_appetite_alignment
            output += f"""
---

## RISK APPETITE ALIGNMENT (SS5/25)

*SS5/25 requires explicit alignment with firm's climate risk appetite framework*

| Factor | Assessment |
|--------|------------|
| **Appetite Category** | **{ra.category}** |
| Justification | {ra.justification} |
| Portfolio Limit Impact | {ra.portfolio_limit_impact or 'N/A'} |
| Escalation Required | {'**Yes** - ' + ra.escalation_reason if ra.escalation_required else 'No'} |

"""

        # SS5/25: ICAAP Considerations (Banks)
        if self.icaap_considerations:
            ic = self.icaap_considerations
            output += f"""
---

## CAPITAL & ICAAP CONSIDERATIONS (SS5/25 - Banks)

*SS5/25 requires banks to evidence climate risk materiality in ICAAPs*

| Factor | Assessment |
|--------|------------|
| **Capital Relevance** | **{ic.capital_relevance}** |
| ICAAP Treatment | {ic.icaap_treatment} |
| Materiality Justification | {ic.materiality_justification} |

"""

        # SS5/25: Data Quality Declaration
        if self.data_quality:
            dq = self.data_quality
            output += f"""
---

## DATA QUALITY DECLARATION (SS5/25)

*SS5/25 requires documentation of data sources, proxies, and limitations*

### Primary Data Sources
"""
            for source in dq.primary_sources:
                output += f"- {source}\n"

            if dq.proxies_used:
                output += "\n### Proxies Used\n"
                output += "| Data Point | Proxy Applied | Limitation |\n"
                output += "|------------|---------------|------------|\n"
                for proxy in dq.proxies_used:
                    output += f"| {proxy.get('data_point', 'N/A')} | {proxy.get('proxy', 'N/A')} | {proxy.get('limitation', 'N/A')} |\n"

            if dq.data_gaps:
                output += "\n### Identified Data Gaps\n"
                for gap in dq.data_gaps:
                    output += f"- {gap}\n"

            if dq.uncertainty_acknowledgment:
                output += f"\n### Uncertainty Acknowledgment\n{dq.uncertainty_acknowledgment}\n"

        output += f"""
---

## SUMMARY & RECOMMENDATIONS

{self.summary}

---

## KEY RISK DRIVERS

"""

        for driver in self.key_risk_drivers:
            output += f"- {driver}\n"

        if self.key_opportunities:
            output += "\n## KEY OPPORTUNITIES\n\n"
            for opp in self.key_opportunities:
                output += f"- {opp}\n"

        output += "\n## MITIGATION MEASURES IN PLACE\n\n"

        for measure in self.mitigation_measures:
            output += f"- {measure}\n"

        output += "\n## MONITORING & REVIEW TRIGGERS\n\n"

        for trigger in self.monitoring_triggers:
            output += f"- {trigger}\n"

        # Add regulatory reference footer
        output += """
---

## REGULATORY REFERENCES

This scorecard is aligned with:
- **PRA SS5/25** - Enhancing banks' and insurers' approaches to managing climate-related risks (December 2025)
- **BCBS Principles** - Principles for effective management and supervision of climate-related financial risks
- **ISSB IFRS S2** - Climate-related Disclosures

*Scorecard generated by Risk Agents Platform*
"""

        return output

    def _score_label(self, score: Optional[int]) -> str:
        """Convert score to descriptive label"""
        if score is None:
            return "Not Assessed"
        elif score <= 1.5:
            return "Excellent"
        elif score <= 2.5:
            return "Good"
        elif score <= 3.5:
            return "Adequate"
        elif score <= 4.5:
            return "Weak"
        else:
            return "None/Critical"

    def _opportunity_label(self, score: Optional[int]) -> str:
        """Convert opportunity score to label (reverse: low = good)"""
        if score is None:
            return "Not Assessed"
        elif score <= 1.5:
            return "Strong Beneficiary"
        elif score <= 2.5:
            return "Some Benefit"
        elif score <= 3.5:
            return "Neutral"
        elif score <= 4.5:
            return "Limited Benefit"
        else:
            return "No Benefit"

    # =========================================================================
    # CREDIT WORKFLOW JSON OUTPUT
    # =========================================================================

    def to_credit_workflow_json(
        self,
        confidence_tracker: Optional[ConfidenceTracker] = None
    ) -> str:
        """
        Generate JSON output for Credit Risk Workflow System integration.

        Returns the scorecard in the exact JSON format required by the
        credit_workflow system, including all ~80 fields, confidence scores,
        and generation notes.

        Args:
            confidence_tracker: Optional ConfidenceTracker with pre-set scores.
                               If None, creates default confidence based on data presence.

        Returns:
            JSON string with scorecard_data, confidence_scores, and generation_notes
        """
        # Create confidence tracker if not provided
        if confidence_tracker is None:
            confidence_tracker = ConfidenceTracker()

        # Calculate overall scores
        transition_score = self.calculate_transition_score()
        physical_score = self.calculate_physical_score()
        overall_score = self.calculate_overall_score()

        # Build scorecard_data
        scorecard_data: Dict[str, Any] = {}

        # SECTION 1: Assessment Context
        scorecard_data["assessment_type"] = self.assessment_type or "initial"

        # SECTION 2: Transition Risk - Preparedness
        prep = self.transition_preparedness
        if prep:
            # Boolean/target fields
            scorecard_data["net_zero_target_exists"] = prep.net_zero_target_exists if prep.net_zero_target_exists is not None else (prep.net_zero_target is not None and prep.net_zero_target <= 4)
            scorecard_data["net_zero_target_year"] = prep.net_zero_target_year
            scorecard_data["net_zero_target_scope"] = prep.net_zero_target_scope
            scorecard_data["net_zero_science_based"] = prep.net_zero_science_based
            scorecard_data["net_zero_score"] = prep.net_zero_target

            # TCFD disclosure
            scorecard_data["tcfd_disclosure_level"] = prep.tcfd_disclosure_level or score_to_tcfd_level(prep.tcfd_disclosure)
            scorecard_data["tcfd_disclosure_score"] = prep.tcfd_disclosure

            # Climate governance
            scorecard_data["climate_governance_board"] = prep.climate_governance_board
            scorecard_data["climate_governance_exec_accountability"] = prep.climate_governance_exec_accountability
            scorecard_data["climate_governance_incentives_linked"] = prep.climate_governance_incentives_linked
            scorecard_data["climate_governance_score"] = prep.governance_structure

            # Transition plan
            scorecard_data["transition_plan_exists"] = prep.transition_plan_exists if prep.transition_plan_exists is not None else (prep.transition_plan is not None and prep.transition_plan <= 4)
            scorecard_data["transition_plan_published"] = prep.transition_plan_published
            scorecard_data["transition_plan_milestones"] = prep.transition_plan_milestones
            scorecard_data["transition_plan_score"] = prep.transition_plan

            # Green capex
            scorecard_data["green_capex_percentage"] = prep.green_capex_percentage
            scorecard_data["capex_alignment_trajectory"] = prep.capex_alignment_trajectory
            scorecard_data["capex_alignment_score"] = prep.capex_alignment
        else:
            # Set all preparedness fields to null
            for field in ["net_zero_target_exists", "net_zero_target_year", "net_zero_target_scope",
                         "net_zero_science_based", "net_zero_score", "tcfd_disclosure_level",
                         "tcfd_disclosure_score", "climate_governance_board", "climate_governance_exec_accountability",
                         "climate_governance_incentives_linked", "climate_governance_score",
                         "transition_plan_exists", "transition_plan_published", "transition_plan_milestones",
                         "transition_plan_score", "green_capex_percentage", "capex_alignment_trajectory",
                         "capex_alignment_score"]:
                scorecard_data[field] = None
                confidence_tracker.set_null_confidence(field)

        # SECTION 3: Transition Risk - Vulnerability
        vuln = self.transition_vulnerability
        if vuln:
            # Carbon intensity
            scorecard_data["carbon_intensity_scope1"] = vuln.carbon_intensity_scope1
            scorecard_data["carbon_intensity_scope2"] = vuln.carbon_intensity_scope2
            scorecard_data["carbon_intensity_scope3"] = vuln.carbon_intensity_scope3
            scorecard_data["carbon_intensity_trend"] = vuln.carbon_intensity_trend
            scorecard_data["carbon_intensity_score"] = vuln.sector_carbon_intensity

            # Stranded assets
            scorecard_data["stranded_asset_exposure"] = vuln.stranded_asset_exposure or score_to_enum_exposure(vuln.stranded_asset_risk)
            scorecard_data["stranded_asset_types"] = vuln.stranded_asset_types
            scorecard_data["stranded_asset_score"] = vuln.stranded_asset_risk

            # Policy pressure
            scorecard_data["policy_pressure_jurisdictions"] = vuln.policy_pressure_jurisdictions
            scorecard_data["policy_pressure_carbon_pricing_exposure"] = vuln.policy_pressure_carbon_pricing_exposure
            scorecard_data["policy_pressure_score"] = vuln.policy_regulatory_risk

            # Tech disruption
            scorecard_data["tech_disruption_risk_level"] = vuln.tech_disruption_risk_level or score_to_enum_risk(float(vuln.technology_disruption) if vuln.technology_disruption else None)
            scorecard_data["tech_disruption_assessment"] = vuln.tech_disruption_assessment
            scorecard_data["tech_disruption_score"] = vuln.technology_disruption

            # Market sentiment
            scorecard_data["market_sentiment_esg_rating"] = vuln.market_sentiment_esg_rating
            scorecard_data["market_sentiment_investor_pressure"] = vuln.market_sentiment_investor_pressure or score_to_enum_exposure(vuln.market_sentiment_risk)
            scorecard_data["market_sentiment_score"] = vuln.market_sentiment_risk

            # Litigation
            scorecard_data["litigation_current_cases"] = vuln.litigation_current_cases
            scorecard_data["litigation_historical_cases"] = vuln.litigation_historical_cases
            scorecard_data["litigation_exposure_assessment"] = vuln.litigation_exposure_assessment
            scorecard_data["litigation_score"] = vuln.legal_litigation_risk

            # Country dependency
            scorecard_data["country_dependency_high_risk_revenue"] = vuln.country_dependency_high_risk_revenue
            scorecard_data["country_dependency_score"] = vuln.country_transition_dependency
        else:
            # Set all vulnerability fields to null
            for field in ["carbon_intensity_scope1", "carbon_intensity_scope2", "carbon_intensity_scope3",
                         "carbon_intensity_trend", "carbon_intensity_score", "stranded_asset_exposure",
                         "stranded_asset_types", "stranded_asset_score", "policy_pressure_jurisdictions",
                         "policy_pressure_carbon_pricing_exposure", "policy_pressure_score",
                         "tech_disruption_risk_level", "tech_disruption_assessment", "tech_disruption_score",
                         "market_sentiment_esg_rating", "market_sentiment_investor_pressure", "market_sentiment_score",
                         "litigation_current_cases", "litigation_historical_cases", "litigation_exposure_assessment",
                         "litigation_score", "country_dependency_high_risk_revenue", "country_dependency_score"]:
                scorecard_data[field] = None
                confidence_tracker.set_null_confidence(field)

        # SECTION 4: Transition Risk - Opportunity
        opp = self.transition_opportunity
        if opp:
            scorecard_data["green_market_growth_potential"] = opp.green_market_growth_potential or score_to_growth_potential(opp.market_growth_potential)
            scorecard_data["green_market_growth_assessment"] = opp.green_market_growth_assessment
            scorecard_data["green_market_growth_score"] = opp.market_growth_potential

            scorecard_data["green_revenue_percentage"] = opp.green_revenue_percentage
            scorecard_data["green_revenue_trend"] = opp.green_revenue_trend or score_to_revenue_trend(opp.green_revenue_share)
            scorecard_data["green_revenue_score"] = opp.green_revenue_share

            scorecard_data["competitive_advantage_assessment"] = opp.competitive_advantage_assessment
            scorecard_data["competitive_advantage_score"] = opp.competitive_advantage
        else:
            for field in ["green_market_growth_potential", "green_market_growth_assessment", "green_market_growth_score",
                         "green_revenue_percentage", "green_revenue_trend", "green_revenue_score",
                         "competitive_advantage_assessment", "competitive_advantage_score"]:
                scorecard_data[field] = None
                confidence_tracker.set_null_confidence(field)

        # SECTION 5: Physical Risk Assessment
        phys = self.physical_risk
        if phys:
            scorecard_data["acute_hazard_exposure"] = phys.acute_hazard_exposure_level or score_to_enum_risk(float(phys.acute_hazard_exposure) if phys.acute_hazard_exposure else None)
            scorecard_data["acute_hazard_types"] = phys.acute_hazard_types or []
            scorecard_data["acute_hazard_score"] = phys.acute_hazard_exposure

            scorecard_data["chronic_exposure_assessment"] = phys.chronic_exposure_assessment
            scorecard_data["chronic_exposure_score"] = phys.chronic_climate_exposure

            scorecard_data["ecosystem_dependency_level"] = phys.ecosystem_dependency_level or score_to_enum_exposure(phys.ecosystem_dependency)
            scorecard_data["ecosystem_dependency_assessment"] = phys.ecosystem_dependency_assessment
            scorecard_data["ecosystem_dependency_score"] = phys.ecosystem_dependency

            scorecard_data["adaptation_capability_level"] = phys.adaptation_capability_level or score_to_adaptation_level(phys.adaptation_capability)
            scorecard_data["adaptation_investments"] = phys.adaptation_investments
            scorecard_data["adaptation_capability_score"] = phys.adaptation_capability
        else:
            for field in ["acute_hazard_exposure", "acute_hazard_types", "acute_hazard_score",
                         "chronic_exposure_assessment", "chronic_exposure_score",
                         "ecosystem_dependency_level", "ecosystem_dependency_assessment", "ecosystem_dependency_score",
                         "adaptation_capability_level", "adaptation_investments", "adaptation_capability_score"]:
                scorecard_data[field] = None if field != "acute_hazard_types" else []
                confidence_tracker.set_null_confidence(field)

        # Scenario Analysis
        saq = self.scenario_analysis_quality
        if saq:
            scorecard_data["scenario_analysis_conducted"] = saq.scenario_analysis_conducted if saq.scenario_analysis_conducted is not None else (saq.analysis_conducted is not None and saq.analysis_conducted <= 4)
            scorecard_data["scenario_analysis_scenarios"] = saq.scenario_analysis_scenarios or []
            scorecard_data["scenario_analysis_time_horizons"] = saq.scenario_analysis_time_horizons or []
            scorecard_data["scenario_analysis_integration"] = saq.scenario_analysis_integration
            scorecard_data["scenario_analysis_score"] = int(saq.calculate_score()) if saq.calculate_score() > 0 else None
        else:
            scorecard_data["scenario_analysis_conducted"] = None
            scorecard_data["scenario_analysis_scenarios"] = []
            scorecard_data["scenario_analysis_time_horizons"] = []
            scorecard_data["scenario_analysis_integration"] = None
            scorecard_data["scenario_analysis_score"] = None
            for field in ["scenario_analysis_conducted", "scenario_analysis_scenarios",
                         "scenario_analysis_time_horizons", "scenario_analysis_integration", "scenario_analysis_score"]:
                confidence_tracker.set_null_confidence(field)

        # SECTION 6: Risk Appetite Alignment
        ra = self.risk_appetite_alignment
        if ra:
            scorecard_data["risk_appetite_category"] = ra.risk_appetite_category or ra.category.lower() if ra.category else None
            scorecard_data["risk_appetite_justification"] = ra.risk_appetite_justification or ra.justification
            scorecard_data["risk_appetite_conditions"] = ra.risk_appetite_conditions
        else:
            scorecard_data["risk_appetite_category"] = None
            scorecard_data["risk_appetite_justification"] = None
            scorecard_data["risk_appetite_conditions"] = None
            for field in ["risk_appetite_category", "risk_appetite_justification", "risk_appetite_conditions"]:
                confidence_tracker.set_null_confidence(field)

        # SECTION 7: Capital & ICAAP Considerations
        ic = self.icaap_considerations
        if ic:
            scorecard_data["pillar_2_treatment"] = ic.pillar_2_treatment or score_to_pillar2_treatment(overall_score)
            scorecard_data["icaap_materiality_assessment"] = ic.icaap_materiality_assessment or ic.materiality_justification
            scorecard_data["capital_add_on_recommendation"] = ic.capital_add_on_recommendation
        else:
            scorecard_data["pillar_2_treatment"] = score_to_pillar2_treatment(overall_score)
            scorecard_data["icaap_materiality_assessment"] = None
            scorecard_data["capital_add_on_recommendation"] = None
            for field in ["icaap_materiality_assessment", "capital_add_on_recommendation"]:
                confidence_tracker.set_null_confidence(field)

        # SECTION 8: Data Quality Declaration
        dq = self.data_quality
        if dq:
            scorecard_data["data_sources"] = dq.primary_sources
            scorecard_data["data_proxies_used"] = "; ".join([f"{p.get('data_point', '')}: {p.get('proxy', '')}" for p in dq.proxies_used]) if dq.proxies_used else None
            scorecard_data["data_gaps_identified"] = "; ".join(dq.data_gaps) if dq.data_gaps else None
            scorecard_data["data_quality_overall"] = "good" if len(dq.data_gaps) < 3 else "fair" if len(dq.data_gaps) < 6 else "poor"
        else:
            scorecard_data["data_sources"] = []
            scorecard_data["data_proxies_used"] = None
            scorecard_data["data_gaps_identified"] = None
            scorecard_data["data_quality_overall"] = "poor"
            for field in ["data_sources", "data_proxies_used", "data_gaps_identified", "data_quality_overall"]:
                confidence_tracker.set_null_confidence(field)

        # SECTION 9: Summary & Recommendations
        scorecard_data["overall_transition_risk_score"] = self.overall_transition_risk_score or score_to_enum_risk(transition_score)
        scorecard_data["overall_physical_risk_score"] = self.overall_physical_risk_score or score_to_enum_risk(physical_score)
        scorecard_data["overall_climate_risk_rating"] = self.overall_climate_risk_rating or score_to_rating(overall_score)

        # Key risk drivers - join list to structured text
        scorecard_data["key_risk_drivers"] = " ".join([f"{i+1}) {driver};" for i, driver in enumerate(self.key_risk_drivers)]) if self.key_risk_drivers else None

        # Key opportunities
        scorecard_data["key_opportunities"] = " ".join([f"{i+1}) {opp};" for i, opp in enumerate(self.key_opportunities)]) if self.key_opportunities else None

        # Recommended mitigations
        scorecard_data["recommended_mitigations"] = self.recommended_mitigations or (" ".join([f"{i+1}) {m};" for i, m in enumerate(self.mitigation_measures)]) if self.mitigation_measures else None)

        # Monitoring triggers
        scorecard_data["monitoring_triggers"] = " ".join([f"{i+1}) {t};" for i, t in enumerate(self.monitoring_triggers)]) if self.monitoring_triggers else None

        # Next review date
        scorecard_data["next_review_date"] = self.next_review_date or (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")

        # Build confidence_scores dictionary
        # Set default confidence for all fields that haven't been explicitly set
        all_fields = list(scorecard_data.keys())
        for field in all_fields:
            if field not in confidence_tracker.scores:
                value = scorecard_data.get(field)
                if value is None or value == [] or value == "":
                    confidence_tracker.set_null_confidence(field)
                else:
                    # Default to medium confidence for populated fields
                    confidence_tracker.set_from_source(field, "derived")

        # Build generation notes
        generation_notes = self._generate_generation_notes(scorecard_data, confidence_tracker)

        # Build final output
        output = {
            "scorecard_data": scorecard_data,
            "confidence_scores": confidence_tracker.to_dict(),
            "generation_notes": generation_notes
        }

        return json.dumps(output, indent=2, default=str)

    def _generate_generation_notes(
        self,
        scorecard_data: Dict[str, Any],
        confidence_tracker: ConfidenceTracker
    ) -> str:
        """Generate explanatory notes about the scorecard generation."""
        # Count data quality
        null_fields = sum(1 for v in scorecard_data.values() if v is None or v == [] or v == "")
        total_fields = len(scorecard_data)
        populated_fields = total_fields - null_fields

        # Collect low confidence fields
        low_confidence_fields = [k for k, v in confidence_tracker.scores.items() if v < 0.5]

        # Build notes
        notes = f"Comprehensive PRA SS5/25-compliant climate scorecard generated for {self.counterparty}. "
        notes += f"Assessment covers {populated_fields}/{total_fields} fields. "

        if self.data_quality and self.data_quality.primary_sources:
            notes += f"Key data sources: {', '.join(self.data_quality.primary_sources[:3])}. "

        if low_confidence_fields:
            notes += f"Fields with low confidence (< 0.5) requiring analyst verification: {', '.join(low_confidence_fields[:5])}{'...' if len(low_confidence_fields) > 5 else ''}. "

        if self.data_quality and self.data_quality.data_gaps:
            notes += f"Data gaps identified: {'; '.join(self.data_quality.data_gaps[:3])}. "

        notes += "Confidence levels reflect data availability and verification status."

        return notes


def example_gcb_enhanced():
    """Example: Enhanced scorecard for GCB Bank"""

    scorecard = EnhancedClimateScorecard(
        counterparty="GCB Bank Ltd",
        country="Ghana",
        sector="Financial Institutions",
        prepared_by="Front Office Credit Team"
    )

    # Transition Preparedness (NEW structure)
    scorecard.assess_transition_preparedness(
        net_zero_target=5,  # No commitment
        tcfd_disclosure=5,  # No disclosure
        governance_structure=3,  # Basic ESG committee
        transition_plan=4,  # Limited plans
        capex_alignment=3,  # Neutral (FI with minimal direct emissions)
        rationale="GCB has limited climate governance. ESG committee exists but no TCFD disclosure, no net-zero target, limited transition planning. As FI with minimal Scope 1/2 emissions, direct transition planning less critical than portfolio-level management.",
        sources=["GCB Annual Report 2023", "Public website review"]
    )

    # Transition Vulnerability
    scorecard.assess_transition_vulnerability(
        sector_carbon_intensity=2,  # Low for universal bank
        stranded_asset_risk=2,  # Low direct risk
        policy_regulatory_risk=3,  # Moderate - Ghana developing regs
        technology_disruption=2,  # Low for banking sector
        market_sentiment_risk=3,  # Moderate - ESG pressure building
        legal_litigation_risk=1,  # Very low in Ghana
        country_transition_dependency=4,  # Ghana dependent on mining/agriculture
        rationale="As universal bank, direct carbon intensity low. However, portfolio exposure to agriculture (climate-vulnerable) and Ghana's economic dependence on mining/cocoa creates indirect transition risk through sovereign and borrower stress.",
        sources=["Ghana NDC", "World Bank Ghana Economic Profile"]
    )

    # Transition Opportunity (NEW)
    scorecard.assess_transition_opportunity(
        market_growth_potential=3,  # Neutral - limited green finance yet
        green_revenue_share=4,  # Low green product penetration
        competitive_advantage=3,  # No particular advantage
        rationale="Limited transition opportunities currently. Green finance market underdeveloped in Ghana. No particular competitive positioning in sustainable finance vs peers.",
        sources=["Ghana Green Bond Market Review"]
    )

    # Physical Risk
    scorecard.assess_physical_risk(
        acute_hazard_exposure=4,  # High - coastal flooding
        chronic_climate_exposure=3,  # Moderate - agricultural impacts
        ecosystem_dependency=2,  # Low direct dependency
        adaptation_capability=3,  # Moderate - some resilience
        scenario_analysis_done=5,  # No scenario analysis by GCB
        rationale="Ghana faces significant coastal flooding risk (Accra). Agricultural sector borrowers vulnerable to changing rainfall. GCB has not conducted climate scenario analysis on portfolio.",
        sources=["World Bank Ghana Climate Profile", "IPCC AR6 West Africa"]
    )

    # Summary
    scorecard.summary = """
GCB Bank demonstrates LOW-MODERATE climate and environmental risk (Overall Score: 2.6/5).

**Transition Risk (2.4/5 - LOW-MODERATE):**
- Preparedness is weak (4.0/5) with no TCFD disclosure or net-zero commitment
- Vulnerability is moderate (2.7/5) primarily through indirect exposure
- Limited transition opportunities (3.7/5)
- As FI with minimal direct emissions, transition risk manifests through portfolio

**Physical Risk (3.4/5 - MODERATE):**
- Coastal flooding exposure material for Accra-based operations and borrowers
- Agricultural loan portfolio vulnerable to climate impacts
- No climate scenario analysis conducted by GCB

**NO DOWNWARD RATING OVERRIDE REQUIRED** - Overall score of 2.6/5 appropriate for Ghanaian universal bank with limited carbon-intensive exposure. However, recommend monitoring agricultural NPLs and encouraging GCB to develop climate risk management capabilities.

**Key Difference from Previous Assessment:** New structure reveals that while GCB has weak preparedness/governance, its actual vulnerability is moderate due to sector positioning. Sovereign/country risk channel more material than direct transition risk.
"""

    scorecard.key_risk_drivers = [
        "Weak climate governance and disclosure (no TCFD, no net-zero target, no scenario analysis)",
        "Coastal flooding exposure affecting Accra operations and real estate collateral",
        "Agricultural loan portfolio vulnerable to changing rainfall and temperature",
        "Country dependency on climate-vulnerable sectors (mining, agriculture) creates sovereign transmission",
        "Indirect transition risk through Ghanaian government bond holdings (33% of assets)"
    ]

    scorecard.key_opportunities = [
        "Potential to lead green finance market in Ghana as it develops",
        "Government ownership may facilitate green credit lines or blended finance",
        "Agricultural transition finance could be growth area"
    ]

    scorecard.mitigation_measures = [
        "Diversified loan portfolio reduces single-sector climate concentration",
        "Strong capital buffers (16% TCR) provide cushion for climate-related losses",
        "Government ownership (51%) provides implicit support for climate shocks"
    ]

    scorecard.monitoring_triggers = [
        "Annual review or upon material climate events",
        "Bank of Ghana climate risk guidelines implementation",
        "Agricultural NPL deterioration > 25% YoY",
        "Introduction of TCFD requirements or climate disclosure mandates in Ghana"
    ]

    return scorecard


if __name__ == "__main__":
    print("=" * 80)
    print("ENHANCED CLIMATE SCORECARD - GCB BANK EXAMPLE")
    print("=" * 80)
    print()

    gcb = example_gcb_enhanced()
    print(gcb.generate_enhanced_scorecard())

    print("\n" + "=" * 80)
    print("SCORE BREAKDOWN")
    print("=" * 80)
    print(f"Transition Preparedness: {gcb.transition_preparedness.calculate_score():.1f}/5")
    print(f"Transition Vulnerability: {gcb.transition_vulnerability.calculate_score():.1f}/5")
    print(f"Transition Opportunity: {gcb.transition_opportunity.calculate_score():.1f}/5")
    print(f"Overall Transition Risk: {gcb.calculate_transition_score():.1f}/5")
    print(f"Physical Risk: {gcb.calculate_physical_score():.1f}/5")
    print(f"Combined Score: {gcb.calculate_overall_score():.1f}/5")
