"""
Telegram Bot for Risk Agent
Provides remote access to Risk Agent capabilities via Telegram
"""

import os
import json
import asyncio
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

# Load environment variables from .env file if it exists
from dotenv import load_dotenv
load_dotenv()

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from src.telegram_utils import extract_message_text, split_long_message

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Session storage directory
SESSIONS_DIR = Path.home() / ".riskagent" / "telegram_sessions"
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


class RiskAgentSession:
    """
    Manages per-user session state for Risk Agent.
    Each Telegram user gets their own session with:
    - Persistent session_id (conversation history)
    - Working directory (CWD)
    - Verbose mode preference
    """

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.session_file = SESSIONS_DIR / f"{user_id}.json"
        self.session_id: Optional[str] = None
        self.cwd: str = str(Path.cwd())
        self.verbose: bool = False
        self.last_updated: str = datetime.utcnow().isoformat() + "Z"

        # Load existing session if available
        self._load()

    def _load(self):
        """Load session from disk if exists"""
        if self.session_file.exists():
            try:
                with open(self.session_file, 'r') as f:
                    data = json.load(f)
                    self.session_id = data.get("session_id")
                    self.cwd = data.get("cwd", str(Path.cwd()))
                    self.verbose = data.get("verbose", False)
                    self.last_updated = data.get("last_updated")
                    logger.info(f"Loaded session for user {self.user_id}: {self.session_id}")
            except Exception as e:
                logger.error(f"Error loading session for user {self.user_id}: {e}")

    def save(self):
        """Save session to disk"""
        try:
            data = {
                "session_id": self.session_id,
                "cwd": self.cwd,
                "verbose": self.verbose,
                "last_updated": datetime.utcnow().isoformat() + "Z"
            }
            with open(self.session_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Saved session for user {self.user_id}")
        except Exception as e:
            logger.error(f"Error saving session for user {self.user_id}: {e}")

    def update_session_id(self, session_id: str):
        """Update session ID after conversation"""
        self.session_id = session_id
        self.last_updated = datetime.utcnow().isoformat() + "Z"
        self.save()

    def set_cwd(self, cwd: str):
        """Set working directory"""
        if os.path.isdir(cwd):
            self.cwd = os.path.abspath(cwd)
            self.save()
            return True
        return False

    def toggle_verbose(self):
        """Toggle verbose mode"""
        self.verbose = not self.verbose
        self.save()
        return self.verbose

    def get_agent_options(self) -> ClaudeAgentOptions:
        """
        Create ClaudeAgentOptions for this session.
        If session_id exists, SDK will resume previous conversation.
        """
        options = ClaudeAgentOptions(
            model="claude-sonnet-4-5",
            permission_mode="acceptEdits",
            setting_sources=["project"],
            system_prompt="agents/risk-intelligence-engine",
            cwd=self.cwd,
            allowed_tools=[
                'Skill',
                'Read',
                'Write',
                'Edit',
                'MultiEdit',
                'Grep',
                'Glob',
                'Task',
                'TodoWrite',
                'WebSearch',
                'WebFetch',
                'Bash',
            ]
        )

        # Add resume parameter if we have a session_id
        if self.session_id:
            options.resume = self.session_id

        return options


# Store active sessions (user_id -> RiskAgentSession)
active_sessions: Dict[int, RiskAgentSession] = {}


def get_session(user_id: int) -> RiskAgentSession:
    """Get or create session for a user"""
    if user_id not in active_sessions:
        active_sessions[user_id] = RiskAgentSession(user_id)
    return active_sessions[user_id]


# Command Handlers

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    session = get_session(user.id)

    welcome_text = (
        f"👋 Welcome to Risk Agent, {user.first_name}!\n\n"
        f"🤖 I'm your AI-powered risk intelligence assistant.\n\n"
        f"**Commands:**\n"
        f"/help - Show help\n"
        f"/status - Show session status\n"
        f"/setcwd - Set working directory\n"
        f"/verbose - Toggle verbose mode\n"
        f"/reset - Reset conversation\n\n"
        f"Just send me a message to get started!"
    )

    await update.message.reply_text(welcome_text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = (
        "**Risk Agent Help**\n\n"
        "**Commands:**\n"
        "• /start - Welcome message\n"
        "• /help - This help message\n"
        "• /status - Show your session status\n"
        "• /setcwd <path> - Set working directory\n"
        "• /verbose - Toggle verbose mode\n"
        "• /reset - Reset conversation (clears history)\n\n"
        "**Capabilities:**\n"
        "• Project Planning\n"
        "• Meeting Minutes\n"
        "• Status Reports\n"
        "• Stakeholder Analysis\n"
        "• ITC Template Filling\n"
        "• ICC Business Case Filling\n\n"
        "**Usage:**\n"
        "Just send me a message describing what you need help with!"
    )

    await update.message.reply_text(help_text)


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command - show session info"""
    user_id = update.effective_user.id
    session = get_session(user_id)

    status_text = (
        f"**Session Status**\n\n"
        f"User ID: {user_id}\n"
        f"Session ID: {session.session_id or 'New session'}\n"
        f"Working Dir: {session.cwd}\n"
        f"Verbose: {'On' if session.verbose else 'Off'}\n"
        f"Last Updated: {session.last_updated}\n"
    )

    await update.message.reply_text(status_text)


async def setcwd_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /setcwd command - set working directory"""
    user_id = update.effective_user.id
    session = get_session(user_id)

    if not context.args:
        await update.message.reply_text(
            f"Current working directory: {session.cwd}\n\n"
            f"Usage: /setcwd <path>\n"
            f"Example: /setcwd /Users/name/projects/myproject"
        )
        return

    new_cwd = ' '.join(context.args)

    # Validate path
    if not os.path.isdir(new_cwd):
        await update.message.reply_text(
            f"❌ Directory not found: {new_cwd}\n\n"
            f"Please provide a valid directory path."
        )
        return

    # Security check - ensure it's an absolute path
    abs_path = os.path.abspath(new_cwd)

    if session.set_cwd(abs_path):
        await update.message.reply_text(
            f"✅ Working directory set to:\n{abs_path}\n\n"
            f"All file operations will be relative to this directory."
        )
    else:
        await update.message.reply_text(f"❌ Could not set working directory")


async def verbose_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /verbose command - toggle verbose mode"""
    user_id = update.effective_user.id
    session = get_session(user_id)

    verbose = session.toggle_verbose()

    status = "enabled" if verbose else "disabled"
    description = (
        "All tool calls and results will be shown" if verbose
        else "Only showing assistant responses and skills"
    )

    await update.message.reply_text(
        f"🔧 Verbose mode {status}\n\n{description}"
    )


async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /reset command - clear conversation history"""
    user_id = update.effective_user.id
    session = get_session(user_id)

    # Clear session ID to start fresh
    session.session_id = None
    session.save()

    await update.message.reply_text(
        "🔄 Conversation reset\n\n"
        "Starting a fresh session. Previous conversation history cleared."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages - query Risk Agent"""
    user_id = update.effective_user.id
    user_message = update.message.text
    session = get_session(user_id)

    logger.info(f"User {user_id} query: {user_message}")

    # Show typing indicator
    await update.message.chat.send_action(action="typing")

    try:
        # Get agent options for this session
        options = session.get_agent_options()

        # Run agent query
        async with ClaudeSDKClient(options=options) as client:
            # Send user query
            await client.query(user_message)

            # Collect response messages
            messages_to_send = []

            async for message in client.receive_response():
                # Extract text from message
                text_parts = extract_message_text(message, verbose=session.verbose)
                messages_to_send.extend(text_parts)

            # Update session ID after conversation
            # The client's session_id contains the updated conversation
            if hasattr(client, '_session_id'):
                session.update_session_id(client._session_id)

        # Send all collected messages to user
        for text in messages_to_send:
            # Split long messages
            chunks = split_long_message(text, max_length=4000)

            for chunk in chunks:
                await update.message.reply_text(chunk)
                # Small delay between chunks
                if len(chunks) > 1:
                    await asyncio.sleep(0.5)

    except Exception as e:
        logger.error(f"Error processing message for user {user_id}: {e}", exc_info=True)
        await update.message.reply_text(
            f"❌ Sorry, I encountered an error:\n\n{str(e)}\n\n"
            f"Please try again or contact support if the issue persists."
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}", exc_info=context.error)


def main():
    """Start the Telegram bot"""
    # Get bot token from environment
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set!")
        logger.error("Please set your bot token: export TELEGRAM_BOT_TOKEN='your-token-here'")
        return

    # Create application
    app = Application.builder().token(token).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("setcwd", setcwd_command))
    app.add_handler(CommandHandler("verbose", verbose_command))
    app.add_handler(CommandHandler("reset", reset_command))

    # Register message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Register error handler
    app.add_error_handler(error_handler)

    # Start bot
    logger.info("Starting Risk Agent Telegram Bot...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
