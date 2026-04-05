# 使用curl_cffi来模拟浏览器请求
# 这个库已经安装

from curl_cffi.requests import Session
import re

def get_pe_from_danjuan(index_code):
    """使用curl_cffi获取蛋卷基金估值数据"""
    url = f"https://danjuanfunds.com/dj-valuation-table-detail/{index_code}"
    
    # 使用Chrome浏览器的TLS指纹
    s = Session(impersonate="chrome110")
    r = s.get(url, timeout=30)
    
    if r.status_code != 200:
        print(f"Error: {r.status_code}")
        return None
    
    text = r.text
    
    # 查找PE值 - 使用正则匹配 "数字.数字" 在特定标签内
    # 页面结构: <div class="value-text">27.35</div>
    matches = re.findall(r'<div[^>]*class="value-text"[^>]*>(\d+\.?\d*)</div>', text)
    
    # 过滤合理范围的PE值
    pe_values = [float(m) for m in matches if 15 <= float(m) <= 50]
    
    if pe_values:
        # 返回第一个（通常是当前PE）
        return pe_values[0]
    
    # 备用方案：找 "数字倍" 或 "数字x"
    match = re.search(r'(\d+\.?\d*)\s*(?:倍|x)', text)
    if match:
        val = float(match.group(1))
        if 10 < val < 100:
            return val
    
    return None

# 测试
print("=== Testing curl_cffi ===")

for name, code in [("NDX", "NDX"), ("SP500", "SP500")]:
    pe = get_pe_from_danjuan(code)
    print(f"{name}: PE = {pe}")

print("\n=== Complete ===")
