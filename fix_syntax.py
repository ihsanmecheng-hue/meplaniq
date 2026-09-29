
import re

with open("frontend/src/Canvas.jsx", "r", encoding="utf-8") as f:
    code = f.read()

# Fix Doors closing
code = code.replace("""                  </g>
                ))}
              </g>
            )}""", """                  </g>
                )})}
              </g>
            )}""")
            
# Fix Windows Map
def win_repl(m):
    return """{solveData?.windows?.map((win, idx) => {
                  const isDragging = dragState?.item?.id === win.id;
                  const tx = isDragging ? dragState.dx : 0;
                  const ty = isDragging ? dragState.dy : 0;
                  const isSelected = selectedItem?.item?.id === win.id;
                  return (
                  <g key={`win-${win.id}-${idx}`}
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
                    {win.lines && win.lines[0] && <circle cx={(win.lines[0][0]+win.lines[0][2])/2} cy={(win.lines[0][1]+win.lines[0][3])/2} r={win.width_mm/2} fill="transparent" />}"""

code = re.sub(r"\{solveData\?\.windows\?\.map\(\(win, idx\) => \(\s+<g key=\{`win-\$\{win\.id\}-\$\{idx\}`\}>", win_repl, code)

with open("frontend/src/Canvas.jsx", "w", encoding="utf-8") as f:
    f.write(code)


