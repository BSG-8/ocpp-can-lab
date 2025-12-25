"""
Senaryo: Hedefli CV Manipülasyonu ile Çevrimdışı Mod Zorlama
(Off-Grid Mode Enforcement via Targeted CV Manipulation)

Bu senaryo, OCPP Konfigürasyon Değişkenlerini (CV) manipüle ederek
Şarj İstasyonunun (CP) Merkezi Yönetim Sistemi (CSMS) ile iletişimini
kasıtlı ve kalıcı olarak keser. Bu sayede CP çevrimdışı moda zorlanır
ve yetkisiz (ücretsiz) şarj erişimi sağlanır.

TC-5, TC-7 test case'lerini kapsar.
"""

import sys
import os
import time
import logging
from pathlib import Path

# Proje kök dizinini path'e ekle
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Hook'ları import et
from scenarios.scenario_02_cv_manipulation_offline.hooks import (
    pre_ocpp,
    post_ocpp,
    pre_can,
    post_can
)

# Logging yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scenario_02_cv_manipulation_offline.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def register_hooks(pipeline):
    """
    Hook'ları pipeline'a kaydeder.
    """
    logger.info("Hook'lar kaydediliyor...")
    
    pipeline.register_hook("pre_ocpp", pre_ocpp)
    pipeline.register_hook("post_ocpp", post_ocpp)
    pipeline.register_hook("pre_can", pre_can)
    pipeline.register_hook("post_can", post_can)
    
    logger.info("✓ Tüm hook'lar başarıyla kaydedildi")


def simulate_attack():
    """
    Ana saldırı simülasyonu.
    
    Senaryo akışı:
    1. CP normal şekilde CSMS'e bağlanır
    2. OfflineTxForUnknownIdEnabled CV'si manipüle edilir (TRUE yapılır)
    3. HeartbeatInterval artırılarak iletişim zayıflatılır
    4. Heartbeat mesajları bazen engellenir
    5. CP çevrimdışı moda zorlanır
    6. Yetkisiz şarj işlemi simüle edilir
    """
    
    logger.info("=" * 80)
    logger.info("SENARYO BAŞLATILIYOR: Hedefli CV Manipülasyonu ile Çevrimdışı Mod Zorlama")
    logger.info("=" * 80)
    
    try:
        # Pipeline'ı import et (proje yapısına göre ayarlanmalı)
        # Not: Gerçek projede infra.pipeline modülünden import edilecek
        logger.info("Pipeline modülü yükleniyor...")
        
        # Pipeline'ı başlat (gerçek implementasyona göre değişebilir)
        # pipeline = Pipeline()
        # register_hooks(pipeline)
        # pipeline.start()
        
        logger.info("Saldırı senaryosu başlatıldı")
        logger.info("")
        logger.info("SALDIRI ADIMLARI:")
        logger.info("1. CP normal şekilde CSMS'e bağlanıyor...")
        time.sleep(1)
        
        logger.info("2. [ANOMALI] OfflineTxForUnknownIdEnabled CV'si TRUE yapılıyor...")
        logger.warning("   → ChangeConfiguration(key='OfflineTxForUnknownIdEnabled', value='true')")
        time.sleep(1)
        
        logger.info("3. [ANOMALI] HeartbeatInterval 3600 saniyeye çıkarılıyor...")
        logger.warning("   → ChangeConfiguration(key='HeartbeatInterval', value='3600')")
        time.sleep(1)
        
        logger.info("4. [ANOMALI] Heartbeat mesajları engelleniyor (iletişim kesiliyor)...")
        logger.warning("   → CSMS ile iletişim kopukluğu simüle ediliyor")
        time.sleep(1)
        
        logger.info("5. [ANOMALI] CP çevrimdışı moda zorlanıyor...")
        logger.warning("   → Yerel yetkilendirme modu aktif")
        time.sleep(1)
        
        logger.info("6. [ANOMALI] Yetkisiz şarj işlemi başlatılıyor...")
        logger.warning("   → CAN frame manipülasyonu ile yetkilendirme sinyali enjekte ediliyor")
        time.sleep(1)
        
        logger.info("")
        logger.info("=" * 80)
        logger.warning("SALDIRI BAŞARILI: CP çevrimdışı modda ve yetkisiz şarj aktif!")
        logger.info("=" * 80)
        
        # Simülasyonu çalışır durumda tut
        logger.info("Simülasyon çalışıyor... (Ctrl+C ile durdurun)")
        
        try:
            while True:
                time.sleep(5)
                logger.info("[SİMÜLASYON] Çevrimdışı mod aktif - Yetkisiz şarj devam ediyor...")
        except KeyboardInterrupt:
            logger.info("Simülasyon durduruldu")
        
    except Exception as e:
        logger.error(f"Hata oluştu: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    # Logs dizinini oluştur
    os.makedirs("logs", exist_ok=True)
    
    # Senaryoyu çalıştır
    simulate_attack()

