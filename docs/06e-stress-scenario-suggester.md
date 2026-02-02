# Stress Scenario Suggester Skill

## Overview

The **Stress Scenario Suggester** skill conducts parallel research across 5 specialized domains to identify emerging market risks and suggest stress scenarios for market risk testing. Unlike the pillar-stress-generator (which parameterizes specific scenarios), this skill answers: "What should we be stress testing that we aren't currently?"

**Skill Name**: `stress-scenario-suggester`
**Location**: `.claude/skills/stress-scenario-suggester/`
**Author**: Risk Agent Team
**Version**: 1.0
**Date**: January 2025

---

## What This Skill Does

### Core Capabilities

1. **Parallel Research Architecture**
   - Launches 5 specialized research agents simultaneously
   - Each agent investigates a different risk domain
   - All agents run in parallel for maximum efficiency
   - Results synthesized into unified recommendations

2. **Web-Powered Research**
   - Uses WebSearch to find current developments (last 3-6 months)
   - Analyzes news, expert commentary, central bank reports
   - Identifies trends not yet priced by markets
   - Distinguishes plausible risks from speculation

3. **Scenario Suggestion**
   - Each agent suggests 2-3 specific stress scenarios
   - Provides trigger mechanisms and transmission channels
   - Identifies affected asset classes
   - Estimates severity and urgency

4. **Prioritization**
   - Ranks scenarios by urgency vs severity
   - Assesses current coverage gaps
   - Recommends immediate vs longer-term development
   - Flags scenarios requiring expert validation

5. **Integration with Pillar Stress Generator**
   - Output format ready for pillar-stress-generator input
   - Seamless workflow from suggestion → parameterization
   - Supports quarterly scenario library reviews

### Research Domains

The skill deploys 5 specialized research agents:

#### 1. Geopolitical Risk Researcher
**Focus**: Political instability, conflicts, sanctions, trade wars

Research Areas:
- Active conflicts and escalation risks (Taiwan, Middle East, Eastern Europe)
- Sanctions regimes and potential expansions
- Trade policy shifts and tariff risks
- Election risks and policy uncertainty
- Regional tensions with market spillover

#### 2. Macroeconomic Risk Researcher
**Focus**: Economic cycles, monetary policy, fiscal policy

Research Areas:
- Central bank policy trajectories and potential errors
- Inflation dynamics and regime changes
- Growth outlook shifts and recession risks
- Sovereign debt sustainability concerns
- Structural economic shifts (deglobalization, demographics)

#### 3. Market Structure Risk Researcher
**Focus**: Financial system vulnerabilities, liquidity risks

Research Areas:
- Leverage in the system (hedge funds, private credit, carry trades)
- Market concentration and crowding risks
- Liquidity fragility in specific markets
- Derivative market structural issues
- Counterparty risk and clearing house vulnerabilities

#### 4. Climate & ESG Risk Researcher
**Focus**: Physical risks, transition risks, regulatory developments

Research Areas:
- Extreme weather events and physical risk trends
- Carbon pricing and regulatory changes
- Stranded asset risks (fossil fuels, high-carbon industries)
- ESG-driven capital flows and divestment
- Climate litigation and disclosure requirements

#### 5. Technology & Sector Risk Researcher
**Focus**: Disruptive technologies, sector-specific vulnerabilities

Research Areas:
- AI disruption to industries and operational risks
- Cyber risk developments and systemic attacks
- Crypto/digital asset stress and regulation
- Sector-specific vulnerabilities (real estate, banking, tech)
- Supply chain dependencies and disruptions

---

## When to Use This Skill

### Ideal Use Cases

✅ **Quarterly Scenario Library Review**
- "Suggest scenarios for our Q1 stress testing review"
- "What emerging risks should we add to our scenario library?"

✅ **Risk Appetite Framework Updates**
- "Identify new risks for RAF discussion"
- "Research developments for annual risk appetite review"

✅ **ICAAP/ILAAP Preparation**
- "Suggest scenarios for ICAAP stress testing chapter"
- "Identify emerging risks for reverse stress testing"

✅ **MLRC Scenario Planning**
- "What scenarios should we develop for next MLRC?"
- "Research market developments for scenario portfolio update"

