import json

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/new_sorted_tree.json") as f:
    tree = json.load(f)

for k, v in tree.items():
    if "helicop" in k.lower() or "wz" in k.lower():
        print(f"Key: {k}")
        print(f"  Files: {v['files']}")
