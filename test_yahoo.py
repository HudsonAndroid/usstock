import requests

# Test yfinance alternative - Yahoo Finance basic quotes
urls = [
    "https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC?range=1d",
    "https://query1.finance.yahoo.com/v8/finance/chart/%5ENDX?range=1d",
]

headers = {'User-Agent': 'Mozilla/5.0'}

for url in urls:
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(f"\n{url}")
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"Keys: {list(data.keys())}")
    except Exception as e:
        print(f"\n{url}: {e}")

print("\n=== Complete ===")
