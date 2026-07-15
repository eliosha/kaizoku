import json

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/new_sorted_tree.json") as f:
    tree = json.load(f)

print("Subdirs inside Tshirts:")
for k, v in sorted(tree.items()):
    if k.startswith("Tshirts/"):
        print(f"  {k} has dirs: {v['dirs']} and {len(v['files'])} files")
        if v["files"] and not v["dirs"]:
            print(f"    Sample files: {v['files'][:5]}")

print("=" * 60)
print("Subdirs inside Hoodies:")
for k, v in sorted(tree.items()):
    if k.startswith("Hoodies/"):
        print(f"  {k} has dirs: {v['dirs']} and {len(v['files'])} files")
