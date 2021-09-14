import asyncio
import logging
import sys

import toml
from lightbulb import Bot

import argus
from argus.schema import config_schema

logger = logging.getLogger(__name__)
root_logger = logger.parent

# Global Bot Variable
bot = None


def start(**kwargs):
    """
    Starts the bot and obtains all necessary config data.
    """
    # Config Loader
    try:
        config = toml.load(kwargs["config_file"])
    except FileNotFoundError:
        logger.error(
            "No config file provided."
        )
        sys.exit()

    # Validate Config
    config_schema.validate(config)

    # Faster Event Loop
    try:
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        pass

    # Override configs from config file with ones from cli
    if kwargs["log_level"]:
        config["bot"]["log_level"] = kwargs["log_level"].upper()

    # Initialize Bot
    global bot
    bot = Bot(token=config["bot"]["token"], slash_commands_only=True, logs=config["bot"]["log_level"])

    logger.info(f"Starting Argus: {argus.__version__}")
    try:
        bot.run()
    except (KeyboardInterrupt, SystemExit):
        bot.close()
    finally:
        sys.exit()
