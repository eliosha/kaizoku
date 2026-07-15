import os
import json

with open("/Users/mac/Desktop/Websites /GITkaizoku/scratch/sorted_images.json") as f:
    sorted_data = json.load(f)

# Find all files in GITkaizoku/ recursively
all_files_on_disk = {}
for root, dirs, files in os.walk("/Users/mac/Desktop/Websites /GITkaizoku"):
    for f in files:
        if f.startswith('.'):
            continue
        all_files_on_disk[f] = os.path.join(root, f)

print(f"Total unique filenames on disk: {len(all_files_on_disk)}")

# Check how many of the files listed in sorted_images.json are on disk
found = 0
not_found = 0
found_paths = []

for folder, files_list in sorted_data.items():
    for f in files_list:
        if f in all_files_on_disk:
            found += 1
            found_paths.append(all_files_on_disk[f])
        else:
            not_found += 1

print(f"Files from sorted_images.json found on disk: {found}")
print(f"Files from sorted_images.json NOT found on disk: {not_found}")
if found_paths:
    print(f"Sample path on disk for found files: {found_paths[:5]}")
