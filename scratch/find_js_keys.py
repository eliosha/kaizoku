import re

main_path = "/Users/mac/Desktop/Websites /GITkaizoku/main.js"
with open(main_path) as f:
    content = f.read()

# Extract keys in productsDB
db_match = re.search(r"window\.productsDB\s*=\s*\{", content)
start_idx = db_match.end() - 1
brace_count = 0
end_idx = None
for idx in range(start_idx, len(content)):
    char = content[idx]
    if char == '{':
        brace_count += 1
    elif char == '}':
        brace_count -= 1
        if brace_count == 0:
            end_idx = idx + 1
            break

db_text = content[start_idx:end_idx]
keys = re.findall(r"['\"]([a-zA-Z0-9_-]+)['\"]\s*:", db_text)

# Let's search keys for some common items:
for target in ["hoodie", "wallet", "ring", "bracelet", "katana", "figure", "poster", "spiderman", "tote"]:
    matches = [k for k in keys if target in k.lower()]
    print(f"Target '{target}': {matches[:5]}")
