import os

pages_dir = "/Users/mac/Desktop/Websites /GITkaizoku/pages"
for f in sorted(os.listdir(pages_dir)):
    if f.endswith('.html'):
        print(f)
