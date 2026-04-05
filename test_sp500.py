import requests
import re

print("=== Testing S&P500 PE Sources ===")

# Test multpl.com
url = "https://www.multpl.com/s-p-500-pe-ratio"
headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(url, headers=headers, timeout=10)
print(f"\nmultpl.com Status: {r.status_code}")

# Look for PE value
patterns = [
    r'(\d+\.?\d*)</span>',
    r'current.*?(\d+\.?\d*)',
    r'(\d+\.\d+)</span',
]

for p in patterns:
    m = re.search(p, r.text)
    if m:
        print(f"  Pattern '{p}': {m.group(1)}")

# Print around the value
idx = r.text.find('span')
if idx > 0:
    print(f"\nAround span: {r.text[idx:idx+100]}")

print("\n=== Complete ===")
