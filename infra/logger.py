"""
Global logger for OCPP and CAN events.

- Creates a new run folder under logs/ for each execution.
- Logs OCPP and CAN as JSON lines (one JSON object per line).
"""

import os
import json
from datetime import datetime


class Logger:
    def __init__(self):
        # Create logs/ directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)

        # Create a unique folder for this run
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.run_dir = os.path.join("logs", f"run_{timestamp}")
        os.makedirs(self.run_dir, exist_ok=True)

        # File paths
        self.ocpp_log_path = os.path.join(self.run_dir, "ocpp_log.jsonl")
        self.can_log_path = os.path.join(self.run_dir, "can_log.jsonl")
        self.scenario_log_path = os.path.join(self.run_dir, "scenario_log.jsonl")

        print(f"[LOGGER] Logging to folder: {self.run_dir}")

    def log_ocpp(self, direction, action, payload=None, reply=None):
        """
        direction: 'sent' or 'received'
        action: OCPP action name (e.g. 'BootNotification')
        payload: dict (optional)
        reply: raw reply string or dict (optional)
        """
        record = {
            "time": datetime.now().isoformat(),
            "direction": direction,
            "action": action,
            "payload": payload,
            "reply": reply,
        }
        with open(self.ocpp_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    def log_can(self, direction, frame):
        """
        direction: 'sent' or 'received'
        frame: dict with at least {'id': ..., 'data': [...]}
        """
        record = {
            "time": datetime.now().isoformat(),
            "direction": direction,
            "frame": frame,
        }
        with open(self.can_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    def log_scenario(self, message):
        """
        Free-form messages from scenarios (e.g. 'attack started', 'threshold exceeded').
        """
        record = {
            "time": datetime.now().isoformat(),
            "message": message,
        }
        with open(self.scenario_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")


# Singleton-style global logger instance
LOGGER = Logger()
