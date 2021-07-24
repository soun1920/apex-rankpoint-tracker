import discord
from discord.ext import commands

import DB
import get_time
import get_status

import json
import os
import sys
import requests
from dotenv import load_dotenv
import sqlite3
import re
import asyncio
import datetime
from operator import itemgetter


load_dotenv()

connect = commands.Bot(command_prefix="/", owner_id=390393927607255040)
discord_api = (os.environ["Discord_KEY"])
base_url = "https://public-api.tracker.gg/v2/apex/standard/"
connect.remove_command("help")


connection = sqlite3.connect("rankPoint_DB.db")
c = connection.cursor()

#c.execute("create table rankPoint (discord_id integer , PlayerName text , old_RP integer , time text )")


class commands:
    @connect.group(invoke_without_command=True)
    async def stat(ctx, user_name):

        if re.match(r"[ぁ-んァ-ヶ亜-熙]+", user_name):
            await ctx.send("```Steamの名前ではなくOriginIDを入力してください```")

        connection = sqlite3.connect("rankPoint_DB.db")
        c = connection.cursor()
        r = get_status.rankPoint(user_name)
        RP = r.get_rp(user_name)

        now_time = get_time.get_jst()
        now = datetime.datetime.now(now_time)
        user_data = (ctx.author.id, user_name, RP,
                     now.strftime('%Y-%m-%d-%H-%M-%S'))

        user_id = ctx.author.id

        c.execute(
            f"SELECT * FROM rankPoint WHERE discord_id={user_id} AND PlayerName='{user_name}'",)
        db = c.fetchall()
        db_all = sorted(db, reverse=True, key=itemgetter(3))

        try:
            print(db_all)
            old_point = db_all[0][2]
        except:
            pass

        if len(db_all) == 0:
            old_point = RP
            c.execute(
                'INSERT INTO rankPoint (discord_id, PlayerName, old_RP, time ) values (?,?,?,?)', user_data)

        if len(db_all) == 7:
            c.execute(
                f"delete from rankpoint where discord_id={user_id} AND PlayerName='{user_name}' and time='{db_all[6][3]}'"
            )

            c.execute(
                'INSERT INTO rankPoint (discord_id, PlayerName, old_RP, time ) values (?,?,?,?)', user_data
            )

        if len(db_all) < 7 and len(db_all) >= 1:

            c.execute(
                'INSERT INTO rankPoint (discord_id, PlayerName, old_RP, time ) values (?,?,?,?)', user_data
            )

        change = RP - old_point
        if change < 0:
            sign = ""
        elif change == 0:
            sign = ""
        elif change > 0:
            sign = "+"
        e = discord.Embed()
        e.add_field(name="RP", value=str(RP))
        e.add_field(name="前回比", value="("+sign+str(change)+")")
        e.set_author(name=str(user_name), icon_url=ctx.author.avatar_url)
        e.set_footer(text="support : @soun_stw_py")
        await ctx.send(embed=e)
        connection.commit()

        c.close()
        connection.close()

    @connect.command(passcontext=True)
    @commands.is_owner()
    async def search(ctx, id):
        result = DB.db_Search(id)
        await ctx.send(result)

    @connect.command(passcontext=True)
    @commands.is_owner()
    async def all(ctx):
        result = DB.db_All()
        await ctx.send(result)

    @connect.command(passcontext=True)
    @commands.is_owner()
    async def all_delete(ctx):
        c.execute("delete from RankPoint",)
        connection.commit()

    @connect.group(invoke_without_command=True)
    async def recr(ctx, member_count, game, channel_name):
        connection = sqlite3.connect("rankPoint_DB.db")
        c = connection.cursor()

        channel = discord.utils.get(
            ctx.message.guild.voice_channels, name=channel_name)
        invite = await channel.create_invite()
        await ctx.message.delete()
        me = await ctx.send(f"{ctx.author.mention} が` {game} `を` {member_count} ` 人募集しています @everyone")
        await me.add_reaction("☑️")
        await me.add_reaction("❌")
        invite = await channel.create_invite()

        message_id = me.id
        d = (message_id, str(invite))
        c.execute(
            f'INSERT INTO invite(discord_message_id,invite_link) values(?,?)', d)

        connection.commit()
        c.close()
        connection.close()

        # Channel用のサブコマンドを作ってutilで検索する。
        # await create

    @connect.command(passcontext=True)
    @connect.is_owner()
    async def exit(ctx):
        sys.exit(0)


