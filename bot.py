import discord 
from discord.ext import commands

import DB

import json
import os
import sys
import requests
from dotenv import load_dotenv
import sqlite3
import re
import asyncio

load_dotenv()

connect = commands.Bot(command_prefix="/",owner_id=390393927607255040)
discord_api=(os.environ["Discord_KEY"])
base_url = "https://public-api.tracker.gg/v2/apex/standard/"
connect.remove_command("help")


connection = sqlite3.connect("rankPoint_DB.db")
c = connection.cursor()

#c.execute("create table invite (discord_message_id intger , invite_link string)")

class commands:
    @connect.group(invoke_without_command=True)
    async def stat(ctx,user_name):
        connection = sqlite3.connect("rankPoint_DB.db")
        c = connection.cursor()
        
        params = {"TRN-Api-Key":(os.environ["APEX_KEY"])}
        endpoint = "profile/"+"origin"+"/"+str(user_name)
        session = requests.Session()
        req = session.get(base_url+endpoint,params=params)
        req.close()
        req_data = json.loads(req.text)

        try:
            RP =  req_data['data']['segments'][0]['stats']['rankScore']['value']
        except KeyError:
            params = {"TRN-Api-Key":(os.environ["APEX_KEY"])}
            endpoint = "profile/"+"psn"+"/"+str(user_name)
            session = requests.Session()
            req = session.get(base_url+endpoint,params=params)
            req.close()
            req_data = json.loads(req.text)
            try:
                RP =  req_data['data']['segments'][0]['stats']['rankScore']['value']
            except KeyError:
                params = {"TRN-Api-Key":(os.environ["APEX_KEY"])}
                endpoint = "profile/"+"xbox"+"/"+str(user_name)
                session = requests.Session()
                req = session.get(base_url+endpoint,params=params)
                req.close()
                req_data = json.loads(req.text)
                try:
                    RP =  req_data['data']['segments'][0]['stats']['rankScore']['value']
                except KeyError:
                    await ctx.send("アカウント名が間違っているか、存在しません")
                    return

        user_data = (ctx.author.id , user_name , RP )



        user_id = ctx.author.id
        
        c.execute(f"SELECT * FROM rankPoint WHERE discord_id={user_id} AND PlayerName='{user_name}'",)
        db_all = c.fetchall()

        if len(db_all) == 0:
            old_point = RP
            c.execute('INSERT INTO rankPoint (discord_id, PlayerName, old_RP) values (?,?,?)', user_data)

        else:
            c.execute(f"SELECT * FROM rankPoint WHERE discord_id={user_id} AND PlayerName='{user_name}'",)
            data_base = c.fetchone()
            old_point = data_base[2]
            c.execute(f"update rankPoint set old_RP={RP} where discord_id={user_id} AND PlayerName='{user_name}'")


        change = RP - old_point
        if change<0:
            sign = ""
        elif change == 0:
            sign = ""
        elif change >0:
            sign = "+"
        e=discord.Embed()
        e.add_field(name="RP",value=str(RP))
        e.add_field(name="前回比",value="("+sign+str(change)+")")
        e.set_author(name=str(user_name),icon_url=ctx.author.avatar_url)
        e.set_footer(text="support : @soun_stw_py")
        await ctx.send(embed=e)
        connection.commit()
        c.close()
        connection.close()

    @connect.command(passcontext=True)
    @commands.is_owner()
    async def search(ctx,id):
        result=DB.db_Search(id)
        await ctx.send(result)

    @connect.command(passcontext=True)
    @commands.is_owner()
    async def all(ctx):
        result=DB.db_All()
        await ctx.send(result)

    @connect.command(passcontext=True)
    @commands.is_owner()
    async def all_delete(ctx):
        c.execute("delete from RankPoint",)
        connection.commit()
    
    @connect.group(invoke_without_command=True)
    async def recr(ctx,member_count,game,channel_name):
        connection = sqlite3.connect("rankPoint_DB.db")
        c = connection.cursor()
        
        channel = discord.utils.get(ctx.message.guild.voice_channels,name=channel_name)
        invite=await channel.create_invite()
        await ctx.message.delete()
        me=await ctx.send(f"{ctx.author.mention} が` {game} `を` {member_count} ` 人募集しています @everyone")
        await me.add_reaction("☑️")
        await me.add_reaction("❌")
        invite=await channel.create_invite()

        message_id=me.id
        d=(message_id,str(invite))
        c.execute(f'INSERT INTO invite(discord_message_id,invite_link) values(?,?)',d)

        connection.commit()
        c.close()
        connection.close()


        
        #Channel用のサブコマンドを作ってutilで検索する。
        #await create        



