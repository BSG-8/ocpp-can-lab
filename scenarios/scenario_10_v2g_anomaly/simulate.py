import sys
import os
import asyncio

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from infra import config
from infra import ocpp_client

print(">>> V2G Deşarj Anomalisi Senaryosu Yükleniyor...")

# Senaryoyu aktif et
config.CONFIG["default_scenario"] = "scenario_09_v2g_anomaly"

if __name__ == "__main__":
    try:
        print(">>> Simülasyon başlatılıyor (OCPP Client)...")
        asyncio.run(ocpp_client.main())
    except KeyboardInterrupt:
        print("\nDurduruluyor...")
    except Exception as e:
        print(f"Hata oluştu: {e}")
