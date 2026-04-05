import yfinance as yf

print("=== Testing Yahoo Finance Data ===")

ndx = yf.Ticker("^NDX")
print(f"\nNDX (NASDAQ 100):")
print(f"  trailingPE: {ndx.info.get('trailingPE')}")
print(f"  forwardPE: {ndx.info.get('forwardPE')}")

sp500 = yf.Ticker("^GSPC")
print(f"\nSP500 (S&P 500):")
print(f"  trailingPE: {sp500.info.get('trailingPE')}")
print(f"  forwardPE: {sp500.info.get('forwardPE')}")

print("\n=== Test Complete ===")
