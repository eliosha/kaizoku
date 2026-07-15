import os
try:
    from PIL import Image
    print("Pillow is installed!")
except ImportError:
    print("Pillow is not installed!")

base_path = "/Users/mac/Desktop/Websites /GITkaizoku/img/Sorted"

# Let's list some folders that seem to have "unlabeled" or "all" or "other" in their names
for root, dirs, files in os.walk(base_path):
    rel_root = os.path.relpath(root, base_path)
    # Check if there are files in this folder
    valid_files = [f for f in files if not f.startswith('.')]
    if valid_files:
        # Check if the folder name is "Other", "All", or similar
        last_dir = os.path.basename(root)
        if last_dir.lower() in ["other", "others", "all", "unsorted", "unlabeled"]:
            print(f"Potential unsorted folder: {rel_root} ({len(valid_files)} files)")
