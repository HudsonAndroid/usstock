import requests
import re

# 检查gzip问题，并尝试解析
url = "https://danjuanfunds.com/dj-valuation-table-detail/SP500"
headers = {'User-Agent': 'Mozilla/5.0'}

# 先检查是否返回gzip
r = requests.get(url, headers=headers, timeout=10)
print(f"Encoding: {r.headers.get('Content-Encoding')}")

# 用相同逻辑测试NDX和SP500
def get_pe_from_page(text):
    # 找 "数字倍" 或 "数字x" 的模式
    match = re.search(r'(\d+\.?\d*)\s*(?:倍|x)', text)
    if match:
        val = float(match.group(1))
        if 10 < val < 100:
            return val
    return None

# 测试
for name, code in [("NDX", "NDX"), ("SP500", "SP500")]:
    url = f"https://danjuanfunds.com/dj-valuation-table-detail/{code}"
    r = requests.get(url, headers=headers, timeout=10)
    text = r.text
    
    pe = get_pe_from_page(text)
    print(f"\n{name}: PE = {pe}")
    print(f"  Text length: {len(text)}")
    
    # 查看text中是否包含倍或x
    if '倍' in text:
        print(f"  Contains '倍': Yes")
        # 找倍数
        bei_matches = re.findall(r'(\d+\.?\d*)\s*倍', text)
        print(f"  倍 matches: {bei_matches[:5]}")
    else:
        print(f"  Contains '倍': No")
