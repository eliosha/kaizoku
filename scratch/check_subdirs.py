import json

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/sorted_structure.json") as f:
    structure = json.load(f)

# Print all subdirectories for each category
print("Folders in img/Sorted:")
for folder, content in sorted(structure.items()):
    if content["dirs"]:
        print(f"  {folder} contains subdirectories: {content['dirs']}")
