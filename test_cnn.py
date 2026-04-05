import requests
import re

print("=== Testing CNN Page Parsing ===")

url = "https://edition.cnn.com/markets/fear-and-greed"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

r = requests.get(url, headers=headers, timeout=10)
text = r.text

# Look for Fear & Greed value patterns
patterns = [
    r'Fear.*?Greed.*?(\d+)',
    r'"value"[:\s]+(\d+)',
    r'fng["\s-]value["\s:]+(\d+)',
    r'index["\s:]+{"value["\s:]+(\d+)',
]

for p in patterns:
    matches = re.findall(p, text, re.IGNORECASE)
    if matches:
        print(f"Pattern: {p} -> {matches[:3]}")

# Look for Extreme Fear / Extreme Greed text
if 'Extreme Fear' in text:
    print("Found 'Extreme Fear' in page")
if 'Extreme Greed' in text:
    print("Found 'Extreme Greed' in page")

print("\n=== Complete ===")
