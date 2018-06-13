#!python
import logging
import os
import fnmatch
from discord.ext import commands

log = logging.getLogger(__name__)

description = '''Discord Open-Source CLI Advanced Terminal.'''

startup_extensions = ["core"] # Add names like "module" which located at "cogs/module.py"

bot = commands.Bot(command_prefix = "/", description = description, self_bot = True)


@bot.event
async def on_ready():
    log.info("Logged in as")
    log.info(f"{bot.user.name} ({bot.user.id})")
    log.info("────────────")


@is_owner()
@bot.command()
async def load(ctx, extension_name: str):
    """Loads an extension."""

    try:
        bot.load_extension(f"cogs.{extension_name.lower()}")
    except (AttributeError, ImportError) as e:
        log.exception(f"{type(e).__name__}: {e}")
        await ctx.send(content = f"```py\n{type(e).__name__}: {e}\n```")
        return
    log.info(f"{extension_name.lower()} loaded.")
    await ctx.send(content = f"{extension_name.lower()} loaded.")


@is_owner()
@bot.command()
async def unload(ctx, extension_name: str):
    """Unloads an extension."""

    bot.unload_extension(extension_name.lower())
    log.info(f"{extension_name.lower()} unloaded.")
    await ctx.send(content = f"{extension_name.lower()} unloaded.")


@is_owner()
@bot.command()
async def reload(ctx, extension_name: str):
    """Reloads an extension."""

    bot.unload_extension(extension_name)
    try:
        bot.load_extension(f"cogs.{extension_name.lower()}")
    except (AttributeError, ImportError) as e:
        log.exception(f"{type(e).__name__}: {e}")
        await ctx.send(content = f"```py\n{type(e).__name__}: {e}\n```")
        return
    log.info(f"{extension_name.lower()} reloaded.")
    await ctx.send(content = f"{extension_name.lower()} reloaded.")


@is_owner()
@bot.command(aliases = ["coglist", "cogslist"])
async def listcogs(ctx):
    """Show all available cogs."""

    filelist = os.listdir('.\\cogs')
    cogslist = []
    pattern = "*.py"
    for entry in filelist:
        if fnmatch.fnmatch(entry, pattern):
            if bot.get_cog(entry.replace('.py', '')) is not None:
                cogslist.append(f"{entry.replace('.py', ''):<20} –  is loaded")
            else:
                cogslist.append(f"{entry.replace('.py', ''):<20} - not loaded")
    await ctx.message.channel.send(content = "**List of available cogs:**\n```xl\n" + "\n".join(cogslist) + "\n```")


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(f"cogs.{extension}")
        except Exception as e:
            log.exception(f"Failed to load extension {extension} from cogs folder.\n{type(e).__name__}: {e}")

try:
    token = ""
    with open("token.txt") as data_file:
        token = data_file.readlines()[0].strip()
    bot.run(token, bot = False)
    log.info("Bot was terminated.")
except FileNotFoundError:
    log.critical("Put your token in \"token.txt\" first.")
    exit(1)