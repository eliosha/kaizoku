import json

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/extracted_products.json") as f:
    products = json.load(f)

print(f"Total products in catalog: {len(products)}")
for p in products:
    print(f"ID: {p['id']}")
    print(f"  Name: {p['name']}")
    print(f"  Images: {p['images']}")