class events:
    @connect.event
    async def on_ready():
        guild=connect.guilds
        print("login")
        await connect.change_presence(activity=discord.Game(name="[/stat]   server: "+str(len(guild))))
        print(guild)
    @connect.event
    async def on_guild_join(guild):
        guilds=connect.guilds
        await connect.change_presence(activity=discord.Game(name="[/stat]   server: "+str(len(guilds))))
        print("server join" + guild.name) 
    @connect.event
    async def on_guild_remove(guild):
        guilds=connect.guilds
        await connect.change_presence(activity=discord.Game(name="[/stat]   server: "+str(len(guilds))))
        print("server remove" + guild.name)
    #@connect.event
    async def on_command_error(ctx,error):
        print(ctx,error)
        pass
    @connect.event
    async def on_reaction_add(reaction,user):

        if user.bot:
            return

        connection = sqlite3.connect("rankPoint_DB.db")
        c = connection.cursor()
        if reaction.emoji == ("☑️"):
            count_check=re.search(r" (\d) ",reaction.message.content).group()
            user_id=re.search(r"<(.*)>",reaction.message.content).group()
            game=re.search(r"が(.*)を",reaction.message.content).group()

            if user.mention != user_id:
                if int(count_check)==1:
                    await reaction.message.clear_reactions()
                    await reaction.message.edit(content=f"終了しました")
                    c.execute(f"delete from invite where discord_message_id={reaction.message.id}")
                    return
                
                await reaction.message.edit(content=f"{user_id}{game}` {int(count_check)-1} `人募集しています @everyone")
                c.execute(f"select * from invite where discord_message_id={reaction.message.id} ",)
                d=c.fetchone()

                invite_link = d[1]
                dm=await user.create_dm()

                try:
                    await dm.send(invite_link)
                except discord.errors.Forbidden:
                    me=await reaction.message.channel.send(user.mention+"  "+invite_link)
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
            count_check=re.search(r" (\d) ",reaction.message.content).group()
            user_id=re.search(r"<(.*)>",reaction.message.content).group()
            game=re.search(r"が(.*)を",reaction.message.content).group()
            if user.mention == user_id :
                #DBにreaction.message.idとauthorを登録
                me = await reaction.message.channel.send(f"本当に終了しますか？ yes=✅ ||{reaction.message.id}||")
                await me.add_reaction("✅")
                await me.add_reaction("❎")
                await reaction.remove(user)
            else :
                await reaction.remove(user)
                me = await reaction.message.channel.send(user.mention+'募集を始めた人以外が押すことはできません')
                await asyncio.sleep(3)
                await me.delete()
        
        if reaction.emoji == ("✅"):
            await reaction.message.delete()
            reaction_me=re.search(r"\d+",reaction.message.content).group()
            reaction_message=await reaction.message.channel.fetch_message(int(reaction_me))
            await reaction_message.delete()
            c.execute(f"select * from invite where discord_message_id={reaction.message.id} ",)
        
        if reaction.emoji == ("❎"):
            await reaction.message.delete()
            reaction_me=re.search(r"\d+",reaction.message.content).group()
            reaction_message=await reaction.message.channel.fetch_message(int(reaction_me))

        connection.commit()
        connection.close()
            
    @connect.event
    async def on_raw_reaction_remove(payload):
        channel=connect.get_channel(payload.channel_id)
        user = connect.get_user(payload.user_id)
        reaction_message=await channel.fetch_message(payload.message_id)

        count_check=re.search(r" (\d) ",reaction_message.content).group() 
        game=re.search(r"が(.*)を",reaction_message.content).group()
        
        if payload.user_id == 778463314543378464:
            return

        if payload.emoji.name == ("☑️"):
            user_id=re.search(r"<(.*?)>",reaction_message.content).group()
            if user_id != f"<@{payload.user_id}>":
                await reaction_message.edit(content=f"{user_id}{game}` {int(count_check)+1} `人募集しています @everyone")
            
        


connect.run(discord_api)
