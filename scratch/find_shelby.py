import json

main_path = "/Users/mac/Desktop/Websites /GITkaizoku/scratch/product_metadata_v2.json"
with open(main_path) as f:
    db = json.load(f)

for k, v in db.items():
    if "shelby" in k.lower() or "shelby" in v["name"].lower():
        print(f"Product: {k}")
        print(f"  Name: {v['name']}")
        print(f"  Series: {v.get('series')}")
        print(f"  Category: {v.get('category')}")
