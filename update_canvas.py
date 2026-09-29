
import sys

with open("frontend/src/Canvas.jsx", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add props
code = code.replace("onCursorMove,", "onCursorMove,\n  onLiveItemUpdate,")

# 2. Add states
states = """  const [isPanning, setIsPanning] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);
  const [dragState, setDragState] = useState(null);"""
code = code.replace("  const [isPanning, setIsPanning] = useState(false);", states)

# 3. Modify handleMouseMove
mouse_move = """  const handleMouseMove = (e) => {
    const coords = getSvgCoordinates(e);
    onCursorMove(coords);

    if (dragState) {
        const dx = coords.x - dragState.startCursorX;
        const dy = coords.y - dragState.startCursorY;
        setDragState(prev => ({ ...prev, dx, dy }));
    } else if (isPanning) {"""
code = code.replace("  const handleMouseMove = (e) => {\n    const coords = getSvgCoordinates(e);\n    onCursorMove(coords);\n\n    if (isPanning) {", mouse_move)

# 4. Modify handleMouseUp
mouse_up = """  const handleMouseUp = () => {
    setIsPanning(false);
    if (dragState && onLiveItemUpdate) {
        const dx = dragState.dx;
        const dy = dragState.dy;
        const ws = dragState.item.wall_side;
        const isHoriz = (ws === "Bottom" || ws === "Top");
        // If left/right wall, offset goes along Y. But wait, in backend:
        // offset is distance along the wall line.
        // Bottom: (0,0) -> (W,0), dx is positive.
        // Top: (W,H) -> (0,H), dx is NEGATIVE for positive offset!
        // Left: (0,H) -> (0,0), dy is NEGATIVE for positive offset!
        // Right: (W,0) -> (W,H), dy is POSITIVE for positive offset!
        let delta = 0;
        if (ws === "Bottom") delta = dx;
        else if (ws === "Right") delta = dy;
        else if (ws === "Top") delta = -dx;
        else if (ws === "Left") delta = -dy;
        
        const finalOffset = dragState.startOffset + delta;
        onLiveItemUpdate(dragState.type, dragState.item.id, { offset_mm: finalOffset });
    }
    setDragState(null);
  };"""
code = code.replace("  const handleMouseUp = () => {\n    setIsPanning(false);\n  };", mouse_up)

# 5. Add overlay to render
overlay = """
      {/* Interactive Overlay for Selected Item */}
      {selectedItem && (
        <div style={{
          position: "absolute", top: 16, right: 16, width: 280,
          background: "rgba(15, 23, 42, 0.95)", border: "1px solid #334155",
          borderRadius: 8, padding: 16, color: "white", zIndex: 50,
          boxShadow: "0 10px 25px -5px rgba(0, 0, 0, 0.5)"
        }}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 12 }}>
            <h4 style={{ margin: 0, fontSize: 14, color: "#38BDF8" }}>Edit {selectedItem.type}</h4>
            <button onClick={() => setSelectedItem(null)} style={{ background: "transparent", border: "none", color: "#94A3B8", cursor: "pointer" }}>'</button>
          </div>
          <p style={{ margin: "0 0 12px 0", fontSize: 12, color: "#94A3B8" }}>ID: {selectedItem.item.id}</p>
          
          <label style={{ display: "block", fontSize: 12, marginBottom: 4 }}>Width (mm)</label>
          <input 
            type="number" 
            defaultValue={selectedItem.item.width_mm} 
            onBlur={(e) => {
               if(onLiveItemUpdate) onLiveItemUpdate(selectedItem.type, selectedItem.item.id, { width_mm: Number(e.target.value) });
            }}
            style={{ width: "100%", background: "#1E293B", border: "1px solid #475569", color: "white", padding: "6px 8px", borderRadius: 4, marginBottom: 12 }}
          />

          {(selectedItem.type === "Door") && (
            <>
              <label style={{ display: "block", fontSize: 12, marginBottom: 4 }}>Swing</label>
              <select 
                defaultValue={selectedItem.item.swing}
                onChange={(e) => {
                   if(onLiveItemUpdate) onLiveItemUpdate(selectedItem.type, selectedItem.item.id, { swing: e.target.value });
                }}
                style={{ width: "100%", background: "#1E293B", border: "1px solid #475569", color: "white", padding: "6px 8px", borderRadius: 4, marginBottom: 12 }}
              >
                <option value="Inward-Left">Inward-Left</option>
                <option value="Inward-Right">Inward-Right</option>
                <option value="Outward-Left">Outward-Left</option>
                <option value="Outward-Right">Outward-Right</option>
              </select>
            </>
          )}
          <p style={{ fontSize: 11, color: "#475569", margin: 0 }}>Tip: Drag the {selectedItem.type.toLowerCase()} directly on the canvas to move it.</p>
        </div>
      )}
    </div>
  );
"""
code = code.replace("    </div>\n  );\n}", overlay + "\n}")

# 6. Inject drag handlers into Door SVG
door_g_start = """                {solveData?.doors?.map((door, idx) => (
                  <g key={`door-${door.id}-${idx}`}>"""
door_g_new = """                {solveData?.doors?.map((door, idx) => {
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
                    {door.hinge && <circle cx={(door.jambs[0][0]+door.jambs[1][0])/2} cy={(door.jambs[0][1]+door.jambs[1][1])/2} r={door.width_mm/2} fill="transparent" />}
"""
code = code.replace(door_g_start, door_g_new)
code = code.replace("                ))}
              </g>
            )}", "                )})}
              </g>
            )}")

# 7. Inject drag handlers into Window SVG
win_g_start = """                {solveData?.windows?.map((win, idx) => (
                  <g key={`window-${win.id}-${idx}`}>"""
win_g_new = """                {solveData?.windows?.map((win, idx) => {
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
                    {win.win_lines && win.win_lines[0] && <circle cx={(win.win_lines[0][0]+win.win_lines[0][2])/2} cy={(win.win_lines[0][1]+win.win_lines[0][3])/2} r={win.width_mm/2} fill="transparent" />}
"""
code = code.replace(win_g_start, win_g_new)
code = code.replace("                ))}
              </g>
            )}", "                )})}
              </g>
            )}")

with open("frontend/src/Canvas.jsx", "w", encoding="utf-8") as f:
    f.write(code)


