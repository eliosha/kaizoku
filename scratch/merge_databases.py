import json
import re
import os
import shutil

main_path = "/Users/mac/Desktop/Websites /GITkaizoku/main.js"

# 1. Load visual matches from task-417 output:
# Sorted: Hats/photo_2026-02-04_23-23-55.jpg matches products/photo_2026-02-04_23-23-55.jpg (dist=0.0000)
# Sorted: Tote Bags/IMG_0406.JPG matches products/photo_2026-02-04_23-21-58.jpg (dist=0.0000)
# Sorted: Action Figures/DanDaDan Action Figures/photo_2026-04-13_16-42-02.jpg matches products/dandanda-figure.jpg (dist=0.0000)
# Sorted: Action Figures/Naruto Action Figures/photo_2026-06-01 01.46.54.jpeg matches products/naruto-figure.jpg (dist=0.0000)
# Sorted: Action Figures/Naruto Action Figures/photo_2026-04-13_16-42-00.jpg matches products/naruto-figure1.jpg (dist=0.0000)
# Sorted: Action Figures/Naruto Action Figures/photo_2026-04-13_16-42-21.jpg matches products/naruto-figure3.jpg (dist=0.0000)
# Sorted: Action Figures/Bleach Action Figures/photo_2026-04-13_16-42-25.jpg matches products/photo_2026-02-04_23-16-15.jpg (dist=0.0000)
# Sorted: Katana/photo_2026-02-09_09-10-39.jpg matches products/photo_2025-06-12_07-32-55.jpg (dist=0.0000)
# Sorted: Rings/IMG_0399.JPG matches products/photo_2025-06-26_13-42-54.jpg (dist=0.0000)
# Sorted: Rings/photo_2026-02-04_23-17-11.jpg matches products/rings.jpg (dist=0.0000)
# Sorted: Tshirts/Solo Leveling Tshirts/IMG_6562.JPG matches products/sololeveling-shirt1.jpg (dist=0.1942)
# Sorted: Tshirts/All/IMG_7470.jpg matches products/shirts.jpg (dist=0.2252)

visual_matches = {
    "Hats/photo_2026-02-04_23-23-55.jpg": "deadpool-keychain",  # Phantom Troupe Cap
    "Tote Bags/IMG_0406.JPG": "jjk-nobara-tote-bag",
    "Action Figures/DanDaDan Action Figures/photo_2026-04-13_16-42-02.jpg": "iron-man-mark-85-figure",
    "Action Figures/Naruto Action Figures/photo_2026-06-01 01.46.54.jpeg": "akaza-figurine", # or other figure
    "Action Figures/Naruto Action Figures/photo_2026-04-13_16-42-00.jpg": "akaza-figurine-demon-slayer-infinity-castle",
    "Action Figures/Naruto Action Figures/photo_2026-04-13_16-42-21.jpg": "batman-dark-knight-alloy-figure",
    "Action Figures/Bleach Action Figures/photo_2026-04-13_16-42-25.jpg": "armored-titan-figurine",
    "Katana/photo_2026-02-09_09-10-39.jpg": "zoro-s-wado-ichimonji",
    "Rings/IMG_0399.JPG": "itachi-uchiha-ring",
    "Rings/photo_2026-02-04_23-17-11.jpg": "akatsuki-rings-red-and-white",
    "Tshirts/Solo Leveling Tshirts/IMG_6562.JPG": "anime-jersey",  # Solo Leveling Shirt
    "Tshirts/All/IMG_7470.jpg": "demon-slayer-tanjiro-haori"
}

# 2. Load the mapping and generated metadata
with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/product_image_mapping.json") as f:
    img_mapping = json.load(f)

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/product_metadata.json") as f:
    generated_metadata = json.load(f)

# Find which group contains each matched image and rename its ID
rename_map = {}
for slug, info in img_mapping.items():
    orig_imgs = info["original_images"]
    folder = info["folder"]
    for img in orig_imgs:
        key = f"{folder}/{img}"
        if key in visual_matches:
            target_id = visual_matches[key]
            rename_map[slug] = target_id
            print(f"Mapping group '{slug}' to existing product ID '{target_id}'")
            break

# 3. Read main.js content
with open(main_path) as f:
    js_content = f.read()

# We need to extract the existing database block and update it
# Let's read products DB as a python dict structure using Javascript parser or regex.
# Actually, since we want to overwrite main.js with a clean merged database, let's write a python script to merge them.
# Let's extract the JS productsDB code block first.
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

# Keep the original JS text of productsDB
original_db_text = js_content[start_idx:end_idx]

# Let's parse all fields of original productsDB in python using regex
# We want to match: 'id': { ... }
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
    
    # Store block text
    original_products[prod_id] = block_text

# Overwrite original images lists for matched products
# For each renamed slug, update the generated metadata to have that ID, and replace the images array in original products
final_database = {}

# Merge the generated products:
for slug, meta in generated_metadata.items():
    actual_id = rename_map.get(slug, slug)
    meta["id"] = actual_id
    
    # If it is an existing product, merge it with the original details
    if actual_id in original_products:
        orig_text = original_products[actual_id]
        
        # Replace the images array inside the original JS block text!
        # Find images: [ ... ]
        new_images_str = "images: [\n      " + ",\n      ".join([f"'{img}'" for img in meta["images"]]) + "\n    ]"
        updated_text = re.sub(r"images\s*:\s*\[.*?\]", new_images_str, orig_text, flags=re.DOTALL)
        
        # Also clean up double-escapes if any
        final_database[actual_id] = updated_text
    else:
        # It's a new product! Let's format it as clean Javascript object notation
        js_obj = "{\n"
        js_obj += f"    name: {repr(meta['name'])},\n"
        js_obj += f"    price: {meta['price']},\n"
        js_obj += f"    priceStr: {repr(meta['priceStr'])},\n"
        js_obj += f"    originalPriceStr: {repr(meta['originalPriceStr'])},\n"
        js_obj += f"    discount: {repr(meta['discount'])},\n"
        js_obj += f"    series: {repr(meta['series'])},\n"
        js_obj += f"    category: {repr(meta['category'])},\n"
        js_obj += f"    description: {repr(meta['description'])},\n"
        
        new_images_str = "[\n      " + ",\n      ".join([f"'{img}'" for img in meta["images"]]) + "\n    ]"
        js_obj += f"    images: {new_images_str},\n"
        
        new_specs_str = "[\n      " + ",\n      ".join([f"'{spec}'" for spec in meta["specs"]]) + "\n    ]"
        js_obj += f"    specs: {new_specs_str}\n"
        js_obj += "  }"
        
        final_database[actual_id] = js_obj

# For existing products that did NOT get matched, keep them exactly as they were!
for orig_id, orig_text in original_products.items():
    if orig_id not in final_database:
        final_database[orig_id] = orig_text

# Now construct the new window.productsDB text block
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
