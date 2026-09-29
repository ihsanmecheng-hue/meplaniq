import re

with open("frontend/src/pages/EditorPage.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update imports
if "createManualProject" not in content:
    content = content.replace(
        "updateProjectById\n} from '../api';",
        "updateProjectById,\n  createManualProject\n} from '../api';"
    )
    if "createManualProject" not in content:
        content = content.replace(
            "updateProjectById",
            "updateProjectById, createManualProject"
        )

# 2. Replace handleLiveItemUpdate
old_handle_pattern = re.compile(
    r"const handleLiveItemUpdate = async \(itemType, itemId, updates\) => \{.*?\n  \};\n\n  const handleUpdateOpening",
    re.DOTALL
)

new_handle = """const handleLiveItemUpdate = async (itemType, itemId, updates) => {
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
      if (updates && updates.name && updates.name !== itemId) {
        newDoors = newDoors.map(d => d.host_room === itemId ? { ...d, host_room: updates.name } : d);
        newWindows = newWindows.map(w => w.host_room === itemId ? { ...w, host_room: updates.name } : w);
        newHvac = newHvac.map(h => h.room_name === itemId ? { ...h, room_name: updates.name } : h);
        setEditableDoors(newDoors);
        setEditableWindows(newWindows);
        setEditableHvac(newHvac);
      }
    } else if (itemType === "AddRoom") {
      newRooms = [...newRooms, updates];
    }

    const updatePayload = {
      name: solveData?.project_name || "Floorplan",
      rooms: newRooms.map(r => ({
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
        location_x: Number(h.location_x ?? h.x ?? 0),
        location_y: Number(h.location_y ?? h.y ?? 0),
        cooling_capacity_tr: Number(h.cooling_capacity_tr ?? h.capacity_tr ?? 1.5),
        status: h.status ?? "Active"
      }))
    };

    try {
      const currentProjectId = solveData?.project_id || projectId;
      let updated;
      if (currentProjectId) {
        updated = await updateProjectById(currentProjectId, updatePayload);
      } else {
        updated = await createManualProject(updatePayload);
      }
      if (updated) {
        setSolveData(updated);
        setEditableDoors(updated.doors || []);
        setEditableWindows(updated.windows || []);
        setEditableHvac(updated.hvac_equipment || []);
        if (!currentProjectId && updated.project_id) {
          navigate(`/editor/${updated.project_id}`, { replace: true });
        }
        showToast(itemType === "AddRoom" ? `Room '${updates.name}' added successfully!` : "Plan updated successfully!", "success");
      }
    } catch (err) {
      console.error("Live sync failed", err);
      showToast(err.message || "Failed to update floorplan geometry.", "error");
    }
  };

  const handleUpdateOpening"""

content = old_handle_pattern.sub(new_handle, content)

# 3. Replace Tabs rendering at bottom
old_tabs_pattern = re.compile(
    r"\{activeTab === 'rooms' && <RoomTable rooms=\{solveData\?\.rooms \|\| \[\]\} onUpdateRoom=\{handleLiveItemUpdate\} />\}.*?</main>",
    re.DOTALL
)

new_tabs = """{activeTab === 'rooms' && (
            <RoomTable 
              rooms={solveData?.rooms || []} 
              onUpdateRoom={handleLiveItemUpdate}
              onAddRoom={(newRoom) => handleLiveItemUpdate("AddRoom", null, newRoom)}
            />
          )}
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
          )}
        </main>"""

content = old_tabs_pattern.sub(new_tabs, content)

with open("frontend/src/pages/EditorPage.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("EditorPage.jsx updated successfully!")
