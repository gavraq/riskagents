# ICBC Template Learnings - Generic Framework Improvements

## Summary

After analyzing the ICBC Standard Bank climate scorecard template, we've incorporated **5 key learnings** into an enhanced generic framework (v2.0). This document explains what we learned, why it matters, and how it improves climate risk assessment.

---

## Key Learnings Incorporated

### 1. **Structured Question-Based Approach** ✨

**What ICBC Does:**
- Specific, actionable questions: "Does CP explicitly target net-zero by 2050?"
- Clear binary/scale assessment points
- Reduces subjectivity and improves consistency

**Old Generic Approach:**
- Broad category: "Policy & Regulatory Risk"
- Assessor decides what to consider
- More subjective, less comparable across counterparties

**Enhancement in v2.0:**
```python
# OLD (v1.0)
scorecard.assess_transition_risk("policy", 4, "High carbon pricing exposure")

# NEW (v2.0)
scorecard.assess_transition_preparedness(
    net_zero_target=5,           # Specific question
    tcfd_disclosure=5,           # Specific question
    governance_structure=3,      # Specific question
    transition_plan=4,           # Specific question
    capex_alignment=3,           # Specific question
    rationale="..."
)
```

**Benefit:**
- ✅ More consistent assessments across different analysts
- ✅ Easier to track changes over time (e.g., "TCFD disclosure improved from 5 to 3")
- ✅ Clear gaps highlighted (e.g., "no net-zero target")
- ✅ Better comparable to ICBC format if needed

---

### 2. **Intent vs. Vulnerability Split for Transition Risk** 🎯

**What ICBC Does:**
- **Intent to Transition** (3 factors): What is the counterparty *doing* about climate?
  - Net-zero commitment, TCFD reporting, governance
- **Vulnerabilities** (8 factors): What *risks* does the counterparty face?
  - Sector exposure, stranded assets, regulatory pressure

**Why This Matters:**
A company can be **well-prepared but highly vulnerable** (oil major with great ESG disclosure but huge stranded asset risk) OR **poorly prepared but low vulnerability** (services company with no disclosure but minimal exposure).

**Enhancement in v2.0:**

```
TRANSITION RISK = 30% Preparedness + 60% Vulnerability - 10% Opportunity

Preparedness (1-5 where 5 = worst):
  - Net-zero target credibility
  - TCFD disclosure quality
  - Governance structure
  - Transition plan credibility
  - Capex alignment with Paris

Vulnerability (1-5 where 5 = worst):
  - Sector carbon intensity
  - Stranded asset risk
  - Policy/regulatory pressure
  - Technology disruption
  - Market sentiment risk
  - Legal/litigation risk
  - Country transition dependency (NEW from ICBC!)
```

**Example - GCB Bank:**
| Component | Score | Insight |
|-----------|-------|---------|
| Preparedness | 4.0/5 | **Weak** - No TCFD, no net-zero, basic governance |
| Vulnerability | 2.4/5 | **Moderate** - Low direct exposure, but country risk |
| **Net Effect** | 2.5/5 | **Moderate** - Weak governance but not in vulnerable sector |

**Benefit:**
- ✅ Separates *what they're doing* from *what they're exposed to*
- ✅ Identifies different intervention points (e.g., "push for better disclosure" vs "reduce sector exposure")
- ✅ More nuanced than single "transition risk" score

---

### 3. **Transition Benefit/Opportunity Assessment** 📈

**What ICBC Asks:**
"Does the counterparty stand to benefit from transition?"

**Why We Missed This:**
Original framework only assessed *risks*, not *opportunities*

**Enhancement in v2.0:**

```python
scorecard.assess_transition_opportunity(
    market_growth_potential=1,      # Renewable energy = huge opportunity
    green_revenue_share=2,          # 40% revenue from green products
    competitive_advantage=2,        # Early mover in solar
    rationale="Well-positioned to benefit from energy transition"
)
```

**Scoring (1-5 where 1 = best positioned):**
- **1** = Strong beneficiary (renewable energy, EVs, green tech)
- **2** = Some benefit (transition enablers like grid infrastructure)
- **3** = Neutral
- **4** = Limited benefit
- **5** = No benefit or negative (coal, oil sands)

**Example Comparison:**