✅ **Forward-Looking Risk Radar**
- "What are the emerging risks on the horizon?"
- "Suggest stress scenarios based on current market conditions"

### When NOT to Use

❌ **Parameterizing Existing Scenarios** → Use `pillar-stress-generator`
❌ **Calculating P&L or VaR** → Not a risk calculation tool
❌ **Historical Scenario Analysis** → This skill focuses on forward-looking risks
❌ **Quick Answer Needed** → Parallel research takes 2-5 minutes

---

## How It Works

### Execution Flow

```
User Request
    ↓
stress-scenario-suggester skill activated
    ↓
Launch 5 research agents IN PARALLEL (single Task tool call)
    ├─ geopolitical-risk-researcher
    ├─ macroeconomic-risk-researcher
    ├─ market-structure-risk-researcher
    ├─ climate-esg-risk-researcher
    └─ technology-sector-risk-researcher
    ↓
Each agent independently:
    1. Uses WebSearch for current developments
    2. Analyzes trends and vulnerabilities
    3. Suggests 2-3 stress scenarios
    4. Returns findings with sources
    ↓
All agents complete (parallel execution)
    ↓
Synthesize findings:
    - Consolidate 10-15 scenario suggestions
    - Remove duplicates and merge related ideas
    - Assess plausibility, severity, urgency
    - Check current coverage gaps
    ↓
Generate prioritized report:
    - Executive summary (top 3-5 scenarios)
    - Full research findings by domain
    - Prioritization matrix
    - Recommended next steps
    ↓
Return comprehensive report
```

### Agent Prompt Structure

Each research agent receives:

```markdown
# [Domain] Risk Research Agent

## Your Task
Research current [domain] developments that could drive market stress scenarios.

## Research Focus
[Domain-specific areas - geopolitical, macro, etc.]

## Requirements
1. Use WebSearch to find current news, analysis, expert commentary
2. Focus on developments from last 3-6 months
3. Identify risks that are:
   - Plausible (not science fiction)
   - Material (could move markets significantly)
   - Actionable (can be translated into stress scenarios)

## Output Format
### [Domain] Risk Findings

**Current Landscape**
[2-3 paragraph summary]

**Scenario Suggestion 1: [Name]**
- Trigger: [What would cause this]
- Transmission: [How it impacts markets]
- Affected Assets: [Rates, FX, Credit, Commodities]
- Severity Estimate: [High/Medium/Low]
- Key Sources: [Where you found this]

[Repeat for 2-3 scenarios]

**Emerging Watch Items**
[Items to monitor but not yet scenario-ready]
```

---

## Output Format

### Report Structure

The skill generates a comprehensive markdown report:

```markdown
# Stress Scenario Suggestions - [Date]

## Executive Summary

Based on current market developments, we recommend the following stress scenarios:

### Priority 1: [Scenario Name]
- **Domain**: [Geopolitical/Macro/Market Structure/Climate/Tech]
- **Trigger**: [What would cause this]
- **Key Risk Factors**: [Asset classes affected]
- **Why Now**: [Current developments making this relevant]
- **Urgency**: [High/Medium/Low]
- **Current Coverage**: [Not tested / Partial / Update needed]

### Priority 2: [Scenario Name]
...

### Priority 3: [Scenario Name]
...

---

## Detailed Research Findings

### Geopolitical Risks
[Agent findings with 2-3 scenario suggestions]

### Macroeconomic Risks
[Agent findings with 2-3 scenario suggestions]

### Market Structure Risks
[Agent findings with 2-3 scenario suggestions]

### Climate & ESG Risks
[Agent findings with 2-3 scenario suggestions]

### Technology & Sector Risks
[Agent findings with 2-3 scenario suggestions]

---

## Prioritization Matrix

| Scenario | Domain | Severity | Urgency | Coverage | Recommendation |
|----------|--------|----------|---------|----------|----------------|
| [Name]   | Geo    | High     | High    | None     | Develop now    |
| [Name]   | Macro  | High     | Medium  | Partial  | Update existing|
| [Name]   | Tech   | Medium   | High    | None     | Q2 development |
| ...      | ...    | ...      | ...     | ...      | ...            |

---

## Recommended Next Steps

1. **Immediate Action**: Develop [Priority 1] via pillar-stress-generator
2. **Short-term**: Review existing [related scenario] for updates
3. **Medium-term**: Consider [Priority 2-3] for next MLRC cycle
4. **Expert Consultation**: Discuss [specific scenario] with [desk/team]

---

## Research Metadata

- **Research Date**: [Timestamp]
- **Sources**: [Web sources used by agents]
- **Confidence**: [High/Medium/Low] based on source quality
- **Recommended Validation**: [What experts should verify]
```

