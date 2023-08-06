import requests
import json
import os, sys

URL = os.getenv("QE_API_SERVER")

print(URL)


def login(server, login_id, login_password):
    response = requests.request("POST", f"{URL}/api/login_user/", data={
            'server' : server,
            'username': login_id,
            'password': login_password
        })
    print(json.loads(response.text))
    return json.loads(response.text)