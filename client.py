import requests

response = requests.get("http://127.0.0.1:8080/hello")
print(response.content)

name = input()
response = requests.get(f"http://127.0.0.1:8080/user/{name}")
print(response.content)

query = input()
response = requests.get(f"http://127.0.0.1:8080/search?q={query}")
print(response.content)