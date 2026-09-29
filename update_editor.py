import re

with open("frontend/src/pages/EditorPage.jsx", "r", encoding="utf-8") as f:
    code = f.read()

old_code = """  const handleLiveItemUpdate = async (itemType, itemId, updates) => {
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

new_code = """  const handleLiveItemUpdate = async (itemType, itemId, updates) => {
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

def normalize(s):
    return re.sub(r'\s+', ' ', s)

for i in range(len(code)):
    for j in range(i+1, min(i+2000, len(code))):
        if normalize(code[i:j]) == normalize(old_code):
            code = code[:i] + new_code + code[j:]
            print("Successfully replaced handleLiveItemUpdate")
            break
    else:
        continue
    break

code = code.replace("{activeTab === 'rooms' && <RoomTable rooms={solveData?.rooms || []} />}", "{activeTab === 'rooms' && <RoomTable rooms={solveData?.rooms || []} onUpdateRoom={handleLiveItemUpdate} />}")

with open("frontend/src/pages/EditorPage.jsx", "w", encoding="utf-8") as f:
    f.write(code)
