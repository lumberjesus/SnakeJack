import requests
import json

s = requests.Session()
start = s.post('http://127.0.0.1:5000/api/game/start')
print('start', start.status_code)
try:
    print(json.dumps(start.json(), indent=2))
except Exception:
    print(start.text)

hit = s.post('http://127.0.0.1:5000/api/game/hit')
print('hit', hit.status_code)
try:
    print(json.dumps(hit.json(), indent=2))
except Exception:
    print(hit.text)
