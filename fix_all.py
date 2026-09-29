
with open("frontend/src/Canvas.jsx", "r", encoding="utf-8") as f:
    lines = f.readlines()

def replace_at(line_idx, old, new):
    if old in lines[line_idx]:
        lines[line_idx] = lines[line_idx].replace(old, new)

# win.jambs
replace_at(244, "})}", "))}")
# windows map end
replace_at(259, "))}", "})}")
# doors map end
replace_at(314, "))}", "})}")

with open("frontend/src/Canvas.jsx", "w", encoding="utf-8") as f:
    f.writelines(lines)

