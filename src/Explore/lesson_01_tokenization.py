import tiktoken

encoding = tiktoken.get_encoding("o200k_base")

samples = [
    "AI",
    "Artificial Intelligence",
    "I am learning AI engineering.",
    "const value = 42;",
    "నమస్తే",
    "🚀🤖",
]

for text in samples:
    token_ids = encoding.encode(text)

    print(f"\nText: {text!r}")
    print(f"Token count: {len(token_ids)}")
    print(f"Token IDs: {token_ids}")

    pieces = [encoding.decode_single_token_bytes(token_id) for token_id in token_ids]

    print(f"Token bytes: {pieces}")
    print(f"Decoded: {encoding.decode(token_ids)}")


# Text: 'AI'
# Token count: 1
# Token IDs: [17527]
# Token bytes: [b'AI']
# Decoded: AI

# Text: 'Artificial Intelligence'
# Token count: 2
# Token IDs: [186671, 42378]
# Token bytes: [b'Artificial', b' Intelligence']
# Decoded: Artificial Intelligence

# Text: 'I am learning AI engineering.'
# Token count: 6
# Token IDs: [40, 939, 7524, 20837, 16411, 13]
# Token bytes: [b'I', b' am', b' learning', b' AI', b' engineering', b'.']
# Decoded: I am learning AI engineering.

# Text: 'const value = 42;'
# Token count: 6
# Token IDs: [1671, 1432, 314, 220, 4689, 26]
# Token bytes: [b'const', b' value', b' =', b' ', b'42', b';']
# Decoded: const value = 42;

# Text: 'నమస్తే'
# Token count: 4
# Token IDs: [3296, 7344, 42708, 3650]
# Token bytes: [b'\xe0\xb0\xa8', b'\xe0\xb0\xae', b'\xe0\xb0\xb8\xe0\xb1\x8d\xe0\xb0\xa4', b'\xe0\xb1\x87']
# Decoded: నమస్తే

# Text: '🚀🤖'
# Token count: 4
# Token IDs: [112927, 222, 50378, 244]
# Token bytes: [b'\xf0\x9f\x9a', b'\x80', b'\xf0\x9f\xa4', b'\x96']
# Decoded: 🚀🤖
