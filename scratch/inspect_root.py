import os

root_dir = "/Users/mac/Desktop/Websites /GITkaizoku"
for item in sorted(os.listdir(root_dir)):
    item_path = os.path.join(root_dir, item)
    is_dir = "Directory" if os.path.isdir(item_path) else "File"
    print(f"{item} ({is_dir})")
