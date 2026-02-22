#!/usr/bin/env python3
from __future__ import annotations

from app.models.scenario import ScenarioName
from app.models.simulation import ControllerMode
from app.services.simulation import SimulationEngine, SimulationRequest


if __name__ == "__main__":
    engine = SimulationEngine()
    request = SimulationRequest(
        scenario=ScenarioName.night,
        controller=ControllerMode.max_pressure,
        compare=True,
        seed=42,
    )
    frames, result = engine.run(request, steps=30)
    print("Frames:", len(frames))
    print("Optimised avg delay:", result.optimised_metrics["avg_delay_s"])
    print("Explainability:", result.explainability)
