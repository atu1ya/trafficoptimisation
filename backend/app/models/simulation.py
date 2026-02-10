from __future__ import annotations

from enum import Enum
from pydantic import BaseModel


class ControllerMode(str, Enum):
    night_fixed = "night_fixed"
    scenario_fixed = "scenario_fixed"
    max_pressure = "max_pressure"
    green_wave = "green_wave"


class SignalState(BaseModel):
    intersection_id: str
    phase: int
    elapsed: int


class IntersectionObservation(BaseModel):
    intersection_id: str
    ns_queue: int
    ew_queue: int
    current_phase: int


class SimulationFrame(BaseModel):
    step: int
    controller: ControllerMode
    network_delay_s: float
    avg_speed_kph: float
    throughput: int
    highlighted_vehicle_progress: float
    top_decisions: list[str]


class ComparisonResult(BaseModel):
    baseline_metrics: dict[str, float]
    optimised_metrics: dict[str, float]
    route_metrics: dict[str, float]
    explainability: list[str]