| Counterparty | Transition Vulnerability | Transition Opportunity | Net Assessment |
|--------------|-------------------------|----------------------|----------------|
| Oil Sands Company | 5/5 (Critical) | 5/5 (No benefit) | Very High Risk |
| Solar Developer | 2/5 (Low) | 1/5 (Strong beneficiary) | **Net Positive** |
| Universal Bank | 3/5 (Moderate) | 3/5 (Neutral) | Moderate Risk |

**Benefit:**
- ✅ Identifies "climate winners" not just "climate losers"
- ✅ Opportunity score offsets some risk (10% weight in calculation)
- ✅ More balanced, complete assessment
- ✅ Helps identify green lending/investment opportunities

---

### 4. **Country-Level Sovereign Risk Transmission** 🌍

**What ICBC Asks:**
"Does the counterparty operate in a country with high FX/fiscal dependency on a vulnerable sector?"

**Why This Matters:**
Even if a company has low direct carbon exposure, **sovereign climate risk can transmit** through:
- FX crisis if country depends on fossil fuel exports (Nigeria oil, coal-dependent economies)
- Fiscal stress if country revenue depends on extractive industries
- Sovereign default risk affecting all domestic companies

**Enhancement in v2.0:**

Added to `transition_vulnerability`:
```python
country_transition_dependency: Optional[int] = None
# 1-5: How dependent is the country on climate-vulnerable sectors?
```

**Example - GCB Bank Ghana:**
- **Direct exposure**: Low (universal bank, no fossil fuel lending)
- **Country dependency**: High (Ghana depends on gold mining, cocoa, oil exports)
- **Transmission channel**:
  - Fiscal stress → sovereign bond risk → GCB balance sheet impact (33% in gov bonds)
  - FX pressure → imported goods inflation → borrower stress

