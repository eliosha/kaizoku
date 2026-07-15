import json

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/product_metadata_v2.json") as f:
    db = json.load(f)

# Group keys by category to find good representation
cats = {}
for k, v in db.items():
    cat = v["category"]
    if cat not in cats:
        cats[cat] = []
    cats[cat].append((k, v["name"]))

for cat, items in cats.items():
    print(f"Category: {cat} (Total: {len(items)})")
    for k, name in items[:8]:
        print(f"  {k} -> {name}")
