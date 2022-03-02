from dotenv import load_dotenv
import requests

from datetime import datetime, timedelta. timezone
import json
import os

load_dotenv()
platform = ["origin", "psn", "xbl"]

base_url = "https://public-api.tracker.gg/v2/apex/standard/"
JST = timezone(timedelta(hours=+9), 'JST')


class Stats:
    def __init__(self, name: str) -> None:
        self.name = name
        self.point = get_RP(self.name)
        self.platform = None
        self.datetime = None

    def get_RP(name: str) -> int:
        params = {"TRN-Api-Key": os.environ["TRN_KEY"]}
        session = requests.Session()

        for i in platform:
            endpoint = "profile/"+i+"/"+str(name)
            req = session.get(base_url+endpoint, params=params)

            req.close()
            if req.status_code == 404:
                continue
            req_data = json.loads(req.text)

            if req_data.get("data"):
                self.platform = i
                self.datetime = datetime.now()
                return req_data['data']['segments'][0]['stats']['rankScore']['value']


if __name__ == '__main__':
    pass
