import sqlite3
import pandas as pd
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
connect = commands.Bot(command_prefix="/",owner_id=390393927607255040)
discord_api=(os.environ["Discord_KEY"])
connection=sqlite3.connect("rankPoint_DB.db")


def db_Search(value):
    return pd.read_sql_query(f"select * from rankPoint where discord_id={value}",connection)

def db_All():
    return pd.read_sql_query(f"select * from rankPoint",connection)
def graph():
    return

if __name__ == "__main__":
    pass