from unittest.mock import patch

from sysmon.monitor import check_thresholds, collect_metrics


def test_collect_metrics_structure():
    metrics = collect_metrics()
    assert "hostname" in metrics
    assert "cpu" in metrics
    assert "memory" in metrics
    assert "disk" in metrics
    assert isinstance(metrics["cpu"]["percent"], float)


def test_check_thresholds_triggers_alerts():
    metrics = {
        "cpu": {"percent": 95},
        "memory": {"percent": 50},
        "disk": {"percent": 50},
    }
    alerts = check_thresholds(metrics, cpu=85, memory=85, disk=90)
    assert len(alerts) == 1
    assert "CPU" in alerts[0]


def test_check_thresholds_all_ok():
    metrics = {
        "cpu": {"percent": 10},
        "memory": {"percent": 20},
        "disk": {"percent": 30},
    }
    assert check_thresholds(metrics, cpu=85, memory=85, disk=90) == []
