import discord 
from discord.ext import commands

import json
import os
import sys
import requests
from dotenv import load_dotenv
import sqlite3

from pprint import pprint

load_dotenv()

connect = commands.Bot(command_prefix="/")
discord_api=(os.environ["Discord_KEY"])
base_url = "https://public-api.tracker.gg/v2/apex/standard/"

os.chdir(os.path.dirname(__file__))

connection = sqlite3.connect("rankPoint_DB")
c = connection.cursor()

#c.execute("create table rankPoint (discord_id intger , PlayerName text , old_RP integer)")

class command():

    @connect.command()
    async def stat(ctx,user_name,platform):
        connection = sqlite3.connect(__file__,"rankPoint_DB")
        c = connection.cursor()
        
        if platfrom =="ps4":
            platform_out="psn"
        platform_out = "pc"
        params = {"TRN-Api-Key":(os.environ["APEX_KEY"])}
        endpoint = "profile/"+platform_out+"/"+str(user_name)
        session = requests.Session()
        req = session.get(base_url+endpoint,params=params)
        req.close()
        req_data = json.loads(req.text)

        
        RP =  req_data['data']['segments'][0]['stats']['rankScore']['value']
        user_data = (ctx.author.id , user_name , RP )
        user_id = ctx.author.id
        
        c.execute(f"SELECT * FROM rankPoint WHERE discord_id={user_id} AND PlayerName='{user_name}'",)

        data_base = c.fetchone()
        
        db_all = c.fetchall()
        if len(db_all) == 0:
            old_point = RP
            c.execute('INSERT INTO rankPoint (discord_id, PlayerName, old_RP) values (?,?,?)', user_data)
        else:
            old_point = data_base[2]
            c.execute(f"update rankPoint set old_RP={RP},where discord_id={user_id} AND PlayerName='{user_name}'")

        #c.execute("select * from rankPoint")

        change = RP - old_point
        if change<0:
            sign = "-"
        elif change == 0:
            sign = ""
        else:
            sign = "+"
        
        await ctx.send(f"{user_name}  の現在のRPは {RP}({sign}{change}) です " )
        
        connection.commit()
        c.close()
        connection.close()


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







connect.run(discord_api)
