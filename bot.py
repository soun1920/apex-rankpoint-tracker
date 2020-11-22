import discord 
from discord.ext import commands

import json
import os
import sys
import requests
import sqlite3

from pprint import pprint

discord_api = ""
connect = commands.Bot(command_prefix="/")

base_url = "https://public-api.tracker.gg/v2/apex/standard/"
APEX_KEY = ""


connection = sqlite3.connect("")
c = connection.cursor()

#c.execute("create table rankPoint (discord_id intger , PlayerName text , old_RP integer)")

class start():

    @connect.command()
    async def stat(ctx,user_name):
        connection = sqlite3.connect(r"C:\Users\aw5qm\Desktop\あぺぼっと\rankPoint")
        c = connection.cursor()

        
        params = {"TRN-Api-Key":APEX_KEY}
        endpoint = "profile/"+"origin"+"/"+str(user_name)
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
        




connect.run(discord_api)
