from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field, field_validator


class ScenarioName(str, Enum):
    night = "night"
    off_peak_morning = "off_peak_morning"
    afternoon_medium = "afternoon_medium"
    peak_rush_hour = "peak_rush_hour"
    incident_mode = "incident_mode"


class ScenarioConfig(BaseModel):
    name: ScenarioName
    demand_intensity: float = Field(ge=0.1, le=5.0)
    speed_compliance_mean: float = Field(ge=0.5, le=1.2)
    speed_compliance_std: float = Field(ge=0.0, le=0.5)
    accel_mean: float = Field(ge=0.5, le=4.0)
    decel_mean: float = Field(ge=0.5, le=6.0)
    driver_imperfection: float = Field(ge=0.0, le=1.0)
    fixed_cycle_seconds: int = Field(ge=40, le=180)
    arterial_green_split: float = Field(ge=0.2, le=0.8)

    @field_validator("speed_compliance_std")
    @classmethod
    def std_guard(cls, value: float) -> float:
        if value > 0.4:
            raise ValueError("speed_compliance_std too high for stable demo")
        return value


SCENARIOS: dict[ScenarioName, ScenarioConfig] = {
    ScenarioName.night: ScenarioConfig(
        name=ScenarioName.night,
        demand_intensity=0.8,
        speed_compliance_mean=1.0,
        speed_compliance_std=0.05,
        accel_mean=2.2,
        decel_mean=3.5,
        driver_imperfection=0.15,
        fixed_cycle_seconds=70,
        arterial_green_split=0.55,
    ),
    ScenarioName.off_peak_morning: ScenarioConfig(
        name=ScenarioName.off_peak_morning,
        demand_intensity=1.0,
        speed_compliance_mean=0.97,
        speed_compliance_std=0.08,
        accel_mean=2.0,
        decel_mean=3.2,
        driver_imperfection=0.2,
        fixed_cycle_seconds=80,
        arterial_green_split=0.58,
    ),
    ScenarioName.afternoon_medium: ScenarioConfig(
        name=ScenarioName.afternoon_medium,
        demand_intensity=1.25,
        speed_compliance_mean=0.94,
        speed_compliance_std=0.1,
        accel_mean=1.9,
        decel_mean=3.0,
        driver_imperfection=0.28,
        fixed_cycle_seconds=95,
        arterial_green_split=0.6,
    ),
    ScenarioName.peak_rush_hour: ScenarioConfig(
        name=ScenarioName.peak_rush_hour,
        demand_intensity=1.6,
        speed_compliance_mean=0.9,
        speed_compliance_std=0.12,
        accel_mean=1.7,
        decel_mean=2.8,
        driver_imperfection=0.35,
        fixed_cycle_seconds=110,
        arterial_green_split=0.62,
    ),
    ScenarioName.incident_mode: ScenarioConfig(
        name=ScenarioName.incident_mode,
        demand_intensity=1.8,
        speed_compliance_mean=0.88,
        speed_compliance_std=0.13,
        accel_mean=1.5,
        decel_mean=2.6,
        driver_imperfection=0.4,
        fixed_cycle_seconds=120,
        arterial_green_split=0.66,
    ),
}
