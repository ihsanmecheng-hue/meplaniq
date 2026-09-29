
import re

with open("frontend/src/Canvas.jsx", "r", encoding="utf-8") as f:
    code = f.read()

overlay_old = """          <label style={{ display: "block", fontSize: 12, marginBottom: 4 }}>Width (mm)</label>
          <input 
            type="number" 
            defaultValue={selectedItem.item.width_mm} 
            onBlur={(e) => {
               if(onLiveItemUpdate) onLiveItemUpdate(selectedItem.type, selectedItem.item.id, { width_mm: Number(e.target.value) });
            }}
            style={{ width: "100%", background: "#1E293B", border: "1px solid #475569", color: "white", padding: "6px 8px", borderRadius: 4, marginBottom: 12 }}
          />"""
          
overlay_new = """          {selectedItem.type !== "HVAC" && (
            <>
              <label style={{ display: "block", fontSize: 12, marginBottom: 4 }}>Width (mm)</label>
              <input 
                type="number" 
                defaultValue={selectedItem.item.width_mm} 
                onBlur={(e) => {
                   if(onLiveItemUpdate) onLiveItemUpdate(selectedItem.type, selectedItem.item.id, { width_mm: Number(e.target.value) });
                }}
                style={{ width: "100%", background: "#1E293B", border: "1px solid #475569", color: "white", padding: "6px 8px", borderRadius: 4, marginBottom: 12 }}
              />
            </>
          )}

          {selectedItem.type === "HVAC" && (
            <>
              <label style={{ display: "block", fontSize: 12, marginBottom: 4 }}>Cooling Capacity (TR)</label>
              <input 
                type="number" 
                step="0.5"
                defaultValue={selectedItem.item.cooling_capacity_tr} 
                onBlur={(e) => {
                   if(onLiveItemUpdate) onLiveItemUpdate("HVAC", selectedItem.item.id, { cooling_capacity_tr: Number(e.target.value) });
                }}
                style={{ width: "100%", background: "#1E293B", border: "1px solid #475569", color: "white", padding: "6px 8px", borderRadius: 4, marginBottom: 12 }}
              />
            </>
          )}"""

code = code.replace(overlay_old, overlay_new)
with open("frontend/src/Canvas.jsx", "w", encoding="utf-8") as f:
    f.write(code)

