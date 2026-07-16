import json

main_path = "/Users/mac/Desktop/Websites /GITkaizoku/scratch/product_metadata_v2.json"
with open(main_path) as f:
    db = json.load(f)

fandom_series = [
    'marvel', 'dc', 'harry potter', 'breaking bad', 'game of thrones', 
    'stranger things', 'peaky blinders', 'the godfather', 'invincible'
]

matches = []
for k in db.keys():
    series_lower = db[k].get("series", "").lower()
    if any(fs in series_lower for fs in fandom_series):
        matches.append(k)

print(f"Total: {len(matches)}")
print("First 10 items in order:")
for m in matches[:10]:
    print(f"  {m}")
