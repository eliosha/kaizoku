import json

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/sorted_images.json") as f:
    data = json.load(f)

print(f"Total keys: {len(data)}")
for k in sorted(data.keys()):
    print(f"  {k}: {len(data[k])} files")
