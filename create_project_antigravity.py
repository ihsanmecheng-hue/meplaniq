import json
from datetime import datetime, timezone
from backend.database import save_project, init_db
from backend.geometry import process_geometry_solve_v2, RoomPayload, OpeningPayload, HVACEquipmentPayload, FurniturePayload
from backend.models import PlumbingFixturePayload, PlumbingPipePayload

init_db()

# Rooms
rooms = [
    RoomPayload(name="Living Room", points=[[0,0], [4000,0], [4000,5000], [0,5000]]),
    RoomPayload(name="Master Bedroom", points=[[4000,0], [8000,0], [8000,4000], [4000,4000]]),
    RoomPayload(name="Bathroom", points=[[4000,4000], [8000,4000], [8000,6000], [4000,6000]]),
    RoomPayload(name="Kitchen", points=[[0,5000], [4000,5000], [4000,8000], [0,8000]]),
    RoomPayload(name="Utility", points=[[0,8000], [4000,8000], [4000,10000], [0,10000]])
]

# Doors/Windows
openings = [
    OpeningPayload(id="D1", type="Door", host_room="Living Room", wall_side="Right", offset_mm=2000, width_mm=900),
    OpeningPayload(id="D2", type="Door", host_room="Master Bedroom", wall_side="Bottom", offset_mm=2000, width_mm=800),
    OpeningPayload(id="D3", type="Door", host_room="Living Room", wall_side="Top", offset_mm=2000, width_mm=900),
    OpeningPayload(id="D4", type="Door", host_room="Kitchen", wall_side="Top", offset_mm=2000, width_mm=800),
]

# HVAC
hvac = [
    HVACEquipmentPayload(id="ODU-1", unit_type="Split-ODU", cooling_capacity_tr=3.0, location_x=9000, location_y=1000, room_name=""),
    HVACEquipmentPayload(id="IDU-1", unit_type="Split-IDU", cooling_capacity_tr=1.5, location_x=2000, location_y=1000, room_name="Living Room"),
    HVACEquipmentPayload(id="IDU-2", unit_type="Split-IDU", cooling_capacity_tr=1.5, location_x=6000, location_y=1000, room_name="Master Bedroom")
]

# Furniture
furniture = [
    FurniturePayload(id="F1", type="Bed", category="Bedroom", width=1800, height=2000, x=6000, y=2000, rotation=0, host_room_id="Master Bedroom"),
    FurniturePayload(id="F2", type="Sofa", category="Living", width=2000, height=900, x=2000, y=4000, rotation=180, host_room_id="Living Room"),
]

# Plumbing (Dual Line - Water Supply & Drainage with Trimmed Endpoints)
plumbing_pipes = [
    # Bathroom Pipes (Trimmed: 3900 to fixture port)
    PlumbingPipePayload(id="WTR-1", type="Water Supply Pipe", host_room_id="Bathroom", diameter=20, path=[[3900, 4100], [5888, 4100]], connected_to="WTR-MAIN"),
    PlumbingPipePayload(id="DRN-1", type="Drainage Pipe", host_room_id="Bathroom", diameter=110, path=[[3950, 4200], [6112, 4200]], connected_to="DRN-MAIN"),
    # Kitchen Pipes (Trimmed: fixture port to 3900)
    PlumbingPipePayload(id="WTR-2", type="Water Supply Pipe", host_room_id="Kitchen", diameter=20, path=[[1776, 5100], [3900, 5100]], connected_to="WTR-MAIN"),
    PlumbingPipePayload(id="DRN-2", type="Drainage Pipe", host_room_id="Kitchen", diameter=50, path=[[2224, 5200], [3950, 5200]], connected_to="DRN-MAIN"),
    # Utility Pipes (Trimmed: fixture port to 3900)
    PlumbingPipePayload(id="WTR-3", type="Water Supply Pipe", host_room_id="Utility", diameter=20, path=[[1832, 8100], [3900, 8100]], connected_to="WTR-MAIN"),
    PlumbingPipePayload(id="DRN-3", type="Drainage Pipe", host_room_id="Utility", diameter=50, path=[[2168, 8200], [3950, 8200]], connected_to="DRN-MAIN"),
    # Main Vertical Interconnected Trunk Risers (strictly bounded between Bathroom & Utility)
    PlumbingPipePayload(id="WTR-MAIN", type="Water Supply Pipe", host_room_id="Kitchen", diameter=32, path=[[3900, 4100], [3900, 8100]], connected_to="City Water Main"),
    PlumbingPipePayload(id="DRN-MAIN", type="Drainage Pipe", host_room_id="Kitchen", diameter=110, path=[[3950, 4200], [3950, 8200]], connected_to="Building Sewer Main"),
]

plumbing_fixtures = [
    PlumbingFixturePayload(id="PLM-1", type="WC", category="Toilet", width=400, height=600, x=6000, y=4500, rotation=0, host_room_id="Bathroom", supplyPipeId="WTR-1", drainagePipeId="DRN-1"),
    PlumbingFixturePayload(id="PLM-2", type="Kitchen Sink", category="Sink", width=800, height=500, x=2000, y=6500, rotation=0, host_room_id="Kitchen", supplyPipeId="WTR-2", drainagePipeId="DRN-2"),
    PlumbingFixturePayload(id="PLM-3", type="Washing Machine", category="Appliance", width=600, height=600, x=2000, y=9000, rotation=0, host_room_id="Utility", supplyPipeId="WTR-3", drainagePipeId="DRN-3"),
]

# Process CAD
result = process_geometry_solve_v2(rooms, openings, hvac, furniture, plumbing_fixtures, plumbing_pipes)

project_id = "project-antigravity"
save_project(
    project_id=project_id,
    name="Project AntiGravity",
    cad_dict=result.model_dump(),
    created_at=datetime.now(timezone.utc).isoformat()
)
print("Project AntiGravity initialized!")
