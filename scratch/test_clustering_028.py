import os
import numpy as np
from PIL import Image

base_path = "/Users/mac/Desktop/Websites /GITkaizoku/img/Sorted"

def get_fast_features(image_path):
    try:
        with Image.open(image_path) as img:
            img = img.convert('L').resize((32, 32), Image.Resampling.BILINEAR)
            arr = np.array(img, dtype=float) / 255.0
            return arr.flatten()
    except Exception as e:
        return None

def cluster_folder(folder_path, threshold=0.28):
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
        
        to_check = [k_i]
        while to_check:
            current = to_check.pop(0)
            for j in range(n):
                k_j = keys[j]
                if visited[k_j]:
                    continue
                dist = np.linalg.norm(features[current] - features[k_j]) / 32.0
                if dist < threshold:
                    group.append(k_j)
                    visited[k_j] = True
                    to_check.append(k_j)
        groups.append(group)
        
    return groups

target_folders = [
    "Tshirts/Bleach Tshirts",
    "Tshirts/Attack On Titan Tshirts",
    "Tshirts/Solo Leveling Tshirts",
    "Tshirts/Demon Slayer Tshirts",
    "Tshirts/Naruto Tshirts"
]

print("Grouping with threshold=0.28:")
for folder in target_folders:
    full_path = os.path.join(base_path, folder)
    if os.path.exists(full_path):
        groups = cluster_folder(full_path, threshold=0.28)
        print(f"  {folder}: {len(groups)} groups")
        for idx, g in enumerate(groups):
            print(f"    Group {idx+1}: {g}")
        print("-" * 50)
