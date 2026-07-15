import json

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/sorted_structure.json") as f:
    structure = json.load(f)

target_folders = [
    "Action Figures/Naruto Action Figures",
    "Action Figures/One Piece Action Figures",
    "Action Figures/Demon Slayaer Action Figures",
    "Action Figures/Attack On Titan Action Figures"
]

for folder in target_folders:
    if folder in structure:
        print(f"Folder: {folder}")
        print(f"  Files ({len(structure[folder]['files'])}): {structure[folder]['files']}")
        print("=" * 80)
