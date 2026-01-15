import requests
import sys
from dv_calculator import calculate_dv, wrong_input, get_planet
from database import db

test_data1 = [{"location" : "aijhfieqhfqehf", "altitude" : None, "capture" : None}]
test_data2 = [{"location" : "Kerbin", "altitude" : 80000, "capture" : False}, {"location" : "Duna", "altitude" : 60000, "capture" : False}]
if (not wrong_input(test_data1)) or wrong_input(test_data2):
    sys.exit(1)

response = requests.get("http://127.0.0.1:28931/")
if response.status_code != 200:
    sys.exit(1)

test_data = [{"location" : "Kerbin", "altitude" : 80000, "capture" : False}, {"location" : "Duna", "altitude" : 60000, "capture" : False}]
response = requests.post("http://127.0.0.1:28931/calculate", json=test_data)
response_json = response.json()
if not (800 < response_json['dv'] < 1200):
    sys.exit(1)

test_data = [{"location" : "Kerbin", "altitude" : 80000, "capture" : False}, {"location" : "Kerbin", "altitude" : 80000, "capture" : True}]
response = requests.post("http://127.0.0.1:28931/calculate", json=test_data)
response_json = response.json()
if response_json['dv'] != 0:
    sys.exit(1)

test_data = [{"location" : "aijhfieqhfqehf", "altitude" : None, "capture" : None}]
response = requests.post("http://127.0.0.1:28931/calculate", json=test_data)
response_json = response.json()
if response_json['dv'] != "Error: invalid input":
    sys.exit(1)