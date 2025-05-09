import requests
from datetime import datetime

url = 'http://127.0.0.1:5000/get_schedule'

subdomain = 'ATZS'
branch = '61'
start = '2024-12-02'
end = '2024-12-09'
mode = "formal"

payload = {"subdomain": subdomain, "branch": branch, "start": start, "end": end, "mode": mode}

start_time = datetime.now()
# Send the request with the .pem key
response = requests.post(url, json=payload, timeout=40)

# Check the response
if response.status_code == 200:
    print("Request was successful")
    print(response.json().keys())
    print(response.json()["Empty"])
    print(response.json()["Summary"])
else:
    print(f"Failed to connect, status code: {response.status_code}")
print("Latency:", datetime.now() - start_time)
