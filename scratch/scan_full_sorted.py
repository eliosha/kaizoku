import os
import json

base_path = "/Users/mac/Desktop/Websites /GITkaizoku/img/Sorted"

def scan_sorted(path):
    tree = {}
    for root, dirs, files in os.walk(path):
        rel_root = os.path.relpath(root, path)
        if rel_root == ".":
            rel_root = "root"
            
        local_files = sorted([f for f in files if not f.startswith('.')])
        tree[rel_root] = {
            "dirs": sorted(dirs),
            "files": local_files
        }
    return tree

tree = scan_sorted(base_path)
with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/new_sorted_tree.json", "w") as f:
    json.dump(tree, f, indent=2)

print("Saved new sorted tree to scratch/new_sorted_tree.json")
