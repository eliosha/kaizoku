import os
import json
import re

base_path = "/Users/mac/Desktop/Websites /GITkaizoku/img/Sorted"

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/new_sorted_tree.json") as f:
    tree = json.load(f)

# Classification list
folder_products = []
file_products = []

for rel_path, content in sorted(tree.items()):
    if rel_path == "root":
        continue
    
    # Check if this folder has subdirectories
    has_subdirs = len(content["dirs"]) > 0
    
    if content["files"]:
        if not has_subdirs:
            # Leaf directory -> Folder is the product!
            folder_products.append({
                "path": rel_path,
                "files": content["files"]
            })
        else:
            # Intermediate directory -> Each file is a separate product!
            for f in content["files"]:
                file_products.append({
                    "path": os.path.join(rel_path, f),
                    "filename": f
                })

print(f"Total folder products: {len(folder_products)}")
print(f"Total file products: {len(file_products)}")

# Look for Spiderman
print("\nSpiderman check:")
for fp in folder_products:
    if "spider" in fp["path"].lower():
        print(f"Folder product: {fp['path']} -> Files: {fp['files']}")
for fp in file_products:
    if "spider" in fp["path"].lower():
        print(f"File product: {fp['path']}")

# Look for Vests
print("\nVests check:")
for fp in folder_products:
    if "vest" in fp["path"].lower():
        print(f"Folder product: {fp['path']} -> Files: {fp['files']}")
for fp in file_products:
    if "vest" in fp["path"].lower():
        print(f"File product: {fp['path']}")
        
# Look for Dual Dagger
print("\nDual Dagger check:")
for fp in folder_products:
    if "dagger" in fp["path"].lower():
        print(f"Folder product: {fp['path']} -> Files: {fp['files']}")
