
import re

with open("frontend/src/pages/EditorPage.jsx", "r", encoding="utf-8") as f:
    code = f.read()

live_update_code = """
  const handleLiveItemUpdate = async (itemType, itemId, updates) => {
    let newDoors = editableDoors.length > 0 ? [...editableDoors] : [...(solveData?.doors || [])];
    let newWindows = editableWindows.length > 0 ? [...editableWindows] : [...(solveData?.windows || [])];
    let newHvac = editableHvac.length > 0 ? [...editableHvac] : [...(solveData?.hvac_equipment || [])];

    if (itemType === "Door") {
        newDoors = newDoors.map(d => d.id === itemId ? { ...d, ...updates } : d);
        setEditableDoors(newDoors);
    } else if (itemType === "Window") {
        newWindows = newWindows.map(w => w.id === itemId ? { ...w, ...updates } : w);
        setEditableWindows(newWindows);
    } else if (itemType === "HVAC") {
        newHvac = newHvac.map(eq => eq.id === itemId ? { ...eq, ...updates } : eq);
        setEditableHvac(newHvac);
    }

    if (!solveData?.project_id) return;
    
    const updatePayload = {
        name: solveData.project_name || "Floorplan",
        rooms: (solveData.rooms || []).map(r => ({
          name: r.name,
          points: r.points,
          fillet_radius: 0.0
        })),
        openings: [
          ...newDoors.map(d => ({
            id: d.id,
            host_room: d.host_room,
            wall_side: d.wall_side,
            offset_mm: Number(d.offset_mm),
            width_mm: Number(d.width_mm),
            height_mm: Number(d.height_mm),
            type: "Door",
            swing: d.swing || "Inward-Right"
          })),
          ...newWindows.map(w => ({
            id: w.id,
            host_room: w.host_room,
            wall_side: w.wall_side,
            offset_mm: Number(w.offset_mm),
            width_mm: Number(w.width_mm),
            height_mm: Number(w.height_mm),
            type: "Window"
          }))
        ],
        hvac_equipment: newHvac.map(h => ({
          id: h.id,
          room_name: h.room_name,
          unit_type: h.unit_type,
          location_x: Number(h.location_x ?? h.x),
          location_y: Number(h.location_y ?? h.y),
          cooling_capacity_tr: Number(h.cooling_capacity_tr),
          status: h.status ?? "Active"
        }))
      };

      try {
        const updated = await updateProjectById(solveData.project_id, updatePayload);
        setSolveData(updated);
        // Note: intentionally NOT changing canvasRenderKey so viewport does not reset
      } catch (err) {
        console.error("Live sync failed", err);
      }
  };
"""

if "const handleLiveItemUpdate" not in code:
    code = code.replace("const handleUpdateOpening = useCallback", live_update_code + "\n  const handleUpdateOpening = useCallback")

# Also pass handleLiveItemUpdate to Canvas
code = code.replace("showHvac={showHvac}", "showHvac={showHvac}\n              onLiveItemUpdate={handleLiveItemUpdate}")

# Remove setCanvasRenderKey(Date.now()) so zoom doesn"t reset on live edit
code = code.replace("setCanvasRenderKey(Date.now());", "")

with open("frontend/src/pages/EditorPage.jsx", "w", encoding="utf-8") as f:
    f.write(code)

