
from logging import getLogger
from os import environ

import discord
import sentry_sdk
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

import utils
from db import SQL
from stats import Stats

logger = getLogger(__name__)


load_dotenv("../.env")
intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix="/")
sentry_sdk.init(environ["sentry"])


@bot.event
async def on_ready():
    print("on_ready")
    print(f"avatar {bot.user.avatar.url}")
    await bot.tree.sync(guild=discord.Object(830279797920759818))


@bot.event
async def on_command_error(context, exception):
    sentry_sdk.capture_exception(exception)


@bot.tree.command(name="rankpointttttt")
async def rankpoint(interaction: discord.Interaction, name: str):
    sql = SQL(interaction.user.id, name)
    await sql.create_pool()
    latest_data = await sql.latest_data()

    if latest_data:
        stats = await Stats.init(name, platform=sql.platform)
    else:
        stats = await Stats.init(name)
        sql.point = stats.rankpoint

    await sql.insert(
        interaction.user.id,
        name,
        stats.platform,
        stats.rankpoint,
        stats.rankedseason,
        utils.now(),
    )
    diff = utils.rp_diff(sql.point, stats.rankpoint)

    await interaction.response.send_message(f"現在: __{stats.rankpoint}__")
    await interaction.response.send_message(f"前回取得との差: __{diff}__")

    await sql.pool.close()

bot.tree.add_command(rankpoint, guild=discord.Object(830279797920759818))
bot.run(environ["Discord_KEY"])
