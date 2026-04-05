import re

html = '''
<div data-v-22e53b5c="" data-v-1c0df567="" class="dj-valuation-table-detail">
...
'''

# 从用户提供的HTML中提取PE值
pe_match = re.search(r'PE.*?value-text.*?(\d+\.?\d*)', html)
print(f"PE match: {pe_match.group(1) if pe_match else 'not found'}")

# 更好的方式：直接找value-text后面的数字
values = re.findall(r'<div[^>]*class="value-text"[^>]*>(\d+\.?\d*)', html)
print(f"All value-text values: {values}")

# 找估值状态
status = re.search(r'class="middle-name"[^>]*>([^<]+)', html)
print(f"Status: {status.group(1) if status else 'not found'}")
