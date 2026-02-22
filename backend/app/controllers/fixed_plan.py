from __future__ import annotations

from app.models.simulation import IntersectionObservation


class FixedPlanController:
    def __init__(self, cycle_seconds: int, arterial_green_split: float) -> None:
        self.cycle_seconds = cycle_seconds
        self.arterial_green_split = arterial_green_split

    def choose_phase(self, obs: IntersectionObservation, step: int) -> int:
        ns_window = int(self.cycle_seconds * self.arterial_green_split)
        cycle_position = step % self.cycle_seconds
        return 0 if cycle_position < ns_window else 1
