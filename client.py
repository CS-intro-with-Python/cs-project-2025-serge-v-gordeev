import requests
import sys

response = requests.get("http://127.0.0.1:28931/")
if response.status_code != 200:
    sys.exit(1)
else:
    print(response.json())