import os
import json
import shutil
import re

base_path = "/Users/mac/Desktop/Websites /GITkaizoku/img/Sorted"
dest_base = "/Users/mac/Desktop/Websites /GITkaizoku/img/products"

COLOR_KEYWORDS = {
    "black": "Black",
    "white": "White",
    "blue": "Blue",
    "yellow": "Yellow",
    "grey": "Grey",
    "gray": "Grey",
    "green": "Green",
    "red": "Red",
    "orange": "Orange",
    "peach": "Peach",
    "pink": "Pink",
    "purple": "Purple",
    "gold": "Gold",
    "silver": "Silver",
    "sliver": "Silver",  # Match common typo on disk
    "brown": "Brown",
    "tan": "Tan",
    "beige": "Beige",
    "cream": "Cream"
}

def clean_slug(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return text.strip('-')

def is_camera_filename(filename):
    name_without_ext = os.path.splitext(filename)[0]
    name_lower = name_without_ext.lower()
    if re.match(r'^_*(img|photo|dscf|dsc|image|pic|screenshot|screen|\d+)[_a-zA-Z]*\d+', name_lower):
        return True
    if name_lower.isdigit():
        return True
    return False

def detect_color_from_name(name):
    name_lower = name.lower()
    for kw, label in COLOR_KEYWORDS.items():
        if re.search(r'\b' + re.escape(kw) + r'\b', name_lower):
            return label
    return None

def map_category(folder_slug):
    f_lower = folder_slug.lower()
    if "action figure" in f_lower:
        return "figurines"
    elif "alloy" in f_lower:
        return "alloy-collectibles"
    elif "tshirt" in f_lower:
        return "clothing"
    elif "hoodie" in f_lower:
        return "clothing"
    elif "vest" in f_lower:
        return "clothing"
    elif "shorts" in f_lower:
        return "clothing"
    elif "socks" in f_lower:
        return "clothing"
    elif "hat" in f_lower or "buckethat" in f_lower:
        # Move headwear to accessories to align with header dropdown
        return "accessories"
    elif "keychain" in f_lower:
        # Move keychains to jewelry to align with header dropdown
        return "jewelry"
    elif "sticker" in f_lower:
        # Move stickers to decor to align with header dropdown
        return "decor"
    elif "plush" in f_lower:
        # Move plushies to collectibles
        return "collectibles"
    elif "necklace" in f_lower:
        return "jewelry"
    elif "earring" in f_lower:
        return "jewelry"
    elif "ring" in f_lower:
        return "jewelry"
    elif "bracelet" in f_lower:
        return "jewelry"
    elif "tote bag" in f_lower or "tote-bag" in f_lower:
        return "accessories"
    elif "wallet" in f_lower:
        return "accessories"
    elif "poster" in f_lower:
        return "decor"
    elif "manga" in f_lower or "comic" in f_lower:
        return "manga"
    elif "katana" in f_lower:
        return "cosplay-kits"
    return "accessories"

def get_default_price(category):
    if category == "clothing":
        return 45000, "UGX 45,000", "UGX 55,000", "18% OFF"
    elif category == "figurines":
        return None, "Contact for Price", None, "Request"
    elif category == "alloy-collectibles":
        return 75000, "UGX 75,000", "UGX 90,000", "17% OFF"
    elif category == "jewelry":
        return 15000, "UGX 15,000", "UGX 20,000", "25% OFF"
    elif category == "collectibles":
        return 50000, "UGX 50,000", "UGX 60,000", "17% OFF"
    elif category == "accessories":
        return 25000, "UGX 25,000", "UGX 30,000", "17% OFF"
    elif category == "decor":
        return 10000, "UGX 10,000", "UGX 15,000", "33% OFF"
    elif category == "manga":
        return 35000, "UGX 35,000", "UGX 40,000", "12% OFF"
    elif category == "cosplay-kits":
        return 120000, "UGX 120,000", "UGX 150,000", "20% OFF"
    return 20000, "UGX 20,000", "UGX 25,000", "20% OFF"

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.tiff', '.bmp', '.jfif', '.heic', '.jpeg'}

# Load new_sorted_tree.json
with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/new_sorted_tree.json") as f:
    tree = json.load(f)

# Extract raw folders and files using the leaf-folder rule
raw_folders = []
raw_files = []

for rel_path, content in sorted(tree.items()):
    if rel_path == "root":
        continue
        
    # Skip duplicate Naruto keychain folder
    if os.path.basename(rel_path).lower() == "multi-charm keychain":
        continue
    
    parts = rel_path.split('/')
    category = parts[0]
    has_subdirs = len(content["dirs"]) > 0
    
    if content["files"]:
        # Filter files by image extensions only
        files_clean = [f for f in content["files"] if os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS]
        if not files_clean:
            continue
            
        if not has_subdirs and len(parts) > 1:
            raw_folders.append({
                "category": category,
                "rel_dir": rel_path,
                "files": files_clean
            })
        else:
            for f in files_clean:
                raw_files.append({
                    "category": category,
                    "rel_dir": rel_path,
                    "filename": f,
                    "filepath": os.path.join(rel_path, f)
                })

# Merge color variants in raw_folders
merged_folders = []
folder_seen = set()

def normalize_name_for_merge(name):
    name_lower = name.lower()
    words_to_strip = list(COLOR_KEYWORDS.keys()) + ["version", "tshirt", "tshirts", "hoodie", "hoodies", "cap", "caps", "hat", "hats", "wallet", "wallets", "tote", "bag", "tote-bag", "tote bag", "series", "edition"]
    for w in words_to_strip:
        name_lower = re.sub(r'\b' + re.escape(w) + r'\b', '', name_lower)
    name_lower = re.sub(r'[^a-z0-9\s]', '', name_lower)
    name_lower = re.sub(r'\s+', ' ', name_lower).strip()
    return name_lower

for i, f1 in enumerate(raw_folders):
    if f1["rel_dir"] in folder_seen:
        continue
    
    base_name = os.path.basename(f1["rel_dir"])
    norm1 = normalize_name_for_merge(base_name)
    color1 = detect_color_from_name(base_name)
    
    current_group = {
        "category": f1["category"],
        "base_name": base_name,
        "dirs": [f1["rel_dir"]],
        "colors": {color1: f1["files"]} if color1 else {"Default": f1["files"]}
    }
    folder_seen.add(f1["rel_dir"])
    
    for j, f2 in enumerate(raw_folders[i+1:]):
        if f2["rel_dir"] in folder_seen or f2["category"] != f1["category"]:
            continue
        
        base_name2 = os.path.basename(f2["rel_dir"])
        norm2 = normalize_name_for_merge(base_name2)
        
        if norm1 == norm2 and norm1 != "":
            color2 = detect_color_from_name(base_name2)
            if color2:
                current_group["dirs"].append(f2["rel_dir"])
                if color2 in current_group["colors"]:
                    current_group["colors"][color2].extend(f2["files"])
                else:
                    current_group["colors"][color2] = f2["files"]
                folder_seen.add(f2["rel_dir"])
                
    merged_folders.append(current_group)

# Merge color variants in raw_files
merged_files = []
file_seen = set()

for i, f1 in enumerate(raw_files):
    filepath1 = f1["filepath"]
    if filepath1 in file_seen:
        continue
        
    name_without_ext = os.path.splitext(f1["filename"])[0]
    norm1 = normalize_name_for_merge(name_without_ext)
    color1 = detect_color_from_name(name_without_ext)
    
    current_group = {
        "category": f1["category"],
        "base_name": name_without_ext,
        "files": [(filepath1, color1 or "Default")]
    }
    file_seen.add(filepath1)
    
    for j, f2 in enumerate(raw_files[i+1:]):
        filepath2 = f2["filepath"]
        if filepath2 in file_seen or f2["category"] != f1["category"]:
            continue
            
        name_without_ext2 = os.path.splitext(f2["filename"])[0]
        norm2 = normalize_name_for_merge(name_without_ext2)
        
        if norm1 == norm2 and norm1 != "":
            color2 = detect_color_from_name(name_without_ext2)
            if color2:
                current_group["files"].append((filepath2, color2))
                file_seen.add(filepath2)
                
    merged_files.append(current_group)

# Process and copy files
products_db = {}
used_slugs = set()

def get_unique_slug(base):
    slug = clean_slug(base)
    if not slug:
        slug = "product"
    candidate = slug
    counter = 1
    while candidate in used_slugs:
        counter += 1
        candidate = f"{slug}-{counter}"
    used_slugs.add(candidate)
    return candidate

def process_product_data(slug, title, category, original_name):
    if is_camera_filename(title):
        num_match = re.search(r'\d+', title)
        num = num_match.group(0) if num_match else "Style"
        folder_leaf = os.path.basename(os.path.dirname(original_name)) if '/' in original_name else category
        title_clean = f"{folder_leaf} - Style {num}"
    else:
        title_clean = title
        
    # Auto-detect series
    series = "Anime"
    name_lower = title_clean.lower() + " " + original_name.lower()
    
    # Check if the path contains Fandom Hub
    if "fandom hub" in original_name.lower() or "fandom" in original_name.lower():
        parts = original_name.split('/')
        # Look for the subfolder right after "Fandom Hub Tshirts" or similar
        try:
            f_idx = -1
            for i, part in enumerate(parts):
                if "fandom" in part.lower():
                    f_idx = i
                    break
            if f_idx != -1 and f_idx + 1 < len(parts):
                series = parts[f_idx+1]
        except Exception:
            pass
            
    # Fallback to keyword matching if not found or if default Anime
    if series == "Anime":
        if "one piece" in name_lower or "luffy" in name_lower or "zoro" in name_lower or "sanji" in name_lower or "chopper" in name_lower or "nami" in name_lower or "ace" in name_lower or "law" in name_lower or "whitebeard" in name_lower or "blackbeard" in name_lower:
            series = "One Piece"
        elif "naruto" in name_lower or "akatsuki" in name_lower or "itachi" in name_lower or "sasuke" in name_lower or "kakashi" in name_lower or "gaara" in name_lower or "madara" in name_lower or "obito" in name_lower or "tobi" in name_lower:
            series = "Naruto"
        elif "demon slayer" in name_lower or "tanjiro" in name_lower or "nezuko" in name_lower or "zenitsu" in name_lower or "inosuke" in name_lower or "akaza" in name_lower or "rengoku" in name_lower or "kamado" in name_lower:
            series = "Demon Slayer"
        elif "attack on titan" in name_lower or "aot" in name_lower or "survey corps" in name_lower or "scout regiment" in name_lower or "erwin" in name_lower or "levi" in name_lower or "eren" in name_lower:
            series = "Attack on Titan"
        elif "dragon ball" in name_lower or "goku" in name_lower or "vegeta" in name_lower or "dbz" in name_lower:
            series = "Dragon Ball"
        elif "solo leveling" in name_lower or "jin-woo" in name_lower or "arise" in name_lower or "monarch" in name_lower:
            series = "Solo Leveling"
        elif "jujutsu kaisen" in name_lower or "jjk" in name_lower or "gojo" in name_lower or "nobara" in name_lower or "satoru" in name_lower or "megumi" in name_lower or "itadori" in name_lower:
            series = "Jujutsu Kaisen"
        elif "breaking bad" in name_lower or "walter" in name_lower or "heisenberg" in name_lower:
            series = "Breaking Bad"
        elif "game of thrones" in name_lower or "targaryen" in name_lower or "stark" in name_lower:
            series = "Game of Thrones"
        elif "stranger things" in name_lower:
            series = "Stranger Things"
        elif "peaky blinders" in name_lower or "shelby" in name_lower:
            series = "Peaky Blinders"
        elif "marvel" in name_lower or "spiderman" in name_lower or "x-men" in name_lower or "deadpool" in name_lower or "wolverine" in name_lower:
            series = "Marvel"
        elif "dc" in name_lower or "joker" in name_lower or "batman" in name_lower or "wonder woman" in name_lower:
            series = "DC"
        elif "one punch man" in name_lower or "saitama" in name_lower:
            series = "One Punch Man"
        elif "hellsing" in name_lower or "alucard" in name_lower:
            series = "Hellsing"
            
    # Normalize series name
    if series.lower() == "marvel":
        series = "Marvel"
    elif series.lower() == "dc":
        series = "DC"
    elif series.lower() == "game of thrones":
        series = "Game of Thrones"
    elif series.lower() == "breaking bad":
        series = "Breaking Bad"
    elif series.lower() == "stranger things":
        series = "Stranger Things"
    elif series.lower() == "peaky blinders":
        series = "Peaky Blinders"
    elif series.lower() == "the godfather":
        series = "The Godfather"
    if series == "Anime" and category == "alloy-collectibles":
        series = "Alloy Collectibles"
        
    title_clean = re.sub(r'\s*\(.*?\)', '', title_clean)
    title_clean = re.sub(r' — .*', '', title_clean)
    title_clean = re.sub(r' (tshirt|t-shirt|hoodie|cap|wallet|tote bag|keychain|necklace|ring|earring|bracelet|sticker|plush|katana|socks)s?$', '', title_clean, flags=re.IGNORECASE)
    
    cat_label = ""
    if category == "clothing":
        if "hoodie" in original_name.lower():
            cat_label = "Hoodie"
        elif "shorts" in original_name.lower():
            cat_label = "Shorts"
        elif "socks" in original_name.lower():
            cat_label = "Socks"
        elif "hat" in original_name.lower() or "cap" in original_name.lower():
            cat_label = "Cap"
        elif "vest" in original_name.lower():
            cat_label = "Vest"
        else:
            cat_label = "Graphic T-Shirt"
    elif category == "figurines":
        # Name them Action Figure so they match the "figure" query parameter
        cat_label = "Action Figure"
    elif category == "alloy-collectibles":
        cat_label = "Alloy Model Car"
    elif category == "jewelry":
        if "necklace" in original_name.lower():
            cat_label = "Necklace"
        elif "earring" in original_name.lower():
            cat_label = "Earrings"
        elif "ring" in original_name.lower():
            cat_label = "Ring"
        elif "keychain" in original_name.lower():
            cat_label = "Keychain"
        else:
            cat_label = "Bracelet"
    elif category == "collectibles":
        if "plush" in original_name.lower():
            cat_label = "Plushie"
        else:
            cat_label = "Collectible"
    elif category == "accessories":
        if "wallet" in original_name.lower():
            cat_label = "Leather Wallet"
        elif "hat" in original_name.lower() or "cap" in original_name.lower():
            cat_label = "Cap"
        else:
            cat_label = "Canvas Tote Bag"
    elif category == "decor":
        if "sticker" in original_name.lower():
            cat_label = "Sticker Pack"
        else:
            cat_label = "A3 Poster"
    elif category == "manga":
        if "comic" in original_name.lower():
            cat_label = "Comic Book"
        else:
            cat_label = "Manga Volume"
    elif category == "cosplay-kits":
        cat_label = "Steel Katana Sword"
    
    if cat_label and cat_label.lower() not in title_clean.lower() and not (cat_label == "Cap" and "hat" in title_clean.lower()):
        title_clean = f"{title_clean} {cat_label}"
        
    title_clean = re.sub(r'\s+', ' ', title_clean).strip()
    title_clean = title_clean.title()
    
    desc_parts = [f"Authentic {series} themed {cat_label or 'merchandise'} featuring premium detailed designs."]
    specs = ["Official design detailing", "Durable construction", "Perfect for collectors and fans"]
    
    if category == "clothing":
        desc_parts.append("Made with ultra-comfortable cotton fabric for standard daily wear and street styling.")
        specs = ["High-density graphic design", "Comfortable fit collar", "Premium stitched seams"]
    elif category == "figurines" or category == "alloy-collectibles":
        desc_parts.append("Exquisite detail representing authentic character modeling or scale dimensions.")
        specs = ["Highly detailed molding", "Matte finish coloring", "Collector display packaging"]
    elif category == "jewelry":
        desc_parts.append("Crafted with durable polished metal accents and secure locking closures.")
        specs = ["Rust-resistant metal alloy", "Embossed emblem detailing", "Adjustable length sizing"]
    elif category == "accessories":
        desc_parts.append("Spacious compartment sizing with sturdy stitched build for everyday durability.")
        specs = ["Heavy duty stitching", "Functional utility compartments", "Premium texture material"]
        
    description = " ".join(desc_parts)
    price, price_str, orig_price_str, discount = get_default_price(category)
    
    return {
        "name": title_clean,
        "price": price,
        "priceStr": price_str,
        "originalPriceStr": orig_price_str,
        "discount": discount,
        "series": series,
        "category": category,
        "description": description,
        "specs": specs
    }

# Process folder products
for idx, gp in enumerate(merged_folders):
    slug = get_unique_slug(gp["base_name"])
    os.makedirs(os.path.join(dest_base, slug), exist_ok=True)
    
    color_images = {}
    
    for raw_color, files in gp["colors"].items():
        for filename in files:
            color_detected = detect_color_from_name(filename) or raw_color
            
            src_file = None
            for d in gp["dirs"]:
                test_path = os.path.join(base_path, d, filename)
                if os.path.isfile(test_path):
                    src_file = test_path
                    break
                    
            if not src_file:
                continue
                
            if color_detected not in color_images:
                color_images[color_detected] = []
            color_images[color_detected].append(src_file)
            
    final_colors = sorted([c for c in color_images.keys() if c != "Default"])
    if not final_colors:
        final_colors = ["Default"]
        
    copied_paths = []
    
    for color in sorted(color_images.keys()):
        files_to_copy = color_images[color][:5]
        color_slug = clean_slug(color)
        
        for file_idx, src_file in enumerate(files_to_copy):
            ext = os.path.splitext(src_file)[1].lower()
            if not ext: ext = ".jpg"
            
            if color == "Default":
                dest_filename = f"{slug}_{file_idx+1:02d}{ext}"
            else:
                dest_filename = f"{slug}_{color_slug}_{file_idx+1:02d}{ext}"
                
            dest_file = os.path.join(dest_base, slug, dest_filename)
            shutil.copy2(src_file, dest_file)
            copied_paths.append(f"img/products/{slug}/{dest_filename}")
            
    cat = map_category(gp["category"])
    prod_data = process_product_data(slug, gp["base_name"], cat, gp["dirs"][0])
    prod_data["images"] = copied_paths
    
    if len(final_colors) > 1 or final_colors[0] != "Default":
        prod_data["colors"] = final_colors
        
    if cat == "clothing" and "socks" not in slug and "hat" not in slug:
        prod_data["sizes"] = ["SM", "MD", "LG", "XL", "2X"]
        
    products_db[slug] = prod_data

# Process file products (loose images)
for idx, gp in enumerate(merged_files):
    slug = get_unique_slug(gp["base_name"])
    os.makedirs(os.path.join(dest_base, slug), exist_ok=True)
    
    copied_paths = []
    colors_list = []
    
    for file_idx, (src_file, color) in enumerate(gp["files"]):
        ext = os.path.splitext(src_file)[1].lower()
        if not ext: ext = ".jpg"
        
        color_slug = clean_slug(color)
        if color == "Default":
            dest_filename = f"{slug}_{file_idx+1:02d}{ext}"
        else:
            dest_filename = f"{slug}_{color_slug}_{file_idx+1:02d}{ext}"
            if color not in colors_list:
                colors_list.append(color)
                
        dest_file = os.path.join(dest_base, slug, dest_filename)
        shutil.copy2(os.path.join(base_path, src_file), dest_file)
        copied_paths.append(f"img/products/{slug}/{dest_filename}")
        
    cat = map_category(gp["category"])
    prod_data = process_product_data(slug, gp["base_name"], cat, gp["files"][0][0])
    prod_data["images"] = copied_paths
    
    if len(colors_list) > 1:
        prod_data["colors"] = sorted(colors_list)
        
    if cat == "clothing" and "socks" not in slug and "hat" not in slug:
        prod_data["sizes"] = ["SM", "MD", "LG", "XL", "2X"]
        
    products_db[slug] = prod_data

print(f"Processed {len(products_db)} total products in catalog.")

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/product_metadata_v2.json", "w") as f:
    json.dump(products_db, f, indent=2)

print("Saved database to scratch/product_metadata_v2.json")
