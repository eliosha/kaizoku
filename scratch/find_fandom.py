import json

main_path = "/Users/mac/Desktop/Websites /GITkaizoku/scratch/product_metadata_v2.json"
with open(main_path) as f:
    db = json.load(f)

targets = ["goodfellas", "kill bill", "by order of", "godfather"]
for k, v in db.items():
    name = v["name"].lower()
    for t in targets:
        if t in name:
            print(f"Product key: {k}")
            print(f"  Name: {v['name']}")
            print(f"  Series: {v.get('series')}")
            print(f"  Category: {v.get('category')}")
            print(f"  Images: {v.get('images')}")
