import os

from dotenv import load_dotenv
import asyncio
import discord
from sqlitedict import SqliteDict as DB
from db.build_db import *
from typing import Literal, Optional
from discord.ext import commands
from discord.ext.commands import Greedy, Context # or a subclass of yours

intents = discord.Intents().all()

bot = commands.Bot(command_prefix='!', intents=intents)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

async def setup_plugins(guild):
    plugins_table = DB('db/db.sqlite', tablename='plugins', autocommit=True)
    plugins = []
    for filename in os.listdir("../plugins"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            plugins.append(filename[:-3])
    for plugin in plugins:
        plugins_table[guild.id].append({plugin: True})
    plugins_table.close()

async def setup_callbacks(guild):
    callbacks_table = DB('db/db.sqlite', tablename='callbacks', autocommit=True)
    callbacks_table[guild.id] = {}
    callbacks_table.close()

async def setup_movies(guild):
    callbacks_table = DB('db/db.sqlite', tablename='movies', autocommit=True)
    callbacks_table[guild.id] = {}
    callbacks_table.close()

@bot.event
async def on_guild_join(guild):
    await setup_plugins(guild)
    await setup_callbacks(guild)
    await setup_movies(guild)

@bot.event
async def on_ready():
    if not os.path.exists('db/db.sqlite'):
        await build_db(bot.guilds)
    await load_extensions()
    print("Ready!")

async def load_extensions():
    for filename in os.listdir("./plugins"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            print("Loading " + filename)
            await bot.load_extension(f"plugins.{filename[:-3]}")
            print("Loaded " + filename)

async def build_db(guilds):
    build_all(guilds)

async def main():
    async with bot:
        
        await bot.start(TOKEN)

@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
  ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

asyncio.run(main())