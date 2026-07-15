import re
import json

main_path = "/Users/mac/Desktop/Websites /GITkaizoku/main.js"

with open(main_path) as f:
    content = f.read()

# Let's extract window.productsDB block
# We can find where window.productsDB starts and where it ends by balancing curly braces.
db_match = re.search(r"window\.productsDB\s*=\s*\{", content)
if not db_match:
    print("productsDB not found")
    exit()

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

# Let's parse individual product blocks using a regex or simple parser
# Each block looks like:
# 'id': {
#    name: '...',
#    ...
# }
# Since it's javascript, we can't just json.loads it directly because keys aren't quoted.
# Let's write a simple parser to extract key-value pairs or just output the text.
# We can find all keys by matching: 'key': { or "key": {
product_matches = re.finditer(r"['\"]([a-zA-Z0-9_-]+)['\"]\s*:\s*\{", db_text)
products = []

# Let's get the positions of matches
matches_list = list(product_matches)
for i in range(len(matches_list)):
    match = matches_list[i]
    prod_id = match.group(1)
    
    # Extract the block text
    start = match.end() - 1
    # Count braces to find the end of this block
    b_count = 0
    p_end = None
    for j in range(start, len(db_text)):
        c = db_text[j]
        if c == '{':
            b_count += 1
        elif c == '}':
            b_count -= 1
            if b_count == 0:
                p_end = j + 1
                break
    block_text = db_text[start:p_end]
    
    # Extract name and images
    name_m = re.search(r"name\s*:\s*['\"](.*?)['\"]\s*,", block_text)
    images_m = re.search(r"images\s*:\s*\[(.*?)\]", block_text, re.DOTALL)
    
    name = name_m.group(1) if name_m else "Unknown"
    images = []
    if images_m:
        images = [img.strip().strip("'\"") for img in images_m.group(1).split(",") if img.strip()]
        
    products.append({
        "id": prod_id,
        "name": name,
        "images": images
    })

print(f"Total products in main.js: {len(products)}")
print(json.dumps(products[:15], indent=2))

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/extracted_products.json", "w") as f:
    json.dump(products, f, indent=2)
