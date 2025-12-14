"""
scenario_03_hayalet_sarj/simulate.py
Hayalet Şarj (Ghost Charge) Senaryosu Giriş Noktası

Kullanım:
    python -m scenarios.scenario_03_hayalet_sarj.simulate

Bu modül, Ghost Charge saldırı senaryosunu aktif hale getirir
ve şarj noktası istemcisini başlatır.
"""

import asyncio
from infra.ocpp_client import main as cp_main
import infra.pipeline as pipeline


def set_active_scenario():
    """
    Pipeline'ın kullanacağı senaryoyu ayarla.
    """
    pipeline.ACTIVE_SCENARIO = "scenario_03_hayalet_sarj"
    print(f"[SCENARIO] Active scenario set → {pipeline.ACTIVE_SCENARIO}")
    print("[SCENARIO] 👻 Ghost Charge Attack - Hayalet Şarj Saldırısı")
    print("[SCENARIO] ⚠️  MeterValues mesajları manipüle edilecek!")


if __name__ == "__main__":
    set_active_scenario()
    asyncio.run(cp_main())
