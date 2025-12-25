# PROJE: ANOMALİ SENARYO BELGESİ

Senaryo Adı: Harici CAN Yansıtma (Reflection) ile Dahili Güç Elektroniği Manipülasyonu

---

## 1. AMAÇ

Bu senaryonun amacı, bir DC hızlı şarj istasyonundaki (EVSE) kritik bir siber-fiziksel zafiyeti göstermektir. Zafiyet, şarj istasyonunun ana denetleyicisinin (MCU - Microcontroller Unit), harici (araç tarafı) CAN veriyolu ile dahili (operasyonel taraf - örn. güç elektroniği) CAN veriyolu arasındaki "gateway" (ağ geçidi) görevini güvenli bir şekilde yerine getirememesinden kaynaklanır.
Amaç, bir saldırganın, şarj portuna (örn. CCS) bağladığı özel bir cihaz aracılığıyla, kendini şarj istasyonunun dahili bir bileşeniymiş gibi tanıtarak (Spoofing) sahte CAN mesajları göndermesini ve bu mesajların zayıf gateway filtresini aşarak (Reflection) güç elektroniği gibi kritik modülleri doğrudan manipüle etmesini (Tampering) simüle etmektir.

## 2. KAPSAM

Bu senaryo, özellikle CCS (Combined Charging System) standardını kullanan DC hızlı şarj istasyonlarını hedef almaktadır.
**Kapsam İçi (In-Scope):**
• DC Hızlı Şarj İstasyonu (EVSE) donanımı.
• Ana Denetleyici (MCU) üzerindeki CAN Gateway (Ağ Geçidi) mantığı.
• Harici (Araç) CAN veriyolu arayüzü (CCS portu üzerinden).
• Dahili (Operasyonel) CAN veriyolu ve bağlı bileşenler (Güç Elektroniği Denetleyicisi, Batarya Yönetim Sensörleri vb.).

**Kapsam Dışı (Out-of-Scope):**
• AC (Alternatif Akım) şarj istasyonları (Type 2 vb.).
• OCPP, CSMS gibi IT/bulut katmanı protokolleri (Bu saldırı fiziksel ve yerel bir saldırıdır).
• Cihazın bellenimini (firmware) ele geçirme (Bu senaryo cihazın yazılımının sağlıklı olduğunu, ancak konfigürasyonunun hatalı olduğunu varsayar).

## 3. SORUN VE KÖK NEDEN

**Sorun:** Fiziksel erişime sahip bir saldırgan, şarj portuna bağladığı bir cihazla, şarj istasyonunun gerçekte desteklemediği veya o an için güvenli olmayan voltaj/akım seviyelerini talep edebilir. Bu durum, istasyonun kendisine, bağlı bir araca (veya simülatöre) ve hatta şebekeye zarar verme potansiyeline sahip donanımsal bir arızaya yol açabilir.
**Kök Neden:** Sorunun kök nedeni, "Yetersiz CAN Gateway İzolasyonu ve Filtrelemesi" olarak tanımlanabilir. Çoğu şarj cihazında MCU, hem araçla (harici CAN) hem de kendi iç bileşenleriyle (dahili CAN) konuşur. Güvenli bir tasarımda, bu iki ağ arasında katı bir "güvenlik duvarı" (firewall) olmalıdır. Bu senaryodaki kök neden, bu gateway'in;

