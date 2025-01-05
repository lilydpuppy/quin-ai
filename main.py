import os
import discord # discord.py-self
import json
import logging
import yaml
import re
from llm_bot import LLMBot
from discord.ext import commands # discord.py-self

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration file
CONFIG_PATH = "config.yaml"

def load_config(path):
    """Load configuration from a YAML file."""
    try:
        with open(path, "r") as file:
            config = yaml.safe_load(file)
            logger.info(f"Configuration loaded from {path}")
            return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {path}")
        exit(1)
    except yaml.YAMLError as e:
        logger.error(f"Error parsing configuration file: {e}")
        exit(1)

CONFIG = load_config(CONFIG_PATH)

# Validate the bot token
token = CONFIG.get('bot', {}).get('token')
if not token or token == "PLACEHOLDER_TOKEN":
    logger.error("Bot token is missing or not set in the configuration.")
    exit(1)

# Initialize the bot with commands extension
bot_client = commands.Bot(command_prefix=CONFIG['bot']['command_prefix'])

# Create an instance of LLMBot with llama3.1 model
bot = LLMBot(model=CONFIG['bot']['model'])

bot.add_message("system", CONFIG['bot']['default_system_prompt'])


class MessageHandler:
    """
    This class handles messages, including user interaction, and fetching responses from the bot.
    """

    @staticmethod
    async def process_message(message):
        """Process incoming messages and get the bot's response."""
        if message.author == bot_client.user:
            return

        if message.author.id == 247283454440374274:  # Special case for ydgdrasil
            await MessageHandler.handle_ydgdrasil_message(message)
        else:
            await MessageHandler.handle_normal_message(message)

    @staticmethod
    async def handle_ydgdrasil_message(message):
        """Handle messages from a specific user (ydgdrasil)."""
        pattern = r"\*\*(\S+)\*\* <:(\S+):(\d+)> (.+)"
        match = re.match(pattern, message.content)
        if match:
            username = match.group(1)  # extract the username
            text = match.group(4)  # extract context

            user_message = {
                "username": username,
                "userid": message.author.id,
                "content": text
            }
            user_message_json = json.dumps(user_message, indent=4)
            logger.debug(f"User message: {user_message_json}")

            bot.add_message("user", user_message_json)

            response = bot.chat(stream=False, temperature=0.7)
            if response and (not "no_response_please" in response.lower()):
                await message.channel.send(response)
                bot.add_message("assistant", response)

    @staticmethod
    async def handle_normal_message(message):
        """Handle regular user messages."""

        user_message = {
            "username": message.author.name,
            "userid": message.author.id,
            "content": message.content
        }
        user_message_json = json.dumps(user_message, indent=4)

        bot.add_message("user", user_message_json)

        response = bot.chat(stream=False, temperature=0.7)
        if response and (not "no_response_please" in response.lower()):
            await message.channel.send(response)
            bot.add_message("assistant", response)

class CommandHandler:
    """
    This class centralizes the command handling logic.
    """

    @staticmethod
    async def set_prompt(ctx, new_prompt: str):
        """Set a new system prompt."""
        global CONFIG
        if ctx.author.id in CONFIG['allowed_users']:
            CONFIG['default_system_prompt'] = new_prompt.strip()
            await ctx.send(f"System prompt set: {new_prompt}")
            logger.info(f"System prompt updated by {ctx.author.name}")
        else:
            await ctx.send("You do not have permission to change the system prompt.")

    @staticmethod
    async def clear_history(ctx):
        """Clear conversation history."""
        if ctx.author.id in CONFIG['allowed_users']:
            bot.clear_history()
            await ctx.send("History cleared.")
            logger.info("Conversation history cleared.")
        else:
            await ctx.send("You do not have permission to clear the history.")

    @staticmethod
    async def show_history(ctx):
        """Show conversation history."""
        if ctx.author.id in CONFIG['allowed_users']:
            history = bot.get_history()
            await ctx.send(f"My history:\n>>> {history}")
            logger.info("Conversation history shown.")
        else:
            await ctx.send("You do not have permission to view the history.")


@bot_client.event
async def on_ready():
    logger.info(f'Logged in as {bot_client.user}')


@bot_client.event
async def on_message(message):
    # Skip processing for bot's own messages
    if message.author == bot_client.user:
        return

    # Check if the message is a command (starts with the bot's prefix)
    if message.content.startswith(bot_client.command_prefix):
        # Process the command (this ensures that commands like !setprompt, !clearhistory, etc., are processed)
        await bot_client.process_commands(message)
    else:
        # Process the message normally (not a command)
        await MessageHandler.process_message(message)


# Bot commands
@bot_client.command()
async def setprompt(ctx, *, new_prompt: str):
    """Command to set a new system prompt."""
    await CommandHandler.set_prompt(ctx, new_prompt)


@bot_client.command()
async def clearhistory(ctx):
    """Command to clear conversation history."""
    await CommandHandler.clear_history(ctx)


@bot_client.command()
async def showhistory(ctx):
    """Command to show conversation history."""
    await CommandHandler.show_history(ctx)


# Run the bot
bot_client.run(token)
