import os
import sys
import numpy as np
from PIL import Image

sorted_path = "/Users/mac/Desktop/Websites /GITkaizoku/img/Sorted"
products_path = "/Users/mac/Desktop/Websites /GITkaizoku/img/products/Anime Merch"

def get_grid_features(image_path, size=32):
    try:
        with Image.open(image_path) as img:
            img = img.convert('RGB').resize((size, size), Image.Resampling.BILINEAR)
            arr = np.array(img, dtype=float) / 255.0
            return arr.flatten()
    except Exception:
        return None

# Load all images in Sorted
sorted_images = []
for root, dirs, files in os.walk(sorted_path):
    for f in files:
        if f.startswith('.') or not f.lower().endswith(('.jpg', '.jpeg', '.png', '.heic', '.webp')):
            continue
        f_path = os.path.join(root, f)
        feat = get_grid_features(f_path)
        if feat is not None:
            rel_path = os.path.relpath(f_path, sorted_path)
            sorted_images.append((rel_path, feat))

print(f"Loaded {len(sorted_images)} images from Sorted.")
sys.stdout.flush()

# For each product template, find top 3 matches
for f in sorted(os.listdir(products_path)):
    if f.startswith('.') or f.lower().endswith('.png') and os.path.getsize(os.path.join(products_path, f)) > 5 * 1024 * 1024:
        continue
    f_path = os.path.join(products_path, f)
    if not os.path.isfile(f_path):
        continue
        
    feat = get_grid_features(f_path)
    if feat is None:
        continue
        
    dists = []
    for rel_path, s_feat in sorted_images:
        dist = np.linalg.norm(feat - s_feat) / 32.0  # normalize
        dists.append((rel_path, dist))
        
    dists.sort(key=lambda x: x[1])
    print(f"Template: {f}")
    for idx, (match, dist) in enumerate(dists[:3]):
        print(f"  Top {idx+1}: {match} (dist={dist:.4f})")
    print("-" * 50)
    sys.stdout.flush()
