import requests
import re

print("=== Testing Danjuanfunds NDX ===")

url = "https://danjuanfunds.com/dj-valuation-table-detail/NDX"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
r = requests.get(url, headers=headers, timeout=10)
text = r.text

# Search for PE or valuation data
patterns = [
    r'pe["\s:]+(\d+\.?\d*)',
    r'PE[:\s]+(\d+\.?\d*)',
    r'估值[:\s]+(\d+\.?\d*)',
    r'(\d+\.?\d*)\s*[倍]',
    r'"pe"\s*:\s*(\d+\.?\d*)',
    r'data-pe="(\d+\.?\d*)"',
]

for p in patterns:
    matches = re.findall(p, text, re.IGNORECASE)
    if matches:
        print(f"Pattern '{p}' found: {matches[:5]}")

# Print a snippet of the text around key terms
if 'PE' in text:
    idx = text.find('PE')
    print(f"\nAround 'PE': ...{text[max(0,idx-20):idx+50]}...")

print("\n=== Testing CNN alternative ===")

# Try alternative CNN endpoints
urls_to_try = [
    "https://dataviz.cnn.io/fear-greed",
    "https://cnn.com/markets/fear-and-greed",
    "https://fng-cdn.com/fng-api/v1/fear-greed",
]

for url in urls_to_try:
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(f"{url}: {r.status_code}")
    except Exception as e:
        print(f"{url}: {e}")

print("\n=== Complete ===")
