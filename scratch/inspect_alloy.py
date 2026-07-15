import os

path = "/Users/mac/Desktop/Websites /GITkaizoku/img/Sorted/Alloy C's"
files = sorted([f for f in os.listdir(path) if not f.startswith('.')])
print(f"Total files: {len(files)}")
print(files[:40])
