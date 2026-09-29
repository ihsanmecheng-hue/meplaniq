import re

with open("frontend/src/pages/EditorPage.jsx", "r", encoding="utf-8") as f:
    code = f.read()

# AddRoom support
code = code.replace('} else if (itemType === "Room") {\n        newRooms = newRooms.map(r => r.name === itemId ? { ...r, ...updates } : r);\n    }', '} else if (itemType === "Room") {\n        newRooms = newRooms.map(r => r.name === itemId ? { ...r, ...updates } : r);\n    } else if (itemType === "AddRoom") {\n        newRooms = [...newRooms, updates];\n    }')

# Tabs replace
pattern = re.compile(
    r"\{activeTab === 'rooms' && <RoomTable rooms=\{solveData\?\.rooms \|\| \[\]\} onUpdateRoom=\{handleLiveItemUpdate\} />\}.*?onUpdateEquipment=\{handleUpdateEquipment\}.*?/>\s*\)}",
    re.DOTALL
)

replacement = """{activeTab === 'rooms' && <RoomTable rooms={solveData?.rooms || []} onUpdateRoom={handleLiveItemUpdate} onAddRoom={(newRoom) => handleLiveItemUpdate('AddRoom', null, newRoom)} />}
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
            )}"""

code = pattern.sub(replacement, code)

with open("frontend/src/pages/EditorPage.jsx", "w", encoding="utf-8") as f:
    f.write(code)
print("Updated EditorPage successfully")
