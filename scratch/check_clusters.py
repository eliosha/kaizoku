import json

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/clustered_products.json") as f:
    results = json.load(f)

target_folders = [
    "Tshirts/Solo Leveling Tshirts",
    "Tshirts/Attack On Titan Tshirts",
    "Tshirts/Bleach Tshirts",
    "Tshirts/Demon Slayer Tshirts",
    "Tshirts/Naruto Tshirts"
]

for folder in target_folders:
    if folder in results:
        print(f"Folder: {folder}")
        print(f"  Groups ({len(results[folder])}):")
        for idx, g in enumerate(results[folder]):
            print(f"    Group {idx+1}: {g}")
        print("=" * 60)