**Old Assessment**: Would miss this entirely (looked only at GCB's loan book)
**New Assessment**: Captures sovereign transmission channel

**Benefit:**
- ✅ Captures indirect, macro-level climate risk
- ✅ Critical for emerging markets where sovereign and corporate risk are linked
- ✅ Explains why banks in carbon-dependent economies have higher risk regardless of own portfolio

---

### 5. **Counterparty Climate Risk Management Capability** 🛠️

**What ICBC Asks:**
- "Has the counterparty assessed its portfolio's vulnerability to physical climate risks (scenario analysis)?"
- "Has the counterparty put in place structures/actions to mitigate capital charges from climate risk?"

**Why This Matters:**
There's a difference between:
- **We assess the counterparty's climate risk** (what we do)
- **The counterparty assesses their own climate risk** (what they do)

If a counterparty hasn't done climate scenario analysis, they may be *unaware* of their own risks and unprepared for sudden shocks.

**Enhancement in v2.0:**

Added to `physical_risk`:
```python
scenario_analysis_done: Optional[int] = None
# 1-5: Has CP conducted physical climate scenario analysis?
# 1 = Comprehensive analysis
# 5 = No analysis done
```

**Example Assessment:**

| Company | Our Risk Assessment | Their Capability | Combined View |
|---------|-------------------|------------------|---------------|
| Company A | High flood risk | Has scenario analysis, adaptation plan | **Moderate** (risk known, being managed) |
| Company B | High flood risk | No scenario analysis, no plan | **Very High** (risk unknown, unmanaged) |

**Benefit:**
- ✅ Assesses counterparty's *preparedness* not just *exposure*
- ✅ Unprepared counterparties are higher risk (surprises likely)
- ✅ Can recommend/encourage climate risk management practices
- ✅ Tracks improvement over time

---

## Comparison: v1.0 vs v2.0

### Scoring Structure

| Aspect | v1.0 (Original) | v2.0 (Enhanced) |
|--------|----------------|-----------------|
| **Transition Risk Categories** | 4 broad (Policy, Tech, Market, Legal) | 3 detailed (Preparedness, Vulnerability, Opportunity) |
| **Transition Sub-factors** | None (free-form) | 17 specific questions |
| **Physical Risk Categories** | 3 (Acute, Chronic, Ecosystem) | 1 comprehensive with 5 sub-factors |
| **Opportunity Assessment** | ❌ Not included | ✅ Included (10% weight) |
| **Country Risk** | Implicit | ✅ Explicit factor |
| **CP Capability Assessment** | ❌ Not included | ✅ Included |

### Output Clarity

**v1.0 Output:**
```
Transition Risk Assessment:
- Policy & Regulatory Risk: 4/5 - "High carbon pricing exposure..."
- Technology Risk: 3/5 - "Moderate disruption risk..."
```

**v2.0 Output:**
```
1. Transition Preparedness (Intent & Capability): 4.0/5
   - Net-Zero Target: 5/5 (None/Critical)
   - TCFD Disclosure: 5/5 (None/Critical)
   - Governance: 3/5 (Adequate)

2. Transition Vulnerability (Exposure): 2.4/5
   - Sector Carbon Intensity: 2/5 (Good)
   - Stranded Asset Risk: 2/5 (Good)
   - Country Transition Dependency: 4/5 (Weak)

3. Transition Opportunity: 3.3/5
   - Market Growth Potential: 3/5 (Neutral)
```

**Improvement:**
- ✅ More granular (can see exactly where problems are)
- ✅ Easier to track improvements
- ✅ Better diagnostic value

---

## When to Use Which Version

### Use v1.0 (Original Generic Framework) When:
- Speed is priority over granularity
- Counterparty has minimal public disclosure (can't answer detailed questions)
- Quick screening assessment
- Non-ICBC bank without specific template

### Use v2.0 (Enhanced Generic Framework) When:
- Detailed assessment needed
- Comparing multiple counterparties consistently
- Tracking progress over time (annual reviews)
- Need to identify specific improvement areas
- Want ICBC-like structure but not ICBC format

### Use ICBC Template When:
- Submitting to ICBC Standard Bank Credit Committee
- Need exact ICBC format
- Have all required ICBC-specific data (CIF, industry code, etc.)

---

## Practical Example: GCB Bank

### Old Assessment (v1.0)
```
Transition Risk: 1.6/5 (Low)
Physical Risk: 2.5/5 (Medium)
Overall: 1.9/5

Conclusion: Moderate risk, no override required
```

**Problem:** Doesn't show *why* or *where* the risk lies

### New Assessment (v2.0)
```
Transition Risk: 2.5/5
  - Preparedness: 4.0/5 ← WEAK GOVERNANCE IDENTIFIED
  - Vulnerability: 2.4/5 ← Moderate exposure
    - Country Dependency: 4/5 ← KEY RISK DRIVER
  - Opportunity: 3.3/5 ← Limited green finance

Physical Risk: 3.4/5
  - Scenario Analysis Done: 5/5 ← NOT DOING SCENARIO ANALYSIS

Overall: 2.8/5
```

**Actionable Insights:**
1. **Recommend:** GCB develop climate scenario analysis capability
2. **Recommend:** Establish TCFD disclosure roadmap
3. **Monitor:** Ghana sovereign climate fiscal risk
4. **Opportunity:** Position for green finance market development

---

## Migration Path

If you have existing v1.0 scorecards, you can:

1. **Keep v1.0 for historical comparisons**
2. **Use v2.0 for new assessments**
3. **Gradually migrate** by adding sub-factor detail to v1.0 assessments

**Backward Compatible:**
v2.0 still supports the high-level category scores from v1.0, so old code still works.

---

## Summary of Improvements

| Learning | Benefit | Impact |
|----------|---------|--------|
| **1. Structured Questions** | Consistency, comparability | 🟢 High |
| **2. Intent vs Vulnerability** | Nuanced assessment | 🟢 High |
| **3. Opportunity Assessment** | Complete picture | 🟡 Medium |
| **4. Country/Sovereign Risk** | Captures indirect transmission | 🟢 High (EM focus) |
| **5. CP Capability Assessment** | Identifies preparedness gaps | 🟡 Medium |

---

## Recommendation

**Use v2.0 (Enhanced Generic Framework) as the default** for new assessments while keeping ICBC template available for bank-specific submissions.

The enhanced framework provides:
- ✅ **Best of both worlds**: ICBC structure + Generic flexibility
- ✅ **More diagnostic**: Identifies specific gaps and opportunities
- ✅ **Actionable**: Clear intervention points
- ✅ **Comparable**: Can track improvements over time
- ✅ **Complete**: Risks AND opportunities

---

**Version:** 2.0
**Date:** 2025-11-29
**Status:** Production Ready
**Recommended for:** All new climate scorecard assessments (non-ICBC format)
