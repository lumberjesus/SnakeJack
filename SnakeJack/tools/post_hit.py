import urllib.request
import json

url = 'http://127.0.0.1:5000/api/game/hit'
req = urllib.request.Request(url, method='POST')
try:
    with urllib.request.urlopen(req, timeout=5) as resp:
        print('status', resp.status)
        body = resp.read().decode('utf-8')
        try:
            print(json.dumps(json.loads(body), indent=2))
        except Exception:
            print(body)
except Exception as e:
    print('request error', repr(e))
