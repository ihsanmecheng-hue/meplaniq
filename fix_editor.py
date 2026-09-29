
import re

with open("frontend/src/pages/EditorPage.jsx", "r", encoding="utf-8") as f:
    code = f.read()

pattern = re.compile(
    r"(const handleLiveItemUpdate.*?let newHvac = .*?;).*?(if \(!solveData\?\.project_id\).*?rooms: \(solveData\.rooms \|\| \[\]\)\.map\(r => \(\{)",
    re.DOTALL
)

def replacer(match):
    return match.group(1) + """
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

      """ + match.group(2).replace("(solveData.rooms || [])", "newRooms")

new_code = pattern.sub(replacer, code)

new_code = new_code.replace(
    "{activeTab === 
rooms && <RoomTable rooms={solveData?.rooms || []} />}",
    "{activeTab === rooms && <RoomTable rooms={solveData?.rooms || []} onUpdateRoom={handleLiveItemUpdate} />}"
)

with open("frontend/src/pages/EditorPage.jsx", "w", encoding="utf-8") as f:
    f.write(new_code)

