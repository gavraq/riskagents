# Climate Scorecard Filler - Quick Reference Card

## 🎯 When to Use
- Credit limit increases requiring Appendix E
- Annual credit reviews
- New counterparty ESG assessments
- Sensitive sector transactions (Energy, Mining, Industrials, Ag)

## 📊 Risk Categories (Score 1-5)

### Transition Risks
| Risk Type | Key Factors |
|-----------|-------------|
| **Policy** | Carbon pricing, emission caps, regulations |
| **Technology** | Stranded assets, clean tech disruption, EVs |
| **Market** | Investor sentiment, ESG exclusions, demand shifts |
| **Legal** | Climate litigation, disclosure obligations |

### Physical Risks
| Risk Type | Key Factors |
|-----------|-------------|
| **Acute** | Floods, hurricanes, wildfires, droughts |
| **Chronic** | Sea-level rise, temperature increases, water stress |
| **Ecosystem** | Deforestation, pollution, biodiversity loss |

## 🚦 Sector Classifications

| Symbol | Category | Action |
|--------|----------|--------|
| 🚫 | **Prohibited** | No appetite - Decline |
| ⚠️ | **Restricted** | Limited - Escalate |
| 👁️ | **Monitored** | Full appetite - Track |

### Prohibited Sectors (🚫)
- Coal (mining, processing, power)
- Oil tar sands
- Arctic drilling
- Mountain top removal
- Palm oil
- Deforestation
- Tobacco

### Restricted Sectors (⚠️)
- Fracking (< 25% exposure limit)
- Cement
- Paper & pulp
- Uranium mining

### Monitored Sectors (👁️)
- Oil & Gas (conventional)
- Chemicals
- Manufacturing
- Agriculture
- Airlines

## 🎲 Scoring Scale

| Score | Rating | Description |
|-------|--------|-------------|
| 1 | Negligible | No material exposure |
| 2 | Low | Minor exposure, good mitigation |
| 3 | Medium | Moderate exposure, some mitigation |
| 4 | High | Significant exposure, limited mitigation |
| 5 | Critical | Severe exposure, inadequate mitigation |

## ⚖️ Rating Override Decision Tree

```
Overall Score > 3.5?
├─ YES → Mandatory 2-notch downgrade
└─ NO → Score 2.5-3.5?
    ├─ YES → Is sector Restricted?
    │   ├─ YES → Consider 1-notch downgrade
    │   └─ NO → No override
    └─ NO → No override required

Prohibited Sector?
└─ YES → Automatic 3-notch downgrade (DECLINE)
```

## 📋 Quick Assessment Checklist

### Before Starting
- [ ] Counterparty name and sector confirmed
- [ ] Sustainability reports gathered (TCFD, CDP, ESG ratings)
- [ ] Geographic exposure identified
- [ ] Sector classification checked vs policy

### During Assessment
- [ ] All 7 risk categories scored with rationale
- [ ] Data sources cited for key claims
- [ ] Mitigation measures verified (not just claimed)
- [ ] Forward scenarios considered (5-10 years)
- [ ] Peer comparison if available

### Before Submission
- [ ] Overall score calculated correctly
- [ ] Rating override logic applied
- [ ] Summary suitable for Credit Committee
- [ ] Monitoring triggers specified
- [ ] Quality check passed (see README)

## 🔍 Top Data Sources

**Company Data**
- Annual/Sustainability reports
- CDP submissions
- TCFD disclosures

**ESG Ratings**
- MSCI ESG Ratings
- Sustainalytics
- S&P Global ESG

**Climate Data**
- IPCC regional reports
- National meteorological services
- WRI Aqueduct (water risk)

**Regulatory**
- Country NDCs
- Carbon pricing databases
- **PRA SS5/25** / MAS Guidelines

## 💡 Common Mistakes to Avoid

❌ **DON'T:**
- Trust ESG ratings blindly (verify!)
- Ignore forward-looking scenarios
- Credit unverified mitigation claims
- Apply sector stereotypes
- Miss supply chain exposures

✅ **DO:**
- Verify claims with primary sources
- Consider 10-30 year physical risks
- Document data gaps and assumptions
- Check peer comparisons
- Apply consistent methodology

## ⚡ Quick Commands

### Via Risk Agent CLI
```bash
uv run riskagent

# Then:
"Complete climate scorecard for [Company] in [Sector]"
```

### Via Python
```python
from climate_scorecard_helper import ClimateScorecard

s = ClimateScorecard("Company", "Country", "Sector")
s.assess_transition_risk("policy", 3, "rationale")
s.assess_physical_risk("acute", 2, "rationale")
s.save_markdown("output.md")
```

## 🎯 Typical Completion Time

| Scenario | Time Estimate |
|----------|---------------|
| Low-risk, good disclosure | 45-60 min |
| Medium-risk, some data | 60-90 min |
| High-risk, complex | 90-120 min |
| Prohibited sector | 30 min (decline) |

## 📞 Escalation Points

**Escalate to Credit Risk Manager if:**
- Overall score > 3.0
- Prohibited or Restricted sector
- Rating override recommended
- Material data gaps

**Escalate to CRO if:**
- Prohibited sector with existing exposure
- Overall score > 4.0
- Regulatory/reputational concerns

## 📚 Key References

- Environmental Risk Policy v4.0 (§5.4 Sector Lists)
- [SKILL.md](SKILL.md) - Full instructions
- [README.md](README.md) - Detailed guide
- [Examples](examples/) - Sample scorecards

## 🔄 Review Frequency

| Risk Score | Review Frequency |
|------------|------------------|
| < 2.0 | Annual |
| 2.0 - 3.0 | Annual + trigger events |
| 3.0 - 4.0 | Semi-annual + triggers |
| > 4.0 | Quarterly + triggers |
| Prohibited | Monthly (if exposure exists) |

---

**Last Updated:** 2025-12-10
**Version:** 3.0.0 (SS5/25 Aligned)
**Maintained By:** Risk Management / Front Office
**Regulatory Basis:** PRA SS5/25 (December 2025)
