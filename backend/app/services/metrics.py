from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MetricAccumulator:
    total_delay_s: float = 0.0
    total_travel_time_s: float = 0.0
    total_stops: int = 0
    total_queue: int = 0
    throughput: int = 0
    samples: int = 0

    def record(self, delay_s: float, travel_time_s: float, stops: int, queue: int, throughput: int) -> None:
        self.total_delay_s += delay_s
        self.total_travel_time_s += travel_time_s
        self.total_stops += stops
        self.total_queue += queue
        self.throughput += throughput
        self.samples += 1

    def summary(self) -> dict[str, float]:
        if self.samples == 0:
            return {"avg_delay_s": 0, "avg_travel_time_s": 0, "avg_stops": 0, "avg_queue": 0, "throughput": 0}
        return {
            "avg_delay_s": self.total_delay_s / self.samples,
            "avg_travel_time_s": self.total_travel_time_s / self.samples,
            "avg_stops": self.total_stops / self.samples,
            "avg_queue": self.total_queue / self.samples,
            "throughput": self.throughput,
        }
