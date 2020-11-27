import discord 
from discord.ext import commands

import DB

import json
import os
import sys
import requests
from dotenv import load_dotenv
import sqlite3

from pprint import pprint

load_dotenv()

connect = commands.Bot(command_prefix="/",owner_id=390393927607255040)
discord_api=(os.environ["Discord_KEY"])
base_url = "https://public-api.tracker.gg/v2/apex/standard/"
connect.remove_command("help")


connection = sqlite3.connect("rankPoint_DB.db")
c = connection.cursor()

#c.execute("create table rankPoint (discord_id intger , PlayerName text , old_RP integer)")

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


class events:
    @connect.event
    async def on_ready():
        guild=connect.guilds
        print("login")
        await connect.change_presence(activity=discord.Game(name="[/stat]   server: "+str(len(guild))))
        print(guild)

    async def on_guild_join(guild):
        guilds=connect.guilds
        await connect.change_presence(activity=discord.Game(name="[/stat]   server: "+str(len(guilds))))
        print("server join" + guild.name) 

    async def on_guild_remove(guild):
        guilds=connect.guilds
        await connect.change_presence(activity=discord.Game(name="[/stat]   server: "+str(len(guilds))))
        print("server remove" + guild.name)
    async def on_command_error(ctx,error):
        print(ctx,error)
        pass


connect.run(discord_api)
