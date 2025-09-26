import requests
import json

s = requests.Session()
print('Starting royal cheat start...')
start = s.post('http://127.0.0.1:5000/api/game/start?cheat=royal')
print('start', start.status_code)
print(start.text)

print('\nTrigger lucky (ace) cheat on hit...')
hit = s.post('http://127.0.0.1:5000/api/game/hit?cheat=ace')
print('hit', hit.status_code)
print(hit.text)

print('\nTrigger python (bust) cheat on stand...')
stand = s.post('http://127.0.0.1:5000/api/game/stand?cheat=bust')
print('stand', stand.status_code)
print(stand.text)
