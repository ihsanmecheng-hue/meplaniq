import re

with open("frontend/src/pages/EditorPage.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update handleLiveItemUpdate
target_search = """    } else if (itemType === "AddRoom") {
      newRooms = [...newRooms, updates];
    }"""

target_replace = """    } else if (itemType === "AddRoom") {
      newRooms = [...newRooms, updates];
    } else if (itemType === "AddOpening" || itemType === "AddDoor" || itemType === "AddWindow") {
      const isDoor = itemType === "AddDoor" || updates.type === "Door" || updates.kind === "Door";
      if (isDoor) {
        newDoors = [...newDoors, { ...updates, type: "Door" }];
        setEditableDoors(newDoors);
      } else {
        newWindows = [...newWindows, { ...updates, type: "Window" }];
        setEditableWindows(newWindows);
      }
    } else if (itemType === "DeleteOpening") {
      newDoors = newDoors.filter(d => d.id !== itemId);
      newWindows = newWindows.filter(w => w.id !== itemId);
      setEditableDoors(newDoors);
      setEditableWindows(newWindows);
    }"""

content = content.replace(target_search, target_replace)

# 2. Update toast logic
toast_search = """showToast(itemType === "AddRoom" ? `Room '${updates.name}' added successfully!` : "Plan updated successfully!", "success");"""
toast_replace = """let toastMsg = "Plan updated successfully!";
        if (itemType === "AddRoom") toastMsg = `Room '${updates.name}' added successfully!`;
        else if (itemType === "AddOpening" || itemType === "AddDoor" || itemType === "AddWindow") {
          const kind = updates.type || (itemType === "AddDoor" ? "Door" : "Window");
          toastMsg = `${kind} '${updates.id}' added to ${updates.host_room}!`;
        } else if (itemType === "DeleteOpening") {
          toastMsg = `Opening '${itemId}' removed!`;
        }
        showToast(toastMsg, "success");"""

content = content.replace(toast_search, toast_replace)

# 3. Update OpeningsTable invocation
table_search = """          {activeTab === 'openings' && (
            <OpeningsTable 
              rooms={solveData?.rooms || []}
              doors={editableDoors.length > 0 ? editableDoors : (solveData?.doors || [])} 
              windows={editableWindows.length > 0 ? editableWindows : (solveData?.windows || [])}
              onUpdateOpening={handleLiveItemUpdate}
            />
          )}"""

table_replace = """          {activeTab === 'openings' && (
            <OpeningsTable 
              rooms={solveData?.rooms || []}
              doors={editableDoors.length > 0 ? editableDoors : (solveData?.doors || [])} 
              windows={editableWindows.length > 0 ? editableWindows : (solveData?.windows || [])}
              onUpdateOpening={handleLiveItemUpdate}
              onAddOpening={(newOpening) => handleLiveItemUpdate("AddOpening", null, newOpening)}
            />
          )}"""

content = content.replace(table_search, table_replace)

with open("frontend/src/pages/EditorPage.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("EditorPage.jsx updated for Doors and Windows management.")
