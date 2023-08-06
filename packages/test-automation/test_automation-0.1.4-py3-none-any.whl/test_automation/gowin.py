import requests
import json
import os

URL = os.getenv("QE_API_SERVER")

def login(username, password):
    return json.loads(requests.request("POST", f"http://{URL}/api/gowin/login/", json={'username':username, 'password':password}).text)

def get_order_list(ordernumber, token) :
    return json.loads(requests.request("GET", f'http://{URL}/api/gowin/order_list/?ordernumber={ordernumber}&token={token}').text)

def received_by_vendor(roid, token) :
    return requests.request("PUT", f"http://{URL}/api/gowin/received_by_vendor/", json={'roid':roid, 'token':token}).text

def deliveries_state(roid, token, state) :
    return requests.request("PUT", f"http://{URL}/api/gowin/state/", json={'roid':roid, 'token':token, 'state':state}).text
