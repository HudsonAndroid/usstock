import yfinance as yf

print("=== Testing yfinance S&P 500 Data ===")

# Get S&P 500 ticker
sp500 = yf.Ticker("^GSPC")

# Try to get info
info = sp500.info
print("\nInfo keys:", list(info.keys())[:20])

# Look for PE
print(f"\ntrailingPE: {info.get('trailingPE')}")
print(f"forwardPE: {info.get('forwardPE')}")
print(f"pegRatio: {info.get('pegRatio')}")

# Try history
hist = sp500.history(period="5d")
print(f"\nHistory:\n{hist}")

# Get basic info
print(f"\nFast info:")
print(f"  regularMarketPE: {info.get('regularMarketPE')}")
print(f"  fiftyDayAverage: {info.get('fiftyDayAverage')}")

print("\n=== Complete ===")
