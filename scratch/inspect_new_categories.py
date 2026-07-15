import json
import os

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/new_sorted_tree.json") as f:
    tree = json.load(f)

print("Listing all folders and files under categories to detect products:")
for path in sorted(tree.keys()):
    if path == "root":
        continue
    
    parts = path.split('/')
    if len(parts) == 1:
        # Category root
        print(f"Category: {path}")
        if tree[path]["dirs"]:
            print(f"  Direct Subdirs: {tree[path]['dirs']}")
        if tree[path]["files"]:
            print(f"  Direct Files ({len(tree[path]['files'])}): {tree[path]['files'][:10]}")
        print("=" * 60)
