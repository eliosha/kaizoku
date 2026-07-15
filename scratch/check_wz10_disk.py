import os

base = "/Users/mac/Desktop/Websites /GITkaizoku/img/Sorted/Alloy Collectibles"
if os.path.exists(base):
    for d in sorted(os.listdir(base)):
        if "wz" in d.lower() or "helicop" in d.lower():
            print(f"Directory on disk: {d}")
else:
    print("Base directory does not exist")
