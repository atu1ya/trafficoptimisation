from pydantic import ValidationError
import pytest

from app.models.scenario import ScenarioConfig, ScenarioName


def test_scenario_validation_rejects_high_std():
    with pytest.raises(ValidationError):
        ScenarioConfig(
            name=ScenarioName.night,
            demand_intensity=1,
            speed_compliance_mean=1,
            speed_compliance_std=0.45,
            accel_mean=2,
            decel_mean=3,
            driver_imperfection=0.2,
            fixed_cycle_seconds=80,
            arterial_green_split=0.5,
        )
