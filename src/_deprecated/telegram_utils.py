"""
Telegram utility functions for Risk Agent
Handles message extraction and formatting for Telegram bot
"""

from claude_agent_sdk import (
    AssistantMessage,
    TextBlock,
    ResultMessage,
    ToolUseBlock,
    ToolResultBlock,
    ThinkingBlock,
    UserMessage,
    Message,
    SystemMessage
)
import json
from typing import List, Dict, Any

# Track skill invocations to match results
_skill_tool_use_ids = {}


def format_tool_result(content) -> str:
    """
    Format tool result content nicely, handling nested JSON strings.
    """
    if isinstance(content, str):
        # Try to parse as JSON and format it
        try:
            parsed = json.loads(content)
            return json.dumps(parsed, indent=2)
        except json.JSONDecodeError:
            return content
    elif isinstance(content, list):
        # Handle list of content blocks (common format)
        formatted_parts = []
        for item in content:
            if isinstance(item, dict) and "text" in item:
                # Try to parse the text field as JSON
                text_content = item["text"]
                try:
                    parsed_json = json.loads(text_content)
                    formatted_json = json.dumps(parsed_json, indent=2)
                    formatted_parts.append(formatted_json)
                except json.JSONDecodeError:
                    # If not JSON, just use the text as-is
                    formatted_parts.append(text_content)
            else:
                # For other dict structures, format as JSON
                formatted_parts.append(json.dumps(item, indent=2))
        return "\n\n".join(formatted_parts)
    else:
        # For other types, convert to JSON
        return json.dumps(content, indent=2)


def extract_message_text(message: Message, verbose: bool = False) -> List[str]:
    """
    Extract text content from a message for Telegram display.
    Returns a list of strings (one per message part).

    Args:
        message: Message to extract text from
        verbose: If True, include tool calls and results

    Returns:
        List of text strings to send to Telegram
    """
    results = []

    # Handle different message types
    if isinstance(message, SystemMessage):
        if message.subtype == "compact_boundary":
            text = (f"ℹ️ System:\n"
                   f"Compaction completed\n"
                   f"Pre-compaction tokens: {message.data['compact_metadata']['pre_tokens']}\n"
                   f"Trigger: {message.data['compact_metadata']['trigger']}")
            results.append(text)
        else:
            results.append(f"ℹ️ System:\n{json.dumps(message.data, indent=2)}")

    elif isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                # Main assistant response - always show
                results.append(f"🤖 Risk Agent:\n{block.text}")

            elif isinstance(block, ToolUseBlock):
                # Check if this is a Skill invocation
                if block.name == "Skill":
                    # Extract skill name from input
                    skill_name = block.input.get("skill", "unknown")
                    skill_args = block.input.get("args", {})

                    # Track this skill invocation
                    _skill_tool_use_ids[block.id] = skill_name

                    # Format skill invocation - always show
                    skill_text = (f"🔧 Skill: {skill_name}\n\n"
                                 f"Arguments:\n{json.dumps(skill_args, indent=2)}")
                    results.append(skill_text)
                else:
                    # Regular tool use - only show in verbose mode
                    if verbose:
                        tool_text = (f"🔨 Tool: {block.name}\n\n"
                                    f"Input:\n{json.dumps(block.input, indent=2)}")
                        results.append(tool_text)

            elif isinstance(block, ThinkingBlock):
                # Show thinking indicator
                results.append("🤖 Risk Agent:\nThinking...")

    elif isinstance(message, UserMessage):
        for block in message.content:
            if isinstance(block, ToolResultBlock):
                formatted_content = format_tool_result(block.content)

                # Check if this is a result from a skill invocation
                if block.tool_use_id in _skill_tool_use_ids:
                    skill_name = _skill_tool_use_ids[block.tool_use_id]
                    result_text = (f"✅ Skill Result: {skill_name}\n\n"
                                  f"{formatted_content}")
                    results.append(result_text)
                    # Clean up the tracking dict
                    del _skill_tool_use_ids[block.tool_use_id]
                else:
                    # Regular tool result - only show in verbose mode
                    if verbose:
                        results.append(f"📋 Result:\n{formatted_content}")

    elif isinstance(message, ResultMessage):
        # Session statistics - format as simple text
        session_id = message.session_id
        duration_s = message.duration_ms / 1000
        cost_usd = message.total_cost_usd
        input_tokens = message.usage["input_tokens"]
        output_tokens = message.usage["output_tokens"]

        stats_text = (f"📊 Session Statistics:\n"
                     f"Session ID: {session_id}\n"
                     f"Result: {message.subtype}\n"
                     f"Duration: {duration_s:.2f}s\n"
                     f"Cost: ${cost_usd:.4f}" if cost_usd else "Cost: N/A\n"
                     f"Input Tokens: {input_tokens}\n"
                     f"Output Tokens: {output_tokens}")
        results.append(stats_text)

    return results


def split_long_message(text: str, max_length: int = 4000) -> List[str]:
    """
    Split a long message into chunks that fit Telegram's 4096 character limit.
    Leaves some buffer for safety.

    Args:
        text: Text to split
        max_length: Maximum length per chunk (default 4000)

    Returns:
        List of text chunks
    """
    if len(text) <= max_length:
        return [text]

    chunks = []
    current_chunk = ""

    # Split by lines to avoid breaking mid-sentence
    lines = text.split('\n')

    for line in lines:
        # If a single line is too long, split it by words
        if len(line) > max_length:
            words = line.split(' ')
            for word in words:
                if len(current_chunk) + len(word) + 1 > max_length:
                    chunks.append(current_chunk)
                    current_chunk = word
                else:
                    current_chunk += ' ' + word if current_chunk else word
        else:
            # Check if adding this line would exceed limit
            if len(current_chunk) + len(line) + 1 > max_length:
                chunks.append(current_chunk)
                current_chunk = line
            else:
                current_chunk += '\n' + line if current_chunk else line

    # Add remaining chunk
    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def format_telegram_code_block(text: str) -> str:
    """
    Format text as a code block for Telegram.
    Telegram uses triple backticks for code blocks.
    """
    return f"```\n{text}\n```"


def escape_telegram_markdown(text: str) -> str:
    """
    Escape special characters for Telegram markdown.
    Note: Only needed if using MarkdownV2 parse mode.
    """
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text
