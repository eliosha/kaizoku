import json
import re

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/product_image_mapping.json") as f:
    mapping = json.load(f)

metadata = {}

# Map category names to GITkaizoku category slugs
def map_category(folder_slug):
    f_lower = folder_slug.lower()
    if "tshirt" in f_lower:
        return "clothing"
    elif "hoodie" in f_lower:
        return "clothing"
    elif "vest" in f_lower:
        return "clothing"
    elif "figure" in f_lower:
        return "collectibles"
    elif "alloy" in f_lower:
        return "collectibles"
    elif "keychain" in f_lower:
        return "gifts"
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
    elif "poster" in f_lower:
        return "decor"
    elif "sticker" in f_lower:
        return "gifts"
    elif "manga" in f_lower:
        return "manga"
    elif "wallet" in f_lower:
        return "accessories"
    elif "shorts" in f_lower:
        return "clothing"
    elif "socks" in f_lower:
        return "clothing"
    elif "hat" in f_lower or "buckethat" in f_lower:
        return "clothing"
    elif "katana" in f_lower:
        return "cosplay-kits"
    return "accessories"

# Set up default prices based on category (approximate UGX values)
def get_default_price(category):
    if category == "clothing":
        return 45000, "UGX 45,000", "UGX 55,000", "18% OFF"
    elif category == "collectibles":
        return 75000, "UGX 75,000", "UGX 90,000", "17% OFF"
    elif category == "jewelry":
        return 15000, "UGX 15,000", "UGX 20,000", "25% OFF"
    elif category == "gifts":
        return 12000, "UGX 12,000", "UGX 15,000", "20% OFF"
    elif category == "accessories":
        return 25000, "UGX 25,000", "UGX 30,000", "17% OFF"
    elif category == "decor":
        return 10000, "UGX 10,000", "UGX 15,000", "33% OFF"
    elif category == "manga":
        return 35000, "UGX 35,000", "UGX 40,000", "12% OFF"
    elif category == "cosplay-kits":
        return 120000, "UGX 120,000", "UGX 150,000", "20% OFF"
    return 20000, "UGX 20,000", "UGX 25,000", "20% OFF"

