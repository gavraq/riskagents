"""
Risk Agent CLI - Main entry point
Follows kenneth-liao conversation loop pattern with Claude Agent SDK
"""

import asyncio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown

# Import our CLI utility functions
from src.cli_utils import parse_and_print_message

console = Console()

def show_welcome():
    """Display welcome banner"""
    welcome = Panel(
        "[bold cyan]Risk Agents[/bold cyan] - AI-Powered Risk Intelligence\n"
        "[dim]MVP: Change Management Agent[/dim]\n\n"
        "Architecture: Orchestrator → Change-Agent → Skills\n\n"
        "[green]✓[/green] Available: Project Planning, Meeting Minutes, Status Reports, Stakeholder Analysis\n"
        "[yellow]⏳[/yellow] Coming Soon: Credit, Market, Operational, Liquidity, Model, Climate, Regulatory, Strategic\n\n"
        "[dim]Commands: help | clear | verbose | interface | exit[/dim]",
        border_style="cyan",
        padding=(1, 2)
    )
    console.print(welcome)

def show_help():
    """Display help information"""
    help_text = """
# Risk Agents Help

## Commands
- **help**: Show this help message
- **clear**: Clear screen (conversation context maintained)
- **verbose** or **v**: Toggle verbose mode (show all tool calls/results)
- **interface** or **i**: Toggle interface mode (rich panels vs simple text)
- **exit**: Exit the application

## Current Capabilities (Change-Agent)

### 1. Project Planning
Create comprehensive project plans with charter, scope, timeline, resources, and risks.

**Example**: `"Help me plan a Basel IV implementation project"`

### 2. Meeting Minutes
Structure meeting notes with action items, decisions, and next steps.

**Example**: `"Structure these meeting notes: [paste your notes]"`

### 3. Status Reports
Generate progress reports with RAG status, risks, and milestones.

**Example**: `"Generate a status report for the IFRS 9 project"`

### 4. Stakeholder Analysis
Map stakeholders with influence/interest and engagement strategies.

**Example**: `"Analyze stakeholders for this regulatory change"`

## How It Works

Your query flows through:
1. **Orchestrator** (risk-intelligence-engine) - Classifies your intent
2. **Change-Agent** - Applies domain expertise
3. **Skills** - Provides structured outputs

## Display Modes

### Interface Mode
- **Rich** (default): Colored panels with borders, syntax highlighting
- **Simple**: Plain text output like standard Claude Code

Toggle with: `interface` command or launch with `uv run riskagent --simple`

### Verbose Mode
By default, the CLI shows a clean interface with only:
- Assistant responses
- Skill invocations and results

In **verbose mode**, you'll see all details like Claude Code terminal:
- Every tool call (Read, Write, Bash, Grep, etc.)
- Tool results (file contents, command outputs)
- Full execution trace

Enable with: `verbose` command or launch with `uv run riskagent --verbose`

### Combining Modes
You can use both together: `uv run riskagent --simple --verbose`
- Simple interface shows plain text (good for Telegram-like output)
- Verbose shows all tool details (good for debugging)

## Tips
- Be specific with project names and context
- Include dates, names, and constraints when available
- Build on previous conversation for iterative refinement
- Use verbose mode when debugging or learning how the agent works
"""
    console.print(Markdown(help_text))

def get_user_input():
    """Get user input with Rich prompt styling"""
    try:
        return Prompt.ask("[bold green]You[/bold green]")
    except (KeyboardInterrupt, EOFError):
        return "exit"


async def main(verbose: bool = False, interface: str = "rich"):
    """
    Main conversation loop

    Args:
        verbose: If True, show all tool calls and results (like Claude Code terminal)
        interface: Display mode - "rich" (panels/colors) or "simple" (plain text)
    """

    show_welcome()

    if verbose:
        console.print("[dim]Verbose mode enabled - showing all tool calls and results[/dim]\n")

    if interface == "simple":
        console.print("[dim]Simple interface mode - plain text output (like Claude Code)[/dim]\n")

    # Configure Agent SDK options
    # Use the risk-intelligence-engine agent as system prompt
    # Output style configured in .claude/settings.local.json
    options = ClaudeAgentOptions(
        model="claude-sonnet-4-5",
        permission_mode="acceptEdits",
        setting_sources=["project"],  # Load settings from .claude/ (includes outputStyle, defaultMode)
        system_prompt="agents/risk-intelligence-engine",  # Use orchestrator agent
        allowed_tools=[
            'Skill',     # CRITICAL - Required for skills to be invoked!
            'Read',
            'Write',
            'Edit',
            'MultiEdit',
            'Grep',
            'Glob',
            'Task',      # Required for subagents!
            'TodoWrite',
            'WebSearch',
            'WebFetch',
            'Bash',
        ]
    )

    console.print("\n[dim]Initializing Risk Intelligence Engine...[/dim]")

    # Main conversation loop with SDK Client
    async with ClaudeSDKClient(options=options) as client:
        console.print("[dim]Agent SDK ready. Type your query or 'help' for assistance.[/dim]\n")

        while True:
            # Get user input
            console.print()
            user_input = get_user_input()

            # Handle exit
            if user_input.lower() in ['exit', 'quit', 'q']:
                console.print("\n[cyan]Thank you for using Risk Agents![/cyan]")
                break

            # Handle help
            if user_input.lower() == 'help':
                show_help()
                continue

            # Handle clear (Note: SDK maintains conversation, so this just shows visual clear)
            if user_input.lower() == 'clear':
                console.clear()
                show_welcome()
                console.print("\n[dim]Screen cleared (conversation context maintained)[/dim]")
                continue

            # Handle verbose toggle
            if user_input.lower() in ['verbose', 'v']:
                verbose = not verbose
                status = "enabled" if verbose else "disabled"
                console.print(f"\n[cyan]Verbose mode {status}[/cyan]")
                console.print(f"[dim]{'All tool calls and results will be shown' if verbose else 'Only showing skill invocations and assistant responses'}[/dim]")
                continue

            # Handle interface toggle
            if user_input.lower() in ['interface', 'i']:
                interface = "simple" if interface == "rich" else "rich"
                console.print(f"\n[cyan]Interface mode: {interface}[/cyan]")
                console.print(f"[dim]{'Plain text output (like Claude Code)' if interface == 'simple' else 'Rich formatted output with panels and colors'}[/dim]")
                continue

            # Send query to agent
            try:
                # Show processing indicator
                with console.status("[bold cyan]Risk Intelligence Engine analyzing query...", spinner="dots"):
                    # Query the risk-intelligence-engine agent
                    # It will route to change-agent which will invoke appropriate skills
                    await client.query(user_input)

                # Receive and display response
                async for message in client.receive_response():
                    # Use proper message parsing from cli_utils
                    # Pass verbose flag and interface mode to control display
                    parse_and_print_message(message, console, print_stats=False, verbose=verbose, interface=interface)

            except Exception as e:
                console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
                console.print("[dim]Please check your setup and try again[/dim]")

def cli():
    """
    CLI entry point for script execution
    Wraps the async main() function
    """
    import sys

    # Check for verbose flag
    verbose = '--verbose' in sys.argv or '-v' in sys.argv

    # Check for interface mode flag
    interface = "simple" if ('--simple' in sys.argv or '-s' in sys.argv) else "rich"

    try:
        asyncio.run(main(verbose=verbose, interface=interface))
    except KeyboardInterrupt:
        console.print("\n[cyan]Interrupted. Goodbye![/cyan]")

if __name__ == "__main__":
    cli()
