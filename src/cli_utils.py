"""
CLI utility functions for Risk Agent
Adapted from kenneth-liao/claude-agent-sdk-intro
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
from rich import print
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.console import Console
from rich.syntax import Syntax
from typing import Literal
import json

# Track skill invocations to match results
_skill_tool_use_ids = {}


def is_json_string(text: str) -> bool:
    """Check if a string is valid JSON"""
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError:
        return False


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


def print_rich_message(
        type: Literal["user", "assistant", "tool_use", "tool_result", "system", "skill_use", "skill_result"],
        message: str,
        console: Console
        ):
    """
    Prints a message in a panel with a title and border color based on the message type.
    """
    styles = {
        "user": {
            "message_style": "bold yellow",
            "panel_title": "User Prompt",
            "border_style": "yellow"
            },
        "assistant": {
            "message_style": "bold green",
            "panel_title": "Risk Agent",
            "border_style": "green"
            },
        "tool_use": {
            "message_style": "bold blue",
            "panel_title": "Tool Use",
            "border_style": "blue"
            },
        "tool_result": {
            "message_style": "bold magenta",
            "panel_title": "Tool Result",
            "border_style": "magenta"
            },
        "skill_use": {
            "message_style": "bold bright_magenta",
            "panel_title": "Skill Invocation",
            "border_style": "bright_magenta"
            },
        "skill_result": {
            "message_style": "bold bright_cyan",
            "panel_title": "Skill Output",
            "border_style": "bright_cyan"
            },
        "system": {
            "message_style": "bold cyan",
            "panel_title": "System Message",
            "border_style": "cyan"}
    }

    # For tool results and skill results, try to apply JSON syntax highlighting
    if type in ["tool_result", "skill_result"] and is_json_string(message):
        panel_content = Syntax(message, "json", theme="monokai", line_numbers=False)
    else:
        panel_content = Text(message, style=styles[type]["message_style"])

    # Use consistent full-width panels for all message types
    panel = Panel(
        panel_content,
        title=styles[type]["panel_title"],
        border_style=styles[type]["border_style"],
        expand=True  # Force full width
    )
    console.print(panel, end="\n\n")


def print_simple_message(
        type: Literal["user", "assistant", "tool_use", "tool_result", "system", "skill_use", "skill_result"],
        message: str,
        console: Console
        ):
    """
    Prints a message in simple text format (no Rich formatting).
    Similar to standard Claude Code output, suitable for Telegram.
    """
    prefixes = {
        "user": "👤 User:",
        "assistant": "🤖 Risk Agent:",
        "tool_use": "🔨 Tool:",
        "tool_result": "📋 Result:",
        "skill_use": "🔧 Skill:",
        "skill_result": "✅ Skill Result:",
        "system": "ℹ️  System:"
    }

    prefix = prefixes.get(type, "")
    console.print(f"\n{prefix}\n{message}\n")


def parse_and_print_message(
        message: Message,
        console: Console,
        print_stats: bool = False,
        verbose: bool = False,
        interface: Literal["rich", "simple"] = "rich"
        ):
    """
    Parse and print a message based on its type and content.

    Args:
        message: Message to parse and print
        console: Rich console for output
        print_stats: Whether to print session statistics
        verbose: If True, show all tool calls and results (not just skills)
        interface: Display mode - "rich" (panels/colors) or "simple" (plain text)
    """
    # Choose the print function based on interface mode
    print_fn = print_simple_message if interface == "simple" else print_rich_message

    # Handle different message types
    if isinstance(message, SystemMessage):
        if message.subtype == "compact_boundary":
            print_fn(
                "system",
                f"Compaction completed \nPre-compaction tokens: {message.data['compact_metadata']['pre_tokens']} \nTrigger: {message.data['compact_metadata']['trigger']}",
                console
                )
        else:
            print_fn("system", json.dumps(message.data, indent=2), console)

    elif isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                print_fn("assistant", block.text, console)
            elif isinstance(block, ToolUseBlock):
                # Check if this is a Skill invocation
                if block.name == "Skill":
                    # Extract skill name from input (SDK uses "skill" key)
                    skill_name = block.input.get("skill", "unknown")
                    skill_args = block.input.get("args", {})

                    # Track this skill invocation
                    _skill_tool_use_ids[block.id] = skill_name

                    # Format skill invocation message
                    skill_message = f"Skill: {skill_name}\n\nArguments:\n{json.dumps(skill_args, indent=2)}"
                    print_fn("skill_use", skill_message, console)
                else:
                    # Regular tool use - only show in verbose mode
                    if verbose:
                        print_fn("tool_use", f"Tool: {block.name}\n\nInput:\n{json.dumps(block.input, indent=2)}", console)
            elif isinstance(block, ThinkingBlock):
                print_fn("assistant", "Thinking...", console)

    elif isinstance(message, UserMessage):
        for block in message.content:
            if isinstance(block, ToolResultBlock):
                formatted_content = format_tool_result(block.content)

                # Check if this is a result from a skill invocation
                if block.tool_use_id in _skill_tool_use_ids:
                    skill_name = _skill_tool_use_ids[block.tool_use_id]
                    print_fn("skill_result", f"Skill '{skill_name}' completed\n\n{formatted_content}", console)
                    # Clean up the tracking dict
                    del _skill_tool_use_ids[block.tool_use_id]
                else:
                    # Regular tool result - only show in verbose mode
                    if verbose:
                        print_fn("tool_result", formatted_content, console)

    elif isinstance(message, ResultMessage):
        if print_stats:
            result = message.subtype
            session_id = message.session_id
            duration_s = message.duration_ms / 1000
            cost_usd = message.total_cost_usd
            input_tokens = message.usage["input_tokens"]
            output_tokens = message.usage["output_tokens"]

            # Create a Rich table for session stats
            table = Table(title="Session Statistics", show_header=True, header_style="bold cyan")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")

            table.add_row("Session ID", session_id)
            table.add_row("Result", result)
            table.add_row("Duration (s)", f"{duration_s:.2f}")
            table.add_row("Cost (USD)", f"${cost_usd:.4f}" if cost_usd else "N/A")
            table.add_row("Input Tokens", str(input_tokens))
            table.add_row("Output Tokens", str(output_tokens))

            console.print(table)
