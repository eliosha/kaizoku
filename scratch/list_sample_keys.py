import json

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/product_metadata_v2.json") as f:
    db = json.load(f)

categories = {}
for k, v in db.items():
    cat = v["category"]
    if cat not in categories:
        categories[cat] = []
    categories[cat].append((k, v["name"]))

for cat, items in categories.items():
    print(f"Category: {cat} (Total: {len(items)})")
    for k, name in items[:5]:
        print(f"  {k} -> {name}")