### Prioritization Criteria

**Severity** (Impact if it occurs):
- **High**: Major market dislocation, systemic stress
- **Medium**: Significant volatility, sector-specific stress
- **Low**: Moderate market moves, contained impact

**Urgency** (Timing likelihood):
- **High**: Imminent risk, already emerging
- **Medium**: Building over 6-12 months
- **Low**: Longer-term structural shift

**Coverage** (Current testing):
- **None**: Not tested in current scenario library
- **Partial**: Similar scenario exists but needs updates
- **Full**: Already well-covered

**Recommendation**:
- **Develop now**: High severity + High urgency + Low coverage
- **Update existing**: Medium/High severity + Partial coverage
- **Q2/Q3 development**: Medium urgency + Medium severity
- **Monitor**: Low urgency or already covered

---

## Example Usage

### Example 1: Quarterly Review

**User Query**:
```
"Suggest stress scenarios based on current market developments for our Q1 review"
```

**Skill Response** (abbreviated):
```markdown
# Stress Scenario Suggestions - January 2025

## Executive Summary

Based on research across 5 domains, we recommend:

### Priority 1: US Commercial Real Estate Collapse
- **Domain**: Market Structure / Macroeconomic
- **Trigger**: Office vacancy rates >25%, regional bank CRE exposure $500B+, refinancing wall 2024-25
- **Key Risk Factors**:
  - Credit spreads: US CMBS +500bps, Regional bank CDS +300bps
  - Rates: Fed forced to cut despite inflation → USD -10%
  - Commodities: Copper -15% (recession signal)
- **Why Now**: Regional bank failures (SVB, Signature) exposed CRE concentrations, WFH structural shift
- **Urgency**: HIGH - stress already materializing
- **Current Coverage**: Not explicitly tested (covered indirectly in "US Recession" scenario)

### Priority 2: AI Disruption to Financial Services
- **Domain**: Technology
- **Trigger**: Rapid GenAI adoption creates winner/loser dynamics, operational dependencies on cloud providers
- **Key Risk Factors**:
  - Equities: Financial sector dispersion (winners +30%, losers -40%)
  - Credit: Legacy bank downgrades, fintech credit stress
  - Operational: Cyber risks, model risk, hallucination incidents
- **Why Now**: ChatGPT adoption S-curve, regulatory scrutiny building
- **Urgency**: MEDIUM - building over 12-24 months
- **Current Coverage**: None (novel scenario type)

### Priority 3: China Property Sector Contagion
- **Domain**: Geopolitical / Macroeconomic
- **Trigger**: Evergrande/Country Garden defaults → shadow banking exposure → CNY devaluation
- **Key Risk Factors**:
  - FX: CNY -20%, EM Asia FX -15%
  - Rates: China cuts aggressively, global rates down (flight to safety)
  - Commodities: Base metals (Cu, Fe) -30%
  - Credit: EM spreads +250bps
- **Why Now**: Developer defaults ongoing, local government debt concerns, property sales -30% YoY
- **Urgency**: HIGH
- **Current Coverage**: PARTIAL - existing "China Hard Landing" scenario but needs update for property specifics

---

## Prioritization Matrix

| Scenario                    | Domain  | Severity | Urgency | Coverage | Recommendation      |
|-----------------------------|---------|----------|---------|----------|---------------------|
| US CRE Collapse             | Market  | High     | High    | Partial  | Develop new variant |
| AI Disruption FinServ       | Tech    | High     | Medium  | None     | Q2 development      |
| China Property Contagion    | Geo     | High     | High    | Partial  | Update existing     |
| EU Energy Crisis Redux      | Geo     | Medium   | Medium  | Full     | No action needed    |
| Private Credit Unwind       | Market  | High     | Medium  | None     | Q2 development      |

---

## Recommended Next Steps

1. **Immediate**: Develop "US CRE Collapse" variant using pillar-stress-generator
   - Collaborate with Credit Risk on commercial real estate exposures
   - Consult Regional Banking desk on portfolio sensitivities

2. **Short-term (Feb MLRC)**: Update "China Hard Landing" with property sector shocks
   - Increase severity of base metals shocks
   - Add developer default assumptions
   - Review exposures to China property developers

3. **Medium-term (Q2)**: Design "AI Disruption" and "Private Credit Unwind" scenarios
   - Novel scenario types requiring expert input
   - Coordinate with Operational Risk on AI risks
   - Consult with Credit team on private credit exposures

4. **Expert Consultation**:
   - Market Risk: Validate scenario plausibility
   - Credit Risk: Review CRE and China developer exposures
   - Front Office: Understand current positioning in these areas
```

