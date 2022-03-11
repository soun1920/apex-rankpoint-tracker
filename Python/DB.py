from dataclasses import dataclass
from platform import platform
from typing import Coroutine
import asyncpg
from dotenv import load_dotenv

import os
from typing import Optional
from dataclasses import dataclass

load_dotenv()
dsn = os.environ["POSTGRES"]
table_name = os.environ["TABLE_NAME"]


async def make_pool() -> asyncpg.Pool:
    return await asyncpg.Pool(dsn)


class SQL:
    def __init__(
            self, id: int,
            name: str,
            platform: str = None,
            latest_only: bool = False,
            rankseson: int = Optional[int]
    ) -> None:
        self.id = id  # discord user id
        self.name = name  # player name
        self.platform = platform
        self.datetime = None
        self.rankpoint = None
        self.season = None
        self.split = None
        self.pool = asyncpg.Pool(dsn)

    async def get_data(self, id, player_name) -> Coroutine:
        return await self.pool.fetch(f'SELECT * FROM {table_name} WHERE id=$1 playername=$2', id, player_name)

    async def insert_data(self) -> Coroutine:
        return await self.pool.execute(f'INSERT INTO ')

    @property
    async def latest_data(self) -> Coroutine:  # 直近のデータ
        return await self.pool.fetch(f"SELECT MAX(datetime) FROM {table_name} WHERE id=$1 playername=$2', id, player_name")


@dataclass
class Status:
    id: int
    name: str
    platform: str
    rankpoint: int
    season: int
    split: int
