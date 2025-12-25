"""
Scenario 07: Harici CAN Yansıtma (Reflection)
Entry point for the simulation.
"""

import asyncio
from infra.ocpp_client import main as cp_main
import infra.pipeline as pipeline

def set_active_scenario():
    # Set the pipeline to use this scenario
    pipeline.ACTIVE_SCENARIO = "scenario_07_can_reflection"
    print(f"[SCENARIO] Active scenario set → {pipeline.ACTIVE_SCENARIO}")

if __name__ == "__main__":
    set_active_scenario()
    asyncio.run(cp_main())
