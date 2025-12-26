# Scenario 11: MCU DoS (CAN Bus-Off Attack)

## 📌 Senaryo Detayı
**Ele Geçirilmiş Denetleyici ile CAN Bus-Off Saldırısı**

Bu senaryo, ele geçirilmiş bir ana denetleyici (MCU) üzerinden iç CAN ağının flood (taşkın) saldırısına maruz bırakılmasını simüle eder. Saldırgan, yüksek öncelikli veya bozuk mesajlarla veri yolunu doldurarak meşru cihazların (örneğin güç elektroniği) iletişim kurmasını engeller ve onları "Bus-Off" durumuna sürükler.

---

## 🛠 Saldırının Çalışma Mantığı

1.  **İlk Erişim:** Saldırgan, bir zafiyet (örn. OCPP komut enjeksiyonu) veya kötü amaçlı bellenim güncellemesi ile MCU üzerinde kontrol sağlar.
2.  **Pivot:** Saldırgan, MCU'yu bir "köprü" olarak kullanarak iç CAN ağına erişir.
3.  **Taşkın (Flooding):**
    *   **Teknik A:** ID `0x000` (en yüksek öncelik) ile saniyede binlerce boş mesaj gönderilir.
    *   **Teknik B:** Kasıtlı hatalı çerçeveler ile ağ hata sayacını (TEC) artırır (Simülasyonda bu durum flood ile taklit edilir).
4.  **Sonuç (Bus-Off):** Kritik bileşenler (Güç Elektroniği) hat dolu olduğu için mesaj gönderemez, hata sayaçları sınır değerleri aşar ve kendilerini ağdan izole ederler (Bus-Off). Şarj işlemi durur.

---

## 🔍 Tespit Yöntemleri (Simülasyon Çıktıları)

Bu saldırı sırasında aşağıdaki anomaliler gözlemlenebilir:

1.  **CAN IDS (Loglar):**
    *   Veri yolu yükünde (Bus Load) %90+ seviyelerine ani artış.
    *   ID `0x000` mesaj frekansında aşırı yükselme.
    *   Meşru ID'lerin (örn. sayaç değerleri) frekansında düşüş veya tamamen kesilme.
2.  **OCPP Tarafı:**
    *   `MeterValues` akışının kesilmesi.
    *   CSMS'in şarj noktasını "Offline" veya yanıt veremez durumda görmesi.

---

## 🛡 Önleme ve Azaltma

*   **CAN Hız Sınırlaması (Rate Limiting):** MCU'nun belirli bir zaman diliminde gönderebileceği mesaj sayısını donanımsal olarak sınırlandırmak.
*   **Beyaz Liste (Whitelist):** Sadece izin verilen CAN ID'lerinin geçişine izin vermek.
*   **Segmentasyon:** Kritik güvenlik bileşenlerini (güvenlik ağ geçidi arkasında) MCU'dan izole etmek.
