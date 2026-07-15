import os
import json
import numpy as np
from PIL import Image

base_path = "/Users/mac/Desktop/Websites /GITkaizoku/img/Sorted"

def get_grid_features(image_path, grid_size=4):
    try:
        with Image.open(image_path) as img:
            img = img.convert('RGB').resize((128, 128))
            w, h = img.size
            cell_w, cell_h = w // grid_size, h // grid_size
            features = []
            for r in range(grid_size):
                for c in range(grid_size):
                    box = (c * cell_w, r * cell_h, (c + 1) * cell_w, (r + 1) * cell_h)
                    cell = img.crop(box)
                    arr = np.array(cell)
                    mean_color = arr.mean(axis=(0, 1)) / 255.0
                    features.extend(mean_color)
            return np.array(features)
    except Exception as e:
        return None

def cluster_folder(folder_path, threshold=0.45):
    files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.heic', '.webp'))])
    if not files:
        return []
    
    features = {}
    for f in files:
        feat = get_grid_features(os.path.join(folder_path, f))
        if feat is not None:
            features[f] = feat
            
    n = len(features)
    keys = list(features.keys())
    visited = {k: False for k in keys}
    groups = []
    
    # We will use a simple single-linkage clustering
    for i in range(n):
        k_i = keys[i]
        if visited[k_i]:
            continue
        group = [k_i]
        visited[k_i] = True
        
        # Grow the cluster
        to_check = [k_i]
        while to_check:
            current = to_check.pop(0)
            for j in range(n):
                k_j = keys[j]
                if visited[k_j]:
                    continue
                dist = np.linalg.norm(features[current] - features[k_j])
                if dist < threshold:
                    group.append(k_j)
                    visited[k_j] = True
                    to_check.append(k_j)
        groups.append(group)
        
    return groups

# Find all leaf directories
leaf_dirs = []
for root, dirs, files in os.walk(base_path):
    valid_files = [f for f in files if not f.startswith('.') and f.lower().endswith(('.jpg', '.jpeg', '.png', '.heic', '.webp'))]
    if valid_files and not dirs:
        leaf_dirs.append(root)

print(f"Found {len(leaf_dirs)} leaf directories with images.")

clustered_results = {}
for l_dir in sorted(leaf_dirs):
    rel_path = os.path.relpath(l_dir, base_path)
    print(f"Clustering {rel_path}...")
    groups = cluster_folder(l_dir, threshold=0.55)  # Using 0.55 threshold for flexible grouping
    clustered_results[rel_path] = groups
    print(f"  Found {len(groups)} groups.")

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/clustered_products.json", "w") as f:
    json.dump(clustered_results, f, indent=2)

print("Clustering complete! Saved to scratch/clustered_products.json")
