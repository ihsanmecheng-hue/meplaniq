
with open("frontend/src/Canvas.jsx", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if i == 244 and ")}"} in line.replace(" ", ""):
        lines[i] = line.replace("))}", "})}")
        
    if i == 298 and ")}"} in line.replace(" ", ""):
        # Check if line 298 is doors closing
        lines[i] = line.replace("))}", "})}")

with open("frontend/src/Canvas.jsx", "w", encoding="utf-8") as f:
    f.writelines(lines)