### Example 2: Integration with Pillar Stress Generator

**Workflow**:
```
Step 1: User → "Suggest stress scenarios for Q1 review"
         ↓
Step 2: stress-scenario-suggester runs parallel research
         ↓
Step 3: Returns report with Priority 1: "US CRE Collapse"
         ↓
Step 4: User → "Develop the US CRE Collapse scenario"
         ↓
Step 5: pillar-stress-generator takes over
         ↓
Step 6: Generates full risk factor parameterization + MLRC memo
```

---

## Quality Standards

### Research Quality

Each agent must:
- ✅ Use reputable sources (major news, research institutions, official data)
- ✅ Distinguish speculation from substantiated risks
- ✅ Provide specific transmission channels (not just "markets fall")
- ✅ Consider second and third-order effects
- ✅ Note confidence level based on source quality

### Scenario Quality

Suggested scenarios must be:
- ✅ **Plausible**: Severe but not impossible (not "end of world")
- ✅ **Material**: Would significantly move markets
- ✅ **Actionable**: Can be parameterized into stress scenarios
- ✅ **Novel** OR **Update**: Either new or clear improvement to existing
- ✅ **Specific**: Clear trigger, transmission, affected assets

### Output Quality

The final report must include:
- ✅ Executive summary with top 3-5 priorities
- ✅ Detailed findings from all 5 domains
- ✅ Prioritization matrix with clear criteria
- ✅ Recommended next steps (immediate, short-term, medium-term)
- ✅ Research metadata (sources, confidence, validation needed)

---

## Governance & Limitations

### What This Skill Does

✅ Identifies emerging risks through current research
✅ Suggests scenarios for further development
✅ Prioritizes based on urgency and severity
✅ Provides sources and confidence levels
✅ Integrates with pillar-stress-generator workflow

### What This Skill Does NOT Do

❌ Parameterize scenarios (use pillar-stress-generator)
❌ Calculate P&L or VaR impacts
❌ Make final decisions on what to test
❌ Replace expert judgment on scenario selection
❌ Provide real-time market data or trading signals

### Human Review Required

All suggestions require review by Market Risk team before:
- Committing resources to scenario development
- Presenting to MLRC
- Modifying existing scenario library
- Allocating stress testing budget

### Confidence Scoring

**High Confidence (>80%)**:
- Based on clear, current news from multiple reputable sources
- Consensus among analysts and institutions
- Historical precedents for calibration
- Recommendation: Proceed with scenario development

**Medium Confidence (60-80%)**:
- Based on credible sources but less consensus
- Some aspects novel without clear precedent
- Recommendation: Expert review before development

**Low Confidence (<60%)**:
- Speculative or single-source information
- Novel scenario type with limited precedent
- Recommendation: Extensive expert validation required

---

## Technical Details

### File Structure

```
.claude/skills/stress-scenario-suggester/
├── SKILL.md                           # Skill definition and prompt
└── (no executable modules - pure research)

.claude/agents/
├── geopolitical-risk-researcher.md
├── macroeconomic-risk-researcher.md
├── market-structure-risk-researcher.md
├── climate-esg-risk-researcher.md
└── technology-sector-risk-researcher.md

.claude/commands/
└── stress-scenario-suggester.md       # Slash command (optional)
```

