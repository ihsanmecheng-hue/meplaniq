
import React, { useState } from "react";

export default function RoomTable({ rooms, onUpdateRoom }) {
  if (!rooms || rooms.length === 0) {
    return (
      <div className="table-container empty">
        <p>No room geometry data available.</p>
      </div>
    );
  }

  return (
    <div className="table-container">
      <h3 className="table-title">Room Spatial Data Summary</h3>
      <table className="cad-table">
        <thead>
          <tr>
            <th>Room Name</th>
            <th>X (mm)</th>
            <th>Y (mm)</th>
            <th>Width (mm)</th>
            <th>Height (mm)</th>
            <th>Carpet Area (sq.m)</th>
            <th>Wall Thickness (mm)</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {rooms.map((room, index) => (
            <RoomRow key={room.name} room={room} index={index} onUpdateRoom={onUpdateRoom} />
          ))}
        </tbody>
      </table>
    </div>
  );
}

function RoomRow({ room, index, onUpdateRoom }) {
  // Infer geometry from points (assuming axis-aligned rectangle)
  const xs = room.points.map(p => p[0]);
  const ys = room.points.map(p => p[1]);
  const initialX = Math.min(...xs);
  const initialY = Math.min(...ys);
  const initialW = Math.max(...xs) - initialX;
  const initialH = Math.max(...ys) - initialY;

  const [editX, setEditX] = useState(initialX);
  const [editY, setEditY] = useState(initialY);
  const [editW, setEditW] = useState(initialW);
  const [editH, setEditH] = useState(initialH);

  const handleUpdate = () => {
    if (onUpdateRoom) {
      const newPoints = [
        [editX, editY],
        [editX + editW, editY],
        [editX + editW, editY + editH],
        [editX, editY + editH]
      ];
      onUpdateRoom("Room", room.name, { points: newPoints });
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") handleUpdate();
  };

  const inputStyle = { width: "60px", background: "#1E293B", border: "1px solid #475569", color: "white", padding: "4px", borderRadius: "4px" };

  return (
    <tr>
      <td className="room-name-cell">
        <span className="room-color-badge" style={{ backgroundColor: getRoomBadgeColor(index) }}></span>
        {room.name}
      </td>
      <td>
        <input type="number" value={editX} onChange={e => setEditX(Number(e.target.value))} onKeyDown={handleKeyDown} style={inputStyle} />
      </td>
      <td>
        <input type="number" value={editY} onChange={e => setEditY(Number(e.target.value))} onKeyDown={handleKeyDown} style={inputStyle} />
      </td>
      <td>
        <input type="number" value={editW} onChange={e => setEditW(Number(e.target.value))} onKeyDown={handleKeyDown} style={inputStyle} />
      </td>
      <td>
        <input type="number" value={editH} onChange={e => setEditH(Number(e.target.value))} onKeyDown={handleKeyDown} style={inputStyle} />
      </td>
      <td className="metric-cell">{room.carpet_area_sqm.toFixed(1)} sq.m</td>
      <td>{room.wall_thickness_mm} mm</td>
      <td>
        <button onClick={handleUpdate} style={{ background: "#3B82F6", color: "white", border: "none", padding: "4px 8px", borderRadius: "4px", cursor: "pointer", fontSize: "11px" }}>
          Update
        </button>
      </td>
    </tr>
  );
}

function getRoomBadgeColor(index) {
  const colors = ["#3B82F6", "#10B981", "#F59E0B", "#EC4899", "#8B5CF6"];
  return colors[index % colors.length];
}

