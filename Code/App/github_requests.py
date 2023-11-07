import requests
import base64
import json
from time import sleep

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