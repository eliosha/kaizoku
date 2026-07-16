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

fandom_series = [
    'marvel', 'dc', 'harry potter', 'breaking bad', 'game of thrones', 
    'stranger things', 'peaky blinders', 'the godfather', 'invincible'
]

# Print raw keys matching fandom
print("Fandom matches in main.js in raw declaration order:")
count = 0
for k in keys:
    # We must extract the series property for key k in db_text
    # Let's find the content for key k
    pat = r"['\"]" + re.escape(k) + r"['\"]\s*:\s*\{"
    match = re.search(pat, db_text)
    if match:
        start_pos = match.end() - 1
        b_count = 0
        end_pos = None
        for i in range(start_pos, len(db_text)):
            c = db_text[i]
            if c == '{':
                b_count += 1
            elif c == '}':
                b_count -= 1
                if b_count == 0:
                    end_pos = i + 1
                    break
        block = db_text[start_pos:end_pos]
        # extract series
        series_match = re.search(r"series\s*:\s*['\"](.*?)['\"]", block)
        series = series_match.group(1) if series_match else ""
        if any(fs in series.lower() for fs in fandom_series):
            count += 1
            print(f"  {count}. Key: {k}, Series: {series}")
