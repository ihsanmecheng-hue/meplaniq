
import re

with open("frontend/src/Canvas.jsx", "r", encoding="utf-8") as f:
    code = f.read()

# Replace Doors map
def door_repl(m):
    return """{solveData?.doors?.map((door, idx) => {
                  const isDragging = dragState?.item?.id === door.id;
                  const tx = isDragging ? dragState.dx : 0;
                  const ty = isDragging ? dragState.dy : 0;
                  const isSelected = selectedItem?.item?.id === door.id;
                  return (
                  <g key={`door-${door.id}-${idx}`}
                     transform={isDragging ? `translate(${tx}, ${ty})` : undefined}
                     onPointerDown={(e) => {
                        e.stopPropagation();
                        setSelectedItem({ type: "Door", item: door });
                        const pt = getSvgCoordinates(e);
                        setDragState({ type: "Door", item: door, startCursorX: pt.x, startCursorY: pt.y, startOffset: door.offset_mm, dx: 0, dy: 0 });
                     }}
                     style={{ cursor: "grab", filter: isSelected ? "drop-shadow(0px 0px 4px #FACC15)" : "none" }}
                  >
                    {/* Hitbox for easier dragging */}
                    {door.hinge && <circle cx={(door.jambs[0][0]+door.jambs[1][0])/2} cy={(door.jambs[0][1]+door.jambs[1][1])/2} r={door.width_mm/2} fill="transparent" />}"""

code = re.sub(r"\{solveData\?\.doors\?\.map\(\(door, idx\) => \(\s+<g key=\{`door-\$\{door\.id\}-\$\{idx\}`\}>", door_repl, code)
code = re.sub(r"(\s+)\}\)\}(\s+</g>\s+)\{\/\* LAYER_DIMENSIONS \*\/\s+", r"\1  )}) \2{/* LAYER_DIMENSIONS */\n", code)

# Fix closing brackets for map
# Find the exact closing for doors
code = code.replace("                  </g>\n                ))}\n              </g>\n            )}", "                  </g>\n                )})}\n              </g>\n            )}")

# Replace Windows map
def win_repl(m):
    return """{solveData?.windows?.map((win, idx) => {
                  const isDragging = dragState?.item?.id === win.id;
                  const tx = isDragging ? dragState.dx : 0;
                  const ty = isDragging ? dragState.dy : 0;
                  const isSelected = selectedItem?.item?.id === win.id;
                  return (
                  <g key={`window-${win.id}-${idx}`}
                     transform={isDragging ? `translate(${tx}, ${ty})` : undefined}
                     onPointerDown={(e) => {
                        e.stopPropagation();
                        setSelectedItem({ type: "Window", item: win });
                        const pt = getSvgCoordinates(e);
                        setDragState({ type: "Window", item: win, startCursorX: pt.x, startCursorY: pt.y, startOffset: win.offset_mm, dx: 0, dy: 0 });
                     }}
                     style={{ cursor: "grab", filter: isSelected ? "drop-shadow(0px 0px 4px #38BDF8)" : "none" }}
                  >
                    {/* Hitbox */}
                    {win.win_lines && win.win_lines[0] && <circle cx={(win.win_lines[0][0]+win.win_lines[0][2])/2} cy={(win.win_lines[0][1]+win.win_lines[0][3])/2} r={win.width_mm/2} fill="transparent" />}"""

code = re.sub(r"\{solveData\?\.windows\?\.map\(\(win, idx\) => \(\s+<g key=\{`window-\$\{win\.id\}-\$\{idx\}`\}>", win_repl, code)

code = code.replace("                  </g>\n                ))}\n              </g>\n            )}", "                  </g>\n                )})}\n              </g>\n            )}")


with open("frontend/src/Canvas.jsx", "w", encoding="utf-8") as f:
    f.write(code)


