from datetime import datetime

import discord


def now():
    return datetime.now()


def rp_diff(before: int, after: int) -> int:
    return after - before


async def parse_embed(
    player_id: str,
    discord_name: str,
    icon: str,
    color: discord.Colour,
    rp: int,
    diff: int,
    rankimg: str,
) -> discord.Embed:
    embed = discord.Embed(color=color, title=player_id)

    embed.set_thumbnail(url=rankimg)
    embed.add_field(name="現在", value=f"{rp}", inline=False)
    embed.add_field(name="前回取得との差", value=f"{diff}")
    embed.set_footer(text=discord_name, icon_url=icon)
    return embed
