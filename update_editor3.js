const fs = require('fs');
let code = fs.readFileSync('frontend/src/pages/EditorPage.jsx', 'utf-8');
const oldStr = 'rooms: (solveData.rooms || []).map(r => ({';
const newStr = 'rooms: (solveData.rooms || []).map(r => ({'; // Actually, let\'s replace the whole function

const fullOld = `    const handleLiveItemUpdate = async (itemType, itemId, updates) => {
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
          rooms: (solveData.rooms || []).map(r => ({`;

const fullNew = `    const handleLiveItemUpdate = async (itemType, itemId, updates) => {
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
          rooms: newRooms.map(r => ({`;

if (code.includes(fullOld)) {
  code = code.replace(fullOld, fullNew);
  const oldTable = "{activeTab === 'rooms' && <RoomTable rooms={solveData?.rooms || []} />}";
  const newTable = "{activeTab === 'rooms' && <RoomTable rooms={solveData?.rooms || []} onUpdateRoom={handleLiveItemUpdate} />}";
  if(code.includes(oldTable)) {
      code = code.replace(oldTable, newTable);
  }
  fs.writeFileSync('frontend/src/pages/EditorPage.jsx', code);
  console.log('Update Successful');
} else {
  console.log('String not found');
}
