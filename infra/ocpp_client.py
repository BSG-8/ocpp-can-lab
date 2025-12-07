import asyncio
import websockets
from infra.pipeline import process_ocpp_message   # NEW — use pipeline


# -----------------------------------------
# CONFIGURATION
# -----------------------------------------
CSMS_URL = "ws://localhost:9000"


# -----------------------------------------
# MAIN CLIENT LOGIC (now uses pipeline)
# -----------------------------------------
async def main():
    print(f"[CP] Connecting to {CSMS_URL} ...")

    async with websockets.connect(CSMS_URL) as ws:

        # ---- BootNotification ----
        await process_ocpp_message(
            "BootNotification",
            {
                "chargePointVendor": "DemoVendor",
                "chargePointModel": "DemoModel-01"
            },
            ws
        )

        # ---- Heartbeat ----
        await process_ocpp_message(
            "Heartbeat",
            {"status": "Online"},
            ws
        )

        # ---- MeterValues ----
        await process_ocpp_message(
            "MeterValues",
            {"energyWh": 1234, "powerW": 3500},
            ws
        )

        print("[CP] Done. Closing connection.")


# -----------------------------------------
# ENTRY POINT
# -----------------------------------------
if __name__ == "__main__":
    asyncio.run(main())
