"""
ICBC Standard Bank Climate & Environmental Risk Scorecard Template

This module implements the specific scorecard template used by ICBC Standard Bank
as shown in their credit papers. It extends the generic ClimateScorecard class
with bank-specific questions and scoring methodology.

Based on: ICBC Standard Bank Environmental Risk Policy v4.0 and credit paper templates
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import sys
import os

# Add parent directory to path to import the base helper
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from climate_scorecard_helper import ClimateScorecard, RiskScore


@dataclass
class ICBCStandardBankScorecard:
    """
    ICBC Standard Bank specific climate scorecard implementation

    Follows the exact template used in ICBC Standard Bank credit papers
    with specific risk factors and scoring questions
    """
    # Counterparty details
    counterparty: str
    cif: str  # Customer Identification Number
    country: str
    sector: str
    industry_code_crs: str = ""
    industry_name: str = ""
    credit_manager: str = ""
    current_rating: str = ""
    date: str = field(default_factory=lambda: datetime.now().strftime("%d-%b-%y"))

    # Transition Risk Factors (0-5 scoring, 5 = best)
    # Note: ICBC uses REVERSE scoring where 5 is BEST (lowest risk)

    # Category 1: Intent to transition
    net_zero_target: Optional[int] = None  # 0-5: Does CP explicitly target net-zero by 2050?
    tcfd_reporting: Optional[int] = None   # 0-5: Does CP publish TCFD or equivalent?
    governance_teams: Optional[int] = None # 0-5: Does CP have governance/teams to address climate risk?

    # Category 2: Vulnerabilities
    vulnerable_sector_concentration: Optional[int] = None  # 0-5: Material asset concentrations in vulnerable sectors?
    vulnerable_country_dependency: Optional[int] = None    # 0-5: Operates in country with high FX/fiscal dependency on vulnerable sector?
    regulatory_decarbonization_pressure: Optional[int] = None  # 0-5: Vulnerable to regulatory pressure to decarbonize?
    mitigation_structures: Optional[int] = None  # 0-5: Structures/actions to mitigate capital charges from climate risk?
    stranded_assets_risk: Optional[int] = None   # 0-5: Risk that assets/business lines become unviable/stranded?
    funding_cost_risk: Optional[int] = None      # 0-5: Risk of increased funding cost as regulators pressure carbon-intensive sectors?
    climate_activist_risk: Optional[int] = None  # 0-5: Vulnerable to climate activists (boardroom) and associated reputational risk?
    transition_benefit: Optional[int] = None     # 0-5: Does CP stand to benefit from transition?

    # Physical Risk Factors (0-5 scoring, 5 = best)
    asset_concentration_climate_risk: Optional[int] = None  # 0-5: Asset concentrations in areas vulnerable to climate risks?
    scenario_analysis: Optional[int] = None       # 0-5: Has CP assessed portfolio vulnerability to physical climate risks?
    office_exposure: Optional[int] = None         # 0-5: Are CP's offices exposed to climate risk factors?

    # Scores
    transition_risk_score: Optional[float] = None
    physical_risk_score: Optional[float] = None
    combined_score: Optional[float] = None

    # Rating adjustment
    rating_adjustment: str = "0.0"  # Format: "0.0" or "-1" or "+1"
    rating_adjustment_notes: str = ""

    # Concluding remarks
    concluding_remarks: str = ""

    # Rationale for each factor
    rationales: Dict[str, str] = field(default_factory=dict)

    # Reverse scoring flag
    REVERSE_SCORING = True  # ICBC uses 5 = best (lowest risk)

    def set_transition_factor(self, factor_name: str, score: int, rationale: str) -> None:
        """Set a transition risk factor score with rationale"""
        if not 0 <= score <= 5:
            raise ValueError(f"Score must be 0-5, got {score}")

        setattr(self, factor_name, score)
        self.rationales[factor_name] = rationale

    def set_physical_factor(self, factor_name: str, score: int, rationale: str) -> None:
        """Set a physical risk factor score with rationale"""
        if not 0 <= score <= 5:
            raise ValueError(f"Score must be 0-5, got {score}")

        setattr(self, factor_name, score)
        self.rationales[factor_name] = rationale

    def calculate_transition_score(self) -> float:
        """
        Calculate average transition risk score

        Returns average of all non-None transition risk factors
        ICBC uses reverse scoring: 5 = best (lowest risk)
        """
        transition_factors = [
            self.net_zero_target,
            self.tcfd_reporting,
            self.governance_teams,
            self.vulnerable_sector_concentration,
            self.vulnerable_country_dependency,
            self.regulatory_decarbonization_pressure,
            self.mitigation_structures,
            self.stranded_assets_risk,
            self.funding_cost_risk,
            self.climate_activist_risk,
            self.transition_benefit
        ]

        valid_scores = [s for s in transition_factors if s is not None]

        if not valid_scores:
            return 0.0

        return sum(valid_scores) / len(valid_scores)

    def calculate_physical_score(self) -> float:
        """
        Calculate average physical risk score

        Returns average of all non-None physical risk factors
        ICBC uses reverse scoring: 5 = best (lowest risk)
        """
        physical_factors = [
            self.asset_concentration_climate_risk,
            self.scenario_analysis,
            self.office_exposure
        ]

        valid_scores = [s for s in physical_factors if s is not None]

        if not valid_scores:
            return 0.0

        return sum(valid_scores) / len(valid_scores)

    def calculate_combined_score(self) -> float:
        """
        Calculate combined climate risk score

        Simple average of transition and physical scores
        ICBC uses reverse scoring: 5 = best (lowest risk)
        """
        transition = self.calculate_transition_score()
        physical = self.calculate_physical_score()

        if transition == 0.0 and physical == 0.0:
            return 0.0

        return (transition + physical) / 2

    def determine_rating_adjustment(self) -> Tuple[str, str]:
        """
        Determine if credit rating adjustment is required

        Returns:
            Tuple of (adjustment_notches, rationale)

        ICBC Guidance (reverse scoring: lower score = higher risk):
            - Combined score < 1.5: Consider -1 to -2 notch downgrade
            - Combined score 1.5-2.5: Consider -1 notch downgrade
            - Combined score 2.5-3.5: Monitor, possible -0.5 adjustment
            - Combined score > 3.5: No adjustment typically

        Also considers sector classification from Environmental Risk Policy
        """
        combined = self.calculate_combined_score()

        # Check prohibited sectors first
        sector_lower = self.sector.lower()
        prohibited_keywords = [
            "coal", "tar sands", "oil sands", "arctic drilling",
            "palm oil", "deforestation", "tobacco"
        ]

        if any(kw in sector_lower for kw in prohibited_keywords):
            return ("-2", "Prohibited sector under Environmental Risk Policy 5.4")

        # Score-based adjustment (remember: reverse scoring, lower = worse)
        if combined < 1.5:
            return ("-1", f"Combined score {combined:.1f} indicates high climate risk exposure")
        elif combined < 2.5:
            notes = f"Combined score {combined:.1f} indicates moderate-high climate risk"
            if "oil" in sector_lower or "gas" in sector_lower or "mining" in sector_lower:
                return ("-1", notes + "; sensitive sector warrants downward adjustment")
            return ("0.0", notes + "; monitoring required but no adjustment at this time")
        elif combined < 3.5:
            return ("0.0", f"Combined score {combined:.1f} indicates moderate climate risk; ongoing monitoring")
        else:
            return ("0.0", f"Combined score {combined:.1f} indicates low climate risk; no adjustment required")

    def generate_icbc_scorecard(self) -> str:
        """Generate scorecard in ICBC Standard Bank format"""

        # Calculate scores
        self.transition_risk_score = self.calculate_transition_score()
        self.physical_risk_score = self.calculate_physical_score()
        self.combined_score = self.calculate_combined_score()

        # Determine rating adjustment if not manually set
        if self.rating_adjustment == "0.0" and not self.rating_adjustment_notes:
            adj, notes = self.determine_rating_adjustment()
            self.rating_adjustment = adj
            self.rating_adjustment_notes = notes

        output = f"""# ICBC STANDARD BANK - CLIMATE & ENVIRONMENTAL RISK SCORECARD

