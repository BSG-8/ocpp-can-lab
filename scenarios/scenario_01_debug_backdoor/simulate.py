
import asyncio
from infra.ocpp_client import main as cp_main
import infra.pipeline as pipeline

from scenarios.scenario_01_debug_backdoor.hooks import Scenario


def set_active_scenario():
    pipeline.ACTIVE_SCENARIO = "scenario_01_debug_backdoor"
    print(f"[SCENARIO] Active scenario set → {pipeline.ACTIVE_SCENARIO}")

if __name__ == "__main__":
    set_active_scenario()
    asyncio.run(cp_main())
