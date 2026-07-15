import os
import json
import shutil
import re

base_path = "/Users/mac/Desktop/Websites /GITkaizoku/img/Sorted"
dest_base = "/Users/mac/Desktop/Websites /GITkaizoku/img/products"

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/grouped_products.json") as f:
    grouped_products = json.load(f)

# Helper function to create clean slugs
def clean_slug(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return text.strip('-')

product_mapping = {}
total_copied = 0

for folder, groups in sorted(grouped_products.items()):
    # Get a clean prefix based on folder path
    # e.g., "Tshirts/Attack On Titan Tshirts" -> "aot-tshirt"
    parts = folder.split('/')
    category = parts[0].lower()
    series = parts[1].lower() if len(parts) > 1 else ""
    
    # Heuristics to clean up series/category prefix
    prefix = ""
    if "tshirts" in category or "tshirts" in series:
        prefix = "tshirt"
    elif "action figures" in category or "figures" in series:
        prefix = "figure"
    elif "hoodies" in category or "hoodies" in series:
        prefix = "hoodie"
    elif "keychains" in category or "keychain" in series:
        prefix = "keychain"
    elif "necklaces" in category or "necklace" in series:
        prefix = "necklace"
    elif "stickers" in category or "stickers" in series:
        prefix = "sticker"
    elif "tote bags" in category:
        prefix = "tote-bag"
    elif "vests" in category:
        prefix = "vest"
    elif "alloy" in category:
        prefix = "alloy-car"
    else:
        prefix = clean_slug(parts[-1])
        
    # Add series if applicable
    series_slug = ""
    if "attack on titan" in series or "aot" in series:
        series_slug = "aot"
    elif "bleach" in series:
        series_slug = "bleach"
    elif "demon slayer" in series or "demonslayer" in series or "slayaer" in series:
        series_slug = "demon-slayer"
    elif "naruto" in series:
        series_slug = "naruto"
    elif "one piece" in series:
        series_slug = "one-piece"
    elif "jujutsu kaisen" in series or "jjk" in series:
        series_slug = "jjk"
    elif "solo leveling" in series:
        series_slug = "solo-leveling"
    elif "invincible" in series:
        series_slug = "invincible"
    elif "breaking bad" in series:
        series_slug = "breaking-bad"
    elif "game of thrones" in series or "got" in series:
        series_slug = "got"
    elif "stranger things" in series:
        series_slug = "stranger-things"
    elif "marvel" in series:
        series_slug = "marvel"
    elif "dc" in series:
        series_slug = "dc"
        
    full_prefix = f"{series_slug}-{prefix}" if series_slug else prefix
    full_prefix = clean_slug(full_prefix)
    
    for idx, group in enumerate(groups):
        product_slug = f"{full_prefix}-{idx+1}"
        product_mapping[product_slug] = {
            "category": category,
            "series": parts[1] if len(parts) > 1 else "",
            "folder": folder,
            "original_images": group,
            "product_images": []
        }
        
        # Create destination directory
        dest_dir = os.path.join(dest_base, product_slug)
        os.makedirs(dest_dir, exist_ok=True)
        
        # Select up to 5 representative images
        selected_images = group[:5]
        for img_idx, img_name in enumerate(selected_images):
            src_file = os.path.join(base_path, folder, img_name)
            ext = os.path.splitext(img_name)[1].lower()
            if not ext:
                ext = ".jpg"
            dest_filename = f"{product_slug}_{img_idx+1:02d}{ext}"
            dest_file = os.path.join(dest_dir, dest_filename)
            
            # Copy file
            shutil.copy2(src_file, dest_file)
            product_mapping[product_slug]["product_images"].append(f"img/products/{product_slug}/{dest_filename}")
            total_copied += 1

print(f"Organized {len(product_mapping)} products and copied {total_copied} images.")

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/product_image_mapping.json", "w") as f:
    json.dump(product_mapping, f, indent=2)

print("Saved mapping to scratch/product_image_mapping.json")
