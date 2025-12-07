# 🔌 OCPP–CAN Güvenlik Laboratuvarı

**EV Charging Infrastructure Attack/Defense Simulation Environment**

## 📖 Genel Bakış

OCPP–CAN Güvenlik Laboratuvarı, Elektrikli Araç (EV) şarj altyapısını güvenlik açısından modellemek ve analiz etmek için oluşturulmuş modüler bir simülasyon ortamıdır. Proje, OCPP mesaj akışı ile EV içindeki CAN-Bus davranışını birleştirerek saldırı senaryolarının modellenmesini mümkün kılar.

Bu yapı, Şarj Noktası (CP) ile Merkezi Sistem Yönetim Sistemi (CSMS) arasındaki gerçek dünya iletişimini simüle eder ve EV tarafındaki CAN-Bus davranışlarıyla genişletilir.

## ⚡ Ana Özellikler

- 🔄 **OCPP İstemci & Sunucu Emülasyonu** – Tam şarj noktası protokol simülasyonu
- 🔀 **OCPP → CAN Çeviri Katmanı** – OCPP mesajlarının CAN-Bus verisine dönüştürülmesi
- 🚌 **CAN-Bus Simülasyonu** – vcan0 tabanlı sanal araç veri yolu
- 🎯 **Modüler Saldırı Senaryoları** – Hook tabanlı anomali enjeksiyon sistemi
- 🛡 **Geleceğe Uygun** – IDS, telemetri ve savunma mekanizmaları eklemeye hazır mimari

## 🏗 Proje Yapısı

```
ocpp-can-lab/
│
├── infra/                      # Temel altyapı bileşenleri
│   ├── ocpp_client.py          # Şarj Noktası (CP) emülatörü
│   ├── ocpp_server.py          # CSMS emülatörü
│   ├── mapping.py              # OCPP → CAN dönüşüm mantığı
│   ├── pipeline.py             # Hook sistemi + işlem hattı
│   ├── setup_vcan.sh           # VCAN kurulumu
│   └── _init_.py
│
├── scenarios/                  # Senaryolar (her biri kendi klasöründe)
│   ├── _template/              # Yeni senaryo şablonu
│   ├── scenario_00_baseline/   # Temiz referans senaryosu (saldırı yok)
│   └── scenario_01_*/          # Örnek saldırı senaryoları
│
├── logs/                       # Çalışma çıktıları (gitignore)
├── .devcontainer/              # Codespaces geliştirme ortamı
├── requirements.txt            # Python bağımlılıkları
├── config.json                 # Proje yapılandırması
└── README.md
```

## 🚀 Hızlı Başlangıç

### 1️⃣ Sanal Ortamı Kurun (Yalnızca Linux)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2️⃣ CAN Simülasyon Arayüzünü Etkinleştirin (Linux)

```bash
sudo bash infra/setup_vcan.sh
```

Bu komut otomatik olarak `vcan0` sanal CAN arayüzünü oluşturur.

## ▶ Çalıştırma Sırası

Her komut ayrı bir terminalde çalıştırılmalıdır. Sistem daima şu sırayı izler:

### Terminal 1 — CSMS Sunucusunu Başlatın

```bash
python -m infra.ocpp_server
```

### Terminal 2 — Şarj Noktası (CP) İstemcisini Başlatın

```bash
python -m infra.ocpp_client
```

## 🎯 Senaryo Çalıştırma (Opsiyonel)

Senaryolar sunucu çalıştıktan sonra başlatılır. Her zaman ayrı bir terminalde çalıştırılır.

### Terminal 3 — Örnek Senaryo

```bash
python -m scenarios.scenario_01_debug_backdoor.simulate
```

Senaryolar, pipeline üzerinden OCPP ve CAN mesajlarını manipüle eder.

## 🧪 Temel Senaryo (Baseline)

`scenario_00_baseline/` dizini saldırı içermeyen referans akışını içerir.

Çalıştırmak için (yine ayrı bir terminal):

```bash
python -m scenarios.scenario_00_baseline.simulate
```

**Beklenen çıktı:**
- ✔ Normal OCPP ↔ CAN mesaj akışı
- ✔ Herhangi bir anomali yok

## 🧩 Yeni Senaryo Oluşturma

Yeni bir senaryo dizin yapısı şöyledir:

```
scenarios/scenario_XY_yeni_senaryo/
   ├── hooks.py        # Hook tabanlı saldırı mantığı
   ├── simulate.py     # Senaryo giriş noktası
   └── README.md       # (Opsiyonel) senaryo açıklaması
```

### Hook Fonksiyonları

| Hook | Açıklama |
|------|----------|
| `pre_ocpp()` | OCPP mesajı gönderilmeden önce |
| `post_ocpp()` | OCPP cevabı alındıktan sonra |
| `pre_can()` | CAN frame gönderilmeden önce |
| `post_can()` | CAN frame gönderildikten sonra |

### Olası Saldırılar

- Mesaj manipülasyonu
- Sahte değer enjeksiyonu
- CAN paket enjeksiyonu
- Yetkisiz frame yaratma
- Debug arka kapısı ekleme

## 📝 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Detaylar için LICENSE dosyasına bakın.

## 🙏 Teşekkürler

- OCPP protokolü için Open Charge Alliance
- CAN-bus için Python-CAN topluluğu
- EV güvenliği araştırmaları yürüten tüm araştırmacılar

---

**EV altyapı güvenliği için ❤ ile geliştirilmiştir.**
