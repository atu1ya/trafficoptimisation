from __future__ import annotations

from app.models.simulation import IntersectionObservation


class GreenWaveController:
    def __init__(self, corridor: list[str], cycle_seconds: int = 90, target_speed_kph: int = 45) -> None:
        self.corridor = corridor
        self.offsets = {node: idx * 7 for idx, node in enumerate(corridor)}
        self.cycle_seconds = cycle_seconds
        self.target_speed_kph = target_speed_kph

    def choose_phase(self, obs: IntersectionObservation, step: int) -> int:
        offset = self.offsets.get(obs.intersection_id, 0)
        position = (step + offset) % self.cycle_seconds
        planned = 0 if position < int(self.cycle_seconds * 0.6) else 1
        imbalance = obs.ew_queue - obs.ns_queue
        if imbalance > 6:
            return 1
        if imbalance < -6:
            return 0
        return planned
