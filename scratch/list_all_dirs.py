import os

base_path = "/Users/mac/Desktop/Websites /GITkaizoku/img/Sorted"

all_dirs = []
for root, dirs, files in os.walk(base_path):
    rel_root = os.path.relpath(root, base_path)
    if rel_root != ".":
        all_dirs.append(rel_root)

print(f"Total directories in img/Sorted: {len(all_dirs)}")
for d in sorted(all_dirs):
    print(f"  {d}")
