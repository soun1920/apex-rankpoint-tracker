import sqlite3
import pandas as pd
import os
connection=sqlite3.connect("rankPoint_DB.db")
def db_Search(value):
    return pd.read_sql_query(f"select * from rankPoint where discord_id={value}",connection)

def db_All():
    return pd.read_sql_query(f"select * from rankPoint",connection)
def graph():
if __name__ == "__main__":
    pass