## Counterparty Details

| Field | Value |
|-------|-------|
| Date | {self.date} |
| Counterparty Name | {self.counterparty} |
| CIF | {self.cif} |
| Sector | {self.sector} |
| Industry Code (CRS) | {self.industry_code_crs} |
| Industry Name | {self.industry_name} |
| Country of Risk | {self.country} |
| Credit Manager | {self.credit_manager} |
| Current Rating | {self.current_rating} |

---

## TRANSITION RISK ASSESSMENT

**Scoring: 0-5 scale where 5 = best (lowest risk)**

### Intent to Transition
| Risk Factor | Score | Examples and scoring guidance |
|-------------|-------|-------------------------------|
"""

        # Intent to transition
        if self.net_zero_target is not None:
            output += f"| Does the counterparty explicitly target net-zero by 2050 | {self.net_zero_target}/5 | {self.rationales.get('net_zero_target', 'N/A')} |\n"

        if self.tcfd_reporting is not None:
            output += f"| Does the counterparty publish a TCFD or equivalent report | {self.tcfd_reporting}/5 | {self.rationales.get('tcfd_reporting', 'N/A')} |\n"

        if self.governance_teams is not None:
            output += f"| Does the counterparty have governance and teams in place to actively address climate risks | {self.governance_teams}/5 | {self.rationales.get('governance_teams', 'N/A')} |\n"

        # Calculate intent average
        intent_scores = [s for s in [self.net_zero_target, self.tcfd_reporting, self.governance_teams] if s is not None]
        intent_avg = sum(intent_scores) / len(intent_scores) if intent_scores else 0

        output += f"""
