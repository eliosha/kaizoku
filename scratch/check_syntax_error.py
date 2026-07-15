with open("/Users/mac/Desktop/Websites /GITkaizoku/main.js") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
print("Last 30 lines:")
for idx, line in enumerate(lines[-30:]):
    print(f"{len(lines)-30+idx+1}: {line}", end='')
