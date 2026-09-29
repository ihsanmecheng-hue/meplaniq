
with open("frontend/src/Canvas.jsx", "r", encoding="utf-8") as f:
    lines = f.readlines()

def fix_line(idx):
    if "})}" in lines[idx]:
        lines[idx] = lines[idx].replace("})}", ");\n              })}")

fix_line(259)
fix_line(314)

with open("frontend/src/Canvas.jsx", "w", encoding="utf-8") as f:
    f.writelines(lines)

