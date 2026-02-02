# Skill Detection Implementation

## Overview

Updated the CLI to detect and display skill invocations with distinct visual styling, making it clear when skills are being used vs regular tools.

## What Was Changed

### File: `src/cli_utils.py`

**1. Added Skill Message Types**
- `skill_use`: Bright magenta border, displays when a skill is invoked
- `skill_result`: Bright cyan border, displays the skill's output

**2. Added Skill Tracking**
```python
_skill_tool_use_ids = {}  # Tracks skill invocations to match results
```

**3. Updated Message Parsing**

**Detection Logic:**
```python
if block.name == "Skill":
    skill_name = block.input.get("skill", "unknown")  # SDK uses "skill" key
    skill_args = block.input.get("args", {})
    _skill_tool_use_ids[block.id] = skill_name
    # Display as skill invocation
```

**Result Matching:**
```python
if block.tool_use_id in _skill_tool_use_ids:
    skill_name = _skill_tool_use_ids[block.tool_use_id]
    # Display as skill result
```

## How It Works

### Message Flow

1. **Skill Invocation (AssistantMessage)**
   ```
   ToolUseBlock(
       name="Skill",
       input={
           "skill": "meeting-minutes",  # SDK uses "skill" not "skill_name"
           "args": {...}
       }
   )
   ```
   - Detected by checking `block.name == "Skill"`
   - Skill name extracted from `input["skill"]`
   - Displays in bright magenta panel: "Skill Invocation"
   - Shows skill name and arguments

2. **Skill Result (UserMessage)**
   ```
   ToolResultBlock(
       tool_use_id="toolu_01ABC123",
       content=[...]
   )
   ```
   - Matched using `_skill_tool_use_ids` tracker
   - Displays in bright cyan panel: "Skill Output"
   - Shows skill name and formatted output

### Visual Distinction

**Before:**
- Skills appeared as generic "Tool Use" with name "Skill"
- Hard to distinguish from other tools
- Skill name buried in JSON

**After:**
- Skills have distinct "Skill Invocation" panel (bright magenta)
- Skill name prominently displayed
- Results labeled "Skill Output" (bright cyan)
- Clear visual separation from regular tools

## Testing

**Test Command:**
```bash
uv run riskagent
```

**Test Input:**
```
Read the transcript from data/Energy VaR Project Phasing Options.docx and create meeting minutes
```

**Expected Output:**

1. **Tool Use** (blue) - Bash command to extract text
2. **Tool Result** (magenta) - Extracted text
3. **Skill Invocation** (bright magenta):
   ```
   Skill: meeting-minutes

   Arguments:
   {
     "meeting_notes": "..."
   }
   ```
4. **Skill Output** (bright cyan):
   ```
   Skill 'meeting-minutes' completed

   [Structured meeting minutes following template]
   ```

## Color Scheme

| Message Type | Border Color | Title |
|-------------|--------------|-------|
| User | Yellow | User Prompt |
| Assistant | Green | Risk Agent |
| Tool Use | Blue | Tool Use |
| Tool Result | Magenta | Tool Result |
| **Skill Use** | **Bright Magenta** | **Skill Invocation** |
| **Skill Result** | **Bright Cyan** | **Skill Output** |
| System | Cyan | System Message |

## Key Implementation Details

### Why Track tool_use_ids?

Skills are invoked via `ToolUseBlock` with `name="Skill"`, but the actual skill name is nested in `input["skill_name"]`. When the result comes back as a `ToolResultBlock`, it only contains `tool_use_id` - not the skill name.

**Solution:** Store a mapping of `tool_use_id` → `skill_name` when we see a skill invocation, then look it up when we receive the result.

### Why Check block.name == "Skill"?

All skill invocations use the generic tool name "Skill". The actual skill identifier is in the nested `input["skill_name"]` field. This is the official Claude SDK convention.

### Thread Safety

The current implementation uses a module-level dictionary `_skill_tool_use_ids`. This works for single-threaded CLI usage. If you need concurrent conversation support, replace with a thread-safe data structure.

## Future Enhancements

Possible improvements:

1. **Skill Statistics**: Track total skills invoked, success rate
2. **Skill Timing**: Measure skill execution duration
3. **Skill Icons**: Add emoji or symbols for different skill types
4. **Nested Skills**: Handle skills that invoke other skills
5. **Skill Errors**: Special formatting for skill failures
6. **Skill Arguments**: Truncate/summarize large arguments for readability

## Troubleshooting

### Skills Not Detected

**Symptom:** Skills still show as regular "Tool Use"

**Check:**
1. `'Skill'` is in `allowed_tools` (line 103 of risk_agent_cli.py)
2. Skills exist in `.claude/skills/*/SKILL.md`
3. `setting_sources=["project"]` is configured

### Skill Results Not Matched

**Symptom:** Results show as regular "Tool Result" instead of "Skill Output"

**Cause:** The `tool_use_id` isn't being tracked properly

**Debug:**
```python
# Add after line 164:
print(f"DEBUG: Tracking skill {skill_name} with ID {block.id}")

# Add after line 181:
print(f"DEBUG: Checking tool_use_id {block.tool_use_id}")
print(f"DEBUG: Known skill IDs: {_skill_tool_use_ids.keys()}")
```

### Skills Not Invoked at All

**Symptom:** No skill invocations appear, even when expected

**Cause:** Skills aren't enabled or descriptions don't match the query

**Check:**
1. Verify `'Skill'` in `allowed_tools`
2. Check skill descriptions in SKILL.md are clear and specific
3. Test with explicit skill-matching query

---

*Last Updated: 2025-01-05*
*Risk Agent Framework v0.1.0*
