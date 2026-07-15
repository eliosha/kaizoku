import os
import time

base_path = "/Users/mac/Desktop/Websites /GITkaizoku/img/Sorted"

def group_by_time(folder_path, max_gap_seconds=120):
    files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.heic', '.webp'))])
    if not files:
        return []
    
    file_times = []
    for f in files:
        f_path = os.path.join(folder_path, f)
        # We can use os.path.getmtime
        mtime = os.path.getmtime(f_path)
        file_times.append((f, mtime))
        
    # Sort by time
    file_times.sort(key=lambda x: x[1])
    
    groups = []
    current_group = []
    last_time = None
    
    for f, t in file_times:
        if last_time is None:
            current_group.append(f)
        elif t - last_time < max_gap_seconds:
            current_group.append(f)
        else:
            groups.append(current_group)
            current_group = [f]
        last_time = t
        
    if current_group:
        groups.append(current_group)
        
    return groups

target_folders = [
    "Tshirts/Bleach Tshirts",
    "Tshirts/Attack On Titan Tshirts",
    "Tshirts/Solo Leveling Tshirts",
    "Tshirts/Demon Slayer Tshirts",
    "Tshirts/Naruto Tshirts"
]

print("Timestamp-based grouping:")
for folder in target_folders:
    full_path = os.path.join(base_path, folder)
    if os.path.exists(full_path):
        groups = group_by_time(full_path, 120)
        print(f"  {folder}: {len(groups)} groups")
        for idx, g in enumerate(groups):
            # Print file names and their modification times
            times_str = []
            for f in g:
                mt = os.path.getmtime(os.path.join(full_path, f))
                times_str.append(f"{f} ({time.strftime('%M:%S', time.localtime(mt))})")
            print(f"    Group {idx+1}: {times_str}")
        print("-" * 50)
