import logging
from discord.ext import commands

log = logging.getLogger(__name__)

class Core():
    """Core functionality for terminal."""

    def __init__(self, bot):
        self.bot = bot


    async def on_ready(self):
        log.info("Core cog loaded.")


    def __unload(self):
        log.info("Core cog unloaded.")


    async def on_message(self, message):
        log.debug("Core.on_message was triggered")


def setup(bot):
    bot.add_cog(Core(bot))