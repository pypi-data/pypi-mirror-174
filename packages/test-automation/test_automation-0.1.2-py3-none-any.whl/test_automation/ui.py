import requests
import json
import os

URL = os.getenv("QE_API_SERVER")

def login_ui(server, login_id, login_password):
    response = requests.request("POST", f"http://{URL}/api/login_user/", data={
            'server' : server,
            'username': login_id,
            'password': login_password
        })
    print(json.loads(response.text))
    return json.loads(response.text)