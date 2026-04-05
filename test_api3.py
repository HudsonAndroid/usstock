import requests
import re

url = "https://danjuanfunds.com/djmodule/value-center"
headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(url, headers=headers, timeout=10)

# Look for API URLs in the page
api_patterns = [
    r'api["\s:]+"([^"]+)"',
    r'url["\s:]+"([^"]+)"',
    r'fetch\("([^"]+)"',
    r'axios\.get\("([^"]+)"',
    r'data-url="([^"]+)"',
]

for p in api_patterns:
    matches = re.findall(p, r.text)
    if matches:
        print(f"\nPattern {p}:")
        for m in set(matches):
            print(f"  {m}")

# Look for specific NDX data
if 'NDX' in r.text:
    idx = r.text.find('NDX')
    print(f"\nAround NDX: {r.text[idx:idx+200]}")
