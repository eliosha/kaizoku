import json

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/product_metadata_v2.json") as f:
    db = json.load(f)

for k, v in db.items():
    if "whataboutanime" in k.lower():
        print(f"Key: {k}")
        print(f"  Name: {v['name']}")
        print(f"  Category: {v['category']}")
        print(f"  Images: {v['images']}")
