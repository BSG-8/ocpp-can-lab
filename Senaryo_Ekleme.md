# 📘 Senaryo Geliştirme Kılavuzu

Bu döküman, OCPP–CAN Güvenlik Laboratuvarı'na yeni bir saldırı / arıza senaryosunun nasıl ekleneceğini adım adım açıklar. Her öğrenci veya geliştirici yeni bir senaryo eklerken bu sürece birebir uymalıdır.

## 🔱 1) Yeni Branch Oluşturma

Her senaryo ayrı bir feature branch üzerinde geliştirilir.

```bash
git checkout dev
git pull
git checkout -b feature/senaryo_xx
```

`senaryo_xx` → senaryonuzun numarasıdır.

**Örnek branch:**
```
feature/senaryo_03_meter_spoofing
```

## 📁 2) Yeni Senaryo Klasörünün Oluşturulması

Yeni senaryolar `scenarios/` dizini altında tutulur.

Yeni klasör oluşturmak için:

```bash
cd scenarios/
cp -r _template scenario_xx_yeni_senaryo
```

**Oluşan dizin yapısı:**

```
scenario_xx_yeni_senaryo/
   ├── simulate.py   → Senaryonun başlatıldığı dosya
   └── hooks.py      → OCPP & CAN manipülasyon kodları
```

Bu iki dosyayı kendi senaryonuza göre düzenleyeceksiniz.

## 🧩 3) Senaryoyu Aktifleştirme

Her senaryoda `simulate.py` içinde pipeline'a aktif senaryo atanır:

```python
pipeline.set_active_scenario("scenario_xx_yeni_senaryo")
```

Ad, dizin adıyla birebir aynı olmalıdır.

## ⚙ 4) Kod Geliştirme – Hook Sistemi

`hooks.py` dosyası senaryonuzun kalbidir. Pipeline her OCPP ve CAN adımında bu fonksiyonları çağırır.

### 🔹 4.1 pre_ocpp()

OCPP mesajı gönderilmeden önce tetiklenir.

```python
def pre_ocpp(self, action, payload):
    self.log("pre_ocpp çağrıldı")
    return action, payload
```

**Kullanım amaçları:**
- OCPP mesajı manipüle etmek
- Payload değiştirmek
- Sahte veri eklemek

### 🔹 4.2 post_ocpp()

CSMS tarafından dönen cevabı yakalar.

```python
def post_ocpp(self, action, payload, reply):
    self.log("post_ocpp çağrıldı")
    return reply
```

**Kullanım amaçları:**
- Cevap paketi değiştirmek
- Senaryo sonrası mantık eklemek

### 🔹 4.3 pre_can()

OCPP → CAN dönüşümünden sonra CAN frame gönderilmeden önce çağrılır.

```python
def pre_can(self, action, payload, frame):
    self.log("pre_can çağrıldı")
    return frame
```

**Kullanım amaçları:**
- CAN spoofing
- Manipülasyon
- Sahte sensör verisi basmak
- Arıza simülasyonu

### 🔹 4.4 post_can() (opsiyonel)

CAN frame gönderildikten sonra çağrılır.

```python
def post_can(self, action, payload, frame):
    self.log("post_can çağrıldı")
    return frame
```

## 📝 Log Yazımı

Her senaryo log yazabilir:

```python
self.log("senaryo mesajı")
```

Pipeline bu mesajları otomatik olarak şuraya kaydeder:

```
logs/run_xxx/scenario_log.jsonl
```

Her çalıştırma kendi `run_` klasörünü oluşturur.

## 🧪 5) Senaryoyu Test Etme

Senaryonuzu test etmek için artık OCPP client başlatmaya gerek yoktur. Sadece aşağıdaki iki terminal yeterlidir:

### Terminal 1 — OCPP Sunucusunu Başlatın

```bash
python -m infra.ocpp_server
```

### Terminal 2 — Senaryoyu Çalıştırın

```bash
python -m scenarios.scenario_xx_yeni_senaryo.simulate
```

**Başarılı çalıştırma sonrası oluşacak dosyalar:**
- OCPP logları
- CAN logları
- Senaryo logları
- Pipeline çalışma çıktıları

Tümü `logs/` dizini altında tutulur.

## 💾 6) Değişiklikleri Kaydetme

```bash
git add .
git commit -m "Senaryo xx eklendi"
git push origin feature/senaryo_xx
```

## 🔀 7) Pull Request Açma

**GitHub → Pull Requests → New Pull Request**

- **Base:** `dev`
- **Compare:** `feature/senaryo_xx`

PR oluşturduktan sonra:
- En az bir reviewer ekleyin
- Açıklayıcı bir açıklama yazın

## ✔ 8) Merge Süreci

Reviewer onayladıktan sonra:
- PR `dev` branch'ine merge edilir
- Feature branch kapatılır
- Senaryonuz artık resmi olarak projededir.
