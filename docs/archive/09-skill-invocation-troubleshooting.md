# Skill Invocation Troubleshooting

## Issue: Skills Not Being Invoked

### Observed Behavior
When asking to "complete ITC template", the agent creates custom Python scripts (analyze_template.py, fill_itc_template.py) instead of invoking the `project-template-filler` skill.

### Root Cause Analysis

**Skill invocation depends on**:
1. ✅ Skill exists in `.claude/skills/[name]/SKILL.md`
2. ✅ `'Skill'` is in `allowed_tools` in risk_agent_cli.py
3. ✅ `setting_sources=["project"]` is configured
4. ❌ **Skill description matches the user's query keywords**
5. ❌ **Model chooses Skill tool over other available tools (Bash, Write)**

### The Problem

When the model has access to both:
- `'Skill'` tool (for invoking skills)
- `'Bash'` + `'Write'` tools (for creating scripts)

It may choose to use Bash/Write to create a custom solution instead of invoking a skill, especially if:
- The skill description doesn't exactly match the query
- The model thinks it can solve the problem more directly with code
- The skill description is too long/complex

## Solutions Attempted

### 1. Updated Skill Description ✅
Changed from:
```yaml
description: Populates ITC (Investment Technology Committee) project governance templates...
```

To:
```yaml
description: Automatically fills out ITC Project Template Excel files. Use this skill when user asks to "complete ITC template", "fill template", "populate template"...
```

**Rationale**: More direct keywords matching user queries

### 2. Added Explicit "When to Use" Section ✅
```markdown
**ALWAYS USE THIS SKILL** (do not write custom Python scripts) when:
- User asks to "complete", "fill", "populate", or "fill out" an ITC template
```

**Rationale**: Explicitly instruct NOT to use alternative approaches

### 3. Updated Change-Agent Instructions ✅
```markdown
**IMPORTANT**: Always use skills for specialized tasks - DO NOT write custom Python scripts or bash commands to replicate skill functionality.
```

**Rationale**: Agent-level instruction to prefer skills

## Testing Strategy

### Test 1: Direct Skill Keyword Match
**Query**: "Use the project-template-filler skill to complete the ITC template"

**Expected**: Skill invoked immediately (explicit skill name mentioned)

**If fails**: Skill tool not properly configured or not available

### Test 2: Natural Language with Keywords
**Query**: "Fill out the ITC template using the meeting minutes"

**Expected**: Skill invoked based on "fill", "ITC template" keywords

**If fails**: Skill description not matching query well enough

### Test 3: Verbose Request
**Query**: "I need to complete the Investment Technology Committee project governance template for the Energy VaR project using information from the meeting minutes"

**Expected**: Skill invoked based on context match

**If fails**: Too verbose, model choosing to break down task differently

## Recommended Next Steps

### Option 1: Simplify Skill Description (Most Likely to Work)
Make the description ultra-short and keyword-focused:

```yaml
---
name: project-template-filler
description: Fills ITC Project Template Excel files from meeting minutes and project documents. Use when user asks to complete, fill, or populate ITC template.
---
```

### Option 2: Remove Competing Tools Temporarily
Test with more restricted `allowed_tools`:

```python
allowed_tools=[
    'Skill',  # Only skills
    'Read',   # Reading files
    'Write',  # Writing output (but not scripts)
    'Task',   # Sub-agents
    # Temporarily remove: 'Bash', 'Edit'
]
```

This forces the model to use skills instead of creating custom scripts.

### Option 3: Create a Slash Command
Create `.claude/commands/fill-itc-template.md`:

```markdown
Use the project-template-filler skill to populate the ITC Project Template with information from the Energy VaR meeting minutes.

Template path: data/icbc_standard_bank/Projects/Energy/Governance/ITC Project Template.xlsx
Meeting minutes: data/icbc_standard_bank/Projects/Energy/Meeting Minutes/Energy_VaR_Project_Meeting_Minutes_20251020.md
```

Then use: `/fill-itc-template`

### Option 4: Explicit Skill Invocation Instruction
Update the skill's "When to Use" section to be even more prominent (in the agent, not the skill):

In `change-agent.md`:
```markdown
## Critical: When to Use Skills

Before using Bash, Write, or Edit tools to create custom solutions, FIRST check if a skill exists:

**Template Population Tasks**:
- ❌ DON'T: Write Python scripts to parse templates
- ✅ DO: Invoke project-template-filler skill

**Meeting Documentation Tasks**:
- ❌ DON'T: Manually format meeting notes
- ✅ DO: Invoke meeting-minutes skill
```

## Diagnostic Questions

### Is the Skill Being Loaded?
Check skill availability in a query:
```
List all available skills in this project
```

Expected: Should mention project-template-filler

### Is the Skill Tool Available?
The CLI should show skill invocations with bright magenta "Skill Invocation" panels. If you're not seeing ANY skills invoked (including meeting-minutes), then the Skill tool may not be configured correctly.

### Test with meeting-minutes Skill
Try:
```
Structure these meeting notes: Met with team about project X. John raised concerns. Sarah needs 2 weeks.
```

**If meeting-minutes skill works**: Problem is specific to project-template-filler description/matching
**If meeting-minutes also fails**: Problem is with Skill tool configuration globally

## Current Configuration Status

### ✅ Completed
- Skill file exists: `.claude/skills/project-template-filler/SKILL.md`
- Skill tool enabled: `'Skill'` in allowed_tools (line 103 of risk_agent_cli.py)
- Settings configured: `setting_sources=["project"]`
- Skill description updated with direct keywords
- Change-agent updated with skill preference instruction

### ⚠️ To Verify
- Skill is actually loaded at runtime (test with explicit mention)
- Skill description is matching the query pattern
- Model is choosing Skill tool over Bash/Write tools

### ❌ Not Tested Yet
- Actual skill invocation with template population
- End-to-end workflow with real data
- Gap analysis output quality

## Quick Fix Recommendation

**Immediate action**: Try this exact query in your CLI:

```
Use the meeting-minutes skill to structure these notes: Met about Energy VaR. Tom sponsored. Phil leads front office piece. Richard leads risk piece. Model validation needed.
```

**If this works** (you see bright magenta "Skill Invocation" panel):
- Skills ARE working
- Problem is project-template-filler description not matching queries
- Solution: Simplify description further

**If this doesn't work** (no skill invocation, just formatted output):
- Skills are NOT being invoked at all
- Problem is configuration issue
- Solution: Debug Skill tool availability

## Alternative: Hybrid Approach

Since the agent already created working Python scripts, you could:

1. **Keep the skill for documentation/future**
2. **Create a helper script** that wraps the logic
3. **Add it to the project** as a utility
4. **Reference it in documentation**

But this defeats the purpose of using skills - skills should be automatically invoked, not manually scripted.

## References

- [skill-detection-implementation.md](06-skill-detection-implementation.md) - How skill detection works
- [project-template-filler SKILL.md](../.claude/skills/project-template-filler/SKILL.md) - The skill definition
- [change-agent.md](../.claude/agents/change-agent.md) - Agent configuration

---

*Created: 2025-01-08*
*Status: Investigating skill invocation issues*
