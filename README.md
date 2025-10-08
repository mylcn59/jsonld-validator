🧠 JSON-LD Schema Validator for icgiyimozel.com

🚀 Otomatik Structured Data (Schema.org) doğrulama sistemi
Her push veya PR’da, sayfalardaki JSON-LD etiketlerini tarar,
Google ve Merchant Center uyumluluğunu test eder,
hataları yakalar ve schema_check.log olarak raporlar.

💡 Neden Bu Sistem Var?

icgiyimozel.com, yüzlerce ürün ve binlerce varyanta sahip büyük bir iç giyim e-ticaret platformu.
Her ürün, kategori ve marka sayfasında Schema.org JSON-LD etiketleri (Product, ItemList, Brand, Organization) bulunuyor.

Bu sistem sayesinde:

🕵️‍♀️ Google Rich Snippet’lar sürekli olarak kontrol altında tutulur

🛍️ Merchant Center feed’leri bozulmadan çalışır

⚙️ Yeni ürün / kategori / varyant eklemelerinde yapılandırılmış veriler otomatik doğrulanır

💥 “Bozuk JSON-LD” veya “geçersiz @id” gibi hatalar build aşamasında fark edilir

Kısacası:

🔒 SEO tarafı artık insan hatasına değil, otomatik test sistemine emanet.

🧩 Kurulum
1️⃣ Gerekli dosyalar
Dosya	Açıklama
tests/schema_check.py	JSON-LD doğrulama betiği
tests/urls.txt	Test edilecek sayfa URL listesi
tests/requirements.txt	Python bağımlılıkları
.github/workflows/schema-check.yml	GitHub Actions workflow
2️⃣ Kurulum Komutları (Yerelde çalıştırmak istersen)
pip install -r tests/requirements.txt
python tests/schema_check.py


Veya doğrudan GitHub Actions çalıştır:

✅ Her push veya PR’da otomatik olarak devreye girer.

⚙️ Workflow Özeti
on:
  push:
  pull_request:
jobs:
  schema_check:
    runs-on: ubuntu-latest
    steps:
      - checkout
      - install python
      - pip install -r tests/requirements.txt
      - run tests/schema_check.py
      - upload log


Her çalıştırmada tests/urls.txt dosyasındaki her URL tek tek kontrol edilir.
Sonuçlar:

Başarılı: ✅ [OK] mesajı

Bozuk veya eksik JSON-LD: ❌ [ERROR] mesajı

schema_check.log dosyasında detaylı hata raporu

🧾 Çıktı Örneği
Schema check started: Wed Oct  8 07:25:40 UTC 2025
URLs file: tests/urls.txt

[OK] 2 JSON-LD blocks found on https://www.icgiyimozel.com/push-up-sutyen-494-urunleri
[OK] 1 JSON-LD block found on https://www.icgiyimozel.com/bella-notte-lacivert-asimetrik-kesim-firfirli-gecelik-15620-102709
[ERROR] Missing @id on https://www.icgiyimozel.com/marka/anil
✅ Completed. 12 URLs checked, 1 error.

🧰 Kullanım İpuçları

🔁 urls.txt dosyasına yeni sayfa türleri ekleyebilirsin:

https://www.icgiyimozel.com/push-up-sutyen-494-urunleri
https://www.icgiyimozel.com/erotik-kadin-ic-giyim-41-modelleri
https://www.icgiyimozel.com/marka/bella-notte


📦 Her başarılı build sonunda schema-validation-log adlı bir artifact yüklenir:
→ GitHub Actions → Artifacts → schema-validation-log

🧹 Eski hataları temizlemek için:

rm schema_check.log

🧬 Teknik Detaylar
Kütüphane	İşlev
extruct	HTML’den JSON-LD çıkarmak
lxml==4.9.3	DOM parse işlemleri (sabit sürüm – uyum garantili)
requests	Sayfa HTML içeriğini almak
jsonschema	Yapı doğrulama
tqdm	CLI ilerleme çubuğu

⚙️ extruct + lxml==4.9.3 sabitlemesi, GitHub Actions ortamında _ElementStringResult hatasını ortadan kaldırır.
Yeni lxml 5.x sürümleriyle extruct uyumlu değildir.

🌈 Başarılı Entegrasyon Sonrası Ne Kazanıyoruz?
Alan	Kazanç
🧭 SEO / Arama Sonuçları	Ürün kartlarında fiyat, stok ve puan direkt görünür
🛍️ Google Merchant Center	Feed doğrulama hataları minimuma iner
🧠 AI / SERP Bağlamı	Google Knowledge Graph için temiz @id ilişkileri
💬 Rich Results	Yıldızlı değerlendirme snippet’ları aktif hale gelir
🔔 Erken Uyarı	Her commit sonrası yapılandırılmış veri hatası anında tespit edilir
✨ Örnek Kullanım – icgiyimozel.com

👗 “Her ürün, Google için doğru tanımlanmış bir hikâyedir.”
— icgiyimozel.com SEO AI Validator

❤️ Katkıda Bulunmak

Yeni test tipleri (ör. BreadcrumbList, Review, FAQPage) eklemek istiyorsan:

schema_check.py içinde validate_jsonld() fonksiyonunu genişlet

PR aç 🎯

Otomatik testler çalışsın

🏁 Lisans

BK Bilgi Teknolojileri ve Ticaret A.Ş. — 2025
Tüm hakları saklıdır.
icgiyimozel.com özel yapısıdır, yalnızca partner markalarla paylaşılabilir.
