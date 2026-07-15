import os
import numpy as np
from PIL import Image

def get_fast_features(image_path):
    with Image.open(image_path) as img:
        img = img.convert('L').resize((32, 32), Image.Resampling.BILINEAR)
        arr = np.array(img, dtype=float) / 255.0
        return arr.flatten()

path = "/Users/mac/Desktop/Websites /GITkaizoku/img/Sorted/Tshirts/Bleach Tshirts"
files = sorted([f for f in os.listdir(path) if not f.startswith('.')])
features = {f: get_fast_features(os.path.join(path, f)) for f in files}

print("Bleach Tshirts pairwise distances:")
for i in range(len(files)):
    for j in range(i + 1, len(files)):
        f1, f2 = files[i], files[j]
        dist = np.linalg.norm(features[f1] - features[f2]) / 32.0
        print(f"  {f1} <-> {f2} : {dist:.4f}")