**Average score: {intent_avg:.1f}**

*This category aims to assess the intent of the client to transition by evaluating their level of public disclosures and commitments to reduce emission levels.*

### Vulnerabilities
| Risk Factor | Score | Examples and scoring guidance |
|-------------|-------|-------------------------------|
"""

        # Vulnerabilities
        if self.vulnerable_sector_concentration is not None:
            output += f"| Does the counterparty have material asset concentrations in vulnerable sectors | {self.vulnerable_sector_concentration}/5 | {self.rationales.get('vulnerable_sector_concentration', 'N/A')} |\n"

        if self.vulnerable_country_dependency is not None:
            output += f"| Does the counterparty operate in a country with high FX/fiscal dependency on a vulnerable sector | {self.vulnerable_country_dependency}/5 | {self.rationales.get('vulnerable_country_dependency', 'N/A')} |\n"

        if self.regulatory_decarbonization_pressure is not None:
            output += f"| Is the counterparty vulnerable to regulatory pressure to decarbonise its portfolio and can this be expected | {self.regulatory_decarbonization_pressure}/5 | {self.rationales.get('regulatory_decarbonization_pressure', 'N/A')} |\n"

        if self.mitigation_structures is not None:
            output += f"| Is the counterparty putting in place structures and actions to mitigate potential additional capital charges based on climate risk | {self.mitigation_structures}/5 | {self.rationales.get('mitigation_structures', 'N/A')} |\n"

        if self.stranded_assets_risk is not None:
            output += f"| Risk that assets/core business lines become economically unviable/stranded | {self.stranded_assets_risk}/5 | {self.rationales.get('stranded_assets_risk', 'N/A')} |\n"

        if self.funding_cost_risk is not None:
            output += f"| Risk of increased cost of funding/shareholder divestment as regulators pressure carbon intensive sectors/institutions | {self.funding_cost_risk}/5 | {self.rationales.get('funding_cost_risk', 'N/A')} |\n"

        if self.climate_activist_risk is not None:
            output += f"| Is the counterparty vulnerable to being targeted by climate activists (including in boardroom) and associated reputational risk - does it have active climate related litigation against it | {self.climate_activist_risk}/5 | {self.rationales.get('climate_activist_risk', 'N/A')} |\n"

        if self.transition_benefit is not None:
            output += f"| Does the counterparty stand to benefit from transition | {self.transition_benefit}/5 | {self.rationales.get('transition_benefit', 'N/A')} |\n"

        # Calculate vulnerabilities average
        vuln_scores = [s for s in [
            self.vulnerable_sector_concentration, self.vulnerable_country_dependency,
            self.regulatory_decarbonization_pressure, self.mitigation_structures,
            self.stranded_assets_risk, self.funding_cost_risk,
            self.climate_activist_risk, self.transition_benefit
        ] if s is not None]
        vuln_avg = sum(vuln_scores) / len(vuln_scores) if vuln_scores else 0

        output += f"""
**Average score: {vuln_avg:.1f}**

*Aims to assess the gross transition risk for the company along with assess the transition mitigation plans capability. Reliance of fossil fuels or heavy polluting sectors are a key determinant of the risk. Operating in a vulnerable sector. Other considerations include the potential financial impact from implementation of carbon taxes or tighter emissions regulations on a forward looking basis.*

---

## PHYSICAL RISK ASSESSMENT