class events:
    @connect.event
    async def on_ready():
        guild = connect.guilds
        print("login")
        await connect.change_presence(activity=discord.Game(name="[/stat]   server: "+str(len(guild))))
        print(guild)

    @connect.event
    async def on_guild_join(guild):
        guilds = connect.guilds
        await connect.change_presence(activity=discord.Game(name="[/stat]   server: "+str(len(guilds))))
        print("server join" + guild.name)

    @connect.event
    async def on_guild_remove(guild):
        guilds = connect.guilds
        await connect.change_presence(activity=discord.Game(name="[/stat]   server: "+str(len(guilds))))
        print("server remove" + guild.name)
    # @connect.event

    async def on_command_error(ctx, error):
        channel = connect.get_channel(778517624949571605)
        print(ctx, error)
        await channel.send(ctx+error)
        pass

    @connect.event
    async def on_reaction_add(reaction, user):

        if user.bot:
            return

        connection = sqlite3.connect("rankPoint_DB.db")
        c = connection.cursor()
        if reaction.emoji == ("☑️"):
            count_check = re.search(
                r" (\d) ", reaction.message.content).group()
            user_id = re.search(r"<(.*)>", reaction.message.content).group()
            game = re.search(r"が(.*)を", reaction.message.content).group()

            if user.mention != user_id:
                if int(count_check) == 1:
                    await reaction.message.clear_reactions()
                    await reaction.message.edit(content=f"終了しました")
                    c.execute(
                        f"delete from invite where discord_message_id={reaction.message.id}")
                    return

                await reaction.message.edit(content=f"{user_id}{game}` {int(count_check)-1} `人募集しています @everyone")
                c.execute(
                    f"select * from invite where discord_message_id={reaction.message.id} ",)
                d = c.fetchone()

                invite_link = d[1]
                dm = await user.create_dm()

                try:
                    await dm.send(invite_link)
                except discord.errors.Forbidden:
                    me = await reaction.message.channel.send(user.mention+"  "+invite_link)
                    voice_status = user.voice
                    while voice_status == None:
                        voice_status = user.voice
                        await asyncio.sleep(1)
                    else:
                        await me.delete()
                        return

            else:
                await reaction.remove(user)
                me = await reaction.message.channel.send(user.mention+'募集を始めた人が押すことはできません')
                await asyncio.sleep(3)
                await me.delete()

        if reaction.emoji == ("❌"):
            count_check = re.search(
                r" (\d) ", reaction.message.content).group()
            user_id = re.search(r"<(.*)>", reaction.message.content).group()
            game = re.search(r"が(.*)を", reaction.message.content).group()
            if user.mention == user_id:
                # DBにreaction.message.idとauthorを登録
                me = await reaction.message.channel.send(f"本当に終了しますか？ yes=✅ ||{reaction.message.id}||")
                await me.add_reaction("✅")
                await me.add_reaction("❎")
                await reaction.remove(user)
            else:
                await reaction.remove(user)
                me = await reaction.message.channel.send(user.mention+'募集を始めた人以外が押すことはできません')
                await asyncio.sleep(3)
                await me.delete()

        if reaction.emoji == ("✅"):
            await reaction.message.delete()
            reaction_me = re.search(r"\d+", reaction.message.content).group()
            reaction_message = await reaction.message.channel.fetch_message(int(reaction_me))
            await reaction_message.delete()
            c.execute(
                f"select * from invite where discord_message_id={reaction.message.id} ",)

        if reaction.emoji == ("❎"):
            await reaction.message.delete()
            reaction_me = re.search(r"\d+", reaction.message.content).group()
            reaction_message = await reaction.message.channel.fetch_message(int(reaction_me))

        connection.commit()
        connection.close()

    @connect.event
    async def on_raw_reaction_remove(payload):
        channel = connect.get_channel(payload.channel_id)
        user = connect.get_user(payload.user_id)
        reaction_message = await channel.fetch_message(payload.message_id)

        count_check = re.search(r" (\d) ", reaction_message.content).group()
        game = re.search(r"が(.*)を", reaction_message.content).group()

        if payload.user_id == 778463314543378464:
            return

        if payload.emoji.name == ("☑️"):
            user_id = re.search(r"<(.*?)>", reaction_message.content).group()
            if user_id != f"<@{payload.user_id}>":
                await reaction_message.edit(content=f"{user_id}{game}` {int(count_check)+1} `人募集しています @everyone")


connect.run(discord_api)
