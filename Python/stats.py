from dotenv import load_dotenv
import aiohttp
import asyncio
from typing import Optional

from datetime import datetime, timedelta, timezone
import json
import os

load_dotenv()
global_platform = ["PC", "PS4", "X1"]
apex_key = os.environ["APEX_KEY"]

base_url = "https://api.mozambiquehe.re/bridge?version=5"
JST = timezone(timedelta(hours=+9), "JST")


class Stats:
    def __init__(self, name: str, platform: Optional[str] = None) -> None:
        self.loop = asyncio.get_event_loop()
        self.name = name
        self.__platform = platform
        self.stats = self.loop.run_until_complete(
            self.get_stats(self.name, platform=self.__platform))

    async def get_stats(self, name: str, *, platform: Optional[str] = None):
        async with aiohttp.ClientSession() as session:
            if platform:
                res = await session.get(self.parse_endpoint(name, platform))
                if res.status == 200:
                    return await res.json(content_type="text/plain")
                else:
                    raise ValueError
            else:
                for i in global_platform:
                    res = await session.get(self.parse_endpoint(name, i))
                    if res.status == 200:
                        return await res.json(content_type="text/plain")
                    else:
                        raise ValueError

    @property
    def rankpoint(self):
        return self.stats["global"]["rank"]["rankScore"]

    @property
    def rankedseason(self):
        return self.stats["global"]["rank"]["rankedSeason"]

    @property
    def platform(self):
        return self.stats['global']['platform']

    def parse_endpoint(self, name, platform) -> str:
        return f"{base_url}&platform={platform}&player={name}&auth={apex_key}"


if __name__ == "__main__":
    s = Stats("soun1920")
    print(s.rankpoint)
