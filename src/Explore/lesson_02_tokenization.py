import tiktoken

encoding = tiktoken.get_encoding("o200k_base")

examples = ["Hello", "What is React?", "I am learning AI engineering.", "నమస్తే", "🚀"]

for text in examples:
    token_ids = encoding.encode(text)

    print("Text:", text)
    print("Token IDs:", token_ids)
    print("Token Count:", len(token_ids))
    print("Decoded:", encoding.decode(token_ids))
    print("-" * 30)


# Text: Hello
# Token IDs: [13225]
# Token Count: 1
# Decoded: Hello
# ------------------------------
# Text: What is React?
# Token IDs: [4827, 382, 6184, 30]
# Token Count: 4
# Decoded: What is React?
# ------------------------------
# Text: I am learning AI engineering.
# Token IDs: [40, 939, 7524, 20837, 16411, 13]
# Token Count: 6
# Decoded: I am learning AI engineering.
# ------------------------------
# Text: నమస్తే
# Token IDs: [3296, 7344, 42708, 3650]
# Token Count: 4
# Decoded: నమస్తే
# ------------------------------
# Text: 🚀
# Token IDs: [112927, 222]
# Token Count: 2
# Decoded: 🚀
