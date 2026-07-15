import json

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/sorted_structure.json") as f:
    structure = json.load(f)

# Let's inspect some folders and print their filenames to see if they are grouped by product
for folder, content in sorted(structure.items()):
    # We want to print directories that have both files and subdirectories, or just folders with many files
    if content["files"] and len(content["files"]) > 0:
        # Check if the folder name is deep (contains /)
        print(f"Folder: {folder}")
        print(f"  Files count: {len(content['files'])}")
        print(f"  Sample files: {content['files'][:10]}")
        print("-" * 50)
