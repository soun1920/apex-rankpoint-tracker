import asyncpg
from dotenv import load_dotenv

import os
from datetime import datetime
from typing import Optional, Any

load_dotenv()
dsn = os.environ["POSTGRES"]
table_name = os.environ["TABLE_NAME"]


async def make_pool() -> asyncpg.Pool:
    return await asyncpg.Pool(dsn)


class SQL:
    def __init__(
            self, id: int,
            name: str,
            platform: Optional[str] = None,
            rankseson: Optional[str] = None
    ) -> None:
        self.id = id  # discord user id
        self.name = name  # apex player name
        self._platform: Optional[str] = platform
        self._rankseason: Optional[str] = rankseson
        self.pool = make_pool()
        self.data = self.latest_data()

    async def select(self, id, player_name) -> asyncpg.Record:
        return await self.pool.fetch(f'SELECT * FROM {table_name} WHERE id=$1 and playername=$2', id, player_name)

    async def insert(
        self, id: int, name: str,
        platform: str, point: int, rankseason: str, dt
    ) -> str:
        return await self.pool.execute(
            f'INSERT INTO {table_name} (id,playername,platform,point,rankseson) VALUES ($1,$2,$3,$4,$5,$6)',
            id, name, platform, point, rankseason, dt
        )

    async def is_exists(self):
        self.pool.fetch(
            f"SELECT EXISTS (SELECT * FROM {table_name} WHERE id={self.id} and playername={self.name})")

    async def latest_data(self) -> asyncpg.Record:  # 直近のデータ
        return await self.pool.fetch(f"SELECT MAX(datetime) FROM {table_name} WHERE id=$1 and playername=$2", self.id, self.name)

    @property
    def platform(self):
        return
