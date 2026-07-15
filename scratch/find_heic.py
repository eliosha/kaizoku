import os

base_path = "/Users/mac/Desktop/Websites /GITkaizoku/img/Sorted"
heic_files = []

for root, dirs, files in os.walk(base_path):
    for f in files:
        if f.lower().endswith('.heic'):
            rel_path = os.path.relpath(os.path.join(root, f), base_path)
            heic_files.append(rel_path)

print(f"Skipped HEIC files ({len(heic_files)}):")
for h in heic_files:
    print(f"  {h}")
