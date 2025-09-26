import requests
import json

s = requests.Session()
print('Starting game with 3 hands...')
start = s.post('http://127.0.0.1:5000/api/game/start?num_hands=3')
print('start', start.status_code)
try:
    print(json.dumps(start.json(), indent=2))
except Exception:
    print(start.text)

print('\nHit hand 0...')
hit0 = s.post('http://127.0.0.1:5000/api/game/hit?hand_index=0')
print('hit0', hit0.status_code)
try:
    print(json.dumps(hit0.json(), indent=2))
except Exception:
    print(hit0.text)

print('\nStand hand 1...')
stand1 = s.post('http://127.0.0.1:5000/api/game/stand?hand_index=1')
print('stand1', stand1.status_code)
try:
    print(json.dumps(stand1.json(), indent=2))
except Exception:
    print(stand1.text)
