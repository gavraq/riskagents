---
name: meeting-minutes
description: Structures meeting notes into professional minutes with clear sections, action items with owners and due dates, decisions made, and open questions. Extracts key discussion points and organizes them for easy reference and follow-up.
---

# Meeting Minutes Skill

## Purpose

Transform raw meeting notes into structured, professional meeting minutes that clearly capture:
- Meeting context (date, attendees, purpose)
- Key discussion points
- Decisions made
- Action items with owners and due dates
- Open questions and issues
- Next steps

## When to Use

This skill is automatically invoked when:
- User provides meeting notes to structure
- User wants to document a meeting
- User needs action item tracking from a meeting
- User asks to "take minutes" or "structure notes"

## What This Skill Provides

### 1. Meeting Metadata
- Meeting date and time
- Attendees list
- Meeting purpose/objective
- Location (if provided)

### 2. Discussion Summary
- Key topics discussed
- Main points from each topic
- Context and background provided
- Concerns or issues raised

### 3. Decisions Made
- Clear list of decisions
- Rationale (if provided)
- Who made the decision
- Implications or next steps from decision

### 4. Action Items
- Specific, actionable tasks
- Assigned owner for each action
- Due date or timeline
- Status (typically "Open" for new minutes)
- Dependencies (if applicable)

### 5. Open Questions & Issues
- Unresolved questions
- Issues that need further discussion
- Items requiring clarification
- Parking lot items

### 6. Next Steps
- Next meeting date/time
- Topics for next meeting
- Pre-work required
- Follow-up actions

## Output Format

Structure meeting minutes using this template:

```markdown
# Meeting Minutes: [Meeting Title/Purpose]

## Meeting Details
- **Date**: [Date and time]
- **Attendees**: [List of attendees]
- **Location**: [Physical/Virtual location]
- **Purpose**: [Brief description of meeting objective]

## Discussion Summary

### [Topic 1]
- [Key point 1]
- [Key point 2]
- [Concerns raised]

### [Topic 2]
- [Key point 1]
- [Key point 2]

## Decisions Made

1. **[Decision 1]**
   - Rationale: [Why this decision was made]
   - Impact: [What this means]
   - Decided by: [Person/group]

2. **[Decision 2]**
   - Rationale: [Why]
   - Impact: [What this means]

## Action Items

| Action | Owner | Due Date | Status | Notes |
|--------|-------|----------|--------|-------|
| [Specific action 1] | [Name] | [Date] | Open | [Any notes] |
| [Specific action 2] | [Name] | [Date] | Open | [Dependencies] |
| [Specific action 3] | [Name] | [Date] | Open | |

## Open Questions & Issues

- **[Question 1]**: [Context if needed]
- **[Issue 1]**: [Description and why it's unresolved]
- **[Question 2]**: [Context]

## Risks & Concerns

- **[Risk/Concern 1]**: [Description and potential impact]
- **[Risk/Concern 2]**: [Description]

## Next Steps

1. [Immediate next step]
2. [Follow-up action]
3. [Preparation for next meeting]

**Next Meeting**: [Date/Time if scheduled, or "TBD"]
**Agenda Items for Next Meeting**:
- [Topic 1]
- [Topic 2]

---
*Minutes prepared by: [Agent-generated]*
*Date prepared: [Current date]*
```

## Guidelines for Structuring

### From Unstructured Notes

When given raw, unstructured notes:

1. **Extract Meeting Context**:
   - Look for dates, names, locations
   - Infer purpose from content if not stated

2. **Identify Discussion Points**:
   - Group related comments into topics
   - Capture who said what (if names provided)
   - Note areas of agreement/disagreement

3. **Spot Decisions**:
   - Look for definitive statements: "agreed", "decided", "approved"
   - Capture what was decided and by whom
   - Note any conditions or caveats

4. **Extract Action Items**:
   - Look for task verbs: "will", "need to", "should", "must"
   - Identify owners from context: "[Name] will...", "[Name] said they would..."
   - Infer due dates from context: "by next week", "before Q2", "ASAP"
   - If owner/date unclear, flag as "[TBD]"

5. **Identify Open Items**:
   - Look for questions: "?", "not sure", "need to clarify"
   - Spot unresolved issues: "still discussing", "to be determined"
   - Note parking lot items: "let's discuss later", "follow up offline"

### For Banking/Risk Meetings

When meeting notes involve risk management or regulatory topics:

