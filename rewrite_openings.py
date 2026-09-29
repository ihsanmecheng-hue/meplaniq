
with open("backend/geometry.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
in_openings = False
skip_till = -1

for idx, line in enumerate(lines):
    if idx < skip_till:
        continue

    if "if norm_openings:" in line and "margin = 50.0" in lines[idx+1]:
        # We found the block!
        new_lines.append(line)
        new_lines.append(lines[idx+1])
        
        pre_pass_code = """
        # --- NEW: Intelligent Opening Collision Detection & Auto-Spacing Pre-pass ---
        from collections import defaultdict
        ops_by_wall = defaultdict(list)
        for i, op in enumerate(norm_openings):
            hr = op.host_room.lower().strip() if op.host_room else ""
            sd = (op.wall_side or "Top").strip().capitalize()
            if sd not in ("Top", "Bottom", "Right", "Left"): sd = "Top"
            ops_by_wall[(hr, sd)].append((i, op))

        computed_offsets = {}
        for (hr, sd), group in ops_by_wall.items():
            group.sort(key=lambda x: float(x[1].offset_mm if x[1].offset_mm is not None else 0.0))
            
            bounds = None
            for k, v in shifted_room_bounds.items():
                if k.lower().strip() == hr:
                    bounds = v
                    break
            if not bounds:
                bounds = list(shifted_room_bounds.values())[0] if shifted_room_bounds else (0.0, 0.0, 6000.0, 5000.0)
                
            minx, miny, maxx, maxy = bounds
            wall_len = (maxx - minx) if sd in ("Top", "Bottom") else (maxy - miny)
            min_c = 150.0
            current_min = min_c
            
            total_req_space = sum(float(op.width_mm) for _, op in group) + min_c * (len(group) + 1)
            
            for i_idx, op in group:
                w = float(op.width_mm)
                # If wall is hopelessly small for everything, just center it
                if wall_len <= (min_c * 2 + w):
                    computed_offsets[i_idx] = (wall_len - w) / 2.0
                    continue
                    
                req = float(op.offset_mm if op.offset_mm is not None else 0.0)
                
                # If total required space exceeds wall, we just pack them from current_min
                if total_req_space > wall_len:
                    eff = current_min
                else:
                    eff = max(req, current_min)
                    if eff + w > wall_len - min_c:
                        eff = wall_len - min_c - w
                        if eff < current_min:
                            eff = current_min
                            
                computed_offsets[i_idx] = eff
                current_min = eff + w + min_c

        for i, op in enumerate(norm_openings):
"""
        new_lines.extend(pre_pass_code.splitlines(True))
        skip_till = idx + 3
        continue
    
    if "raw_offset = float(op.offset_mm if op.offset_mm is not None else 0.0)" in line:
        # replace the clearance enforcement block
        new_lines.append("            effective_offset = computed_offsets[i]\n")
        # skip next lines
        skip_till = idx + 8
        continue
        
    if "for op in norm_openings:" in line and "margin = 50.0" not in line:
        continue # handled by the prepass loop

    new_lines.append(line)

with open("backend/geometry.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

