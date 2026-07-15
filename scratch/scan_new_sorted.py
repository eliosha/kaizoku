import os

base_path = "/Users/mac/Desktop/Websites /GITkaizoku/img/Sorted"

def scan_dir(path):
    for root, dirs, files in os.walk(path):
        rel_root = os.path.relpath(root, path)
        if rel_root == ".":
            continue
        
        # Check files that are directly in this directory (filtering out hidden files)
        local_files = [f for f in files if not f.startswith('.')]
        
        # We only want to print:
        # 1. Folders that contain subdirectories (which are category levels)
        # 2. Folders that contain files directly (which can be a product folder or category folder with loose images)
        if local_files or dirs:
            print(f"Directory: {rel_root}")
            if dirs:
                print(f"  Subdirs ({len(dirs)}): {sorted(dirs)[:10]}...")
            if local_files:
                print(f"  Files ({len(local_files)}): {sorted(local_files)[:10]}...")
            print("-" * 60)

scan_dir(base_path)
