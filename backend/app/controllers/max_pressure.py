from __future__ import annotations

from app.models.simulation import IntersectionObservation


class MaxPressureController:
    def __init__(self, min_green: int = 8) -> None:
        self.min_green = min_green
        self.last_switch_step: dict[str, int] = {}

    def choose_phase(self, obs: IntersectionObservation, step: int) -> int:
        last = self.last_switch_step.get(obs.intersection_id, -10_000)
        if step - last < self.min_green:
            return obs.current_phase

        ns_pressure = obs.ns_queue
        ew_pressure = obs.ew_queue
        target = 0 if ns_pressure >= ew_pressure else 1
        if target != obs.current_phase:
            self.last_switch_step[obs.intersection_id] = step
        return target
