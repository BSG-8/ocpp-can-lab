"""
🚨 Hayali İstasyon - StatusNotification Spoofing Hooks
Hazırlayan: Özgür Kerem Öncel
Fırat Üniversitesi — Bilgi Sistemleri ve Güvenliği (2025 Güz)

Bu senaryo, şarj istasyonunun gerçek durumunun
CSMS'den gizlenerek operatörün yanıltılmasını simüle eder.
"""

import time
from infra.scenario_base import ScenarioHooks


class Scenario(ScenarioHooks):
    """
    Hayali İstasyon (Sahte Durum Bildirimi) Senaryosu

    Saldırı Türü: StatusNotification Spoofing (MitM)
    Hedef: OCPP StatusNotification mesajları
    """

    def __init__(self):
        super().__init__()
        self.attack_active = False
        self.attack_start_time = None
        self.real_status = "Faulted"
        self.spoofed_status = "Available"

    def pre_ocpp(self, action, payload):
        """
        OCPP mesajı CSMS'ye gönderilmeden önce çağrılır.
        StatusNotification mesajı manipüle edilir.
        """

        if action == "StatusNotification":
            self.log("=" * 50)
            self.log("🚨 SALDIRI BAŞLATILDI: StatusNotification Spoofing")
            self.log("=" * 50)

            self.attack_active = True
            self.attack_start_time = time.time()

            # Gerçek durumu logla
            self.log(f"📡 Gerçek İstasyon Durumu: {payload.get('status')}")

            # Durum manipülasyonu
            payload["status"] = self.spoofed_status
            payload["errorCode"] = "NoError"

            self.log("⚠️  DURUM MANİPÜLASYONU GERÇEKLEŞTİRİLDİ")
            self.log(f"   ➜ Sahte Durum: {self.spoofed_status}")

        return action, payload

    def post_ocpp(self, action, payload, reply):
        """
        CSMS cevabı alındıktan sonra çağrılır.
        Mantıksal anomali tespit sistemi simüle edilir.
        """

        if action == "StatusNotification" and self.attack_active:
            self.log("-" * 50)
            self.log("🤖 CSMS MANTIKSAL ANOMALİ TESPİT MODÜLÜ")
            self.log("-" * 50)

            anomaly_detected = self._detect_anomaly(payload)

            if anomaly_detected:
                detection_time = time.time() - self.attack_start_time

                self.log("🔴 ANOMALİ TESPİT EDİLDİ!")
                self.log(f"   ⏱  Tespit Süresi: {detection_time:.2f} saniye")

                self.log("")
                self.log("🛡  CSMS TEPKİSİ:")
                self.log("   ✓ İstasyon 'İnceleme Altında' olarak işaretlendi")
                self.log("   ✓ Operasyon ekibine otomatik uyarı gönderildi")
                self.log("   ✓ İstasyon geçici olarak pasif duruma alındı")

                if isinstance(reply, dict):
                    reply["note"] = "LOGICAL_ANOMALY: Status inconsistency detected"

        return reply

    def pre_can(self, can_frame):
        """
        CAN frame gönderilmeden önce çağrılır.
        Operasyonel güvenlik uyarısı simüle edilir.
        """

        if self.attack_active:
            self.log("")
            self.log("🚌 CAN-BUS OPERASYONEL UYARI")

            if isinstance(can_frame, dict):
                can_frame["arbitration_id"] = 0x6FF
                can_frame["data"] = [0xEE, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01]
                # 0xEE = Operasyonel anomali
                # 0x02 = Sahte durum bildirimi
                # 0x01 = Yüksek risk

            self.log("   📡 CAN uyarısı gönderildi (Risk Seviyesi: YÜKSEK)")

        return can_frame

    def post_can(self, can_frame):
        """
        CAN frame gönderildikten sonra çağrılır.
        Senaryo sonuç raporu oluşturulur.
        """

        if self.attack_active and self.attack_start_time:
            total_time = time.time() - self.attack_start_time

            self.log("")
            self.log("=" * 50)
            self.log("📊 SENARYO SONUÇ RAPORU")
            self.log("=" * 50)
            self.log("   Senaryo: Hayali İstasyon (Status Spoofing)")
            self.log("   Saldırı Türü: MitM + Mesaj Manipülasyonu")
            self.log(f"   Toplam Süre: {total_time:.2f} saniye")
            self.log("   Sonuç: SALDIRI TESPİT EDİLDİ ✓")
            self.log("=" * 50)

            self.attack_active = False
            self.attack_start_time = None

    def _detect_anomaly(self, payload):
        """
        Mantıksal anomali tespiti simülasyonu.
        Gerçek sistemde davranışsal analiz veya ML modeli kullanılabilir.
        """

        anomaly_score = 0

        # Uzun süre Available olma durumu (simülasyon)
        if payload.get("status") == "Available":
            anomaly_score += 40
            self.log("   🔍 Uzun süre 'Available' durumu şüpheli")

        # Hata kodu olmaması ama işlem yokluğu varsayımı
        if payload.get("errorCode") == "NoError":
            anomaly_score += 30
            self.log("   🔍 İşlem olmadan 'NoError' durumu")

        # Davranışsal tutarsızlık
        anomaly_score += 30
        self.log("   🔍 Davranışsal tutarsızlık tespit edildi")

        self.log(f"   📈 Anomali Skoru: {anomaly_score}/100")

        return anomaly_score >= 60
