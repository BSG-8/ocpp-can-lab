"""
🚨 Hayali İstasyon - StatusNotification Spoofing Senaryosu
Hazırlayan: Özgür Kerem Öncel
Fırat Üniversitesi — Bilgi Sistemleri ve Güvenliği Dersi (2025 Güz)

Bu senaryo, şarj istasyonunun gerçek durumunun
StatusNotification mesajları manipüle edilerek
CSMS'den gizlenmesini simüle eder.
"""

import asyncio
from infra.ocpp_client import main as cp_main
import infra.pipeline as pipeline


def set_active_scenario():
    """
    Pipeline üzerinde aktif çalışacak senaryoyu belirler.
    """
    pipeline.ACTIVE_SCENARIO = "scenario_07_status_notification_spoofing"
    print(f"[SCENARIO] Active scenario set → {pipeline.ACTIVE_SCENARIO}")


if __name__ == "__main__":
    set_active_scenario()
    asyncio.run(cp_main())
