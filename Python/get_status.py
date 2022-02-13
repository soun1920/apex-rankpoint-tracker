import requests
from dotenv import load_dotenv
import json
import os

load_dotenv()

base_url = "https://public-api.tracker.gg/v2/apex/standard/"

class rankPoint:

    def __init__(self,user_name):
        self.user_name = user_name

    def get_rp(self,user_name):
        
        params = {"TRN-Api-Key":(os.environ["APEX_KEY"])}
        endpoint = "profile/"+"origin"+"/"+str(user_name)
        session = requests.Session()
        req = session.get(base_url+endpoint,params=params)
        req.close()
        req_data = json.loads(req.text)

        try:
            RP =  req_data['data']['segments'][0]['stats']['rankScore']['value']
        except KeyError:
            params = {"TRN-Api-Key":(os.environ["APEX_KEY"])}
            endpoint = "profile/"+"psn"+"/"+str(user_name)
            session = requests.Session()
            req = session.get(base_url+endpoint,params=params)
            req.close()
            req_data = json.loads(req.text)
            try:
                RP =  req_data['data']['segments'][0]['stats']['rankScore']['value']
            except KeyError:
                params = {"TRN-Api-Key":(os.environ["APEX_KEY"])}
                endpoint = "profile/"+"xbox"+"/"+str(user_name)
                session = requests.Session()
                req = session.get(base_url+endpoint,params=params)
                req.close()
                req_data = json.loads(req.text)
                try:
                    RP =  req_data['data']['segments'][0]['stats']['rankScore']['value']
                except KeyError:
                    return  "``` Key Error ```"
        return RP

if __name__ == "__main__":
    pass