### Invocation Methods

**Auto-invoked by market-risk-agent**:
```
User: "What scenarios should we test for Q1?"
→ market-risk-agent detects intent
→ Invokes stress-scenario-suggester skill
```

**Slash command**:
```
/stress-scenario-suggester
```

**Explicit request**:
```
User: "Use the stress-scenario-suggester skill to research emerging risks"
```

### Performance

- **Parallel execution**: ~2-5 minutes (5 agents running simultaneously)
- **Web searches**: ~5-10 per agent = 25-50 total searches
- **Output length**: ~2000-5000 words
- **Scenarios suggested**: 10-15 raw suggestions → 3-5 prioritized

---

## Related Skills

### Workflow Integration

```
stress-scenario-suggester → pillar-stress-generator
    (What to test)             (How to test it)
```

**stress-scenario-suggester**:
- Researches emerging risks
- Suggests scenarios
- Prioritizes by urgency/severity

**pillar-stress-generator**:
- Takes scenario suggestions
- Parameterizes risk factors
- Generates MLRC documentation
- Validates consistency

### Complementary Skills

- **project-planner**: Plan scenario library refresh project
- **meeting-minutes**: Capture MLRC discussion on scenario selection
- **status-reporter**: Report on scenario development progress

---

## Best Practices

### For Users

1. **Run Quarterly**: Align with risk appetite and MLRC cycles
2. **Review Promptly**: Market developments change quickly
3. **Validate with Experts**: Don't blindly adopt suggestions
4. **Track Over Time**: Monitor which suggestions materialized
5. **Feed Forward**: Use insights for scenario library evolution

### For Market Risk Teams

1. **Combine with Internal Views**: Augment, don't replace, expert judgment
2. **Cross-Check Sources**: Verify agent findings independently
3. **Consider Portfolio**: Prioritize based on actual exposures
4. **Document Decisions**: Track which suggestions were adopted/rejected and why
5. **Share Insights**: Circulate report to Front Office for awareness

### For MLRC/Governance

1. **Include in Agenda**: Regular "Emerging Risks" agenda item
2. **Challenge Assumptions**: Question plausibility and severity
3. **Resource Planning**: Budget for scenario development based on priorities
4. **Stakeholder Buy-in**: Ensure Front Office engaged in novel scenarios
5. **Audit Trail**: Document scenario selection rationale

---

## Troubleshooting

### Issue: "Scenarios seem generic or outdated"

**Cause**: WebSearch not finding recent developments
**Solution**:
- Check date filter in agent prompts (should be last 3-6 months)
- Manually provide recent news articles to supplement
- Re-run skill if market conditions changed significantly

### Issue: "Too many scenarios, hard to prioritize"

**Cause**: All 5 agents returning 3 scenarios each
**Solution**:
- Focus on Priority 1-3 from executive summary
- Filter by "Current Coverage = None" (novel scenarios)
- Align with risk appetite statement priorities

### Issue: "Scenarios don't match our portfolio"

**Cause**: Generic market research, not portfolio-specific
**Solution**:
- This skill identifies market risks, not portfolio-specific impacts
- Use suggestions as input, then assess materiality to your book
- Prioritize scenarios affecting your key trading desks

### Issue: "Confidence scores are low"

**Cause**: Novel scenarios with limited precedent
**Solution**:
- Low confidence ≠ bad suggestion
- Requires more expert validation, not rejection
- Consider for "reverse stress testing" or tail scenarios

---

## Version History

### v1.0 (January 2025)
- Initial release
- 5 parallel research agents
- WebSearch integration
- Prioritization matrix
- Integration with pillar-stress-generator

### Planned Enhancements

- Integration with risk data feeds (Bloomberg, Refinitiv)
- Historical scenario performance tracking
- Automated MLRC memo generation
- Portfolio-specific materiality assessment
- Machine learning for scenario clustering

---

## Support

For questions or issues:
1. Check this reference guide
2. Review `.claude/skills/stress-scenario-suggester/SKILL.md`
3. Consult [Skills Guide](06-skills-guide.md)
4. Raise issue in project repository

---

**Last Updated**: January 2025
**Maintained By**: Risk Agent Team
