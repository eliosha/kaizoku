import os
import numpy as np
from PIL import Image

sorted_path = "/Users/mac/Desktop/Websites /GITkaizoku/img/Sorted"
products_path = "/Users/mac/Desktop/Websites /GITkaizoku/img/products/Anime Merch"

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
    except Exception:
        return None

# Load product features
prod_features = {}
for f in os.listdir(products_path):
    if f.startswith('.'):
        continue
    f_path = os.path.join(products_path, f)
    if os.path.isfile(f_path):
        feat = get_grid_features(f_path)
        if feat is not None:
            prod_features[f] = feat

print(f"Loaded {len(prod_features)} product template images.")

# Match against Sorted
matches = []
for root, dirs, files in os.walk(sorted_path):
    for f in files:
        if f.startswith('.') or not f.lower().endswith(('.jpg', '.jpeg', '.png', '.heic', '.webp')):
            continue
        f_path = os.path.join(root, f)
        feat = get_grid_features(f_path)
        if feat is None:
            continue
        
        # Compare with all templates
        best_match = None
        min_dist = 999.0
        for p_name, p_feat in prod_features.items():
            dist = np.linalg.norm(feat - p_feat)
            if dist < min_dist:
                min_dist = dist
                best_match = p_name
                
        # If distance is very small, we have a match!
        if min_dist < 0.25:  # tuned threshold for near identity
            rel_path = os.path.relpath(f_path, sorted_path)
            matches.append((rel_path, best_match, min_dist))

print(f"Found {len(matches)} visual matches:")
for m in sorted(matches, key=lambda x: x[2]):
    print(f"  Sorted: {m[0]} matches products/{m[1]} (dist={m[2]:.4f})")