**Scoring: 0-5 scale where 5 = best (lowest risk)**

| Risk Factor | Score | Examples and scoring guidance |
|-------------|-------|-------------------------------|
"""

        if self.asset_concentration_climate_risk is not None:
            output += f"| Does the counterparty have asset concentrations in areas vulnerable to climate risks | {self.asset_concentration_climate_risk}/5 | {self.rationales.get('asset_concentration_climate_risk', 'N/A')} |\n"

        if self.scenario_analysis is not None:
            output += f"| Has the counterparty assessed its portfolio's vulnerability to physical climate risks e.g. scenario analysis of changing climate risk | {self.scenario_analysis}/5 | {self.rationales.get('scenario_analysis', 'N/A')} |\n"

        if self.office_exposure is not None:
            output += f"| Are the counterparty's offices exposed to climate risk factors | {self.office_exposure}/5 | {self.rationales.get('office_exposure', 'N/A')} |\n"

        output += f"""
**Average score: {self.physical_risk_score:.1f}**

---

## COMBINED ASSESSMENT

| Metric | Score |
|--------|-------|
| **Transition Risk Score** | **{self.transition_risk_score:.1f}** |
| **Physical Risk Score** | **{self.physical_risk_score:.1f}** |
| **Combined Average Score** | **{self.combined_score:.1f}** |

---

## RATING ADJUSTMENT

**Rating Adjustment:** {self.rating_adjustment}

{self.rating_adjustment_notes}

*If positive = -1, if neutral = -0, if negative = +1. e.g. if adjust from RG16 to RG17 = -1*

---

## CONCLUDING REMARKS

{self.concluding_remarks}

---

## SCORING INTERPRETATION GUIDE

### Transition Risk (Reverse Scoring: 5 = Best)
- **0-1.0**: Critical transition risk - sector/business model incompatible with Paris goals
- **1.0-2.0**: High transition risk - significant stranded asset or policy exposure
- **2.0-3.0**: Moderate transition risk - some vulnerabilities, mitigation plans developing
- **3.0-4.0**: Low transition risk - limited exposure or strong mitigation strategies
- **4.0-5.0**: Negligible transition risk - aligned with transition or benefiting from it

### Physical Risk (Reverse Scoring: 5 = Best)
- **0-1.0**: Critical physical risk - assets in highly vulnerable locations, no adaptation
- **1.0-2.0**: High physical risk - material geographic exposure, limited resilience
- **2.0-3.0**: Moderate physical risk - some exposure, adaptation plans in place
- **3.0-4.0**: Low physical risk - limited exposure or strong adaptation measures
- **4.0-5.0**: Negligible physical risk - minimal geographic vulnerability

### Combined Score Guidance
- **< 1.5**: Consider -1 to -2 notch downgrade; very high climate risk
- **1.5-2.5**: Consider -1 notch downgrade; high climate risk, especially for sensitive sectors
- **2.5-3.5**: Monitor closely; moderate climate risk, possible -0.5 adjustment
- **> 3.5**: No adjustment typically; low climate risk

---

