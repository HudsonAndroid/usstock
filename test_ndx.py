import requests

url = "https://danjuanfunds.com/market/valuation"
headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://danjuanfunds.com/'}
r = requests.get(url, headers=headers, timeout=10)
print("Status:", r.status_code)
print("Length:", len(r.text))
print("Content:", r.text[:1000])
