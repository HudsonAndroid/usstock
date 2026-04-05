import requests
import re

# 用户提供的HTML是浏览器渲染后的完整HTML
# 让我们直接在返回的HTML中搜索可能的数据

url = "https://danjuanfunds.com/dj-valuation-table-detail/SP500"
headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(url, headers=headers, timeout=10)

text = r.text

# 检查是否有 "27.35" 或类似的PE值
matches = re.findall(r'(\d+\.\d+)', text)
print(f"Found {len(matches)} decimal numbers")

# 找包含27或28的数字（在合理范围内）
pe_values = [m for m in matches if 20 <= float(m) <= 40]
print(f"PE-like values: {pe_values}")

# 检查是否有多次加载的数据
if 'vue' in text.lower() or 'react' in text.lower():
    print("\nThis is a Vue/React app - data loaded client-side")

# 看看能不能找到API调用
api_patterns = [
    r'api[:"/]+(\w+)',
    r'url[:"/]+([^"]+\.json)',
    r'fetch\("([^"]+)"',
    r'axios\.get\("([^"]+)"',
]

for p in api_patterns:
    matches = re.findall(p, text)
    if matches:
        print(f"\nAPI pattern '{p}': {matches[:3]}")

print("\n=== Complete ===")
