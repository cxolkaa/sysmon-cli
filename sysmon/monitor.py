"""System metrics collection."""

from __future__ import annotations

import json
import platform
import socket
from datetime import datetime, timezone
from typing import Any

import psutil


def bytes_to_gb(value: int) -> float:
    return round(value / (1024**3), 2)


def collect_metrics() -> dict[str, Any]:
    boot = datetime.fromtimestamp(psutil.boot_time(), tz=timezone.utc)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "uptime_hours": round((datetime.now(timezone.utc) - boot).total_seconds() / 3600, 1),
        "cpu": {
            "percent": psutil.cpu_percent(interval=0.5),
            "cores_logical": psutil.cpu_count(logical=True),
            "cores_physical": psutil.cpu_count(logical=False),
        },
        "memory": {
            "total_gb": bytes_to_gb(mem.total),
            "used_gb": bytes_to_gb(mem.used),
            "percent": mem.percent,
        },
        "disk": {
            "total_gb": bytes_to_gb(disk.total),
            "used_gb": bytes_to_gb(disk.used),
            "free_gb": bytes_to_gb(disk.free),
            "percent": disk.percent,
        },
        "processes": len(psutil.pids()),
    }


def check_thresholds(metrics: dict[str, Any], cpu: int, memory: int, disk: int) -> list[str]:
    alerts: list[str] = []
    if metrics["cpu"]["percent"] >= cpu:
        alerts.append(f"CPU usage high: {metrics['cpu']['percent']}% (threshold {cpu}%)")
    if metrics["memory"]["percent"] >= memory:
        alerts.append(
            f"Memory usage high: {metrics['memory']['percent']}% (threshold {memory}%)"
        )
    if metrics["disk"]["percent"] >= disk:
        alerts.append(f"Disk usage high: {metrics['disk']['percent']}% (threshold {disk}%)")
    return alerts


def export_json(metrics: dict[str, Any], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
