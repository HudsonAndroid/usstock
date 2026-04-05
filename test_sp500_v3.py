import requests
import re

url = "https://www.multpl.com/s-p-500-pe-ratio"
headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(url, headers=headers, timeout=10)

# Look for the main PE value - it's probably in a heading or prominent place
# Let's find all numbers that look like PE values
numbers = re.findall(r'(\d+\.?\d*)', r.text)

# Filter for reasonable PE values (between 10 and 100)
pe_values = [float(n) for n in numbers if 10 <= float(n) <= 100]
unique_pe = sorted(set(pe_values), reverse=True)

print("Possible PE values found:", unique_pe[:20])

# Look for "current" section
if 'current' in r.text.lower():
    idx = r.text.lower().find('current')
    print(f"\nAround 'current': {r.text[idx:idx+200]}")

# Look for the specific div/span with the value
match = re.search(r'(\d+\.\d+)</', r.text)
if match:
    print(f"\nDecimal match: {match.group(1)}")
