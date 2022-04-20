import discord
from discord.ext import commands
from dotenv import load_dotenv

from stats import Stats
from db import SQL
import utils

from os import environ
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
    latest_data = await sql.latest_data()
    if latest_data is None:
        latest_data = {"point": 0}

    embed = discord.Embed()

    if await sql.is_exists():
        stats = await Stats.init(name, platform=sql.platform)
    else:
        stats = await Stats.init(name)
    await sql.insert(ctx.author.id, name, stats.platform, stats.rankpoint,
                     stats.rankedseason, utils.now())

    diff = utils.rp_diff(latest_data["point"], stats.rankpoint)
    await ctx.send(f"現在: __{stats.rankpoint}__")
    await ctx.send(f"前回取得との差: __{diff}__")

    await sql.close()

bot.run(environ["Discord_KEY"])
