from __future__ import annotations

import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from app.core.config import get_settings
from app.models.scenario import SCENARIOS, ScenarioName
from app.models.simulation import ControllerMode
from app.services.benchmark import benchmark_google
from app.services.map_matching import compute_route, match_coordinate_to_edge
from app.services.simulation import SimulationEngine, SimulationRequest

router = APIRouter()
engine = SimulationEngine()


class RouteRequest(BaseModel):
    start_lat: float
    start_lon: float
    end_lat: float
    end_lon: float


class SimRequest(BaseModel):
    scenario: ScenarioName
    controller: ControllerMode
    compare: bool = True
    seed: int = 42
    steps: int = 120


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/api/scenarios")
def list_scenarios():
    return [sc.model_dump() for sc in SCENARIOS.values()]


@router.post("/api/route")
def route(req: RouteRequest):
    start = match_coordinate_to_edge(req.start_lat, req.start_lon)
    end = match_coordinate_to_edge(req.end_lat, req.end_lon)
    return {
        "start": start.__dict__,
        "end": end.__dict__,
        "route_edges": compute_route(start.edge_id, end.edge_id),
    }


@router.post("/api/simulate")
def simulate(req: SimRequest):
    frames, comparison = engine.run(
        SimulationRequest(scenario=req.scenario, controller=req.controller, compare=req.compare, seed=req.seed), req.steps
    )
    return {"frames": [f.model_dump() for f in frames], "comparison": comparison.model_dump()}


@router.get("/api/benchmark")
def benchmark(start: str, end: str):
    settings = get_settings()
    return benchmark_google(start, end, settings.google_maps_api_key)


@router.websocket("/ws/simulate")
async def simulate_ws(ws: WebSocket):
    await ws.accept()
    settings = get_settings()
    try:
        payload = await ws.receive_json()
        req = SimRequest(**payload)
        frames, comparison = engine.run(
            SimulationRequest(scenario=req.scenario, controller=req.controller, compare=req.compare, seed=req.seed), req.steps
        )
        for frame in frames:
            await ws.send_json({"type": "frame", "data": frame.model_dump()})
            await asyncio.sleep(settings.websocket_tick_ms / 1000)
        await ws.send_json({"type": "summary", "data": comparison.model_dump()})
    except WebSocketDisconnect:
        return
