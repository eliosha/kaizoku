import os
import numpy as np
from PIL import Image

def get_grid_features(image_path, grid_size=4):
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

path = "/Users/mac/Desktop/Websites /GITkaizoku/img/Sorted/Tshirts/Solo Leveling Tshirts"
files = sorted([f for f in os.listdir(path) if not f.startswith('.')])
features = {f: get_grid_features(os.path.join(path, f)) for f in files}

print("Pairwise distances:")
for i in range(len(files)):
    for j in range(i + 1, len(files)):
        f1, f2 = files[i], files[j]
        dist = np.linalg.norm(features[f1] - features[f2])
        print(f"  {f1} <-> {f2} : {dist:.4f}")