1. Yön Bağımlı Filtreleme Yapmaması: Harici (araç) porttan gelen bir mesajın, dahili bir bileşenin CAN ID'sine (örn. 0x201 - Güç Kontrol) sahip olmasına izin vermesi.
2. Beyaz Liste (Whitelist) Kullanmaması: Harici porttan sadece araçtan gelmesi beklenen (örn. 0x300 - Araç Durumu) ID'leri kabul etmek yerine, tüm ID'lere izin vermesi (veya en azından kritik ID'leri engellememesi).
3. İletme (Forwarding) Mantığı: Gelen sahte mesajı (örn. "Güç Elektroniği, voltajı 800V yap") bir hata olarak ayıklamak yerine, "Bu mesajın hedefi iç ağdaymış" diyerek olduğu gibi dahili ağa iletmesi (yansıtması).

## 4. TEHDİT MODELİ & SENARYO

**STRIDE Kategorisi:** Spoofing (Kimlik Hırsızlığı - Saldırganın kendini dahili bir bileşen gibi göstermesi) ve Tampering (Manipülasyon - Güç elektroniği komutlarının değiştirilmesi).
**Saldırgan Profili:** Orta düzey teknik bilgiye sahip. CAN-bus protokolünü, can-utils gibi araçları ve temel gömülü sistemleri bilen. Özel donanıma (Raspberry Pi + CAN Transceiver) sahip.
**Hedef Varlık:** Güç Elektroniği Denetleyicisi (Fiziksel) ve MCU Gateway Mantığı (Mantıksal).

**Aşamalı Saldırı Senaryosu:**
• **Aşama 1: Fiziksel Erişim ve Keşif**
o Saldırgan, hedef şarj istasyonuna meşru bir EV (veya EV simülatörü) bağlar.
o Araya bir "CAN-in-the-middle" cihazı (örn. PCAN analizör veya cansniffer çalıştıran bir RPi) yerleştirerek şarj seansını başlatır.
o MCU ile Güç Elektroniği arasındaki dahili komutları (örn. CAN ID: 0x210, Data: [Voltaj, Akım, ...]) ve bunların araçtan gelen taleplerle ilişkisini analiz ederek kritik CAN ID'lerini öğrenir.
• **Aşama 2: Hazırlık ve Bağlantı**
o Saldırgan, meşru aracı devreden çıkarır.
o Kendi saldırı cihazını (RPi + CAN Transceiver) doğrudan şarj istasyonunun CCS portundaki CAN pinlerine (CAN-H, CAN-L) bağlar.
o Cihaz, istasyonun bir araç bağlandığını sanması için gerekli temel el sıkışma (handshake) mesajlarını (eğer gerekiyorsa) taklit eder.
• **Aşama 3: Kimlik Hırsızlığı ve Yansıtma (Spoofing & Reflection)**
o Saldırı cihazı, harici porttan olmasına rağmen, kendini dahili MCU gibi tanıtan bir CAN mesajı yayınlamaya başlar.
o Örnek Saldırı Paketi:
 CAN ID: 0x210 (Aşama 1'de keşfedilen "Güç Elektroniği Ayar" ID'si)
 Veri (Data): [0F A0 0C 80 00 00 00 01]
 Anlamı (Varsayımsal): Voltajı 900V (0x0FA0), Akımı 300A (0x0C80) ayarla, şarjı başlat (0x01).
• **Aşama 4: Yürütme ve Manipülasyon (Execution & Tampering)**
o Şarj istasyonunun MCU'su, bu mesajı harici (araç) portunda alır.
o Zafiyet (Kök Neden) burada tetiklenir: MCU'nun gateway mantığı, "Bu ID (0x210) harici porttan gelmemeli" diye bir kurala sahip değildir.
o MCU, bu paketi "hedefine" (Güç Elektroniği) ulaştırmak için olduğu gibi dahili CAN veriyoluna iletir (yansıtır).
o Güç Elektroniği Denetleyicisi, bu komutun MCU'dan geldiğini zanneder (çünkü ID ve format doğrudur) ve tehlikeli voltaj/akım seviyesini ayarlamaya çalışır.
• **Aşama 5: Fiziksel Sonuç**
o (Fiziksel ortamda) İstasyona hiçbir araç bağlı olmamasına rağmen (veya sahte bir yük bağlıysa), güç elektroniği modülleri maksimum kapasitede çalışmaya zorlanır.
o Bu durum, sigortaların atmasına, kontaktörlerin zarar görmesine, güç modüllerinin aşırı ısınarak yanmasına veya istasyonun kalıcı bir donanım arızası durumuna geçmesine neden olur.

## 5. SİMÜLASYON TEST ORTAMI

Bu senaryodaki siber-fiziksel zafiyeti (Kök Neden 3) güvenli, maliyetsiz ve tekrarlanabilir bir şekilde kanıtlamak için, test ortamı fiziksel donanım yerine sanal bir simülasyon olarak kurgulanmıştır.
Simülasyon, fiziksel bir CAN veriyolunun davranışlarını taklit eden sanal ağ arayüzleri kullanılarak gerçekleştirilecektir.
• **Platform:** Python 3.x
• **Kütüphane:** python-can (CAN veriyolu protokollerini simüle etmek için)
• **Mimari:** İki adet sanal CAN arayüzü (vcan0 ve vcan1)
o vcan0 (Harici Ağ): Saldırganın bağlandığı, aracın bulunduğu ağı temsil eder.
o vcan1 (Dahili Ağ): Güç elektroniği gibi kritik iç bileşenlerin bulunduğu ağı temsil eder.
• **Simüle Edilen Bileşenler (Python Scriptleri):** 1. **Saldırı Cihazı (saldirgan.py):** vcan0 (Harici Ağ) arayüzüne bağlanır. Bu ağa, normalde dahili ağda olması gereken bir komut olan ID: 0x210 (Güç Elektroniği Ayar) paketini gönderir. 2. **Zafiyetli Gateway/MCU (zafiyetli_gateway.py):** İki sanal ağ arasında köprü görevi görür. vcan0'ı dinler, gelen mesajı alır ve (zafiyet burada!) hiçbir ID/yön filtrelemesi yapmadan olduğu gibi vcan1'e yansıtır. 3. **Kurban (Güç Elektroniği Denetleyicisi) (guc_elektronigi.py):** Sadece vcan1 (Dahili Ağ) arayüzünü dinler. ID: 0x210 olan bir komut alırsa, saldırının başarılı olduğunu belirten bir alarmı terminale basar.

## 6. BAŞARI ÖLÇÜTLERİ (SİMÜLASYON)

Senaryonun sanal ortamda başarılı kabul edilmesi için aşağıdaki koşulların gözlemlenmesi gerekir:

1. **Yansıtmanın Tespiti:** zafiyetli_gateway.py script'inin, vcan0 (harici) ağından gelen ID: 0x210 paketini algıladığı ve bu paketi vcan1 (dahili) ağına başarılı bir şekilde ilettiğinin (yansıttığının) terminal çıktısında gözlemlenmesi.
2. **Komutun İcrası (Simülasyon):** guc_elektronigi.py script'inin, vcan1 (dahili) ağı üzerinde, normalde asla harici ağdan gelmemesi gereken ID: 0x210 paketini aldığı anda "TEHLİKE: YETKİSİZ KOMUT ALINDI" veya benzeri bir kritik uyarıyı terminale yazdırması.
3. **Engelleme Olmaması:** Zafiyetli Gateway'in, bu anormal (harici porttan gelen dahili ID) paketi bir tehdit olarak algılayıp engellemediğinin veya loglamadığının (yani, paketi sorunsuzca ilettiğinin) doğrulanması.

## 7. NASIL ENGELLERİZ / ETKİSİNİ AZALTIRIZ (ÖNLEMLER)

Bu siber-fiziksel saldırıyı engellemek için savunma, gateway (ağ geçidi) katmanında yoğunlaşmalıdır.
• **Katman 1: Katı Gateway Filtrelemesi (En Kritik Önlem)**
o MCU'nun gateway yazılımı, yön bağımlı (direction-aware) bir filtreleme mantığına sahip olmalıdır.
o Kural (Örnek): Harici (araç) porttan gelen veriler arasında 0x210, 0x21A, 0x201 (tüm dahili kontrol ID'leri) bulunuyorsa, bu paketler KESİNLİKLE yok edilmeli (drop) ve dahili ağa asla iletilmemelidir.
o Beyaz Liste (Whitelist): Harici port, sadece bilinen ve araçtan gelmesi beklenen CAN ID'lerini (örn. ISO 15118 veya CHAdeMO standardında tanımlı ID'ler) kabul etmelidir.
• **Katman 2: Dahili Ağ Saldırı Tespiti (IDS)**
o MCU, dahili veriyolunu da sürekli izlemelidir.
o Eğer Güç Elektroniği, MCU'nun kendisinin göndermediği bir komuta (0x210) yanıt veriyorsa (örn. "voltaj ayarlandı" ACK mesajı), MCU bunun bir "yansıtma" veya "spoofing" saldırısı olduğunu anlamalı, tüm sistemi derhal güvenli bir duruma (örn. acil durdurma) getirmeli ve olayı CSMS'e raporlamalıdır.
• **Katman 3: Fiziksel Güvenlik ve Mantıksal Kontroller**
o (Fiziksel ortamda) Güç elektroniği modülleri, MCU'dan gelen komutları körü körüne uygulamalıdır. Örneğin, "Araca bağlı değilken 900V ver" komutu, donanımsal bir güvenlik mantığı (interlock) tarafından "imkansız talep" olarak reddedilmelidir.

## 8. KAYNAKÇA (Referanslar)

1. Idaho National Laboratory (INL). (2020). Cyber Security Research and Development – CAN Bus Security Research Across Multiple Sectors. (Rapor No: INL/RPT-18-51111). U.S. Department of Energy.
2. ArXiv. (2025). Physical-Layer Signal Injection Attacks on EV Charging Ports: Bypassing Authentication via Electrical-Level Exploits.
3. Chowdhury, M. M. R., et al. (2021). "Cybersecurity of Electric Vehicle Charging Infrastructure: A Review on Attack and Defense." IEEE Access, Cilt 9.
4. ResearchGate. (2024). Cyber-Physical Security Trends of EV Charging Systems: A Survey.
5. ISO 15118-2:2014. Road vehicles -- Vehicle to grid communication interface -- Part 2: Network and application protocol requirements.
6. Miller, C., & Valasek, C. (2018). A Hacker's Guide to Automotive CAN Bus.
7. Murad, M. A. A., et al. (2022). "Development and Validation of V2G Technology for Electric Vehicle Chargers Using Combo CCS Type 2 Connector Standards". Energies, 15(19), 7364.
