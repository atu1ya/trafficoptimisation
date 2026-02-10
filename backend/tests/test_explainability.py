from app.services.explainability import rank_intersections


def test_explainability_ranking():
    ranked = rank_intersections(
        [
            {"intersection_id": "a", "queue_reduction": 3.0},
            {"intersection_id": "b", "queue_reduction": 8.0},
            {"intersection_id": "a", "queue_reduction": 2.0},
        ],
        top_n=1,
    )
    assert ranked == [("b", 8.0)]
