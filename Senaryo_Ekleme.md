
# 📘 Senaryo Geliştirme Kılavuzu

Bu döküman, projeye **yeni bir saldırı / arıza senaryosunun nasıl ekleneceğini** adım adım açıklar.  
Her öğrenci, yeni bir senaryo eklerken bu kılavuza uymalıdır.

---

## 🔱 1) Yeni Branch Oluşturma

Her senaryo, kendi feature branch'i üzerinden geliştirilir:

```bash
git checkout dev
git pull
git checkout -b feature/senaryo_xx
```

`senaryo_xx` → senaryonuzun numarasıdır.  
Örn: `feature/senaryo_03_meter_spoofing`

---

## 📁 2) Senaryo Klasörünün Oluşturulması

Senaryolar `scenarios/` klasöründe bulunur.

Yeni bir senaryo eklemek için:

```bash
cd scenarios/
cp -r _template scenario_xx_yeni_senaryo
```

Bu klasörde iki dosya bulunur:

- `simulate.py` → Senaryonun başlatıldığı dosya
- `hooks.py` → OCPP ve CAN manipülasyonlarının yazıldığı yer

Bu iki dosyayı kendi senaryonuza göre düzenleyin.

---

## 🧩 3) Senaryoyu Aktifleştirme

Her senaryonun kendi `simulate.py` dosyasında:

```python
pipeline.set_active_scenario("scenario_xx_yeni_senaryo")
```

Senaryonuzun klasör adını burada kullanın.

---

## ⚙️ 4) Kod Geliştirme

Senaryoların ana mantığı `hooks.py` dosyasında yazılır.

Üç temel fonksiyon şunlardır:

### 🔹 4.1 pre_ocpp()

OCPP mesajı gönderilmeden hemen önce çalışır.

```python
def pre_ocpp(self, action, payload):
    self.log("pre_ocpp çağrıldı")
    return action, payload
```

### 🔹 4.2 post_ocpp()

OCPP cevabı alındıktan sonra çalışır.

```python
def post_ocpp(self, action, payload, reply):
    self.log("post_ocpp çağrıldı")
    return reply
```

### 🔹 4.3 pre_can()

OCPP → CAN dönüşümünden sonra CAN frame'i manipüle etmek için kullanılır.

```python
def pre_can(self, action, payload, frame):
    self.log("pre_can çağrıldı")
    return frame
```

---

## 📝 Log Yazımı

Log eklemek için her sınıfta:

```python
self.log("senaryo mesajı")
```

Bu mesaj otomatik olarak:

```
logs/run_xxx/scenario_log.jsonl
```

dosyasına yazılır.

---

## 🧪 5) Senaryoyu Test Etme

Önce OCPP server'ı başlatın:

```bash
python -m infra.ocpp_server
```

Ayrı bir terminalde senaryonuzu çalıştırın:

```bash
python -m scenarios.scenario_xx_yeni_senaryo.simulate
```

Eğer hata yoksa:

- OCPP logları
- CAN logları
- Senaryo logları

otomatik oluşturulur.

---

## 💾 6) Değişiklikleri Kaydetme

```bash
git add .
git commit -m "Senaryo xx eklendi"
git push origin feature/senaryo_xx
```

---

## 🔀 7) Pull Request Açma

GitHub → Pull Requests → New Pull Request

- Base: `dev`
- Compare: `feature/senaryo_xx`

Ardından:

- En az 1 reviewer ekleyin
- PR onaylanınca merge edilir

---

## ✔️ 8) Merge

Reviewer tarafından onaylandıktan sonra:

- PR `dev` branch'ine merge edilir
- Branch kapatılır
