
import json
import urllib.request

payload = {
  "name": "Antigravity Project",
  "rooms": [
    {
      "name": "Living Room",
      "points": [[0, 0], [6000, 0], [6000, 5000], [0, 5000]]
    },
    {
      "name": "Kitchen",
      "points": [[6000, 0], [10000, 0], [10000, 5000], [6000, 5000]]
    },
    {
      "name": "Master Bedroom",
      "points": [[0, 5000], [4500, 5000], [4500, 10000], [0, 10000]]
    },
    {
      "name": "Master Bath",
      "points": [[4500, 5000], [7000, 5000], [7000, 8000], [4500, 8000]]
    },
    {
      "name": "Hallway Laundry",
      "points": [[4500, 8000], [7000, 8000], [7000, 10000], [4500, 10000]]
    },
    {
      "name": "Guest Bedroom",
      "points": [[7000, 5000], [10000, 5000], [10000, 10000], [7000, 10000]]
    }
  ],
  "openings": [
    {
      "id": "D-Front",
      "host_room": "Living Room",
      "wall_side": "Bottom",
      "offset_mm": 2500,
      "width_mm": 1000,
      "height_mm": 2100,
      "type": "Door",
      "swing": "Inward-Right"
    },
    {
      "id": "D-Kit",
      "host_room": "Living Room",
      "wall_side": "Right",
      "offset_mm": 2000,
      "width_mm": 900,
      "height_mm": 2100,
      "type": "Door",
      "swing": "Inward-Right"
    },
    {
      "id": "D-MBed",
      "host_room": "Living Room",
      "wall_side": "Top",
      "offset_mm": 500,
      "width_mm": 900,
      "height_mm": 2100,
      "type": "Door",
      "swing": "Inward-Left"
    },
    {
      "id": "D-MBath",
      "host_room": "Master Bedroom",
      "wall_side": "Right",
      "offset_mm": 500,
      "width_mm": 800,
      "height_mm": 2100,
      "type": "Door",
      "swing": "Inward-Right"
    },
    {
      "id": "D-Guest",
      "host_room": "Kitchen",
      "wall_side": "Top",
      "offset_mm": 2000,
      "width_mm": 900,
      "height_mm": 2100,
      "type": "Door",
      "swing": "Inward-Left"
    },
    {
      "id": "D-Hall",
      "host_room": "Guest Bedroom",
      "wall_side": "Left",
      "offset_mm": 3500,
      "width_mm": 800,
      "height_mm": 2100,
      "type": "Door",
      "swing": "Inward-Right"
    },
    {
      "id": "W-Liv1",
      "host_room": "Living Room",
      "wall_side": "Left",
      "offset_mm": 2000,
      "width_mm": 1500,
      "height_mm": 1200,
      "type": "Window"
    },
    {
      "id": "W-Liv2",
      "host_room": "Living Room",
      "wall_side": "Bottom",
      "offset_mm": 500,
      "width_mm": 1500,
      "height_mm": 1200,
      "type": "Window"
    },
    {
      "id": "W-Kit",
      "host_room": "Kitchen",
      "wall_side": "Bottom",
      "offset_mm": 1500,
      "width_mm": 1200,
      "height_mm": 1200,
      "type": "Window"
    },
    {
      "id": "W-MBed",
      "host_room": "Master Bedroom",
      "wall_side": "Left",
      "offset_mm": 2000,
      "width_mm": 1500,
      "height_mm": 1200,
      "type": "Window"
    },
    {
      "id": "W-GBed1",
      "host_room": "Guest Bedroom",
      "wall_side": "Right",
      "offset_mm": 2000,
      "width_mm": 1500,
      "height_mm": 1200,
      "type": "Window"
    },
    {
      "id": "W-GBed2",
      "host_room": "Guest Bedroom",
      "wall_side": "Top",
      "offset_mm": 1000,
      "width_mm": 1500,
      "height_mm": 1200,
      "type": "Window"
    },
    {
      "id": "W-Hall",
      "host_room": "Hallway Laundry",
      "wall_side": "Top",
      "offset_mm": 1000,
      "width_mm": 800,
      "height_mm": 800,
      "type": "Window"
    }
  ],
  "hvac_equipment": [
    {
      "id": "IDU-Living",
      "room_name": "Living Room",
      "unit_type": "Split-IDU",
      "location_x": 3000,
      "location_y": 100,
      "cooling_capacity_tr": 2.0,
      "status": "Active"
    },
    {
      "id": "IDU-MBed",
      "room_name": "Master Bedroom",
      "unit_type": "Split-IDU",
      "location_x": 2250,
      "location_y": 9800,
      "cooling_capacity_tr": 1.5,
      "status": "Active"
    },
    {
      "id": "IDU-GBed",
      "room_name": "Guest Bedroom",
      "unit_type": "Split-IDU",
      "location_x": 8500,
      "location_y": 9800,
      "cooling_capacity_tr": 1.0,
      "status": "Active"
    },
    {
      "id": "ODU-Main",
      "room_name": "Master Bedroom",
      "unit_type": "VRF-ODU",
      "location_x": -1000,
      "location_y": 9000,
      "cooling_capacity_tr": 4.5,
      "status": "Active"
    },
    {
      "id": "EXH-Bath",
      "room_name": "Master Bath",
      "unit_type": "Exhaust-Fan",
      "location_x": 5750,
      "location_y": 6500,
      "cooling_capacity_tr": 0.0,
      "status": "Active"
    }
  ]
}

req = urllib.request.Request("http://127.0.0.1:8000/api/projects/manual", data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req) as response:
    print(response.status)
    data = json.loads(response.read().decode())
    print("Project ID:", data.get("project_id"))

