import os
from PIL import Image

path = "/Users/mac/Desktop/Websites /GITkaizoku/img/Sorted/Tshirts/Solo Leveling Tshirts"
files = sorted([f for f in os.listdir(path) if not f.startswith('.')])

for f in files:
    f_path = os.path.join(path, f)
    with Image.open(f_path) as img:
        print(f"File: {f:20} Size: {os.path.getsize(f_path):10} Format: {img.format:5} Mode: {img.mode:5} Res: {img.size}")
