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
            self, id: int,
            name: str,
            platform: Optional[str] = None,
            rankseason: Optional[str] = None
    ) -> None:
        self.id = id  # discord user id
        self.name = name  # apex player name
        self._platform: Optional[str] = platform
        self._rankseason: Optional[str] = rankseason
        self.pool = None

    @classmethod
    async def init(cls, id: int,
                   name: str,
                   platform: Optional[str] = None,
                   rankseason: Optional[str] = None):
        cls.pool = await asyncpg.create_pool(dsn)
        return cls(id, name, platform, rankseason)

    async def create_pool(self):
        self.pool = await asyncpg.create_pool(dsn)
        if self.pool is None:
            logger.warning("SQLへの接続が失敗しました")

    async def select(self) -> asyncpg.Record:
        return await self.pool.fetch(f'SELECT * FROM {table_name} WHERE id=$1 and name=$2', self.id, self.name)

    async def insert(
        self, id: int, name: str,
        platform: str, point: int, rankseason: str, dt
    ) -> str:
        return await self.pool.execute(
            f'INSERT INTO {table_name} VALUES ($1,$2,$3,$4,$5,$6)',
            id, name, platform, point, rankseason, dt
        )

    async def is_exists(self) -> bool:
        res = await self.select()
        if len(res) == 0:
            return False
        else:
            return True

    async def latest_data(self) -> asyncpg.Record:  # 直近のデータ
        return await self.pool.fetchrow(
            f'SELECT * FROM {table_name} WHERE id=$1 and name=$2 and datetime=(SELECT MAX(datetime) FROM test)', self.id, self.name)

    @property
    def platform(self):
        return
