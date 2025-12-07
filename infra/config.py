import json
from pathlib import Path

# Default values if config.json is missing or incomplete
DEFAULT_CONFIG = {
    "csms_url": "ws://localhost:9000",
    "vcan_channel": "vcan0",
    "default_scenario": "scenario_00_baseline",
    "log_level": "INFO",
}

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.json"


def load_config():
    config = DEFAULT_CONFIG.copy()

    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            config.update({k: v for k, v in data.items() if k in DEFAULT_CONFIG})
        except Exception as e:
            print(f"[CONFIG] Failed to load config.json, using defaults. Error: {e}")

    else:
        print("[CONFIG] config.json not found, using defaults.")

    return config


CONFIG = load_config()
