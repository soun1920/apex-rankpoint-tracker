import asyncpg
from dotenv import load_dotenv

import os
import logging
from typing import Optional, Any

load_dotenv("../.env")
dsn = os.environ["POSTGRES"]
table_name = os.environ["TABLE_NAME"]

logger = logging.getLogger(__name__)


class SQL:
    def __init__(
        self,
        id: int,
        name: str,
        platform: Optional[str] = None,
        rankseason: Optional[str] = None,
    ) -> None:
        self.id = id  # discord user id
        self.name = name  # apex player name
        self._platform: Optional[str] = platform
        self._rankseason: Optional[str] = rankseason
        self._rankpoint = None
        self.pool = None

    @classmethod
    async def init(
        cls,
        id: int,
        name: str,
        platform: Optional[str] = None,
        rankseason: Optional[str] = None,
    ):
        cls.pool = await asyncpg.create_pool(dsn)
        return cls(id, name, platform, rankseason)

    async def create_pool(self):
        self.pool = await asyncpg.create_pool(dsn)
        if self.pool is None:
            logger.warning("SQLへの接続が失敗しました")

    async def select(self) -> asyncpg.Record:
        async with self.pool.acquire() as conn:
            return await conn.fetch(
                f"SELECT * FROM {table_name} WHERE id=$1 and name=$2", self.id, self.name
            )

    async def insert(
        self, id: int, name: str, platform: str, point: int, rankseason: str, dt
    ) -> str:
        async with self.pool.acquire() as conn:
            return await conn.execute(
                f"INSERT INTO {table_name} VALUES ($1,$2,$3,$4,$5,$6)",
                id,
                name,
                platform,
                point,
                rankseason,
                dt,
            )

    async def is_exists(self) -> bool:
        res = await self.select()
        if len(res) == 0:
            return False
        else:
            return True

    async def latest_data(self) -> asyncpg.Record:  # 直近のデータ
        async with self.pool.acquire() as conn:
            record = await conn.fetchrow(
                f"SELECT * FROM {table_name} WHERE id=$1 and name=$2 and datetime=(SELECT MAX(datetime) FROM test)",
                self.id,
                self.name,
            )
        self._platform = record["platform"]
        self._rankpoint = record["point"]
        return record

    @property
    def platform(self):
        return self._platform

    @property
    def point(self):
        return self._rankpoint
