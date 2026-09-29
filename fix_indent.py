
with open("backend/geometry.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "effective_offset = computed_offsets[i]" in line:
        start_idx = i - 2
        end_idx = i + 3
        break

new_lines = lines[:start_idx] + ["            effective_offset = computed_offsets[i]\n"] + lines[end_idx:]

with open("backend/geometry.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

