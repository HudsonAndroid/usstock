import requests
import re
import json

url = "https://danjuanfunds.com/dj-valuation-table-detail/NDX"
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
text = r.text

# Look for embedded JSON data
patterns = [
    r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\});',
    r'window\.data\s*=\s*(\{.*?\});',
    r'"initialState"\s*:\s*(\{.*?\})',
    r'var\s+data\s*=\s*(\{.*?\})',
]

for p in patterns:
    matches = re.findall(p, text, re.DOTALL)
    if matches:
        try:
            data = json.loads(matches[0])
            print(f"Found JSON with pattern: {p[:30]}...")
            print(f"Keys: {list(data.keys())[:10]}")
        except:
            pass

# Look for specific NDX PE
ndx_matches = re.findall(r'NDX["\s:]+[^"]*"pe"[:\s]+(\d+\.?\d*)', text)
if ndx_matches:
    print(f"\nNDX PE: {ndx_matches}")

# Print part of the HTML around PE
if 'PE' in text.lower():
    idx = text.lower().find('pe')
    print(f"\nAround PE: {text[max(0,idx-50):idx+100]}")
