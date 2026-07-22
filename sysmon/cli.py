"""CLI entry point."""

from __future__ import annotations

import json

import click
from rich.console import Console
from rich.table import Table

from sysmon.monitor import check_thresholds, collect_metrics, export_json

console = Console()


@click.command()
@click.option("--cpu-threshold", default=85, show_default=True, help="CPU alert threshold (%)")
@click.option("--memory-threshold", default=85, show_default=True, help="Memory alert threshold (%)")
@click.option("--disk-threshold", default=90, show_default=True, help="Disk alert threshold (%)")
@click.option("--json", "as_json", is_flag=True, help="Print raw JSON output")
@click.option("--export", "export_path", type=click.Path(), help="Save metrics to JSON file")
def main(cpu_threshold: int, memory_threshold: int, disk_threshold: int, as_json: bool, export_path: str | None):
    """Monitor system health: CPU, memory, disk, uptime."""
    metrics = collect_metrics()
    alerts = check_thresholds(metrics, cpu_threshold, memory_threshold, disk_threshold)

    if export_path:
        export_json(metrics, export_path)

    if as_json:
        console.print_json(json.dumps(metrics))
        if alerts:
            raise SystemExit(1)
        return

    table = Table(title="System Health Report", show_header=True)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Hostname", metrics["hostname"])
    table.add_row("Platform", metrics["platform"])
    table.add_row("Uptime (hours)", str(metrics["uptime_hours"]))
    table.add_row("CPU %", f"{metrics['cpu']['percent']}%")
    table.add_row("Memory", f"{metrics['memory']['used_gb']} / {metrics['memory']['total_gb']} GB ({metrics['memory']['percent']}%)")
    table.add_row("Disk", f"{metrics['disk']['used_gb']} / {metrics['disk']['total_gb']} GB ({metrics['disk']['percent']}%)")
    table.add_row("Processes", str(metrics["processes"]))

    console.print(table)

    if alerts:
        console.print("\n[bold red]ALERTS:[/bold red]")
        for alert in alerts:
            console.print(f"  • {alert}")
        raise SystemExit(1)

    console.print("\n[green]All metrics within thresholds.[/green]")


if __name__ == "__main__":
    main()
