from discord import Bot, ApplicationContext
from discord.commands import Option
from dotenv import load_dotenv

from stats import Stats

from os import environ

load_dotenv()
bot = Bot()


@bot.slash_command(name="rankpoint")
async def rp_command(ctx: ApplicationContext, name: Option(str, "OriginID・PSNIDを入力してください")):
    stats = Stats(name)
    await ctx.respond(stats.point)

bot.run(environ["Discord_KEY"])
