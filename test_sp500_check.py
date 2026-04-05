import requests

# Check if the exact HTML you showed exists in our response
url = "https://danjuanfunds.com/dj-valuation-table-detail/SP500"
headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(url, headers=headers, timeout=10)

text = r.text

# Check for key elements from your HTML
checks = [
    ("value-text", 'class="value-text"' in text),
    ("middle-name", 'class="middle-name"' in text),
    ("detail-value", 'class="detail-value"' in text),
    ("tit-middle", 'class="tit-middle"' in text),
    ("27.35", "27.35" in text),
    ("26.77", "26.77" in text),
    ("PE走势", "PE走势" in text),
]

print("=== Checking SP500 page structure ===")
for name, result in checks:
    print(f"{name}: {result}")

# Also check content length vs what you provided
print(f"\nOur response length: {len(text)}")
print(f"Your HTML length: ~120 lines (scrolled)")

# Try to find any PE-related text
import re
pe_mentions = re.findall(r'PE[^\<]{0,50}', text)
print(f"\nPE mentions in our response: {pe_mentions[:3]}")
