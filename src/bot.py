
from logging import getLogger
from os import environ

import discord
import sentry_sdk
from discord.ext import commands
from dotenv import load_dotenv

import utils
from db import SQL
from stats import Stats

logger = getLogger(__name__)


load_dotenv("../.env")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)
sentry_sdk.init(environ["sentry"])


@bot.event
async def on_ready():
    print("on_ready")
    print(f"avatar {bot.user.avatar.url}")


@bot.event
async def on_command_error(context, exception):
    sentry_sdk.capture_exception(exception)


@bot.command(name="rp")
async def rp_command(ctx, name):

    sql = SQL(ctx.author.id, name)
    await sql.create_pool()
    latest_data = await sql.latest_data()

    if latest_data:
        stats = await Stats.init(name, platform=sql.platform)
    else:
        stats = await Stats.init(name)
        sql.point = stats.rankpoint

    await sql.insert(
        ctx.author.id,
        name,
        stats.platform,
        stats.rankpoint,
        stats.rankedseason,
        utils.now(),
    )
    diff = utils.rp_diff(sql.point, stats.rankpoint)

    await ctx.send(f"現在: __{stats.rankpoint}__")
    await ctx.send(f"前回取得との差: __{diff}__")

    await sql.pool.close()


bot.run(environ["Discord_KEY"])
