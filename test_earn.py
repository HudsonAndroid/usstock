import requests

# Try to get S&P 500 earnings data from Yahoo
url = "https://query1.finance.yahoo.com/v10/finance/quoteSummary/%5EGSPC?modules=earnings"
headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(url, headers=headers, timeout=10)

print("Status:", r.status_code)
if r.status_code == 200:
    data = r.json()
    print("Keys:", list(data.get('quoteSummary', {}).keys()))
    result = data.get('quoteSummary', {}).get('result', [])
    if result:
        print("Result keys:", list(result[0].keys()))
        if 'earnings' in result[0]:
            earnings = result[0]['earnings']
            print("Earnings:", earnings)
