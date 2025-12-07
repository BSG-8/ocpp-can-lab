"""
scenario_00_baseline/simulate.py
This module runs the baseline (normal) behavior scenario.
"""

import asyncio
from infra.ocpp_client import main as cp_main
import infra.pipeline as pipeline


def set_active_scenario():
    """
    This sets the scenario that the pipeline uses.
    """
    pipeline.ACTIVE_SCENARIO = "scenario_00_baseline"
    print(f"[SCENARIO] Active scenario set → {pipeline.ACTIVE_SCENARIO}")


if __name__ == "__main__":
    set_active_scenario()
    asyncio.run(cp_main())
