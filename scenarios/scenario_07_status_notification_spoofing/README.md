🚨 Hayali İstasyon — StatusNotification Spoofing Anomali Senaryosu

“Sahte Durum” ile Operatör Sabotajı

Hazırlayan: Özgür Kerem Öncel
Ders: Bilgi Sistemleri ve Güvenliği
Dönem: 2025 Güz
Kapsam: OCPP Tabanlı Şarj Altyapılarında Operasyonel Anomali Tespiti

🎯 Amaç

Bu senaryonun temel amacı, bir şarj istasyonunun (Charge Point – CP) gerçek fiziksel durumunun, Merkezi Şarj Yönetim Sisteminden (CSMS) gizlenmesi yoluyla operatörün (CPO) bilinçli olarak yanıltılmasını simüle etmektir.

Bu saldırı senaryosu:

Finansal kazançtan ziyade

Operasyonel kaos oluşturmayı,

Müşteri memnuniyetini sabote etmeyi,

CPO’nun marka itibarına zarar vermeyi

hedeflemektedir.

🧩 Senaryo Özeti

Saldırgan, şarj istasyonu ile CSMS arasındaki iletişime Araya Girme (Man-in-the-Middle – MitM) saldırısı gerçekleştirir. Fiziksel olarak arızalanan bir istasyonun CSMS’ye gönderdiği “Faulted” durum mesajı yolda yakalanır ve “Available” olarak değiştirilir.

Bu manipülasyon sonucunda:

CSMS istasyonu çalışır zanneder

Mobil uygulamalar istasyonu kullanılabilir gösterir

Gerçekte arızalı olan istasyon sahte bir şekilde “aktif” görünür

🧠 Senaryo Akışı
Aşama	Durum	Açıklama
1	Normal	CP yalnızca gerçek durumunu CSMS’ye bildirir
2	Saldırı	MitM ile StatusNotification mesajı yakalanır
3	Manipülasyon	“Faulted” → “Available” olarak değiştirilir
4	Aldatma	CSMS ve kullanıcılar yanlış bilgilendirilir
5	Sonuç	Operasyonel körlük ve müşteri mağduriyeti
⚙️ Yöntemler ve Saldırı Vektörü

Saldırı Vektörü:

Man-in-the-Middle (MitM)

Mesaj Değiştirme (Message Tampering)

Hedef Protokol:

OCPP (Open Charge Point Protocol)

Hedef Mesaj:

StatusNotification

🔐 Gerekli Koşullar

Zayıf Ağ Güvenliği

Korumasız Wi-Fi

Güvensiz 4G modem

Fiziksel ağ erişimi

Zayıf Şifreleme

WS (şifresiz WebSocket)

Zayıf TLS/SSL yapılandırması

Karşılıklı sertifika doğrulamasının olmaması

Protokol Bilgisi

OCPP mesaj yapısı

CP kimliği (Charge Point ID)

🧨 Saldırı Adımları

MitM Konumlandırma
Saldırgan, ARP Spoofing veya DNS Zehirlenmesi ile CP–CSMS arasına yerleşir.

Gerçek Arıza Oluşumu
İstasyon fiziksel bir arıza yaşar (örn. güç elektroniği hatası).

Gerçek OCPP Mesajı

StatusNotification(
  connectorId=1,
  status="Faulted",
  errorCode="InternalError"
)


Mesaj Yakalama
Saldırgan mesajı ağ üzerinde yakalar.

Sahte Mesaj Enjeksiyonu

StatusNotification(
  connectorId=1,
  status="Available",
  errorCode="NoError"
)

🚧 Tehditler ve Sonuçlar

Operasyonel Körlük
CPO arızadan haberdar olmaz, teknik müdahale gecikir.

Müşteri Mağduriyeti
Sürücüler arızalı istasyonlara yönlendirilir.

İtibar Kaybı
Güven kaybı nedeniyle kullanıcılar rakip ağlara geçer.

Finansal Kayıp
Uzayan downtime nedeniyle gelir düşer.

🔍 Anomali Göstergeleri (Tespit Yöntemleri)

Kullanıcı Şikayetleri (En Güçlü Gösterge)
“Kullanılabilir” görünen istasyon için yoğun arıza bildirimleri.

Mantıksal Tutarsızlıklar

Uzun süre “Available” durumda kalan

Hiç StartTransaction veya MeterValues göndermeyen istasyonlar

Ağ İzleme Bulguları

IDS / Firewall loglarında

Sertifika uyarıları veya anormal trafik yönlendirmeleri

🛡️ Önerilen Önlemler

Güvenli İletişim (Zorunlu)

OCPP üzerinden WSS

En az TLS 1.2+

Karşılıklı Kimlik Doğrulama

Mutual Certificate Authentication

MitM saldırılarını pratikte engeller

CSMS Seviyesinde Mantıksal Anomali Tespiti

Örnek Kural:

“Bir istasyon 12 saatten uzun süredir Available durumunda ve bu sürede 0 işlem gerçekleştirmişse, otomatik inceleme uyarısı üret.”

📚 İlgili Standartlar

OCPP (1.6 / 2.0.x)

ISO 15118

ISO/IEC 27001

IEC 62443 (Endüstriyel Güvenlik)

🔍 SWOT Analizi
Güçlü Yönler

Gerçekçi MitM saldırı modeli

OCPP protokol seviyesinde tehdit analizi

Operasyonel etkisi yüksek senaryo

Zayıf Yönler

Fiziksel ağ erişimi varsayımı

Sertifika yönetimi karmaşıklığı

Fırsatlar

AI tabanlı mantıksal anomali tespiti

CSMS davranışsal analiz geliştirme

Tehditler

Gelişmiş MitM teknikleri

Tedarik zinciri kaynaklı güvenlik açıkları

📌 Not:
Bu senaryo, elektrikli araç şarj altyapılarında görünmeyen ama yüksek etkili operasyonel saldırıların anlaşılması ve tespit edilmesi amacıyla hazırlanmıştır.