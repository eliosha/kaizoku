import os
import shutil

products_dir = "/Users/mac/Desktop/Websites /GITkaizoku/img/products"
keep_dirs = {"Anime Merch", "anime-jersys"}

deleted = []
kept = []

for item in os.listdir(products_dir):
    item_path = os.path.join(products_dir, item)
    if os.path.isdir(item_path):
        if item in keep_dirs:
            kept.append(item)
        else:
            shutil.rmtree(item_path)
            deleted.append(item)
    else:
        # Keep flat files in products_dir if any
        kept.append(item)

print(f"Kept: {kept}")
print(f"Deleted {len(deleted)} folders.")
