
import re

with open("frontend/src/Canvas.jsx", "r", encoding="utf-8") as f:
    code = f.read()

# Replace HVAC map
def hvac_repl(m):
    return """{solveData?.hvac_equipment?.map((eq, idx) => {
                  const isDragging = dragState?.item?.id === eq.id;
                  const tx = isDragging ? dragState.dx : 0;
                  const ty = isDragging ? dragState.dy : 0;
                  const isSelected = selectedItem?.item?.id === eq.id;
                  return (
                  <g key={`hvac-${eq.id}-${idx}`}
                     transform={isDragging ? `translate(${tx}, ${ty})` : undefined}
                     onPointerDown={(e) => {
                        e.stopPropagation();
                        setSelectedItem({ type: "HVAC", item: eq });
                        const pt = getSvgCoordinates(e);
                        setDragState({ type: "HVAC", item: eq, startCursorX: pt.x, startCursorY: pt.y, startOffsetX: eq.x, startOffsetY: eq.y, dx: 0, dy: 0 });
                     }}
                     style={{ cursor: "grab", filter: isSelected ? "drop-shadow(0px 0px 6px #10B981)" : "none" }}
                  >
                    {/* Hitbox */}
                    <circle cx={eq.x} cy={eq.y} r={eq.radius} fill="transparent" />"""

code = re.sub(r"\{solveData\?\.hvac_equipment\?\.map\(\(eq, idx\) => \(\s+<g key=\{`hvac-\$\{eq\.id\}-\$\{idx\}`\}>", hvac_repl, code)

code = code.replace("                  </g>\n                ))}\n              </g>\n            )}", "                  </g>\n                )})}\n              </g>\n            )}")

# Also update the mouseUp logic for HVAC
mouse_up_old = """        const ws = dragState.item.wall_side;
        // If left/right wall, offset goes along Y.
        let delta = 0;
        if (ws === "Bottom") delta = dx;
        else if (ws === "Right") delta = dy;
        else if (ws === "Top") delta = -dx;
        else if (ws === "Left") delta = -dy;
        
        const finalOffset = dragState.startOffset + delta;
        onLiveItemUpdate(dragState.type, dragState.item.id, { offset_mm: finalOffset });"""
mouse_up_new = """        if (dragState.type === "HVAC") {
            onLiveItemUpdate("HVAC", dragState.item.id, { 
                location_x: dragState.startOffsetX + dx, 
                location_y: dragState.startOffsetY + dy 
            });
        } else {
            const ws = dragState.item.wall_side;
            let delta = 0;
            if (ws === "Bottom") delta = dx;
            else if (ws === "Right") delta = dy;
            else if (ws === "Top") delta = -dx;
            else if (ws === "Left") delta = -dy;
            
            const finalOffset = dragState.startOffset + delta;
            onLiveItemUpdate(dragState.type, dragState.item.id, { offset_mm: finalOffset });
        }"""
code = code.replace(mouse_up_old, mouse_up_new)

with open("frontend/src/Canvas.jsx", "w", encoding="utf-8") as f:
    f.write(code)

