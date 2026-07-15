import os
import numpy as np
from PIL import Image

def get_dhash(image, hash_size=8):
    # Grayscale and resize
    image = image.convert('L').resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
    pixels = np.array(image.getdata(), dtype=float).reshape((hash_size, hash_size + 1))
    # Compare adjacent pixels
    diff = pixels[:, 1:] > pixels[:, :-1]
    # Convert to hex string
    return ''.join(f'{x:x}' for x in np.packbits(diff.flatten()))

def get_hamming_distance(hash1, hash2):
    # Convert hex string to integer and compute hamming distance
    h1 = int(hash1, 16)
    h2 = int(hash2, 16)
    return bin(h1 ^ h2).count('1')

def get_color_histogram(image, bins=8):
    # Resize to speed up and smooth
    image = image.resize((64, 64), Image.Resampling.LANCZOS).convert('RGB')
    hist = image.histogram()
    # Normalize histogram
    hist = np.array(hist, dtype=float)
    hist /= hist.sum()
    return hist

def get_similarity(hist1, hist2):
    # Cosine similarity of color histograms
    dot_product = np.dot(hist1, hist2)
    norm1 = np.linalg.norm(hist1)
    norm2 = np.linalg.norm(hist2)
    if norm1 == 0 or norm2 == 0:
        return 0
    return dot_product / (norm1 * norm2)

def cluster_folder(folder_path):
    files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.heic', '.webp'))])
    if not files:
        return []
    
    images_data = []
    for f in files:
        f_path = os.path.join(folder_path, f)
        try:
            with Image.open(f_path) as img:
                dhash = get_dhash(img)
                hist = get_color_histogram(img)
                images_data.append({
                    "filename": f,
                    "hash": dhash,
                    "hist": hist
                })
        except Exception as e:
            print(f"Error loading {f}: {e}")
            
    # Grouping logic
    # We will build a similarity graph and find connected components
    n = len(images_data)
    visited = [False] * n
    groups = []
    
    for i in range(n):
        if visited[i]:
            continue
        # Start a new group
        group = [images_data[i]["filename"]]
        visited[i] = True
        
        # Find all similar images
        for j in range(i + 1, n):
            if visited[j]:
                continue
            # Compare hash and histogram
            h_dist = get_hamming_distance(images_data[i]["hash"], images_data[j]["hash"])
            sim = get_similarity(images_data[i]["hist"], images_data[j]["hist"])
            
            # If distance is small or color similarity is extremely high
            # We can tune these thresholds
            if h_dist <= 14 or sim >= 0.95:
                group.append(images_data[j]["filename"])
                visited[j] = True
                
        groups.append(group)
        
    return groups

# Let's test on Solo Leveling Tshirts
test_path = "/Users/mac/Desktop/Websites /GITkaizoku/img/Sorted/Tshirts/Solo Leveling Tshirts"
groups = cluster_folder(test_path)
print(f"Found {len(groups)} groups in Solo Leveling Tshirts:")
for idx, group in enumerate(groups):
    print(f"  Group {idx + 1}: {group}")
