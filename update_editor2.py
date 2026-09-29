
import re

with open("frontend/src/pages/EditorPage.jsx", "r", encoding="utf-8") as f:
    code = f.read()

update_func_old = """    const handleLiveItemUpdate = async (itemType, itemId, updates) => {
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
          })),"""

update_func_new = """    const handleLiveItemUpdate = async (itemType, itemId, updates) => {
      let newDoors = editableDoors.length > 0 ? [...editableDoors] : [...(solveData?.doors || [])];
      let newWindows = editableWindows.length > 0 ? [...editableWindows] : [...(solveData?.windows || [])];
      let newHvac = editableHvac.length > 0 ? [...editableHvac] : [...(solveData?.hvac_equipment || [])];
      let newRooms = solveData?.rooms || [];

      if (itemType === "Door") {
          newDoors = newDoors.map(d => d.id === itemId ? { ...d, ...updates } : d);
          setEditableDoors(newDoors);
      } else if (itemType === "Window") {
          newWindows = newWindows.map(w => w.id === itemId ? { ...w, ...updates } : w);
          setEditableWindows(newWindows);
      } else if (itemType === "HVAC") {
          newHvac = newHvac.map(eq => eq.id === itemId ? { ...eq, ...updates } : eq);
          setEditableHvac(newHvac);
      } else if (itemType === "Room") {
          newRooms = newRooms.map(r => r.name === itemId ? { ...r, ...updates } : r);
      }

      if (!solveData?.project_id) return;
      
      const updatePayload = {
          name: solveData.project_name || "Floorplan",
          rooms: newRooms.map(r => ({
            name: r.name,
            points: r.points,
            fillet_radius: 0.0
          })),"""
code = code.replace(update_func_old, update_func_new)

code = code.replace("{activeTab === 
\rooms\' && <RoomTable rooms={solveData?.rooms || []} />}", "{activeTab === \rooms\' && <RoomTable rooms={solveData?.rooms || []} onUpdateRoom={handleLiveItemUpdate} />}")

with open("frontend/src/pages/EditorPage.jsx", "w", encoding="utf-8") as f:
    f.write(code)

