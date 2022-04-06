import discord
from discord.ext import commands
from dotenv import load_dotenv

from stats import Stats
from db import SQL
import utils

from os import environ
import sys
from logging import getLogger

logger = getLogger(__name__)

load_dotenv("../.env")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    print("on_ready")


@bot.command(name="rp")
async def rp_command(ctx, name):
    sql = SQL(ctx.author.id, name)
    await sql.create_pool()

    if await sql.is_exists():
        stats = await Stats.init(name, platform=sql.platform)
    else:
        stats = await Stats.init(name)
    await sql.insert(ctx.author.id, name, stats.platform, stats.rankpoint,
                     stats.rankedseason, utils.now())

    await ctx.send(stats.rankpoint)


bot.run(environ["Discord_KEY"])
