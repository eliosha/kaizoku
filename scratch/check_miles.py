import json

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/product_metadata_v2.json") as f:
    db = json.load(f)

for k in db.keys():
    if "miles" in k.lower() or "morales" in k.lower():
        print(f"Found matching key: {k}")
