🔌 OCPP–CAN Security Lab
EV Charging Infrastructure Attack/Defense Simulation Environment
Bu proje, Elektrikli Araç (EV) şarj altyapısını güvenlik açısından test etmek için geliştirilmiş modüler bir simülasyon laboratuvarıdır.
 Amaç, OCPP mesaj akışı ile EV iç CAN-Bus davranışını birleştirerek saldırı senaryoları ve savunma mekanizmaları geliştirmektir.

⚡ Ana Özellikler
OCPP (Open Charge Point Protocol) istemci & sunucu emülasyonu


OCPP → CAN dönüşüm katmanı


vcan0 üzerinden CAN-Bus simülasyonu


Saldırı senaryoları (anomaly scenarios)


Gelecekte: Savunma mekanizmaları, IDS, ML/RAG destekli analiz


Bu yapı, gerçek hayattaki CP (Charge Point) ↔ CSMS (Central System) iletişim akışını simüle eder ve EV tarafındaki CAN-Bus davranışı ile genişletir.

📂 Proje Yapısı
ocpp-can-lab/
│
├── infra/                      # Temel altyapı bileşenleri
│    ├── ocpp_client.py         # Charge Point emülatörü
│    ├── ocpp_server.py         # CSMS emülatörü
│    ├── mapping.py             # OCPP → CAN dönüşüm mantığı
│    ├── pipeline.py            # Hook sistemi + CP işlem hattı
│    ├── setup_vcan.sh          # VCAN kurulum scripti
│    └── __init__.py
│
├── scenarios/                  # Senaryolar (her biri kendi klasöründe)
│    ├── _template/             # Yeni senaryolar için şablon
│    ├── scenario_00_baseline/  # Temel senaryo (saldırı yok)
│    └── scenario_01_*          # Örnek saldırı senaryosu
│
├── logs/                       # Çalışma çıktıları (git tarafında ignore)
│
├── .devcontainer/              # Codespaces geliştirme ortamı
├── requirements.txt
├── config.json                 # Proje yapılandırma ayarları
└── README.md


🚀 Kurulum ve Çalıştırma
1️⃣ Sanal ortam oluşturun
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


2️⃣ CAN simülasyon arayüzünü etkinleştirin (Linux)
sudo bash infra/setup_vcan.sh

Bu komut otomatik olarak vcan0 arayüzünü oluşturur.

3️⃣ CSMS Sunucusunu Başlatın
python -m infra.ocpp_server


4️⃣ Charge Point (CP) İstemcisini Çalıştırın
python -m infra.ocpp_client


🧪 Baseline Senaryosu
scenario_00_baseline/ hiçbir saldırı içermeyen temel referans senaryosudur.
 Pipeline’ın doğru çalıştığını doğrulamak için kullanılır.
Çalıştırmak için:
python -m scenarios.scenario_00_baseline.simulate


🧩 Yeni Senaryo Oluşturma
Her senaryo kendi klasöründe yaşar:
scenarios/scenario_XY_name/
   ├── hooks.py
   ├── simulate.py
   └── README.md (opsiyonel)

Hook fonksiyonlarıyla manipülasyon yapabilirsiniz:
pre_ocpp() → OCPP mesajı gönderilmeden önce


post_ocpp() → OCPP cevabı alındıktan sonra


pre_can() → CAN frame gönderilmeden önce


post_can() → CAN frame gönderildikten sonra


Bu fonksiyonlarla:
✔ Mesaj değiştirme
 ✔ Sahte değer ekleme
 ✔ Saldırı paketleri oluşturma
 ✔ Debug arka kapısı ekleme
 ✔ CAN frame enjeksiyonu
gibi işlemler yapılabilir.

🛠 Geliştirici Rehberi (Kısa)
➤ Yeni senaryo için:
git checkout dev
git pull
git checkout -b feature/senaryo_xx

cp -r scenarios/_template scenarios/scenario_xx_yeni_senaryo

Test:
python -m scenarios.scenario_xx_yeni_senaryo.simulate

Commit:
git add .
git commit -m "Senaryo XX eklendi"
git push origin feature/senaryo_xx

Pull Request aç → dev branch’ine merge edilir.

🔐 Gelecek Çalışmalar (Roadmap)
12 anomaly senaryosunun tam saldırı modelleri


CAN + OCPP için IDS (Intrusion Detection System)


Gerçek zamanlı dashboard + telemetri


Savunma scriptleri (anti-manipulation filters)



👥 Takım Notları
Her öğrenci kendi senaryosu için ayrı branch açar


Pipeline her senaryoyu otomatik olarak işler


Codespace sayesinde herkes Linux kurmadan çalışabilir


Tüm testler vcan0 üzerinden tekrarlanabilir ve deterministik sonuç verir

