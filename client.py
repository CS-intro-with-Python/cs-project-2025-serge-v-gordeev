import requests
import sys

response = requests.get("http://127.0.0.1:8080/")
if response.status_code != 200:
    sys.exit(1)