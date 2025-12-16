# infra/pipeline.py
from infra.config import CONFIG
from infra.logger import LOGGER
from infra.mapping import ocpp_to_can
import can
import importlib
from infra.scenario_base import ScenarioHooks

# -----------------------------------------
# ACTIVE SCENARIO
# -----------------------------------------
ACTIVE_SCENARIO = CONFIG["default_scenario"]


# -----------------------------------------
# SCENARIO LOADER
# -----------------------------------------
def load_scenario():
    """
    Dynamically load scenario module:
    scenarios.<scenario>/hooks.py
    """
    try:
        module_path = f"scenarios.{ACTIVE_SCENARIO}.hooks"
        module = importlib.import_module(module_path)

        # LOG ACTIVE SCENARIO ONCE
        LOGGER.log_scenario_meta(ACTIVE_SCENARIO)

        # Find class inside module
        for attr in dir(module):
            obj = getattr(module, attr)
            if isinstance(obj, type) and issubclass(obj, ScenarioHooks) and obj is not ScenarioHooks:
                return obj()  # instantiate scenario class

        print(f"[PIPELINE] Warning: No scenario class found in {module_path}, using default.")
        return ScenarioHooks()

    except Exception as e:
        print(f"[PIPELINE] Could not load scenario {ACTIVE_SCENARIO}: {e}")
        return ScenarioHooks()


# -----------------------------------------
# MAIN OCPP → CAN PROCESSING PIPELINE
# -----------------------------------------
async def process_ocpp_message(action, payload, ws):
    """
    Core pipeline that handles:
    1. Scenario pre-OCPP hook
    2. Sending OCPP message to CSMS
    3. Receiving OCPP reply
    4. Scenario post-OCPP hook
    5. Mapping OCPP → CAN
    6. Scenario pre-CAN hook
    7. Sending CAN frame via vcan0
    8. Scenario post-CAN hook
    """

    # Load scenario instance
    scenario = load_scenario()

    # ---- 1. SCENARIO HOOK: pre_ocpp() ----
    action, payload = scenario.pre_ocpp(action, payload)

    # ---- 2. SEND OCPP TO CSMS ----
    message = {
        "action": action,
        "payload": payload,
    }

    await ws.send(str(message))
    LOGGER.log_ocpp(
        direction="sent",
        action=action,
        payload=payload
    )
    print(f"[PIPELINE] Sent OCPP -> {message}")


    # ---- 3. RECEIVE OCPP REPLY ----
    reply = await ws.recv()

    # ---- 4. SCENARIO HOOK: post_ocpp() ----
    reply = scenario.post_ocpp(action, payload, reply)

    LOGGER.log_ocpp(
    direction="received",
    action=action,
    payload=payload,
    reply=reply
    )

    print(f"[PIPELINE] Received OCPP reply <- {reply}")

    # ---- 5. MAP OCPP → CAN ----
    can_frame = ocpp_to_can(action, payload)
    if can_frame is None:
        print(f"[PIPELINE] No CAN mapping for action '{action}'")
        return reply

    print(f"[PIPELINE] CAN frame produced -> {can_frame}")

    # ---- 6. SCENARIO HOOK: pre_can() ----
    can_frame = scenario.pre_can(can_frame)
    if can_frame is None:
        print(f"[PIPELINE] Scenario dropped CAN frame for '{action}'")
        return reply

    # ---- 7. SEND CAN FRAME VIA vcan0 ----
    VCAN_CHANNEL = CONFIG["vcan_channel"]
    bus = can.interface.Bus(channel=VCAN_CHANNEL, interface="socketcan")


    msg = can.Message(
        arbitration_id=can_frame["id"],
        data=can_frame["data"],
        is_extended_id=False
    )
    bus.send(msg)

    # log CAN
    LOGGER.log_can(
        direction="sent",
        frame=can_frame,
    )


    print(f"[PIPELINE] Sent CAN frame -> {msg}")

    # ---- 8. SCENARIO HOOK: post_can() ----
    scenario.post_can(can_frame)

    return reply
