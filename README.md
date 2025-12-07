# 🔌 OCPP–CAN Güvenlik Laboratuvarı

<div align="center">

**Elektrikli Araç Şarj Altyapısı Saldırı/Savunma Simülasyon Ortamı**

*Elektrikli araç şarj altyapısı için modüler güvenlik test çerçevesi*

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Lisans](https://img.shields.io/badge/lisans-MIT-green.svg)](LICENSE)
[![OCPP](https://img.shields.io/badge/OCPP-1.6%20%7C%202.0-orange.svg)](https://www.openchargealliance.org/)

</div>

---

## 📖 Genel Bakış

**OCPP–CAN Güvenlik Laboratuvarı**, Elektrikli Araç (EV) şarj altyapısını güvenlik açısından test etmek için geliştirilmiş modüler bir simülasyon laboratuvarıdır. Proje, OCPP mesaj akışı ile EV iç CAN-Bus davranışını birleştirerek saldırı senaryoları ve savunma mekanizmaları geliştirmeyi amaçlar.

Bu çerçeve, **Şarj Noktası (CP)** ile **Merkezi Sistem Yönetim Sistemleri (CSMS)** arasındaki gerçek dünya iletişim akışını simüle eder ve EV tarafındaki CAN-Bus davranışı ile genişletilmiştir.

### ⚡ Ana Özellikler

- 🔄 **OCPP İstemci & Sunucu Emülasyonu** - Tam şarj noktası protokol simülasyonu
- 🔀 **OCPP → CAN Çeviri Katmanı** - Şarj protokolü ile araç veri yolu arasında köprü
- 🚌 **CAN-Bus Simülasyonu** - Gerçekçi test için sanal CAN arayüzü (vcan0)
- 🎯 **Saldırı Senaryoları** - Modüler anomali enjeksiyon sistemi

---

## 🏗️ Proje Yapısı

```
ocpp-can-lab/
│
├── 📁 infra/                      # Temel altyapı bileşenleri
│   ├── ocpp_client.py             # Şarj Noktası emülatörü
│   ├── ocpp_server.py             # CSMS emülatörü
│   ├── mapping.py                 # OCPP → CAN dönüşüm mantığı
│   ├── pipeline.py                # Hook sistemi + CP işlem hattı
│   ├── setup_vcan.sh              # VCAN kurulum scripti
│   └── __init__.py
│
├── 📁 scenarios/                  # Senaryolar (her biri kendi klasöründe)
│   ├── _template/                 # Yeni senaryolar için şablon
│   ├── scenario_00_baseline/      # Temel senaryo (saldırı yok)
│   └── scenario_01_*/             # Örnek saldırı senaryoları
│
├── 📁 logs/                       # Çalışma çıktıları (git'de ignore)
│
├── 📁 .devcontainer/              # Codespaces geliştirme ortamı
├── requirements.txt               # Python bağımlılıkları
├── config.json                    # Proje yapılandırması
└── README.md
```

---

## 🚀 Hızlı Başlangıç

### 1️⃣ Sanal Ortamı Kurun (Codespace'de mevcut gerek yok)

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

### 3️⃣ CSMS Sunucusunu Başlatın

```bash
python -m infra.ocpp_server
```

### 4️⃣ Şarj Noktası İstemcisini Çalıştırın

```bash
python -m infra.ocpp_client
```

---

## 🧪 Temel Senaryo (Baseline)

`scenario_00_baseline/` dizini **saldırı içermeyen** temiz bir referans senaryosu içerir. Pipeline işlevselliğini doğrulamak için kullanın.

**Temel senaryoyu çalıştırın:**

```bash
python -m scenarios.scenario_00_baseline.simulate
```

Beklenen çıktı: Anomali içermeyen normal OCPP ↔ CAN iletişim akışı.

---

## 🧩 Yeni Senaryo Oluşturma

Her senaryo `scenarios/` altında kendi dizininde yaşar:

```
scenarios/scenario_XY_isim/
   ├── hooks.py          # Saldırı mantığı hook'ları
   ├── simulate.py       # Senaryo giriş noktası
   └── README.md         # (Opsiyonel) senaryo dokümantasyonu
```

### Hook Fonksiyonları

Pipeline'ın farklı aşamalarında veri manipülasyonu yapın:

| Hook | Tetiklenme Noktası |
|------|-------------------|
| `pre_ocpp()` | OCPP mesajı gönderilmeden önce |
| `post_ocpp()` | OCPP cevabı alındıktan sonra |
| `pre_can()` | CAN frame gönderilmeden önce |
| `post_can()` | CAN frame gönderildikten sonra |

### Saldırı Örnekleri

✅ Mesaj manipülasyonu  
✅ Sahte değer enjeksiyonu  
✅ Kötü amaçlı paket oluşturma  
✅ Debug arka kapısı ekleme  
✅ CAN frame enjeksiyonu  

---

## 🛠️ Geliştirici Rehberi

### Yeni Senaryo Oluşturma

```bash
# Feature branch oluştur
git checkout dev
git pull
git checkout -b feature/scenario_xx

# Şablonu kopyala
cp -r scenarios/_template scenarios/scenario_xx_yeni_saldiri

# hooks.py içinde hook'larınızı geliştirin
# Yerel olarak test edin
python -m scenarios.scenario_xx_yeni_saldiri.simulate
```

### Commit ve Push

```bash
git add .
git commit -m "Senaryo XX eklendi: [saldırı açıklaması]"
git push origin feature/scenario_xx
```

`dev` branch'ine merge etmek için Pull Request açın.

---

---

## 👥 Takım İşbirliği

- 🌿 Her öğrenci senaryosu için **ayrı branch** oluşturur
- ⚙️ Pipeline tüm senaryoları otomatik olarak işler
- ☁️ **Codespaces hazır** - Linux kurulumu gerektirmez
- 🔄 Tüm testler `vcan0` üzerinde çalışır - **deterministik** ve **tekrarlanabilir**

---

## 📊 Test ve Doğrulama

### Tüm Senaryoları Çalıştır

```bash
# Tüm senaryoları sırayla çalıştır
for scenario in scenarios/scenario_*/; do
    python -m "${scenario%/}.simulate"
done
```

### CAN Trafiğini İzle

```bash
# Gerekirse can-utils kurun
sudo apt-get install can-utils

# Sanal CAN arayüzünü izle
candump vcan0
```

---

## 🤝 Katkıda Bulunma

1. Repository'yi fork edin
2. Feature branch'inizi oluşturun (`git checkout -b feature/MuhteşemSenaryo`)
3. Değişikliklerinizi commit edin (`git commit -m 'Muhteşem saldırı senaryosu eklendi'`)
4. Branch'inizi push edin (`git push origin feature/MuhteşemSenaryo`)
5. Pull Request açın

---

---

---

<div align="center">

**CanBus Araştırması için geliştirildi**

⭐ Faydalı bulduysanız bu repo'ya yıldız verin!

</div>
