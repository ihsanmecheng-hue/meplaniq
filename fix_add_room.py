import re

with open("frontend/src/RoomTable.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old_func_pattern = re.compile(r"const handleAddNewRoom = \(\) => \{.*?setNewRoomName\(\"Room \" \+ \(rooms\.length \+ 1\)\);\s*\}\s*\};", re.DOTALL)

new_func = """const handleAddNewRoom = () => {
    // 1. Defensive type-checking and fallbacks
    const name = newRoomName.trim();
    if (!name) {
      alert("Room name cannot be empty.");
      return;
    }
    const x = Number(newRoomX) || 0;
    const y = Number(newRoomY) || 0;
    const w = Number(newRoomW) || 3000;
    const h = Number(newRoomH) || 3000;
    
    if (w <= 0 || h <= 0) {
      alert("Room width and height must be positive values.");
      return;
    }

    if (onAddRoom) {
      const pts = [
        [x, y],
        [x + w, y],
        [x + w, y + h],
        [x, y + h]
      ];
      
      // 2. Safely trigger backend synchronization
      onAddRoom({ name, points: pts });
      
      // 3. Reset input fields back to their default states
      setNewRoomName("Room " + (rooms.length + 1));
      setNewRoomX(0);
      setNewRoomY(0);
      setNewRoomW(3000);
      setNewRoomH(3000);
    }
  };"""

updated_content = old_func_pattern.sub(new_func, content)

with open("frontend/src/RoomTable.jsx", "w", encoding="utf-8") as f:
    f.write(updated_content)

print("RoomTable updated successfully.")
