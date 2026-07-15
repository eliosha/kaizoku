import json

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/product_metadata_v2.json") as f:
    db = json.load(f)

for k in db.keys():
    if "nobara" in k.lower():
        print(f"Found nobara key: {k}")
