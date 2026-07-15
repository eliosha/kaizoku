import os

base = "/Users/mac/Desktop/Websites /GITkaizoku/img/Sorted"
for root, dirs, files in os.walk(base):
    for d in dirs:
        if "fandom" in d.lower():
            print(f"Directory: {os.path.relpath(os.path.join(root, d), base)}")
