import requests

url = "https://www.multpl.com/s-p-500-pe-ratio"
headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(url, headers=headers, timeout=10)

print("Status:", r.status_code)
print("Content length:", len(r.text))

# Find value in page
if 'value' in r.text.lower():
    idx = r.text.lower().find('value')
    print(f"\nAround 'value': {r.text[idx:idx+150]}")
