# Changelog - Climate Scorecard Filler Skill

## [3.0.1] - 2025-12-11

### Fixed - Regulatory Reference Correction
- **CORRECTION**: All references updated from SS4/25 to **SS5/25** (correct PRA reference number)
- The PRA published PS25/25 and SS5/25 on 3 December 2025, superseding SS3/19
- Updated all skill files, documentation, and output templates

---

## [3.0.0] - 2025-12-10

### Changed - PRA SS5/25 Alignment
- **REGULATORY UPDATE**: Full alignment with PRA SS5/25 (December 2025), which replaces SS3/19
- Updated all regulatory references throughout the skill
- Enhanced scorecard output with SS5/25 compliance sections

### Added - SS5/25 New Requirements

**Risk Appetite Alignment Section**
- New `RiskAppetiteAlignment` dataclass
- `set_risk_appetite_alignment()` method
- Accept/Manage/Avoid categorization per SS5/25
- Portfolio limit impact tracking
- Escalation requirement flagging

**ICAAP/Capital Considerations (Banks)**
- New `ICaapConsiderations` dataclass
- `set_icaap_considerations()` method
- Capital relevance assessment (High/Medium/Low/Not Material)
- ICAAP treatment recommendation (Pillar 2A/Stress Testing/Not Material)
- Materiality justification documentation

**Enhanced Litigation Risk Assessment**
- New `LitigationRiskAssessment` dataclass
- `assess_litigation_risk()` method
- Flexible treatment: subset of transition risk OR distinct transmission channel (per SS5/25)
- Litigation type classification (climate_disclosure, greenwashing, physical_damage, duty_of_care)

**Enhanced Scenario Analysis Quality**
- New `ScenarioAnalysisQuality` dataclass
- `assess_scenario_analysis_quality()` method
- 4-factor assessment: analysis conducted, results integrated, horizons appropriate, documentation quality
- Addresses SS5/25 requirement that CSA must inform actual decision-making

**Data Quality Declaration**
- New `DataQualityDeclaration` dataclass
- `set_data_quality_declaration()` method
- Primary sources documentation
- Proxy tracking with limitations
- Data gaps identification
- Uncertainty acknowledgment

### Technical
- Added 5 new dataclasses for SS5/25 compliance
- Added 5 new assessment methods to `EnhancedClimateScorecard`
- Enhanced `generate_enhanced_scorecard()` with new sections
- Added regulatory reference footer to scorecard output
- Maintained backward compatibility with v2.0 scorecards

### Documentation
- Updated SKILL.md with SS5/25 references
- Updated README.md with new regulatory sources
- Updated QUICK_REFERENCE.md
- Created SS4-25-Climate-Scorecard-Update-Recommendation.md

### Word Document Generation
- New `climate_scorecard_document_builder.py` module
- `ClimateScorecardDocumentBuilder` class for professional .docx output
- Branded cover page with www.risk-agents.com
- PRA SS5/25 Aligned badge on cover
- Professional tables for risk assessments
- Color-coded risk indicators
- All SS5/25 compliance sections included
- Footer branding with generation date

### References
- PRA SS5/25 (December 2025) - Replaces SS3/19
- BCBS Principles for climate-related financial risks
- ISSB IFRS S2 Climate-related Disclosures

---

## [2.0.0] - 2025-11-29

### Changed - Enhanced Generic Framework
- **BREAKING**: Replaced generic framework with enhanced version incorporating ICBC learnings
- `climate_scorecard_helper.py` now uses `EnhancedClimateScorecard` class (was `ClimateScorecard`)
- Improved from 7 broad categories to 17 specific assessment factors

### Added - ICBC Template Learnings
- **Transition Preparedness** assessment (5 factors): Net-zero target, TCFD disclosure, governance, transition plan, capex alignment
- **Transition Vulnerability** assessment (7 factors): Sector intensity, stranded assets, policy risk, tech disruption, market sentiment, litigation, **country dependency**
- **Transition Opportunity** assessment (3 factors): Market growth, green revenue, competitive advantage
- **Enhanced Physical Risk** (5 factors): Acute, chronic, ecosystem, **adaptation capability**, **scenario analysis done**
- Country/sovereign climate risk transmission assessment
- Counterparty climate risk management capability assessment
- `key_opportunities` field (not just risks)

