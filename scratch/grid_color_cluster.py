import os
import numpy as np
from PIL import Image

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
                    mean_color = arr.mean(axis=(0, 1)) / 255.0  # normalize to 0-1
                    features.extend(mean_color)
            return np.array(features)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def cluster_images(folder_path, threshold=0.3):
    files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.heic', '.webp'))])
    features = {}
    for f in files:
        feat = get_grid_features(os.path.join(folder_path, f))
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
        
        for j in range(i + 1, n):
            k_j = keys[j]
            if visited[k_j]:
                continue
            # Euclidean distance
            dist = np.linalg.norm(features[k_i] - features[k_j])
            if dist < threshold:
                group.append(k_j)
                visited[k_j] = True
        groups.append(group)
        
    return groups, features

path = "/Users/mac/Desktop/Websites /GITkaizoku/img/Sorted/Tshirts/Solo Leveling Tshirts"
groups, features = cluster_images(path, threshold=0.35)
print(f"Clustered into {len(groups)} groups:")
for idx, group in enumerate(groups):
    print(f"  Group {idx + 1}: {group}")
