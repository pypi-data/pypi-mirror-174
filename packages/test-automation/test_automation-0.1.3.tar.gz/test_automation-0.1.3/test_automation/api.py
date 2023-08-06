import requests
import json
import os

URL = os.getenv("QE_API_SERVER")


def login_user(server, login_id, login_password):
    response = requests.request("POST", f"http://{URL}/api/login_user/", data={
        'server': server,
        'username': login_id,
        'password': login_password
    })
    return json.loads(response.text)

def restaurant(server, restaurant):
    response = requests.request("GET", f"http://{URL}/api/restaurant?server={server}&restaurant={restaurant}")
    return json.loads(response.text)

def login_admin(server, login_id, login_password):
    response = requests.request("POST", f"http://{URL}/api/login_admin/", data={
        'server': server,
        'username': login_id,
        'password': login_password
    })
    return json.loads(response.text)

def send_message_salck(channel, text, type):
    response = requests.request("POST", f"http://{URL}/api/send_message/", data={
        'channel': channel,
        'text': text,
        'type': type
    })
    return json.loads(response.text)

def update_message_slack(channel, text, type, ts):
    response = requests.request("POST", f"http://{URL}/api/update_message/", data={
        'channel': channel,
        'text': text,
        'type': type,
        'ts': ts
    })
    return json.loads(response.text)

def send_message_salck_fulfilment(channel, text, type):
    response = requests.request("POST", f"http://{URL}/api/send_message_fulfilment/", data={
        'channel': channel,
        'text': text,
        'type': type
    })
    return json.loads(response.text)

def update_message_slack_fulfilment(channel, text, type, ts):
    response = requests.request("POST", f"http://{URL}/api/update_message_fulfilment/", data={
        'channel': channel,
        'text': text,
        'type': type,
        'ts': ts
    })
    return json.loads(response.text)

def cart(server, restaurant, session):
    response = requests.request("GET",
                                f"http://{URL}/api/cart?server={server}&restaurant={restaurant}&session={session}")
    return json.loads(response.text)

def cart_submit(server, lat, lng, restaurant, session, delivery_fee, full_price, email, phone):
    response = requests.request("POST", f"http://{URL}/api/cart_submit/", data={
        'server': server,
        'lat': lat,
        'lng': lng,
        'restaurant': restaurant,
        'session': session,
        'delivery_fee': delivery_fee,
        'full_price': full_price,
        'email': email,
        'phone': phone
    })
    return json.loads(response.text)

def login_vms(server, login_id, login_password):
    response = requests.request("POST", f"http://{URL}/api/login_vms/", data={
        'server': server,
        'login_id': login_id,
        'login_password': login_password
    })
    return json.loads(response.text)