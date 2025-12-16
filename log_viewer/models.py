from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Event:
    ts: str
    source: str
    action: str
    message: str
    data: Any

    direction: Optional[str] = None
