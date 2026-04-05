import requests
import re

urls = [
    "https://danjuanfunds.com/dj-valuation-table-detail/NDX",
    "https://danjuanfunds.com/dj-valuation-table-detail/sp500",
    "https://danjuanfunds.com/valuation/NDX",
    "https://danjuanfunds.com/api/valuation/NDX",
]

for url in urls:
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        print(f"\n{url}")
        print(f"  Status: {r.status_code}")
        
        # Try to find JSON
        json_matches = re.findall(r'\{[^{}]*"pe"[^{}]*\}', r.text)
        if json_matches:
            print(f"  Found JSON: {json_matches[0][:200]}")
        
        # Try to find PE value
        pe_matches = re.findall(r'(\d+\.?\d*)\s*[倍xX]', r.text)
        if pe_matches:
            print(f"  PE values found: {pe_matches[:5]}")
    except Exception as e:
        print(f"\n{url}: {e}")

print("\n=== Complete ===")