for slug, info in mapping.items():
    cat = map_category(info["category"] or slug)
    series = info["series"] or ""
    
    # Generate clean Title
    # e.g. "aot-tshirt-1" -> "Attack On Titan Graphic T-Shirt"
    title_words = []
    if series:
        title_words.append(series.title())
    
    # Check item type
    item_type = "Product"
    if "tshirt" in slug:
        item_type = "Graphic T-Shirt"
    elif "hoodie" in slug:
        item_type = "Cosplay Hoodie"
    elif "figure" in slug:
        item_type = "Action Figure Figurine"
    elif "alloy-car" in slug:
        item_type = "Alloy Model Car Collectible"
    elif "keychain" in slug:
        item_type = "Metal Keychain"
    elif "necklace" in slug:
        item_type = "Pendant Necklace"
    elif "ring" in slug:
        item_type = "Cosplay Ring"
    elif "bracelet" in slug:
        item_type = "Braided Bracelet"
    elif "tote-bag" in slug:
        item_type = "Canvas Tote Bag"
    elif "sticker" in slug:
        item_type = "Anime Sticker Pack"
    elif "poster" in slug:
        item_type = "A3 Poster"
    elif "manga" in slug:
        item_type = "Manga Volume"
    elif "wallet" in slug:
        item_type = "Leather Wallet"
    elif "shorts" in slug:
        item_type = "Anime Shorts"
    elif "vest" in slug:
        item_type = "Cosplay Vest"
    elif "katana" in slug:
        item_type = "Steel Katana Sword"
        
    title_words.append(item_type)
    
    # Add index to title if multiple exist
    m = re.search(r'-(\d+)$', slug)
    if m:
        title_words.append(f"Style {m.group(1)}")
        
    title = " ".join(title_words)
    
    # Generate short description based on visible details
    desc_parts = []
    specs = []
    
    if "tshirt" in slug:
        desc_parts.append(f"Premium quality graphic tee featuring a vibrant printed design inspired by {series or 'anime'}.")
        desc_parts.append("Short sleeves and standard crew neck collar make it perfect for casual street fashion.")
        specs = ["Crew neck collar", "Front graphic print design", "Short sleeve styling", "Double-stitched seams"]
    elif "hoodie" in slug:
        desc_parts.append(f"Cosmic anime-themed pullover hoodie featuring {series or 'anime'} detailing.")
        desc_parts.append("Features adjustable drawstrings, front kangaroo pouch pockets, and elastic ribbed cuffs.")
        specs = ["Pullover hood", "Adjustable drawstrings", "Front kangaroo pocket", "Ribbed cuffs and waistband"]
    elif "figure" in slug:
        desc_parts.append(f"Detailed collectible display figure of a character from {series or 'anime'}.")
        desc_parts.append("Includes structured base stand and highly detailed molded textures representing signature outfit details.")
        specs = ["Molded collectible figure", "Display base stand included", "Detailed costume styling", "Matte color finish"]
    elif "keychain" in slug:
        desc_parts.append(f"Premium metal alloy keychain featuring a detailed emblem from {series or 'anime'}.")
        desc_parts.append("Comes with a secure split key ring and lobster clasp hanger attachment.")
        specs = ["Zinc alloy construction", "Split ring and secure clasp", "Double-sided detail design", "Glossy finish"]
    elif "necklace" in slug:
        desc_parts.append(f"Elegant pendant necklace showcasing the signature {series or 'anime'} logo.")
        desc_parts.append("Includes a matching link chain with a secure lobster claw clasp.")
        specs = ["Metal pendant charm", "Link chain link style", "Lobster claw clasp closure", "Silver or gold tone polish"]
    elif "ring" in slug:
        desc_parts.append(f"Engraved metal cosplay ring styled after the iconic symbols in {series or 'anime'}.")
        specs = ["Polished metal band", "Embossed symbol detail", "Compact jewelry box included"]
    elif "bracelet" in slug:
        desc_parts.append(f"Braided faux-leather cord bracelet accented with a polished metal {series or 'anime'} charm.")
        specs = ["Braided synthetic cord", "Metallic accent piece", "Adjustable secure lock"]
    elif "tote-bag" in slug:
        desc_parts.append(f"Eco-friendly canvas tote bag with a high-density print of {series or 'anime'}.")
        desc_parts.append("Large main compartment with thick shoulder strap carrying handles.")
        specs = ["Woven canvas fabric", "Vibrant graphic print front", "Thick dual shoulder handles", "Spacious open top"]
    elif "katana" in slug:
        desc_parts.append(f"Cosplay reproduction katana sword inspired by {series or 'anime'}.")
        desc_parts.append("Features detailed hilt wrapping, textured guard, and a protective matching scabbard.")
        specs = ["Reproduction blade", "Wrapped handle grip hilt", "Ornate matching scabbard included", "Cosplay safe display piece"]
    elif "alloy-car" in slug:
        desc_parts.append("Detailed die-cast alloy metal model car collectible.")
        desc_parts.append("Accurate model design with rubber tires, openable doors, and detailed interior styling.")
        specs = ["Diecast metal body construction", "Rolling rubber tires", "Openable side doors", "Detailed scale interior"]
    else:
        desc_parts.append(f"Premium {series or 'anime'} themed merchandise.")
        desc_parts.append("Designed with high quality materials and authentic detailing.")
        specs = ["Authentic design detailing", "Durable construction", "Perfect for collectors and fans"]

    description = " ".join(desc_parts)
    price, price_str, orig_price_str, discount = get_default_price(cat)
    
    metadata[slug] = {
        "id": slug,
        "name": title,
        "price": price,
        "priceStr": price_str,
        "originalPriceStr": orig_price_str,
        "discount": discount,
        "series": series or "Anime",
        "category": cat,
        "description": description,
        "images": info["product_images"],
        "specs": specs
    }

print(f"Generated metadata for {len(metadata)} products.")

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/product_metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

print("Saved metadata to scratch/product_metadata.json")
