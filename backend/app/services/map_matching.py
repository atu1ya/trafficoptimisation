from __future__ import annotations

import hashlib
from dataclasses import dataclass


@dataclass
class MatchedPoint:
    edge_id: str
    snapped_lat: float
    snapped_lon: float


def match_coordinate_to_edge(lat: float, lon: float) -> MatchedPoint:
    digest = hashlib.md5(f"{lat:.5f},{lon:.5f}".encode()).hexdigest()[:8]
    return MatchedPoint(edge_id=f"edge_{digest}", snapped_lat=lat, snapped_lon=lon)


def compute_route(start_edge: str, end_edge: str) -> list[str]:
    return [start_edge, "edge_connector_a", "edge_connector_b", end_edge]
