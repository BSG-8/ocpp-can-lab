import asyncio
import json
import time
import websockets

import can
from infra.mapping import ocpp_to_can


# -----------------------------------------
# CONFIGURATION
# -----------------------------------------
CSMS_URL = "ws://localhost:9000"
CAN_CHANNEL = "vcan0"

# Create CAN bus object for sending CAN frames
bus = can.Bus(interface="socketcan", channel=CAN_CHANNEL)


# -----------------------------------------
# SEND OCPP + SEND CAN
# -----------------------------------------
async def send_message(ws, action, payload):
    # Build OCPP message
    message = {
        "action": action,
        "payload": payload,
        "timestamp": time.time()
    }

    text = json.dumps(message)
    print(f"[CP] Sending {action}: {text}")

    # 1) Send OCPP to CSMS
    await ws.send(text)

    # 2) Convert OCPP → CAN
    can_frame = ocpp_to_can(action, payload)

    # 3) Send CAN frame if mapping exists
    if can_frame is not None:
        msg = can.Message(
            arbitration_id=can_frame["id"],
            data=can_frame["data"],
            is_extended_id=False
        )
        bus.send(msg)
        print(f"[CP] Sent CAN frame: {msg}")
    else:
        print("[CP] No CAN mapping for this action.")

    # 4) Receive reply from CSMS
    reply = await ws.recv()
    print(f"[CP] Received from CSMS: {reply}")


# -----------------------------------------
# MAIN CLIENT LOGIC
# -----------------------------------------
async def main():
    print(f"[CP] Connecting to {CSMS_URL} ...")

    async with websockets.connect(CSMS_URL) as ws:
        # BootNotification
        await send_message(ws, "BootNotification", {
            "chargePointVendor": "DemoVendor",
            "chargePointModel": "DemoModel-01"
        })

        # Heartbeat
        await asyncio.sleep(0.1)
        await send_message(ws, "Heartbeat", {"status": "Online"})

        # MeterValues
        await asyncio.sleep(0.1)
        await send_message(ws, "MeterValues", {
            "energyWh": 1234,
            "powerW": 3500
        })

        print("[CP] Done. Closing connection.")


# -----------------------------------------
# ENTRY POINT
# -----------------------------------------
if __name__ == "__main__":
    asyncio.run(main())
