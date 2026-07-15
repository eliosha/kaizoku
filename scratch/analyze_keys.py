import re

main_path = "/Users/mac/Desktop/Websites /GITkaizoku/main.js"
with open(main_path) as f:
    content = f.read()

# Match the productsDB declaration
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
# Find keys exactly as they appear (single or double quoted)
keys = re.findall(r"['\"]([a-zA-Z0-9\s_-]+)['\"]\s*:", db_text)

print("Total keys found:", len(keys))
print("First 10 keys:")
for k in keys[:10]:
    print(f"  {repr(k)}")

print("\nChecking exact match for 'tanjiro-kamado-hoodie-demon-slayer':")
matches = [k for k in keys if "tanjiro-kamado-hoodie-demon-slayer" in k]
print(f"Matches: {matches}")
