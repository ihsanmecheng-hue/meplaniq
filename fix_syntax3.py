
with open("frontend/src/Canvas.jsx", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if i == 244 and "))}" in line:
        lines[i] = line.replace("))}", "})}")
        print("Fixed windows closing at line 244")

with open("frontend/src/Canvas.jsx", "w", encoding="utf-8") as f:
    f.writelines(lines)

