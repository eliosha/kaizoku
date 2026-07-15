import os
import json

base_path = "/Users/mac/Desktop/Websites /GITkaizoku/img/Sorted"

def scan_dir(path):
    structure = {}
    for root, dirs, files in os.walk(path):
        rel_root = os.path.relpath(root, path)
        if rel_root == ".":
            rel_root = "root"
        structure[rel_root] = {
            "dirs": dirs,
            "files": sorted([f for f in files if not f.startswith('.')])
        }
    return structure

structure = scan_dir(base_path)

# Let's print out the list of directories that contain files
print("Folders containing files:")
for folder, content in sorted(structure.items()):
    if content["files"]:
        print(f"  {folder}: {len(content['files'])} files")

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/sorted_structure.json", "w") as f:
    json.dump(structure, f, indent=2)
