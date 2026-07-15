import json

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/sorted_structure.json") as f:
    structure = json.load(f)

# Print all folders that contain files and what subdirectories they contain (if any)
for folder, content in sorted(structure.items()):
    # Check if this folder has files directly and also has subdirectories (which might contain organized products)
    if content["files"] and content["dirs"]:
        print(f"Folder containing BOTH files and subdirs: {folder}")
        print(f"  Files: {content['files'][:5]}")
        print(f"  Subdirs: {content['dirs']}")
        print("-" * 50)
