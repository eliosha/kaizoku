import os

path = "/Users/mac/Desktop/Websites /GITkaizoku/img/Sorted/Action Figures/Bleach Action Figures"
files = sorted([f for f in os.listdir(path) if not f.startswith('.')])
print(f"Total files: {len(files)}")
print(files)
