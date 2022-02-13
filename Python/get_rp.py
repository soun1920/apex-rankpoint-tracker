import requests
import json

platform = ["origin", "psn", "xbl"]

base_url = "https://public-api.tracker.gg/v2/apex/standard/"


def get_RP(name: str) -> int:
    params = {"TRN-Api-Key": "9f94a856-dc42-486c-9c8d-46a1410f818a"}
    session = requests.Session()

    for i in platform:
        endpoint = "profile/"+i+"/"+str(name)
        req = session.get(base_url+endpoint, params=params)

        req.close()
        req_data = json.loads(req.text)

        if req_data.get("data"):
            return req_data['data']['segments'][0]['stats']['rankScore']['value']
