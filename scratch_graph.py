import math
from typing import List, Dict, Any, Tuple, Set
from pydantic import BaseModel
from shapely import STRtree
from shapely.geometry import Polygon, box

class RoomPayload(BaseModel):
    name: str
    points: List[List[float]]
    fillet_radius: float = 0.0

class SpatialNode:
    def __init__(self, idx: int, name: str, points: List[List[float]], bounds: Tuple[float, float, float, float]):
        self.idx = idx
        self.name = name
        self.points = points
        self.minx, self.miny, self.maxx, self.maxy = bounds
        self.width = self.maxx - self.minx
        self.height = self.maxy - self.miny
        self.is_external_wing = False
        self.solved_x = self.minx
        self.solved_y = self.miny

class SpatialEdge:
    def __init__(self, from_node: int, to_node: int, axis: str, weight: float, overlap_span: float):
        self.from_node = from_node
        self.to_node = to_node
        self.axis = axis
        self.weight = weight
        self.overlap_span = overlap_span

class SpatialGraph:
    def __init__(self, rooms: List[RoomPayload], tolerance_mm: float = 10.0, gap_mm: float = 115.0):
        self.tolerance_mm = tolerance_mm
        self.gap_mm = gap_mm
        self.nodes: List[SpatialNode] = []
        self.edges_x: List[SpatialEdge] = []
        self.edges_y: List[SpatialEdge] = []
        
        for idx, r in enumerate(rooms):
            xs = [p[0] for p in r.points]
            ys = [p[1] for p in r.points]
            bounds = (min(xs), min(ys), max(xs), max(ys))
            node = SpatialNode(idx, r.name, r.points, bounds)
            # Classification of external wing
            lower_name = r.name.lower()
            if any(w in lower_name for w in ["porch", "garage", "patio", "balcony", "deck", "verandah"]):
                node.is_external_wing = True
            self.nodes.append(node)
            
        self._build_graph()

    def _build_graph(self):
        polygons = [box(n.minx, n.miny, n.maxx, n.maxy) for n in self.nodes]
        tree = STRtree(polygons)
        
        for idx_i, node_i in enumerate(self.nodes):
            # Query expanded bounding box to find neighbors within tolerance
            query_box = box(
                node_i.minx - self.tolerance_mm - 1.0, 
                node_i.miny - self.tolerance_mm - 1.0, 
                node_i.maxx + self.tolerance_mm + 1.0, 
                node_i.maxy + self.tolerance_mm + 1.0
            )
            neighbor_indices = tree.query(query_box)
            
            for idx_j in neighbor_indices:
                if idx_i == idx_j:
                    continue
                node_j = self.nodes[idx_j]
                
                # Check X adjacency (j is to the right of i)
                y_overlap = min(node_i.maxy, node_j.maxy) - max(node_i.miny, node_j.miny)
                if y_overlap > self.tolerance_mm:
                    dist_x = node_j.minx - node_i.maxx
                    if -self.tolerance_mm <= dist_x <= self.gap_mm + self.tolerance_mm:
                        self.edges_x.append(SpatialEdge(idx_i, idx_j, 'X', self.gap_mm, y_overlap))
                        
                # Check Y adjacency (j is above i)
                x_overlap = min(node_i.maxx, node_j.maxx) - max(node_i.minx, node_j.minx)
                if x_overlap > self.tolerance_mm:
                    dist_y = node_j.miny - node_i.maxy
                    if -self.tolerance_mm <= dist_y <= self.gap_mm + self.tolerance_mm:
                        self.edges_y.append(SpatialEdge(idx_i, idx_j, 'Y', self.gap_mm, x_overlap))

    def _topological_sort(self, edges: List[SpatialEdge]) -> List[int]:
        adj = {i: [] for i in range(len(self.nodes))}
        in_degree = {i: 0 for i in range(len(self.nodes))}
        for e in edges:
            adj[e.from_node].append(e.to_node)
            in_degree[e.to_node] += 1
            
        queue = [i for i in range(len(self.nodes)) if in_degree[i] == 0]
        
        topo_order = []
        while queue:
            queue.sort(key=lambda idx: self.nodes[idx].minx + self.nodes[idx].miny)
            u = queue.pop(0)
            topo_order.append(u)
            for v in adj[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)
                    
        return topo_order

    def solve(self):
        topo_x = self._topological_sort(self.edges_x)
        topo_y = self._topological_sort(self.edges_y)
        
        # Solve X
        adj_x = {i: [] for i in range(len(self.nodes))}
        for e in self.edges_x:
            adj_x[e.from_node].append(e)
            
        for u in topo_x:
            for e in adj_x[u]:
                v = e.to_node
                needed_x = self.nodes[u].solved_x + self.nodes[u].width + e.weight
                if needed_x > self.nodes[v].solved_x:
                    self.nodes[v].solved_x = needed_x
                    
        # Solve Y
        adj_y = {i: [] for i in range(len(self.nodes))}
        for e in self.edges_y:
            adj_y[e.from_node].append(e)
            
        for u in topo_y:
            for e in adj_y[u]:
                v = e.to_node
                needed_y = self.nodes[u].solved_y + self.nodes[u].height + e.weight
                if needed_y > self.nodes[v].solved_y:
                    self.nodes[v].solved_y = needed_y

        offsets = []
        for node in self.nodes:
            sx = node.solved_x - node.minx
            sy = node.solved_y - node.miny
            offsets.append((sx, sy))
            
        return offsets


if __name__ == "__main__":
    rooms = [
        RoomPayload(name="Room 1", points=[[0,0], [1000,0], [1000,1000], [0,1000]]),
        RoomPayload(name="Room 2", points=[[1000,0], [2000,0], [2000,1000], [1000,1000]]),
    ]
    graph = SpatialGraph(rooms)
    offsets = graph.solve()
    print("Offsets:", offsets)
