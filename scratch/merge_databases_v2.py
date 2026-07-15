import json
import re
import os

main_path = "/Users/mac/Desktop/Websites /GITkaizoku/main.js"

# Load generated metadata
with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/product_metadata_v2.json") as f:
    generated_db = json.load(f)

# Load existing main.js content
with open(main_path) as f:
    js_content = f.read()

# Extract original products database block
db_match = re.search(r"window\.productsDB\s*=\s*\{", js_content)
if not db_match:
    print("Could not find window.productsDB in main.js")
    exit()

start_idx = db_match.end() - 1
brace_count = 0
end_idx = None
for idx in range(start_idx, len(js_content)):
    char = js_content[idx]
    if char == '{':
        brace_count += 1
    elif char == '}':
        brace_count -= 1
        if brace_count == 0:
            end_idx = idx + 1
            break

original_db_text = js_content[start_idx:end_idx]

# Parse each product block in main.js
product_blocks = re.finditer(r"['\"]([a-zA-Z0-9_-]+)['\"]\s*:\s*\{", original_db_text)
original_products = {}
matches_list = list(product_blocks)

for i in range(len(matches_list)):
    match = matches_list[i]
    prod_id = match.group(1)
    
    start = match.end() - 1
    b_count = 0
    p_end = None
    for j in range(start, len(original_db_text)):
        c = original_db_text[j]
        if c == '{':
            b_count += 1
        elif c == '}':
            b_count -= 1
            if b_count == 0:
                p_end = j + 1
                break
    block_text = original_db_text[start:p_end]
    original_products[prod_id] = block_text

# Map existing IDs to generated slugs using token matching
mapping_existing_to_slug = {}
slug_to_existing = {}

# Keywords mapping for existing product names
existing_keywords = {
    "jjk-nobara-tote-bag": ["nobara", "tote", "bag"],
    "akatsuki-rings-red-and-white": ["akatsuki", "ring"],
    "aot-wings-of-freedom-bracelet": ["wings", "freedom", "bracelet"],
    "akaza-figurine": ["akaza", "figure"],
    "akaza-figurine-demon-slayer-infinity-castle": ["akaza", "infinity", "castle"],
    "armored-titan-figurine": ["armored", "titan"],
    "female-titan-figurine": ["female", "titan"],
    "luffy-gear-5-sun-god-nika-figurine": ["luffy", "gear", "5", "nika"],
    "akatsuki-premium-hoodie": ["akatsuki", "hoodie"],
    "zoro-s-wado-ichimonji": ["wado", "ichimonji"],
    "goku-ultra-instinct-figure": ["goku", "ultra", "instinct"],
    "itachi-uchiha-ring": ["itachi", "ring"],
    "attack-on-titan-poster-a3": ["attack", "titan", "poster"],
    "deadpool-keychain": ["deadpool", "keychain"],
    "bugatti-chiron-alloy-model-1-24": ["bugatti", "chiron"],
    "porsche-911-gt3-alloy-model-1-24": ["porsche", "911"],
    "mercedes-benz-g63-alloy-model-1-24": ["g63"],
    "batman-dark-knight-alloy-figure": ["batman"],
    "iron-man-mark-85-figure": ["iron", "man"],
    "harry-potter-golden-snitch-necklace": ["golden", "snitch"],
    "demon-slayer-manga-vol-1": ["demon", "slayer", "manga", "1"],
    "one-piece-manga-box-set-1": ["one", "piece", "manga", "box"],
    "naruto-manga-vol-72": ["naruto", "manga", "72"],
    "attack-on-titan-manga-vol-1": ["attack", "titan", "manga", "1"],
    "akatsuki-cloak-cosplay": ["akatsuki", "cloak"],
    "demon-slayer-tanjiro-haori": ["tanjiro", "haori"],
    "naruto-leaf-village-headband": ["leaf", "village", "headband"],
    "tanjiro-hanafuda-earrings": ["hanafuda", "earring"],
    "anime-jersey": ["jersey"]
}

for existing_id, tokens in existing_keywords.items():
    # Search for the best matching slug in the new database
    best_slug = None
    best_score = 0
    
    for slug, info in generated_db.items():
        slug_clean = slug.lower()
        score = sum(1 for token in tokens if token in slug_clean)
        
        # If all tokens match, this is a strong candidate
        if score == len(tokens) and score > best_score:
            best_score = score
            best_slug = slug
            
    if best_slug:
        mapping_existing_to_slug[existing_id] = best_slug
        slug_to_existing[best_slug] = existing_id
        print(f"Mapped existing ID '{existing_id}' to new slug '{best_slug}'")

# Construct final merged database
final_database = {}

for slug, meta in generated_db.items():
    actual_id = slug_to_existing.get(slug, slug)
    
    # Format properties as JavaScript object notation
    js_obj = "{\n"
    js_obj += f"    name: {repr(meta['name'])},\n"
    if meta['price'] is None:
        js_obj += "    price: null,\n"
    else:
        js_obj += f"    price: {meta['price']},\n"
    js_obj += f"    priceStr: {repr(meta['priceStr'])},\n"
    if meta['originalPriceStr'] is None:
        js_obj += "    originalPriceStr: null,\n"
    else:
        js_obj += f"    originalPriceStr: {repr(meta['originalPriceStr'])},\n"
    js_obj += f"    discount: {repr(meta['discount'])},\n"
    js_obj += f"    series: {repr(meta['series'])},\n"
    js_obj += f"    category: {repr(meta['category'])},\n"
    js_obj += f"    description: {repr(meta['description'])},\n"
    
    # Format images array
    new_images_str = "[\n      " + ",\n      ".join([f"'{img}'" for img in meta["images"]]) + "\n    ]"
    js_obj += f"    images: {new_images_str},\n"
    
    # Format specs array
    new_specs_str = "[\n      " + ",\n      ".join([f"'{spec}'" for spec in meta["specs"]]) + "\n    ]"
    js_obj += f"    specs: {new_specs_str}"
    
    # Add sizes if present
    if "sizes" in meta:
        new_sizes_str = "[\n      " + ",\n      ".join([f"'{s}'" for s in meta["sizes"]]) + "\n    ]"
        js_obj += f",\n    sizes: {new_sizes_str}"
        
    # Add colors if present
    if "colors" in meta:
        new_colors_str = "[\n      " + ",\n      ".join([f"'{c}'" for c in meta["colors"]]) + "\n    ]"
        js_obj += f",\n    colors: {new_colors_str}"
        
    js_obj += "\n  }"
    
    final_database[actual_id] = js_obj

# For existing products that did NOT get mapped, keep them exactly as they were
for orig_id, orig_text in original_products.items():
    if orig_id not in final_database:
        final_database[orig_id] = orig_text

# Construct the window.productsDB text block
new_db_text = "window.productsDB = {\n"
for idx, (p_id, p_text) in enumerate(sorted(final_database.items())):
    comma = "," if idx < len(final_database) - 1 else ""
    new_db_text += f"  '{p_id}': {p_text}{comma}\n"
new_db_text += "};"

# Replace block in main.js
new_js_content = js_content[:db_match.start()] + new_db_text + js_content[end_idx:]

with open(main_path, "w") as f:
    f.write(new_js_content)

print(f"Successfully merged databases! Total products in main.js: {len(final_database)}")
