with open("frontend/src/Canvas.jsx", "r", encoding="utf-8") as f:
    text = f.read()

# Let's inspect where LAYER_ROOM_HANDLES starts and ends
start_marker = "{/* INTERACTIVE ROOM CORNER & WALL RESIZE HANDLES */}"
preview_marker = "{/* DYNAMIC LIVE DRAG PREVIEW FOR ROOM RESIZING */}"

idx1 = text.find(start_marker)
idx2 = text.find(preview_marker)

if idx1 != -1 and idx2 != -1:
    section_to_replace = text[idx1:idx2]
    
    clean_handles_section = """{/* INTERACTIVE ROOM CORNER & WALL RESIZE HANDLES (Visible only when isResizeModeActive is true) */}
          {isResizeModeActive && (
            <g id="LAYER_ROOM_HANDLES">
              {solveData?.rooms?.map((room, rIdx) => {
                const rawPoints = room.points || [];
                if (rawPoints.length < 4) return null;
                const bounds = getRoomBounds(rawPoints);
                const { minX, maxX, minY, maxY } = bounds;

                const corners = [
                  { idx: 0, x: minX, y: minY, cursor: 'nesw-resize', label: 'BL' },
                  { idx: 1, x: maxX, y: minY, cursor: 'nwse-resize', label: 'BR' },
                  { idx: 2, x: maxX, y: maxY, cursor: 'nesw-resize', label: 'TR' },
                  { idx: 3, x: minX, y: maxY, cursor: 'nwse-resize', label: 'TL' }
                ];

                const wallMidpoints = [
                  { side: 'Bottom', x: (minX + maxX) / 2, y: minY, cursor: 'ns-resize' },
                  { side: 'Right', x: maxX, y: (minY + maxY) / 2, cursor: 'ew-resize' },
                  { side: 'Top', x: (minX + maxX) / 2, y: maxY, cursor: 'ns-resize' },
                  { side: 'Left', x: minX, y: (minY + maxY) / 2, cursor: 'ew-resize' }
                ];

                return (
                  <g key={`room-handles-${rIdx}`}>
                    <rect
                      x={minX} y={minY}
                      width={maxX - minX} height={maxY - minY}
                      fill="none"
                      stroke="rgba(56, 189, 248, 0.25)"
                      strokeWidth={1 / zoom}
                      strokeDasharray={`${6 / zoom} ${4 / zoom}`}
                    />

                    {wallMidpoints.map((w, wIdx) => (
                      <g key={`wall-handle-${wIdx}`}>
                        <rect
                          x={w.side === 'Bottom' || w.side === 'Top' ? w.x - 200 : w.x - (6 / zoom)}
                          y={w.side === 'Left' || w.side === 'Right' ? w.y - 200 : w.y - (6 / zoom)}
                          width={w.side === 'Bottom' || w.side === 'Top' ? 400 : (12 / zoom)}
                          height={w.side === 'Left' || w.side === 'Right' ? 400 : (12 / zoom)}
                          fill="transparent"
                          style={{ cursor: w.cursor }}
                          onPointerDown={(e) => {
                            e.stopPropagation();
                            const pt = getSvgCoordinates(e);
                            setDragState({
                              type: 'RoomResize',
                              mode: 'wall',
                              wallSide: w.side,
                              roomName: room.name,
                              initialBounds: bounds,
                              startCursorX: pt.x,
                              startCursorY: pt.y,
                              currentPoints: rawPoints
                            });
                          }}
                        />
                        <circle
                          cx={w.x} cy={w.y}
                          r={5.5 / zoom}
                          fill="#F59E0B"
                          stroke="#FFFFFF"
                          strokeWidth={1.5 / zoom}
                          style={{ cursor: w.cursor, pointerEvents: 'none' }}
                        />
                      </g>
                    ))}

                    {corners.map((c) => (
                      <g key={`corner-handle-${c.idx}`}>
                        <circle
                          cx={c.x} cy={c.y}
                          r={24 / zoom}
                          fill="transparent"
                          style={{ cursor: c.cursor }}
                          onPointerDown={(e) => {
                            e.stopPropagation();
                            const pt = getSvgCoordinates(e);
                            setDragState({
                              type: 'RoomResize',
                              mode: 'corner',
                              cornerIndex: c.idx,
                              roomName: room.name,
                              initialBounds: bounds,
                              startCursorX: pt.x,
                              startCursorY: pt.y,
                              currentPoints: rawPoints
                            });
                          }}
                        />
                        <circle
                          cx={c.x} cy={c.y}
                          r={8 / zoom}
                          fill="#38BDF8"
                          stroke="#FFFFFF"
                          strokeWidth={2 / zoom}
                          style={{ cursor: c.cursor, pointerEvents: 'none', filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.5))' }}
                        />
                      </g>
                    ))}
                  </g>
                );
              })}
            </g>
          )}

          """
    new_text = text[:idx1] + clean_handles_section + text[idx2:]
    with open("frontend/src/Canvas.jsx", "w", encoding="utf-8") as f:
        f.write(new_text)
    print("Fixed Canvas.jsx handles block!")
else:
    print("Could not find markers:", idx1, idx2)
