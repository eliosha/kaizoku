import json

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/sorted_images.json") as f:
    data = json.load(f)

deep_keys = [k for k in data.keys() if k.count('/') >= 2]
print(f"Deep keys (nested >= 2 levels): {len(deep_keys)}")
for dk in sorted(deep_keys):
    print(f"  {dk}: {len(data[dk])} files")
