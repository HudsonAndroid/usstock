import requests
import re

# Test both NDX and SP500 pages
urls = [
    ("NDX", "https://danjuanfunds.com/dj-valuation-table-detail/NDX"),
    ("SP500", "https://danjuanfunds.com/dj-valuation-table-detail/SP500"),
]

headers = {'User-Agent': 'Mozilla/5.0'}

for name, url in urls:
    r = requests.get(url, headers=headers, timeout=10)
    text = r.text
    
    # Try multiple patterns
    patterns = [
        r'class="value-text"[^>]*>(\d+\.?\d*)',
        r'"value-text"'[:20] + r'.*?>(\d+\.?\d*)',
        r'(\d+\.\d+)</div>.*?value-text',
    ]
    
    print(f"\n=== {name} ===")
    print(f"Status: {r.status_code}")
    
    # Find value-text elements
    matches = re.findall(r'class="value-text"[^>]*>(\d+\.?\d*)', text)
    print(f"value-text matches: {matches}")
    
    # Find any numbers around 20-40 (likely PE values)
    all_nums = re.findall(r'\d+\.\d+', text)
    pe_candidates = [n for n in all_nums if 20 <= float(n) <= 40]
    print(f"PE candidates (20-40): {set(pe_candidates)}")

print("\n=== Complete ===")
