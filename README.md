# Sysmon CLI

Cross-platform command-line tool for IT operations teams to quickly check server and workstation health.

Monitors **CPU**, **memory**, **disk usage**, **uptime**, and running **process count** with configurable alert thresholds.

## Features

- Real-time system metrics via `psutil`
- Colorful terminal output with Rich
- JSON export for monitoring pipelines
- Configurable alert thresholds (exit code 1 on breach)
- Works on Windows, Linux, and macOS

## Tech Stack

- Python 3.10+
- psutil, Click, Rich

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

## Usage

```bash
# Default report
sysmon

# Custom thresholds
sysmon --cpu-threshold 80 --memory-threshold 90 --disk-threshold 95

# JSON output (for scripts / cron jobs)
sysmon --json

# Export to file
sysmon --export report.json
```

### Example Output

```
┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric               ┃ Value                        ┃
┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Hostname             │ WORKSTATION-01               │
│ CPU %                │ 23.5%                        │
│ Memory               │ 8.2 / 16.0 GB (51.3%)        │
│ Disk                 │ 120.5 / 512.0 GB (23.5%)     │
└──────────────────────┴──────────────────────────────┘
```

## Use Cases

- Daily health checks on servers
- Pre-maintenance snapshots
- Cron job monitoring with `--json` + exit codes
- Quick diagnostics during helpdesk tickets

## Run Tests

```bash
pip install -e ".[dev]" 2>nul || pip install pytest
pytest -v
```

## License

MIT
