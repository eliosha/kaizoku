import os
import json
import re

base_path = "/Users/mac/Desktop/Websites /GITkaizoku/img/Sorted"

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/new_sorted_tree.json") as f:
    tree = json.load(f)

# We want to identify:
# 1. Product groups that are defined by folders (directories containing files but no subdirs, or explicitly named)
# 2. Product groups defined by loose files (directly under category folders or folders that contain both)
# 3. Merging color variants of the same product (e.g. Black/White folders or files)

# Let's list all files in Sorted/ with their folder relative paths
all_leaf_products = {}
loose_products = {}

# Keep track of categories
categories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]

print(f"Categories: {categories}")

# Traverse tree to extract raw folder-based products and file-based products
folder_products = []
file_products = []

for rel_path, content in sorted(tree.items()):
    if rel_path == "root":
        continue
    
    parts = rel_path.split('/')
    category = parts[0]
    
    # If the folder has files:
    if content["files"]:
        # If it has NO subdirs, it is a leaf folder representing a product (or a category folder containing loose files)
        # Wait, how to distinguish?
        # If it's a deep folder (len(parts) > 1), and there are no subdirs, it's a product folder!
        # E.g. "Tshirts/Solo Leveling Tshirts/Black Shadow Monarch Long-Sleeve T-shirt"
        # What about "Necklaces/Naruto Necklaces" which has subdirs AND files?
        # The files inside are loose products (single-image).
        # What if it's a folder like "Hoodies/Stranger Things Hoodies" (no subdirs, has files)?
        # Does it represent a single product "Stranger Things Hoodie" with multiple files?
        # Or does it contain 3 separate files that are different hoodies?
        # Let's check files inside "Hoodies/Stranger Things Hoodies":
        # Let's see: if the filenames are generic (e.g. IMG_xxxx), it's likely different angles of the same product.
        # If the filenames are descriptive (e.g. "Tanjiro Kamado black hoodie.JPG"), then each descriptive file is a separate product!
        # This is a very important heuristic:
        # - If a file has a descriptive name (contains letters, spaces, etc.), it represents a product where the name is the filename.
        # - If files have camera names (like IMG_xxxx.jpg, photo_xxxx.jpg), they are different angles of the folder product.
        
        has_subdirs = len(content["dirs"]) > 0
        
        if has_subdirs:
            # Files in this directory are loose products!
            for f in content["files"]:
                file_products.append({
                    "category": category,
                    "rel_dir": rel_path,
                    "filename": f,
                    "filepath": os.path.join(rel_path, f)
                })
        else:
            # No subdirectories. Is the folder itself a product, or are the files separate products?
            # Let's check filenames:
            descriptive_files = []
            camera_files = []
            for f in content["files"]:
                name_without_ext = os.path.splitext(f)[0]
                # If name is mostly numbers or starts with photo_ / IMG_, it's a camera file
                if re.match(r'^(img_|img|photo_|photo|dscf|dsc|_dsc|image|pic|\d+)[_\-\s]*\d+', name_without_ext.lower()) or name_without_ext.isdigit():
                    camera_files.append(f)
                else:
                    descriptive_files.append(f)
                    
            if len(descriptive_files) > 0 and len(camera_files) == 0:
                # Every descriptive file is a separate product!
                for f in content["files"]:
                    file_products.append({
                        "category": category,
                        "rel_dir": rel_path,
                        "filename": f,
                        "filepath": os.path.join(rel_path, f)
                    })
            else:
                # The folder is the product!
                folder_products.append({
                    "category": category,
                    "rel_dir": rel_path,
                    "files": content["files"]
                })

print(f"Extracted {len(folder_products)} folder products and {len(file_products)} file products.")

# Let's write the raw extraction to JSON for inspection
with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/raw_extracted_products.json", "w") as f:
    json.dump({"folders": folder_products, "files": file_products}, f, indent=2)
