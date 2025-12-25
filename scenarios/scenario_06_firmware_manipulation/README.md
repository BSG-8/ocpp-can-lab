# 🔐 Firmware ve Yazılım Açıkları — Anomali Senaryosu

**Hazırlayan:** Sena Köse  
**Ders:** Bilgi Sistemleri ve Güvenliği (2025 Güz)  
**Kurum:** Fırat Üniversitesi

---

## 🎯 Amaç

İmzalanmamış, değiştirilmiş veya sürümü düşürülmüş firmware dosyalarının yapay zekâ destekli sistem tarafından tespit edilip otomatik olarak engellenmesini simüle etmek.

---

## 🧩 Senaryo Akışı

| Aşama | Durum | Açıklama |
|-------|-------|----------|
| 1 | Normal | Şarj istasyonu yalnızca doğrulanmış firmware kabul eder |
| 2 | Saldırı | İmzasız/eski firmware enjekte edilir |
| 3 | Tespit | AI sistemi anomaliyi algılar |
| 4 | Tepki | Güncelleme durdurulur, karantina uygulanır |

---

## ⚙️ Saldırı Parametreleri

```python
{
    "signature_valid": False,   # İmza geçersiz
    "hash_match": False,        # Hash eşleşmiyor
    "downgrade": True,          # Sürüm düşürme
    "version": "1.0.0"          # Eski sürüm
}
```

---

## 📏 Başarı Kriterleri

- ✅ Tespit doğruluğu: **≥ %95**
- ✅ Tespit süresi: **< 30 saniye**
- ✅ Yanlış pozitif oranı: **≤ %5**

---

## ▶️ Çalıştırma

```bash
# Terminal 1 - Sunucu
python -m infra.ocpp_server

# Terminal 2 - Senaryo
python -m scenarios.scenario_06_firmware_manipulation.simulate
```

---

## 🔗 İlgili Standartlar

- ISO 15118
- OCPP 2.0
- ISO 27001

---

## 📊 Hook Fonksiyonları

| Hook | İşlev |
|------|-------|
| `pre_ocpp()` | Firmware URL'sini manipüle eder |
| `post_ocpp()` | AI tespit sonucunu değerlendirir |
| `pre_can()` | CAN-Bus güvenlik uyarısı gönderir |
| `post_can()` | Sonuç raporu oluşturur |

---

## 🔍 SWOT Analizi

### Güçlü Yönler
- Yapay zekâ tabanlı anomali tespit sistemi
- Dijital imzalı firmware yapısı
- Merkezi güncelleme kontrolü

### Zayıf Yönler
- Sertifika yaşam döngüsü karmaşıklığı
- Yanlış pozitif tespit olasılığı

### Fırsatlar
- ISO 15118, OCPP 2.0 uyumluluğu
- Yapay zekâ ile sürekli iyileştirme

### Tehditler
- Zero-day güvenlik açıkları
- Tedarik zinciri saldırıları
- Firmware reverse engineering
