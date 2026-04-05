import requests

url = "https://danjuanfunds.com/dj-valuation-table-detail/SP500"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

r = requests.get(url, headers=headers, timeout=10)

print(f"Status: {r.status_code}")
print(f"Headers: {dict(r.headers)}")
print(f"Content length: {len(r.text)}")
print(f"\nFirst 2000 chars:\n{r.text[:2000]}")
