import requests

print("=== Testing fear-greed library ===")

try:
    from fear_greed import FearAndGreed
    fg = FearAndGreed()
    value = fg.get_current_value()
    print(f"Fear&Greed value: {value}")
except Exception as e:
    print(f"Error: {e}")

print("\n=== Complete ===")