**Template Version:** ICBC Standard Bank v1.0 (aligned with Environmental Risk Policy v4.0)
**Assessment Date:** {self.date}
"""

        return output

    def to_dict(self) -> Dict:
        """Export as dictionary for JSON/Excel"""
        return {
            "bank_template": "ICBC Standard Bank",
            "counterparty": self.counterparty,
            "cif": self.cif,
            "country": self.country,
            "sector": self.sector,
            "industry_code_crs": self.industry_code_crs,
            "industry_name": self.industry_name,
            "credit_manager": self.credit_manager,
            "current_rating": self.current_rating,
            "date": self.date,
            "transition_risk_factors": {
                "net_zero_target": self.net_zero_target,
                "tcfd_reporting": self.tcfd_reporting,
                "governance_teams": self.governance_teams,
                "vulnerable_sector_concentration": self.vulnerable_sector_concentration,
                "vulnerable_country_dependency": self.vulnerable_country_dependency,
                "regulatory_decarbonization_pressure": self.regulatory_decarbonization_pressure,
                "mitigation_structures": self.mitigation_structures,
                "stranded_assets_risk": self.stranded_assets_risk,
                "funding_cost_risk": self.funding_cost_risk,
                "climate_activist_risk": self.climate_activist_risk,
                "transition_benefit": self.transition_benefit
            },
            "physical_risk_factors": {
                "asset_concentration_climate_risk": self.asset_concentration_climate_risk,
                "scenario_analysis": self.scenario_analysis,
                "office_exposure": self.office_exposure
            },
            "scores": {
                "transition_risk": self.transition_risk_score,
                "physical_risk": self.physical_risk_score,
                "combined": self.combined_score
            },
            "rating_adjustment": self.rating_adjustment,
            "rating_adjustment_notes": self.rating_adjustment_notes,
            "concluding_remarks": self.concluding_remarks,
            "rationales": self.rationales
        }


def example_gcb_bank():
    """Example: Complete ICBC scorecard for GCB Bank (from screenshot)"""

    scorecard = ICBCStandardBankScorecard(
        counterparty="GCB",
        cif="100060256",
        country="Ghana",
        sector="Bank",
        industry_code_crs="64194",
        industry_name="General Banks",
        credit_manager="Robin Rouger",
        current_rating="RG24",
        date="24-Feb-25"
    )

    # Intent to transition
    scorecard.set_transition_factor(
        "net_zero_target", 0,
        "No - GCB has not committed to net-zero by 2050"
    )

    scorecard.set_transition_factor(
        "tcfd_reporting", 0,
        "None - No TCFD or equivalent sustainability report published"
    )

    scorecard.set_transition_factor(
        "governance_teams", 2,
        "The bank has an ESG strategy in place which is reviewed by the Ethics, Governance, Compliance & Nomination committee"
    )

    # Vulnerabilities
    scorecard.set_transition_factor(
        "vulnerable_sector_concentration", 5,
        "None, the largest exposure are to retail and services"
    )

    scorecard.set_transition_factor(
        "vulnerable_country_dependency", 1,
        "Yes, the country is reliant on mining and agricultural exports"
    )

    scorecard.set_transition_factor(
        "regulatory_decarbonization_pressure", 2,
        "In May 2024, the Bank of Ghana published a Climate-Related Financial Risk directive"
    )

    scorecard.set_transition_factor(
        "mitigation_structures", 1,
        "No"
    )

    scorecard.set_transition_factor(
        "stranded_assets_risk", 2,
        "None, the largest exposure are to retail and services"
    )

    scorecard.set_transition_factor(
        "funding_cost_risk", 3,
        "The bank majority-owned by the government of Ghana"
    )

    scorecard.set_transition_factor(
        "climate_activist_risk", 3,
        "None that I could find"
    )

    scorecard.set_transition_factor(
        "transition_benefit", 1,
        "Yes as the bank has little exposure to climate risks"
    )

    # Physical risks
    scorecard.set_physical_factor(
        "asset_concentration_climate_risk", 1,
        "Ghana is most at risk to droughts, coastal erosion, floods and landslides"
    )

    scorecard.set_physical_factor(
        "scenario_analysis", 1,
        "No"
    )

    scorecard.set_physical_factor(
        "office_exposure", 3,
        "Unknown"
    )

    # Concluding remarks
    scorecard.concluding_remarks = """There is no evidence that GCB has active climate risk mitigation strategies in place - no TCFD/sustainability reports are published on the website. It is unlikely, though, that GCB will be subject to pressure from shareholders or regulators to improve its climate risk strategy in the near term. The bank's largest credit exposure is to Ghanaian sovereign bonds and the loan book is relatively small with no material concentrations in high-carbon sectors."""

    # Rating adjustment
    scorecard.rating_adjustment = "0.0"
    scorecard.rating_adjustment_notes = "No rating adjustment required. Combined score of 1.8 indicates moderate climate risk, but this is appropriate for a Ghanaian universal bank with limited carbon-intensive exposure. Sovereign risk (33% assets in gov securities) is the primary climate transmission channel rather than direct transition risk."

    return scorecard


if __name__ == "__main__":
    # Generate example scorecard
    gcb = example_gcb_bank()
    print(gcb.generate_icbc_scorecard())

    # Save to file
    with open("output/gcb_icbc_scorecard.md", "w") as f:
        f.write(gcb.generate_icbc_scorecard())

    print("\n" + "="*80)
    print("Scorecard saved to: output/gcb_icbc_scorecard.md")
    print(f"Transition Risk Score: {gcb.transition_risk_score:.1f}/5")
    print(f"Physical Risk Score: {gcb.physical_risk_score:.1f}/5")
    print(f"Combined Score: {gcb.combined_score:.1f}/5")
    print(f"Rating Adjustment: {gcb.rating_adjustment}")
