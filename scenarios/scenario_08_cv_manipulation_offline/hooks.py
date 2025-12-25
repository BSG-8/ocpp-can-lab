"""
Hook fonksiyonları: Hedefli CV Manipülasyonu ile Çevrimdışı Mod Zorlama

Bu senaryo, OCPP Konfigürasyon Değişkenlerini (CV) manipüle ederek
CP'nin CSMS ile iletişimini keser ve çevrimdışı moda zorlar.
"""

import logging
import json
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


def pre_ocpp(message: Dict[str, Any], message_type: str) -> Optional[Dict[str, Any]]:
    """
    OCPP mesajı gönderilmeden önce manipüle eder.
    
    Bu hook, ChangeConfiguration mesajlarını yakalar ve
    OfflineTxForUnknownIdEnabled CV'sini TRUE yapar.
    Ayrıca CSMS ile iletişimi kesmek için mesajları manipüle eder.
    """
    
    # ChangeConfiguration mesajını yakala ve manipüle et
    if message_type == "ChangeConfiguration":
        key = message.get("key", "")
        value = message.get("value", "")
        
        # OfflineTxForUnknownIdEnabled CV'sini TRUE yap
        if key == "OfflineTxForUnknownIdEnabled":
            logger.warning(f"[ANOMALI] CV Manipülasyonu: {key} = {value} -> TRUE")
            message["value"] = "true"
            return message
        
        # Diğer kritik CV'leri de manipüle edebiliriz
        # Örneğin: HeartbeatInterval'ı artırarak iletişimi zayıflat
        if key == "HeartbeatInterval":
            logger.warning(f"[ANOMALI] HeartbeatInterval manipülasyonu: {value} -> 3600")
            message["value"] = "3600"  # 1 saat (normalde çok daha kısa)
            return message
    
    # BootNotification mesajını manipüle ederek CSMS'e yanlış bilgi gönder
    if message_type == "BootNotification":
        logger.warning("[ANOMALI] BootNotification manipülasyonu - CSMS ile iletişim zayıflatılıyor")
        # Mesajı olduğu gibi bırak ama logla
        return message
    
    # StatusNotification mesajlarını manipüle et
    if message_type == "StatusNotification":
        # CP durumunu manipüle ederek CSMS'in yanlış bilgi almasını sağla
        logger.warning("[ANOMALI] StatusNotification manipülasyonu")
        return message
    
    # Heartbeat mesajlarını bazen engelle (iletişimi kesmek için)
    if message_type == "Heartbeat":
        # %30 ihtimalle heartbeat'i engelle (iletişim kopukluğu simülasyonu)
        import random
        if random.random() < 0.3:
            logger.warning("[ANOMALI] Heartbeat mesajı engellendi - iletişim kesiliyor")
            return None  # Mesajı gönderme
    
    return message


def post_ocpp(response: Dict[str, Any], message_type: str) -> Optional[Dict[str, Any]]:
    """
    OCPP cevabı alındıktan sonra manipüle eder.
    
    CSMS'den gelen cevapları manipüle ederek CP'nin yanlış yapılandırma
    almasını sağlar.
    """
    
    # ChangeConfiguration cevabını manipüle et
    if message_type == "ChangeConfiguration":
        status = response.get("status", "")
        
        # Eğer CSMS reddetti ise, cevabı Accepted olarak değiştir
        if status == "Rejected" or status == "NotSupported":
            logger.warning(f"[ANOMALI] ChangeConfiguration cevabı manipüle edildi: {status} -> Accepted")
            response["status"] = "Accepted"
            return response
    
    # GetConfiguration cevabını manipüle et
    if message_type == "GetConfiguration":
        configuration_key = response.get("configurationKey", [])
        
        # OfflineTxForUnknownIdEnabled değerini TRUE olarak ayarla
        for config in configuration_key:
            if config.get("key") == "OfflineTxForUnknownIdEnabled":
                if config.get("value") != "true":
                    logger.warning("[ANOMALI] GetConfiguration cevabında OfflineTxForUnknownIdEnabled TRUE yapıldı")
                    config["value"] = "true"
                    config["readonly"] = False  # Değiştirilebilir yap
    
    return response


def pre_can(can_frame: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    CAN frame gönderilmeden önce manipüle eder.
    
    Çevrimdışı modda, CP'nin yerel yetkilendirme sinyallerini
    manipüle ederek yetkisiz şarjı simüle eder.
    """
    
    # CAN ID'ye göre frame'i manipüle et
    can_id = can_frame.get("id", 0)
    data = can_frame.get("data", [])
    
    # Örnek: Şarj yetkilendirme sinyalini manipüle et
    # (Gerçek CAN ID'ler projeye göre değişebilir)
    if can_id == 0x123:  # Örnek: Yetkilendirme frame ID
        logger.warning("[ANOMALI] CAN frame manipülasyonu - Yetkisiz şarj sinyali enjekte edildi")
        # Data'yı manipüle et - yetkilendirme sinyalini aktif yap
        if len(data) > 0:
            data[0] = 0x01  # Yetkilendirme aktif
    
    return can_frame


def post_can(can_frame: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    CAN frame gönderildikten sonra işlem yapar.
    
    Çevrimdışı modda gönderilen frame'leri loglar.
    """
    
    can_id = can_frame.get("id", 0)
    logger.info(f"[ANOMALI] CAN frame gönderildi (çevrimdışı mod): ID=0x{can_id:X}")
    
    return can_frame

