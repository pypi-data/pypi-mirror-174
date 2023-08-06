import requests
import json
import os
import time

URL = os.getenv("QE_API_SERVER")

def get_order_id(order_number):
    data = json.loads(requests.request("GET", f"http://{URL}/api/hubyo/get_order_id/?ordernumber={order_number}").text)
    return data['order_id'], data['json_data']

def get_ygy_order_id(order_id):
    return json.loads(requests.request("GET", f"http://{URL}/api/hubyo/get_ygy_order_id?ordernumber={order_id}").text)

def get_conveyo_status(json_data, status):
    for i in json_data:
        if "message" in i:
            if i['message'] == "Order status changed" and i['status'] == status:
                return True

"""
노티요에서 TEMPLATE CODE로 수락/거부/취소되었는지 확인
"""

def get_notiyo_accepted(json_data):
    for i in json_data:
        if "message" in i:
            if "TEMPLATE CODE: Notiyov2submitted" in i['message']:
                return True

def get_notiyo_declined(json_data):
    for i in json_data:
        if "message" in i:
            if "TEMPLATE CODE: NotiyoSystemUser39" or "TEMPLATE CODE: NotiyoRestDeclined" in i['message']:
                return True

def get_notiyo_cancelled(json_data):
    for i in json_data:
        if "message" in i:
            if "TEMPLATE CODE: NotiyoSystemUser32" or "TEMPLATE CODE: NotiyoRestDeclined" in i['message']:
                return True

"""
노티요에서 TEMPlATE CODE로 고윈 - 배달출발안내 되었는지 확인
"""

def get_notiyo_delivered(json_data):
    for i in json_data:
        if "message" in i:
            if "TEMPLATE CODE: NotiyoSystemUser42" in i['message']:
                return True

"""
허브요 데이터 받아서 주문전달 되었는지 확인 
"""

def get_orderyo_sending(json_data):
    msg_list = []
    for i in json_data:
        if "message" in i:
            if "주문접수: 접수 중 (RECEIVING)" in i['message']:
                msg_list.append(i['message'])
            elif "주문전달: 전달 중 (SENDING)" in i['message']:
                msg_list.append(i['message'])
            elif "주문전달: 전달 완료 (RECEIVED)" in i['message']:
                msg_list.append(i['message'])

    if len(msg_list) == 5:
        return True
    else:
        return False

"""
오더요에서 수락되었는지 확인
"""

def get_orderyo_accepted(json_data):
    for i in json_data:
        if "message" in i:
            if "주문성공: 수락 완료 (ACCEPTED)" in i['message']:
                return True

"""
오더요에서 거절되었는지 확인
"""

def get_orderyo_declined(json_data):
    for i in json_data:
        if "message" in i:
            if "주문취소: 배달 취소 (CANCELLED)" in i['message']:
                return True

"""
오더요에서 수락 후 취소 또는 취소가 되었는지 확인
"""

def get_orderyo_canceled(json_data):
    for i in json_data:
        if "message" in i:
            if "주문취소: 배달 취소 (CANCELLED)" in i['message']:
                return True

def check_orderyo_sending(order_number):
    time.sleep(30)

    return get_orderyo_sending(get_order_id(order_number))


def check_conveyo(order_state):
    return get_conveyo_status(order_state)

def check_notiyo(order_state):
    if order_state == "ACCEPTED":
        return get_notiyo_accepted()
    elif order_state == "CANCELLED":
        return get_notiyo_cancelled()
    else:
        return get_notiyo_declined()

def check_orderyo(order_id, order_state):
    if order_state == "ACCEPTED" and "DELIVERED":
        return get_orderyo_accepted()
    elif order_state == "CANCELLED":
        return get_orderyo_canceled()
    else:
        return get_orderyo_declined()