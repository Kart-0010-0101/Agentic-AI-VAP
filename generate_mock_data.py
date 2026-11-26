"""Create sample sensor telemetry JSON inside data/."""

from __future__ import annotations

import json
from pathlib import Path


def ensure_sample_data(base_dir: Path) -> Path:
    data_dir = base_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    log_path = data_dir / "iot_sensor_log.json"
    records = [
        {"node": "ESP32-N1", "temp_c": 41.2, "vbus_v": 4.98, "status": "ok"},
        {"node": "ESP32-N2", "temp_c": 88.7, "vbus_v": 4.71, "status": "thermal_alert"},
        {"node": "ESP32-N3", "temp_c": 39.5, "vbus_v": 5.01, "status": "ok"},
    ]
    log_path.write_text(json.dumps(records, indent=2), encoding="utf-8")
    return log_path


if __name__ == "__main__":
    p = ensure_sample_data(Path(__file__).resolve().parent)
    print(f"Generated sample telemetry at {p}")
