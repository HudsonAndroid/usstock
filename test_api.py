import requests

print("=== Testing Data Sources ===")

# Test Shiller API
try:
    r = requests.get("https://posix4e.github.io/shiller_wrapper_data/data/latest.json", timeout=10)
    data = r.json()
    print(f"\n1. Shiller S&P500 CAPE: {data['stock_market']['cape']}")
except Exception as e:
    print(f"\n1. Shiller failed: {e}")

# Test CNN Fear and Greed
try:
    url = "https://production.datavix.cnn.io/fsg-auth-1/fear-greed"
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers, timeout=10)
    data = r.json()
    print(f"2. CNN Fear&Greed: {data.get('data', {}).get('now', {}).get('value')}")
except Exception as e:
    print(f"2. CNN Fear&Greed failed: {e}")

# Test Danjuanfunds NDX
try:
    url = "https://danjuanfunds.com/dj-valuation-table-detail/NDX"
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers, timeout=10)
    print(f"3. Danjuan NDX - Status: {r.status_code}, Length: {len(r.text)}")
except Exception as e:
    print(f"3. Danjuan NDX failed: {e}")

print("\n=== Complete ===")