- **Reference frameworks**: Mention Basel, IFRS, risk appetite if relevant
- **Governance items**: Flag decisions requiring Board/Committee approval
- **Regulatory implications**: Note if regulator engagement needed
- **Risk flags**: Highlight any risks to timelines, compliance, or delivery
- **Approval paths**: Note approval requirements for decisions

### Quality Checklist

Before finalizing minutes, ensure:
- ✅ All action items have owners (or marked [TBD])
- ✅ Action items are specific and actionable (not vague)
- ✅ Decisions are clearly stated (not buried in discussion)
- ✅ Due dates are realistic and clear
- ✅ Open questions are captured for follow-up
- ✅ Next meeting is scheduled or noted as TBD
- ✅ Meeting purpose/context is clear for future reference
- ✅ Attendees are listed (helps with accountability)

## Example Transformation

**Input (Raw Notes)**:
```
Met with credit risk team about Basel IV. John raised concerns about
data quality for new risk weights. Sarah from IT said system changes
will take 6 months minimum. Agreed to present plan to board next month.
Mike will draft the board paper. Need to hire 2 more analysts. Timeline
is tight with Jan 2025 deadline. Question about whether standardized
approach applies to all portfolios.
```

**Output (Structured Minutes)**:
```markdown
# Meeting Minutes: Basel IV Implementation Planning

## Meeting Details
- **Date**: [Today's date]
- **Attendees**: Credit Risk Team, John, Sarah (IT), Mike
- **Purpose**: Discuss Basel IV implementation approach and timeline

## Discussion Summary

### Basel IV Implementation Approach
- Team reviewed requirements for new standardized approach
- Discussion of implementation timeline and key milestones
- Regulatory deadline: January 2025

### Data Quality Concerns
- John raised concerns about data quality for calculating new risk weights
- Current data may not support granularity required
- Needs assessment and remediation plan

### System Requirements
- Sarah (IT) assessed system change requirements
- Minimum 6 months needed for system modifications
- Critical path item for overall timeline

### Resource Requirements
- Identified need for additional analytical capacity
- 2 more risk analysts required for implementation team

## Decisions Made

1. **Board Presentation**
   - Rationale: Need executive approval for budget and timeline
   - Impact: Board paper required by next month
   - Decided by: Team consensus

## Action Items

| Action | Owner | Due Date | Status | Notes |
|--------|-------|----------|--------|-------|
| Draft board presentation paper | Mike | Next month | Open | Include budget, timeline, risks |
| Assess data quality gaps | John | TBD | Open | For new risk weight calculations |
| Confirm system change timeline | Sarah/IT | Next meeting | Open | Detailed requirements needed |
| Initiate analyst recruitment | [TBD] | ASAP | Open | 2 FTE required |

## Open Questions & Issues

- **Portfolio Scope**: Does standardized approach apply to all portfolios or subset?
  - Needs regulatory clarification
- **Data Quality**: What is the extent of data gaps and remediation timeline?
- **System Changes**: What is detailed scope of IT changes and dependencies?

## Risks & Concerns

- **Timeline Risk**: 6-month IT timeline creates pressure on January 2025 deadline
- **Data Quality**: Potential delays if data remediation more extensive than expected
- **Resource Risk**: Delay in hiring analysts could impact delivery

## Next Steps

1. Mike to begin drafting board paper
2. John to scope data quality assessment
3. Sarah to provide detailed IT requirements
4. HR to start analyst recruitment process
5. Schedule follow-up meeting to review progress

**Next Meeting**: [TBD - within 2 weeks]
**Agenda Items for Next Meeting**:
- Data quality assessment results
- Detailed IT requirements and timeline
- Board paper review (draft)
- Recruitment progress

---
*Minutes prepared by: Risk Agent (meeting-minutes skill)*
*Date prepared: [Current date]*
```

## Tips for Effective Use

1. **Provide full context**: The more detail in the input notes, the better the structured output
2. **Include names**: Helps assign action items correctly
3. **Note timing**: Any mentions of "next week", "Q2", "by Friday" help set due dates
4. **Capture concerns**: Even vague concerns should be noted for follow-up
5. **Iterate if needed**: Can ask for refinement if initial output needs adjustment

## Integration with Change-Agent

When the change-agent invokes this skill:
- Skill provides the structured format
- change-agent adds banking/risk context
- change-agent flags governance or regulatory items
- change-agent suggests realistic timelines based on domain knowledge
