import fear_greed as fg

print("=== Testing FearGreedClient ===")

try:
    client = fg.FearGreedClient()
    result = client.get()
    print(f"Result: {result}")
except Exception as e:
    print(f"Error with client.get(): {e}")

try:
    score = fg.get_score()
    print(f"get_score(): {score}")
except Exception as e:
    print(f"Error with get_score(): {e}")

try:
    rating = fg.get_rating()
    print(f"get_rating(): {rating}")
except Exception as e:
    print(f"Error with get_rating(): {e}")

print("\n=== Complete ===")
