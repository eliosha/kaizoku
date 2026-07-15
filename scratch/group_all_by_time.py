import os
import json
import time

base_path = "/Users/mac/Desktop/Websites /GITkaizoku/img/Sorted"

def group_folder_by_time(folder_path, max_gap_seconds=180):
    # Get all valid image files (skip HEIC to avoid Pillow issues)
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')) and not f.startswith('.')]
    if not files:
        return []
    
    file_times = []
    for f in files:
        f_path = os.path.join(folder_path, f)
        mtime = os.path.getmtime(f_path)
        file_times.append((f, mtime))
        
    # Sort by mtime
    file_times.sort(key=lambda x: x[1])
    
    groups = []
    current_group = []
    last_time = None
    
    for f, t in file_times:
        if last_time is None:
            current_group.append(f)
        elif t - last_time < max_gap_seconds:
            current_group.append(f)
        else:
            groups.append(current_group)
            current_group = [f]
        last_time = t
        
    if current_group:
        groups.append(current_group)
        
    return groups

# Find all leaf folders
leaf_folders = []
for root, dirs, files in os.walk(base_path):
    valid_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')) and not f.startswith('.')]
    if valid_files and not dirs:
        leaf_folders.append(root)

grouped_catalog = {}
total_products = 0

for folder in sorted(leaf_folders):
    rel_path = os.path.relpath(folder, base_path)
    groups = group_folder_by_time(folder)
    if groups:
        grouped_catalog[rel_path] = groups
        total_products += len(groups)

print(f"Grouped {len(leaf_folders)} folders into {total_products} products.")

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/grouped_products.json", "w") as f:
    json.dump(grouped_catalog, f, indent=2)

print("Saved grouped products to scratch/grouped_products.json")
