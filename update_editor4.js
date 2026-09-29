const fs = require('fs');

let code = fs.readFileSync('frontend/src/pages/EditorPage.jsx', 'utf-8');

// 1. Add "AddRoom" support to handleLiveItemUpdate
const updateFuncSearch = '} else if (itemType === "Room") {\n        newRooms = newRooms.map(r => r.name === itemId ? { ...r, ...updates } : r);\n    }';
const updateFuncReplace = '} else if (itemType === "Room") {\n        newRooms = newRooms.map(r => r.name === itemId ? { ...r, ...updates } : r);\n    } else if (itemType === "AddRoom") {\n        newRooms = [...newRooms, updates];\n    }';

if (code.includes(updateFuncSearch)) {
    code = code.replace(updateFuncSearch, updateFuncReplace);
}

// 2. Modify tabs rendering
const tabsSearch = `{activeTab === 'rooms' && <RoomTable rooms={solveData?.rooms || []} onUpdateRoom={handleLiveItemUpdate} />}
            {activeTab === 'openings' && (
              <OpeningsTable 
                doors={editableDoors.length > 0 ? editableDoors : (solveData?.doors || [])} 
                windows={editableWindows.length > 0 ? editableWindows : (solveData?.windows || [])}
                onUpdateOpening={handleUpdateOpening}
              />
            )}
            {activeTab === 'hvac' && (
              <HVACTable 
                loads={solveData?.hvac_loads || []} 
                equipment={editableHvac.length > 0 ? editableHvac : (solveData?.hvac_equipment || [])} 
                pipes={solveData?.hvac_pipes || []}
                onUpdateEquipment={handleUpdateEquipment}
              />
            )}`;

const tabsReplace = `{activeTab === 'rooms' && <RoomTable rooms={solveData?.rooms || []} onUpdateRoom={handleLiveItemUpdate} onAddRoom={(newRoom) => handleLiveItemUpdate('AddRoom', null, newRoom)} />}
            {activeTab === 'openings' && (
              <OpeningsTable 
                rooms={solveData?.rooms || []}
                doors={editableDoors.length > 0 ? editableDoors : (solveData?.doors || [])} 
                windows={editableWindows.length > 0 ? editableWindows : (solveData?.windows || [])}
                onUpdateOpening={handleLiveItemUpdate}
              />
            )}
            {activeTab === 'hvac' && (
              <HVACTable 
                rooms={solveData?.rooms || []}
                loads={solveData?.hvac_loads || []} 
                equipment={editableHvac.length > 0 ? editableHvac : (solveData?.hvac_equipment || [])} 
                pipes={solveData?.hvac_pipes || []}
                onUpdateEquipment={handleLiveItemUpdate}
              />
            )}`;

if (code.includes(tabsSearch)) {
    code = code.replace(tabsSearch, tabsReplace);
    fs.writeFileSync('frontend/src/pages/EditorPage.jsx', code);
    console.log("Successfully updated EditorPage.jsx tabs");
} else {
    console.log("Could not find tabs string to replace.");
}

