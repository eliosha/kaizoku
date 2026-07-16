import json

main_path = "/Users/mac/Desktop/Websites /GITkaizoku/scratch/product_metadata_v2.json"
with open(main_path) as f:
    db = json.load(f)

series = set()
for k, v in db.items():
    s = v.get("series", "")
    if s:
        series.add(s)

print("All unique series on disk:")
for s in sorted(series):
    print(f"  {repr(s)}")
