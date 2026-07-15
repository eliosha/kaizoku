import json

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/new_sorted_tree.json") as f:
    tree = json.load(f)

print("Folders or files mentioning 'black' or 'white':")
for rel_path, content in sorted(tree.items()):
    # Check if folder name contains black or white
    folder_lower = rel_path.lower()
    if "black" in folder_lower or "white" in folder_lower:
        print(f"Folder: {rel_path}")
        print(f"  Files: {content['files'][:5]}")
        
    for f in content["files"]:
        f_lower = f.lower()
        if "black" in f_lower or "white" in f_lower:
            print(f"File in folder '{rel_path}': {f}")
