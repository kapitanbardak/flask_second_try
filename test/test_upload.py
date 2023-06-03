import requests
import json

url = 'http://localhost:80/api/users'
data = '{"username": "AlexDarkStalker"}'
headers = {'Content-type': 'application/json'}
response = requests.post(url, json=json.loads(data), headers=headers)

response_data = json.loads(response.text)
user_id = response_data["user_id"]
access_token = response_data["access_token"]


url = 'http://localhost:80/api/upload'
file_path = 'audio.wav'
data = {'user_id': user_id, 'access_token': access_token}
headers = {'Content-type': 'multipart/form-data'}

with open(file_path, 'rb') as file:
    response = requests.post(url, data=data, files={'audio_file': file})


print(response.text)
