import requests
import re

url = "https://www.gurufocus.com/economic_indicators/6778/nasdaq-100-pe-ratio"
headers = {'User-Agent': 'Mozilla/5.0'}

r = requests.get(url, headers=headers, timeout=10)
print(f"Status: {r.status_code}")

# Look for PE value
patterns = [
    r'PE Ratio.*?(\d+\.?\d*)',
    r'(\d+\.?\d*)\s*\(As of',
    r'value.*?(\d+\.\d+)',
]

for p in patterns:
    m = re.search(p, r.text)
    if m:
        print(f"Pattern '{p}': {m.group(1)}")

print("\n=== Complete ===")
