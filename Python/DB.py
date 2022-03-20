from dataclasses import dataclass
from platform import platform
from typing import Coroutine
import asyncpg
from dotenv import load_dotenv

import os
import datatime
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
            rankseson: Optional[str] = None
    ) -> None:
        self.id = id  # discord user id
        self.name = name  # apex player name
        self.platform = platform
        self.datetime = None
        self.rankpoint = rankpoint
        self.rankseason = rankseson
        self.pool = make_pool()

    async def get_data(self, id, player_name) -> list:
        return await self.pool.fetch(f'SELECT * FROM {table_name} WHERE id=$1 and playername=$2', id, player_name)

    async def insert_data(
        self, id: int, name: str,
        platform: str, point: int, rankseason: str, dt: datatime
    ) -> str:
        return await self.pool.execute(
            f'INSERT INTO {table_name} (id,playername,platform,point,rankseson) VALUES ($1,$2,$3,$4,$5,$6)',
            id, name, platform, point, rankseason, dt
        )

    async def is_exists(self):
        self.pool.fetch(
            f"SELECT EXISTS (SELECT * FROM {table_name} WHERE id={self.id} and playername={self.name})")

    @property
    async def latest_data(self) -> list:  # 直近のデータ
        return await self.pool.fetch(f"SELECT MAX(datetime) FROM {table_name} WHERE id=$1 and playername=$2", self.id, self.name)
