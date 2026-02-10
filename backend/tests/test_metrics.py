from app.services.metrics import MetricAccumulator


def test_metrics_aggregation():
    acc = MetricAccumulator()
    acc.record(delay_s=10, travel_time_s=20, stops=2, queue=5, throughput=3)
    acc.record(delay_s=30, travel_time_s=40, stops=4, queue=7, throughput=5)
    summary = acc.summary()
    assert summary["avg_delay_s"] == 20
    assert summary["throughput"] == 8
