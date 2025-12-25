# Senaryo 02: Hedefli CV Manipülasyonu ile Çevrimdışı Mod Zorlama

**Off-Grid Mode Enforcement via Targeted CV Manipulation**

## 📋 Senaryonun Amacı ve Kapsamı

### Amaç
Şarj İstasyonunun (CP) Merkezi Yönetim Sistemi (CSMS) ile iletişimini kasıtlı ve kalıcı olarak keserek, CP'yi yerel yetkilendirme moduna zorlamak ve bu sayede yetkisiz (ücretsiz) şarj erişimi sağlamaktır.

**Test Case'ler:** TC-5, TC-7

### Kapsam
Senaryo, öncelikle OCPP Konfigürasyon Değişkenlerinin (CV) manipülasyonu yoluyla siber katmanda Hizmet Engelleme (Denial of Service) yaratarak, CP'nin yerel yetkilendirme (fiziksel) fonksiyonunu istismar etmeyi hedefler.

## 🎯 Saldırı Adımları

### 1. CV Manipülasyonu
- **OfflineTxForUnknownIdEnabled** CV'si `TRUE` yapılır
- Bu sayede CP, bilinmeyen kimliklerle çevrimdışı şarj işlemlerine izin verir

### 2. İletişim Zayıflatma
- **HeartbeatInterval** CV'si artırılır (örn: 3600 saniye)
- Heartbeat mesajları bazen engellenir (%30 ihtimalle)
- CSMS ile iletişim kopukluğu simüle edilir

### 3. Çevrimdışı Moda Zorlama
- CP, CSMS ile iletişim kuramadığı için çevrimdışı moda geçer
- Yerel yetkilendirme modu aktif hale gelir

### 4. Yetkisiz Şarj
- CAN-Bus üzerinden yetkilendirme sinyalleri manipüle edilir
- Yetkisiz kullanıcılar ücretsiz şarj yapabilir

## 🔧 Teknik Detaylar

### Manipüle Edilen OCPP Mesajları

#### ChangeConfiguration
```json
{
  "key": "OfflineTxForUnknownIdEnabled",
  "value": "true"
}
```

#### HeartbeatInterval Manipülasyonu
```json
{
  "key": "HeartbeatInterval",
  "value": "3600"
}
```

### Hook Fonksiyonları

| Hook | Açıklama |
|------|----------|
| `pre_ocpp()` | OCPP mesajlarını gönderilmeden önce manipüle eder |
| `post_ocpp()` | CSMS'den gelen cevapları manipüle eder |
| `pre_can()` | CAN frame'lerini manipüle eder (yetkilendirme sinyalleri) |
| `post_can()` | Gönderilen CAN frame'lerini loglar |

## 🚀 Çalıştırma

```bash
python -m scenarios.scenario_02_cv_manipulation_offline.simulate
```

## 📊 Beklenen Çıktı

1. ✅ CP normal şekilde CSMS'e bağlanır
2. ⚠️ OfflineTxForUnknownIdEnabled CV'si TRUE yapılır
3. ⚠️ HeartbeatInterval manipüle edilir
4. ⚠️ Heartbeat mesajları engellenir
5. ⚠️ CP çevrimdışı moda zorlanır
6. ⚠️ Yetkisiz şarj işlemi başlatılır

## 🛡️ Savunma Önerileri

### 1. CV Değer Doğrulama
- CSMS, CV değişikliklerini doğrulamalı
- Kritik CV'lerin (OfflineTxForUnknownIdEnabled) değiştirilmesini engellemeli veya sıkı kontrol etmeli

### 2. İletişim İzleme
- Heartbeat mesajlarının düzenliliğini izlemeli
- Anormal iletişim kopukluklarını alarm olarak bildirmeli

### 3. Güvenlik Politikası
- `OfflineTxForUnknownIdEnabled` CV'sinin varsayılan olarak `FALSE` olmasını sağlamalı
- Çevrimdışı yetkilendirmeyi yalnızca önceden bilinen ve yerel beyaz listede olan kimliklerle sınırlandırmalı

### 4. Giriş Kontrolü
- CP'ye uzaktan erişim sağlayan kullanıcıların güçlü kimlik doğrulama mekanizmaları kullanmasını zorunlu kılmalı
- Yönetim erişimini sıkı bir şekilde loglamalı

### 5. Anomali Takibi
- CSMS'te, bir CP'nin iletişim değişkenlerinin varsayılan değerlerden sapması durumunda anında yüksek öncelikli alarm üreten bir kural tanımlamalı

## 📝 Log Dosyası

Senaryo çalıştırıldığında log dosyası şu konumda oluşturulur:
```
logs/scenario_02_cv_manipulation_offline.log
```

## ⚠️ Uyarı

Bu senaryo yalnızca güvenlik testi ve araştırma amaçlıdır. Gerçek sistemlerde yetkisiz kullanımı yasaktır.

