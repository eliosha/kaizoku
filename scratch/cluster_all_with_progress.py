import os
import json
import time
import numpy as np
from PIL import Image

base_path = "/Users/mac/Desktop/Websites /GITkaizoku/img/Sorted"

def get_fast_features(image_path):
    try:
        with Image.open(image_path) as img:
            # Resize to 32x32 and convert to grayscale to make it extremely fast
            img = img.convert('L').resize((32, 32), Image.Resampling.BILINEAR)
            arr = np.array(img, dtype=float) / 255.0
            return arr.flatten()
    except Exception as e:
        return None

def cluster_folder(folder_path, threshold=0.35):
    files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.heic', '.webp'))])
    if not files:
        return []
    
    features = {}
    for f in files:
        feat = get_fast_features(os.path.join(folder_path, f))
        if feat is not None:
            features[f] = feat
            
    n = len(features)
    keys = list(features.keys())
    visited = {k: False for k in keys}
    groups = []
    
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
                # normalized Euclidean distance
                dist = np.linalg.norm(features[current] - features[k_j]) / 32.0  # normalize by sqrt(1024)
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
start_time = time.time()
for idx, l_dir in enumerate(sorted(leaf_dirs)):
    rel_path = os.path.relpath(l_dir, base_path)
    print(f"[{idx+1}/{len(leaf_dirs)}] Clustering {rel_path}...")
    groups = cluster_folder(l_dir, threshold=0.15)  # optimized threshold for normalized distance
    clustered_results[rel_path] = groups
    print(f"  Found {len(groups)} groups in {rel_path}.")

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/clustered_products.json", "w") as f:
    json.dump(clustered_results, f, indent=2)

print(f"Clustering complete in {time.time() - start_time:.2f} seconds! Saved to scratch/clustered_products.json")
