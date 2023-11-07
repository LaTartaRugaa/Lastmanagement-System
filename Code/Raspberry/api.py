import requests
import base64
import json
import wattpilot
from time import sleep


class Fronius:
    def __init__(self, ip="192.168.188.28"):
        self.request_url = (f'http://{ip}/solar_api/v1/GetPowerFlowRealtimeData.fcgi/')

    def get_data(self, request_type):
        data = requests.get(self.request_url).json()
        data = self.request["Body"]["Data"]["Site"][request_type]
        print(data)
        return data 


class Github:
    def __init__(self, username, repository_name, file_path, token):
        self.username = username
        self.repository_name = repository_name
        self.file_path = file_path
        self.token_header = {"Authorization" : f"token {token}"}
        
        self.url = f"https://api.github.com/repos/{self.username}/{self.repository_name}/contents/{self.file_path}"

    def get_data(self, content_type):
        c = 0
        while c <= 5:
            get_request = requests.get(self.url, headers=self.token_header)
            if get_request.status_code == 200:
                print("get_request was successful - try ", c)
                break
            else:
                print("get request failed - try ", c)
            c += 1
            sleep(0.3)

        final_content = get_request.json()[content_type]


        if content_type == "content":
            decoded_content = base64.b64decode(final_content)
            final_content = json.loads(decoded_content.decode("utf-8"))
        
        return final_content
        
    def put_data(self, new_content, main_key, sub_key = None, name = "Michael Enderli", email = "michael@enderli.net"):
        db_check = self.get_data("content")
        if sub_key == None:
            db_check[main_key] = new_content
        else:
            if main_key in db_check:
                db_check[main_key][sub_key] = new_content
            else:
                db_check[main_key] = {}
                db_check[main_key][sub_key] = new_content
            
        new_content = json.dumps(db_check, indent = 0).replace("'", '"')
        encoded_content = base64.b64encode(new_content.encode("utf-8")).decode("utf-8")
        sha = self.get_data("sha")

        data = {"message" : "content update",
                "committer" : {
                    "name" : name,
                    "email" : email
                },
                "content" : encoded_content,
                "sha": sha
                }

        c = 0
        while c <= 5:
            put_request = requests.put(self.url, json=data, headers=self.token_header)
            if put_request.status_code == 200:
                print("put request was successful - try ", c)
                break
            else:
                print("put request failed - try ", c)
            c += 1
            sleep(0.3)






class Wattpilot:
    def __init__(self, ip, password):
        self.ip = ip
        self.password = password

        self.wp = wattpilot.Wattpilot(ip, password)
        self.wp.connect()
        
        c = 0

        while not self.wp.connected and c < 25:
            sleep(1)
            c += 1
        print("Wattpilot connected", "\n")

    def get_data(self, requested_data):
        # carConnected, mode, power (kW), energyCounterSinceStart (Wh), energyCounterTotal (Wh)

        wattpilot_call = {"carConnected" : self.wp.carConnected,
                         "mode" : self.wp.mode,
                         "power" : self.wp.power,
                         "energyCounterSinceStart" : self.wp.energyCounterSinceStart,
                         "energyCounterTotal" : self.wp.energyCounterTotal}
        
        return wattpilot_call[requested_data]

class Meteo:
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

        api_url = "https://api.srgssr.ch/oauth/v1/accesstoken?grant_type=client_credentials"
        authorization = base64.b64encode(f"{self.key}:{self.secret}".encode("utf-8")).decode("utf-8")
        self.headers = {"Authorization": authorization,
                  "Cache-Control" : "no-cache"}
        
        response = requests.post(api_url, headers=self.headers)
        token = response.json()["access_token"]
        self.headers["Authorization"] = f"Bearer {token}"

    def get_data(self, requested_data, geolocation_id):
        get_url = f"https://api.srgssr.ch/srf-meteo/v2/{requested_data}/{geolocation_id}"
        response = requests.get(get_url, headers=self.headers).json()
        return response