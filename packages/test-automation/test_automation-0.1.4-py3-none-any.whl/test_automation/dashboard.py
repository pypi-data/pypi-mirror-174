import requests
import json
import os

URL = os.getenv("QE_API_SERVER")

def get_test_list():
    response = requests.request("GET", f"http://{URL}/testlist")
    return json.loads(response.text)