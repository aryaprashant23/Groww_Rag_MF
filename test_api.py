import requests
import json
import sys

url = 'https://web-production-c611f.up.railway.app/chat'
payload = {"query": "What is the NAV of Nippon India small cap?"}
headers = {'Content-Type': 'application/json'}

try:
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
