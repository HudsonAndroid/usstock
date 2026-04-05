import requests
import json

# Try the value-center API endpoint
urls = [
    "https://danjuanfunds.com/djmodule/value-center",
    "https://danjuanfunds.com/IronforgeService/valuation/list",
    "https://danjuanfunds.com/api/valuation/list",
    "https://danjuanfunds.com/IronforgeService/market/valuation",
]

headers = {'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'}

for url in urls:
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(f"\n{url}")
        print(f"  Status: {r.status_code}")
        
        # Check if response is JSON
        if 'json' in r.headers.get('Content-Type', ''):
            try:
                data = r.json()
                print(f"  JSON keys: {list(data.keys())}")
                # Find NDX data
                if 'data' in data:
                    items = data['data'] if isinstance(data['data'], list) else data['data'].get('list', [])
                    for item in items:
                        if 'NDX' in str(item.get('index_code', '')):
                            print(f"  NDX data: {item}")
            except:
                pass
    except Exception as e:
        print(f"\n{url}: {e}")

print("\n=== Complete ===")
