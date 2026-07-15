import json

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/new_sorted_tree.json") as f:
    tree = json.load(f)

for k, v in tree.items():
    if "sticker" in k.lower():
        print(f"Key: {k}")
        print(f"  Dirs: {v['dirs']}")
        print(f"  Files: {v['files']}")
