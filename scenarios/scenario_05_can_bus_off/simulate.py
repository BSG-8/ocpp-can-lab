"""
Template for running a scenario.

Everyone copies the folder _template -> scenario_XX_name,
then modifies ACTIVE_SCENARIO below.
"""

import asyncio
from infra.ocpp_client import main as cp_main
import infra.pipeline as pipeline

def set_active_scenario():
    # Replace with your scenario folder name
    pipeline.ACTIVE_SCENARIO_NAME = "scenario_d02_can_bus_off"
    print(f"[SCENARIO] Active scenario set → {pipeline.ACTIVE_SCENARIO}")

if __name__ == "__main__":
    set_active_scenario()
    asyncio.run(cp_main())
