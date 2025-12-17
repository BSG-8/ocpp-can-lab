# Anomali Senaryosu: "Protokol Köprüsü" Üzerinden Gizli Talep Manipülasyonu

Bu belge, elektrikli araç (EV) şarj altyapısı için gelişmiş bir siber-fiziksel anomali senaryosunu ve bu senaryonun SWOT analizini detaylandırmaktadır.

## 1. Anomali Senaryosu

Senaryo, bir saldırganın hem şarj altyapısını (OCPP) hem de istasyonun iç donanımını (CAN bus) hedef alarak, merkezi sistemleri aldatırken fiziksel şebekeye zarar verdiği gelişmiş ve tespiti zor bir birleşik saldırıyı (FDI + Mad) temel alır.

### A. Hedef ve Kapsam
*   **Saldırganın Amacı:** Dağıtım Sistemi Operatörünün (DSO) veya Şarj Noktası Operatörünün (CPO) haberi olmadan, kontrol altındaki çok sayıda şarj istasyonu (CP) üzerinden koordineli bir talep artışı başlatmak. Nihai hedef, yerel bir transformatörü aşırı yüklemek veya daha geniş ölçekte şebeke kararsızlığına (örn. frekans düşmesi) yol açmaktır.
*   **Hedef Altyapı:** Zayıf siber güvenlik önlemlerine sahip (örn. zayıf şifreleme, ağ segmentasyonu eksikliği) halka açık Şarj İstasyonları (CP).

### B. Saldırı Vektörü: Protokol Köprüsü
Bu saldırı, Şarj İstasyonunun (CP) iki farklı ağı birbirine bağlayan bir "köprü" görevi görmesi üzerine kuruludur:
1.  **IT Ağı (OCPP):** CP'nin buluttaki merkezi yönetim sistemi (CSMS) ile konuştuğu, internet tabanlı protokoldür.
2.  **OT Ağı (CAN Bus):** CP'nin içindeki donanımların (güç elektroniği, röleler, sayaçlar) kendi aralarında haberleştiği yerel, endüstriyel protokoldür.

Saldırgan, CP'nin ana kontrolcüsünü (MCU) ele geçirerek bu iki ağ arasında bir köprü kurar.

### C. Saldırı Aşamaları (Birleşik Saldırı)

#### Aşama 1: Sahte Veri Enjeksiyonu (FDI - Yemleme)
Saldırgan, ele geçirdiği CP'nin OCPP protokolü üzerinden merkezi sisteme (CSMS) sahte ve normal görünen veriler göndermesini sağlar.
*   **Eylem:** CP, merkezi sisteme `MeterValues` (Sayaç Değerleri) mesajlarında düşük veya "0" (sıfır) enerji tüketimi raporlar.
*   **Sonuç (Siber Katman):** Merkezi sistem (CPO/DSO), bu istasyonun ya boşta olduğunu ya da çok az enerji çektiğini düşünür.

#### Aşama 2: Talep Manipülasyonu (Mad - Fiziksel Etki)
Aynı anda, saldırgan CP'nin iç ağına müdahale eder.
*   **Eylem:** CP'nin ana kontrolcüsü (MCU), merkezi sistemden bağımsız olarak, doğrudan güç elektroniğini kontrol eden CAN bus ağına özel hazırlanmış komutlar (örn. CAN ID `0x210`, payload: `[max_current]`) gönderir.
*   **Sonuç (Fiziksel Katman):** Bu komut, istasyona bağlı olan araca maksimum kapasitede güç çekmesi talimatını verir.

### D. Anomali ve Tespiti
*   **Anomali:** Siber (bildirilen) durum ile fiziksel (gerçek) durum arasında büyük bir uyumsuzluk oluşur.
*   **Tespit Zorluğu:** Geleneksel IDS sistemleri ya sadece OCPP trafiğini ya da sadece şebeke yükünü izler. Bu birleşik saldırı, ancak her iki alandan gelen verileri birleştiren gelişmiş IDS sistemleri tarafından tespit edilebilir.

---

## 2. SWOT Analizi (Saldırgan Perspektifinden)

### Strengths (Güçlü Yönler)
*   **Yüksek Gizlilik (Stealth):** Saldırı, sahte veri enjeksiyonu (FDI) kullanarak siber katmanda normal bir operasyon görüntüsü yaratır.
*   **Doğrudan Fiziksel Etki:** Saldırı, protokol seviyesinde kalmayıp, CAN bus aracılığıyla doğrudan donanımı manipüle ederek fiziksel talep artışına neden olur.
*   **Birleşik Saldırı:** Hem FDI hem de Mad tekniklerini birleştirmesi, tek bir veri kaynağını izleyen basit IDS sistemlerini atlatmasını sağlar.

### Weaknesses (Zayıf Yönler)
*   **Yüksek Teknik Bilgi Gereksinimi:** Saldırganın hem IT hem de OT konularında derin teknik bilgiye sahip olması gerekir.
*   **Ön Koşul (CP Sızması):** Saldırı, CP'nin ana kontrolcüsüne (MCU) sızılmasını gerektirir.
*   **Ölçeklenme Zorunluluğu:** Şebeke üzerinde gerçek bir etki yaratmak için tek bir CP yeterli değildir.

### Opportunities (Fırsatlar)
*   **Zayıf Güvenlikli Ekipmanlar:** Şifresiz veya zayıf TLS sertifikalı OCPP iletişimi kullanan istasyonlar.
*   **Segmentasyon Eksikliği:** CP içinde IT ve OT ağları arasında yeterli izolasyon olmaması.
*   **Gelişmiş IDS Eksikliği:** Çoğu operatörün henüz şebeke verileri ile şarj verilerini çapraz kontrol eden sistemlere sahip olmaması.

### Threats (Tehditler)
*   **Gelişmiş Tespit Sistemleri:** Şebeke verileri ile CPO raporlarını karşılaştıran IDS sistemleri.
*   **Güvenli Donanım ve Yazılım:** Secure Boot ve imzalı firmware kullanımı.
*   **Güçlü Kriptografi:** mTLS veya CAN katmanında mesaj doğrulaması (HMAC).
