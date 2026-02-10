from __future__ import annotations

from collections import defaultdict


def rank_intersections(decision_log: list[dict[str, float]], top_n: int = 5) -> list[tuple[str, float]]:
    scores: dict[str, float] = defaultdict(float)
    for decision in decision_log:
        scores[decision["intersection_id"]] += decision["queue_reduction"]
    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return ranked[:top_n]


def narrative_from_ranking(ranked: list[tuple[str, float]]) -> list[str]:
    if not ranked:
        return ["No significant control interventions recorded."]
    lines = ["Network gains came from balancing queues on high-pressure intersections:"]
    for inter_id, score in ranked:
        lines.append(f"{inter_id} reduced cumulative queue pressure by {score:.1f} vehicle-seconds.")
    return lines