### Technical
- Structured question-based approach within each category
- Transition risk split: 30% Preparedness + 60% Vulnerability - 10% Opportunity
- More diagnostic output showing exactly where gaps/strengths are
- Backward compatible scoring (still 1-5 scale)

### Documentation
- Added `ICBC_LEARNINGS.md` documenting the 5 key improvements
- Updated README with enhanced framework examples
- Updated all examples to show new structure

## [1.0.0] - 2025-11-29

### Added - Initial Release
- Initial release of Climate & Environmental Risk Scorecard Filler skill
- Comprehensive SKILL.md following Anthropic Claude Code skills guidelines
- Python helper module (`climate_scorecard_helper.py`) with basic ClimateScorecard class (now superseded by v2.0)
- Detailed README with usage instructions and quality checklists
- Example scorecards:
  - GCB Bank (Financial Institution, moderate risk)
  - PetroNorth Energy (Oil Sands, prohibited sector, very high risk)
- Support for both transition and physical climate risk assessment
- Automated rating override determination based on Environmental Risk Policy
- Sector classification (Prohibited/Restricted/Monitored)
- Markdown and JSON export capabilities

### Features
- **7-factor risk assessment**: Policy, Technology, Market, Legal (transition) + Acute, Chronic, Ecosystem (physical)
- **Sector-aware scoring**: Different weightings for FIs, agriculture, real estate, energy
- **Policy compliance**: Aligned with Environmental Risk Policy v4.0
- **Data source tracking**: References for all risk assessments
- **Mitigation evaluation**: Framework for assessing counterparty climate strategies
- **Interactive guidance**: Step-by-step process for Front Office teams
- **Quality assurance**: Built-in validation and common pitfall warnings

### Technical Details
- Built on `dataclasses` for type safety
- Scoring methodology: 1-5 scale with weighted averages
- Default weights: 60% transition / 40% physical (adjustable by sector)
- Rating override logic: >3.5 = mandatory, 2.5-3.5 = consider, <2.5 = none
- Compatible with Risk Agent CLI and standalone Python usage

### Documentation
- Comprehensive SKILL.md (200+ lines) with examples and instructions
- README.md with quick start guide and QA checklist
- Example scorecards demonstrating low-risk and high-risk scenarios
- Inline code documentation and docstrings

### Integration
- Designed for use via Risk Intelligence Engine orchestrator
- Callable via slash command: `/climate-scorecard-filler`
- Compatible with existing skills (itc-template-filler, icc-business-case-filler)
- Outputs suitable for Credit Committee submissions (Appendix E)

### Future Enhancements (Planned)
- [ ] Excel template generation (.xlsx format)
- [ ] Integration with external ESG data APIs (MSCI, Sustainalytics)
- [ ] Automated climate scenario analysis (NGFS, IPCC)
- [ ] Portfolio-level climate risk aggregation for FIs
- [ ] Dashboard for tracking scorecard trends over time
- [ ] Word document export (.docx) for credit papers

### References
- Environmental Risk Policy v4.0 (March 2025)
- **PRA SS5/25** - Enhancing banks' and insurers' approaches to managing climate-related risks (December 2025, replaces SS3/19)
- MAS Guidelines on Environmental Risk Management
- TCFD Recommendations
- NGFS Climate Scenarios

---

## Development Notes

**Design Principles:**
1. **Policy-driven** - Strictly follows Bank's Environmental Risk Policy
2. **Evidence-based** - Requires data sources for all risk scores
3. **Transparent** - Clear scoring methodology and override logic
4. **Actionable** - Provides specific recommendations and monitoring triggers
5. **Consistent** - Standardized framework for all counterparties

**Testing:**
- Validated against GCB Bank credit paper example
- Tested Python helper module successfully
- Verified markdown generation and formatting
- Confirmed sector classification logic
- Checked rating override calculations

**Code Quality:**
- Type hints throughout Python code
- Comprehensive docstrings
- Example usage in module
- Error handling for invalid scores
- Extensible design for future enhancements
