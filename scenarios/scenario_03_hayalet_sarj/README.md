# 👻 Scenario 03: Hayalet Şarj (Ghost Charge Attack)

## Açıklama
Bu senaryo, EV şarj istasyonlarına yönelik bir "Hayalet Şarj" saldırısını simüle eder.

Saldırgan, şarj noktasının CSMS'e gönderdiği `MeterValues` mesajlarını manipüle ederek gerçek enerji tüketiminden çok daha düşük değerler raporlar. Sonuç olarak CSMS düşük fatura keser ve saldırgan ücretsiz/ucuz şarj yapmış olur.

## Saldırı Mekanizması

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   METER     │      │     CP      │      │    CSMS     │
│  (Gerçek)   │      │  (Manipüle) │      │  (Sahte)    │
└─────────────┘      └─────────────┘      └─────────────┘
       │                    │                    │
       │  1234 Wh           │                    │
       │───────────────────>│                    │
       │                    │  10 Wh (SAHTE!)    │
       │                    │───────────────────>│
       │                    │                    │
       │                    │     Fatura: 10 Wh  │
       │                    │<───────────────────│
       │                    │                    │
```

## Çalıştırma

```bash
# Terminal 1 - CSMS Sunucusu
python -m infra.ocpp_server

# Terminal 2 - Senaryo
python -m scenarios.scenario_03_hayalet_sarj.simulate
```

## Beklenen Çıktı

- `[GHOST ATTACK]` log mesajları
- MeterValues'da manipüle edilmiş düşük değerler
- CSMS'in sahte değerleri kabul etmesi

## Hook Fonksiyonları

| Hook | Açıklama |
|------|----------|
| `pre_ocpp()` | MeterValues mesajlarındaki `energyWh` değerini sahte değerle değiştirir |
| `post_ocpp()` | CSMS cevabını loglar |
| `pre_can()` | CAN frame'i değiştirmeden geçirir |
| `post_can()` | CAN frame gönderimini loglar |

## Dosya Yapısı

```
scenario_03_hayalet_sarj/
├── hooks.py      # Saldırı mantığı (GhostChargeScenario)
├── simulate.py   # Giriş noktası
└── README.md     # Bu dosya
```
