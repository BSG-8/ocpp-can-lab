"""
🔐 Firmware Manipulation Senaryosu
Hazırlayan: Sena Köse
Fırat Üniversitesi — Bilgi Sistemleri ve Güvenliği Dersi (2025 Güz)

Bu senaryo, imzalanmamış veya manipüle edilmiş firmware güncellemelerinin
tespit edilmesini simüle eder.
"""

import asyncio
from infra.ocpp_client import main as cp_main
import infra.pipeline as pipeline


def set_active_scenario():
    pipeline.ACTIVE_SCENARIO = "scenario_06_firmware_manipulation"
    print(f"[SCENARIO] Active scenario set → {pipeline.ACTIVE_SCENARIO}")


if __name__ == "__main__":
    set_active_scenario()
    asyncio.run(cp_main())
