# Anomali Senaryosu-2: Denetleyici ile CAN Bus-Off Saldırısı (D-02)

## 📌 Genel Bakış
Bu senaryo, ele geçirilmiş bir **Ana Denetleyici (MCU)** üzerinden dahili CAN veriyoluna yönelik bir **Hizmet Reddi (DoS)** saldırısını simüle eder. Saldırgan, CAN protokolünün hata yönetimi mekanizmasını istismar ederek güç elektroniği gibi kritik bileşenleri **Bus-Off** durumuna zorlar ve şarj işlemini fiziksel olarak durdurur.

## 🎯 Amaç
- **IT-OT Pivot:** Dış ağdan (OCPP) ele geçirilen bir cihazın iç ağı (CAN) nasıl felç edebileceğini göstermek.
- **Protokol Zafiyeti:** CAN protokolünün çarpışma önleme (arbitration) ve hata yönetimi mekanizmalarının nasıl silaha dönüştürülebileceğini kanıtlamak.
- **Kritik Etki:** Şarj istasyonunun kalıcı olarak devre dışı kalmasını simüle etmek.

## ⚙️ Saldırı Mekanizması
Saldırı, **Priority Flooding** (Öncelik Taşkını) tekniğini kullanır:

1. **Aşama 1 (Tetikleme):** Herhangi bir meşru CAN trafiği öncesinde (`pre_can`) hook devreye girer.
2. **Aşama 2 (Enjeksiyon):** Saldırgan kod, veriyoluna **ID 0x000** (en yüksek öncelik) sahip 100+ adet boş çerçeveyi çok kısa sürede enjekte eder.
3. **Aşama 3 (Sonuç):** 
   - Düşük öncelikli meşru mesajlar veriyoluna erişemez.
   - Hedef cihazlar (Güç Elektroniği) sürekli iletişim hatası algılar.
   - Hedef cihazların hata sayaçları (TEC) artar ve cihazlar **Bus-Off** moduna geçerek kendilerini kapatır.

## 🚀 Çalıştırma

### 1. Sunucuyu Başlatın
```bash
python -m infra.ocpp_server
```

### 2. Senaryoyu Başlatın
```bash
python -m scenarios.scenario_d02_can_bus_off.simulate
```

## 🔍 Gözlem ve Tespit
Log görüntüleyici (`streamlit run log_viewer/app.py`) üzerinden şunları gözlemleyebilirsiniz:

- **Anormal Yük:** Veriyolu yükü aniden tavan yapar.
- **ID 0x000 Fırtınası:** Zaman çizelgesinde yoğun bir `0x000` mesaj bloğu görülür.
- **İletişim Kesintisi:** Diğer meşru ID'lerden (örn. 0x200, 0x300 ex.) gelen mesajların akışı durur veya gecikir.

---
**Not:** Bu senaryo sanal bir ortamda (`vcan0`) gerçekleştiği için fiziksel bir donanımın "Bus-Off" olup kapandığını göremezsiniz; ancak loglarda saldırının yoğunluğunu ve protokol üzerindeki baskıyı net bir şekilde görebilirsiniz.
