import os
from PIL import Image

sorted_path = "/Users/mac/Desktop/Websites /GITkaizoku/img/Sorted"
products_path = "/Users/mac/Desktop/Websites /GITkaizoku/img/products/Anime Merch"

# Collect all files in products/Anime Merch
prod_files = {}
for f in os.listdir(products_path):
    if f.startswith('.'):
        continue
    f_path = os.path.join(products_path, f)
    if os.path.isfile(f_path):
        try:
            with Image.open(f_path) as img:
                prod_files[f] = {
                    "size": os.path.getsize(f_path),
                    "res": img.size
                }
        except Exception:
            prod_files[f] = {
                "size": os.path.getsize(f_path),
                "res": None
            }

# Collect all files in Sorted/
sorted_files = {}
for root, dirs, files in os.walk(sorted_path):
    for f in files:
        if f.startswith('.'):
            continue
        f_path = os.path.join(root, f)
        rel_path = os.path.relpath(f_path, sorted_path)
        try:
            with Image.open(f_path) as img:
                sorted_files[rel_path] = {
                    "filename": f,
                    "size": os.path.getsize(f_path),
                    "res": img.size
                }
        except Exception:
            sorted_files[rel_path] = {
                "filename": f,
                "size": os.path.getsize(f_path),
                "res": None
            }

# Find direct filename matches
name_matches = []
size_matches = []

for rel_path, meta in sorted_files.items():
    fn = meta["filename"]
    if fn in prod_files:
        name_matches.append((rel_path, fn))
        if meta["size"] == prod_files[fn]["size"]:
            size_matches.append((rel_path, fn))

print(f"Total filename matches: {len(name_matches)}")
for m in name_matches[:10]:
    print(f"  {m[0]} matches products/{m[1]}")

print(f"Total exact size/filename matches: {len(size_matches)}")
