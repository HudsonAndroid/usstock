import requests
import json

# Test if we can get S&P 500 earnings and calculate PE
# Try Yahoo Finance chart API
url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC?interval=1d&range=1mo"
headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(url, headers=headers, timeout=10)

print("Status:", r.status_code)
if r.status_code == 200:
    data = r.json()
    print("Keys:", list(data.keys()))
    if 'chart' in data and 'result' in data['chart']:
        result = data['chart']['result']
        if result:
            meta = result[0].get('meta', {})
            print("Meta:", meta)
            print("Previous Close:", meta.get('previousClose'))
            print("Chart Period:", result[0].get('period'))
