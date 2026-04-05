import requests
import re

url = "https://danjuanfunds.com/dj-valuation-table-detail/SP500"
headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(url, headers=headers, timeout=10)

print(f"Status: {r.status_code}")

# 直接找 value-text 的值
text = r.text

# 找PE值 - 在 "PE" 后面的 value-text 中
pe_pattern = r'PE[^<]*<div[^>]*class="value-text"[^>]*>(\d+\.?\d*)'
pe_match = re.search(pe_pattern, text)
print(f"PE: {pe_match.group(1) if pe_match else 'not found'}")

# 找估值状态
status_pattern = r'class="middle-name"[^>]*>([^<]+)'
status_match = re.search(status_pattern, text)
print(f"Status: {status_match.group(1) if status_match else 'not found'}")

# 找PE百分位
percent_pattern = r'PE百分位[^<]*<div[^>]*class="value-text"[^>]*>(\d+\.?\d*)'
percent_match = re.search(percent_pattern, text)
print(f"PE Percentile: {percent_match.group(1) if percent_match else 'not found'}")

print("\n=== Complete ===")
