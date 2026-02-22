from app.controllers.max_pressure import MaxPressureController
from app.models.simulation import IntersectionObservation


def test_max_pressure_deterministic_decision():
    controller = MaxPressureController(min_green=0)
    obs = IntersectionObservation(intersection_id="i1", ns_queue=12, ew_queue=4, current_phase=1)
    assert controller.choose_phase(obs, step=10) == 0
