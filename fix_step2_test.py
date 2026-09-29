
def test_step_2_wall_thickness_and_miter_fusing():
    from backend.geometry import RoomPayload, process_geometry_solve_v2, SolveRequest
    from shapely.geometry import Polygon
    
    # 2 rooms next to each other
    rooms = [
        RoomPayload(name="Room A", points=[[0, 0], [3000, 0], [3000, 3000], [0, 3000]]),
        RoomPayload(name="Room B", points=[[3115, 0], [6115, 0], [6115, 3000], [3115, 3000]])
    ]
    req = SolveRequest(rooms=rooms)
    resp = process_geometry_solve_v2(req)
    
    all_xs = []
    all_ys = []
    for wp in resp.wall_polygons:
        poly = Polygon(wp.outer_polygon, wp.inner_polygons)
        assert poly.is_valid is True, "Wall polygon is not topologically valid!"
        for p in wp.outer_polygon:
            all_xs.append(p[0])
            all_ys.append(p[1])
            
    assert min(all_xs) == -230.0
    assert max(all_xs) == 6345.0
    assert min(all_ys) == -230.0
    assert max(all_ys) == 3230.0
    
    # Find the party wall
    party_wall = None
    for wp in resp.wall_polygons:
        xs = [p[0] for p in wp.outer_polygon]
        if min(xs) >= 3000.0 and max(xs) <= 3115.0:
            party_wall = wp
            break
            
    assert party_wall is not None

