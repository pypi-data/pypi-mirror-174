import requests
import json
import os

URL = os.getenv("QE_API_SERVER")


def login(server, login_id, login_password):
    response = requests.request("POST", f"http://{URL}/api/login_user/", data={
            'server' : server,
            'username': login_id,
            'password': login_password
        })
    return json.loads(response.text)