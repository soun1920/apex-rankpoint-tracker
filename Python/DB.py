import asyncpg
from dotenv import load_dotenv

import os

load_dotenv()
dsn = os.environ["POSTGRES"]


async def make_pool():
    return await asyncpg.Pool(dsn)


class Psql:
    def __init__(self, id, name):
        self.id = id  # discord user id
        self.name = name  # player name
        self.platform = None
        self.datetime = None
        self.rankpoint = None
        self.season = None
        self.split = None
        self.pool = asyncpg.Pool(dsn)

    async def get_data():
        return self.pool.fetch('SELECT * FROM')
