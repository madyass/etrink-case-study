# 🤖 Etrink AI Recommendation Agent

Bu proje, bir ürün kataloğu üzerinde doğal dil işleme (NLP) ve yapay zeka (LLM) kullanarak, kullanıcıların karmaşık isteklerine (bütçe, kategori, stok durumu vb.) uygun ürün önerileri sunan otonom bir ajandır. 

## ✨ Özellikler

- **Akıllı Veri Yönetimi:** Öncelikle canlı veri kaynağından (API vb.) veriyi çekmeyi dener. Eğer ağ hatası veya erişim sorunu yaşanırsa, otomatik olarak lokaldeki (`data/`) yedek JSON dosyasına geçer.
- **Katalog Normalizasyonu:** Farklı formatlarda gelebilecek ham veriyi temizler, ayrıştırır ve yapay zekanın anlayabileceği standart bir formata (`CatalogNormalizer`) dönüştürür.
- **LLM Tabanlı Öneri Motoru:** Sadece anahtar kelime eşleştirmesi yapmaz; kullanıcının niyetini anlar (örn: "Türk kahvesi seven birine hediye", "300 dolar bütçe") ve buna uygun mantıksal sonuçlar üretir.
- **Çoklu Çıktı Desteği:** Üretilen senaryo sonuçlarını analiz ve entegrasyon kolaylığı için hem **CSV** hem de **JSON** formatında `outputs/` klasörüne kaydeder.
- **Detaylı Loglama:** Süreç boyunca gerçekleşen başarılı/başarısız tüm adımları konsola ve log dosyalarına yazar.

## 📂 Proje Yapısı

\`\`\`text
etrink-case-study/
│
├── data/
│   └── alfiq_catalog_snapshot.json  # Canlı veriye ulaşılamadığında kullanılan lokal yedek
│
├── outputs/                         # Uygulama çalıştığında otomatik oluşturulan çıktılar
│   ├── results.csv                  # Sonuçların tablo formatı
│   └── results.json                 # Sonuçların JSON formatı
│
├── src/                             # Uygulamanın kaynak kodları
│   ├── agent.py                     # Llama 3.2 modelini yöneten RecommendationAgent sınıfı
│   ├── exporter.py                  # CSV vb. dışa aktarma (export) fonksiyonları
│   ├── fetcher.py                   # Veri çekme işlemleri (fetch_live_data, load_local_data)
│   ├── normalizer.py                # Veri temizleme ve standardize etme (CatalogNormalizer)
│   ├── utils.py                     # Log konfigürasyonları ve yardımcı fonksiyonlar
│   └── main.py                      # Projenin ana akışını yöneten çalıştırılabilir dosya
│
└── README.md
\`\`\`

## 🚀 Kurulum ve Çalıştırma

### Gereksinimler

Projenin çalışması için bilgisayarınızda Python 3.8+ sürümünün kurulu olması gerekmektedir. Ayrıca AI modelinin yerel (local) çalışabilmesi için Llama 3.2'nin erişilebilir olduğundan (örneğin Ollama üzerinden) emin olun.

1. **Depoyu Klonlayın:**
   \`\`\`bash
   git clone https://github.com/madyass/etrink-case-study.git
   cd etrink-case-study
   \`\`\`

2. **Gerekli Kütüphaneleri Yükleyin:**
   Eğer bir `requirements.txt` dosyanız varsa:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **Projeyi Çalıştırın:**
   \`\`\`bash
   python src/main.py
   \`\`\`

## 🧪 Örnek Senaryolar

Sistem varsayılan olarak `main.py` içerisinde şu senaryoları test eder:

1. *"100 dolar altında, iyi puanlı, hediyelik bir ürün öner"*
2. *"Bir spa işletmesi için 300 dolar bütçeyle 2 ürün öner"*
3. *"Türk kahvesi seven birine hediye arıyorum, stokta olsun"*

Kendi sorgularınızı test etmek isterseniz, `src/main.py` dosyasındaki `test_queries` listesini düzenleyebilirsiniz.

## 📝 Loglar ve Çıktılar

Uygulama tamamlandıktan sonra çıktılarınıza `outputs/` klasörü altından ulaşabilirsiniz:
- Yapay zeka kararlarını makine formatında incelemek için: `outputs/results.json`
- Excel üzerinden okumak için: `outputs/results.csv`

Çalışma anında oluşan hatalar (API bağlantı kopması, model yanıt vermemesi vb.) terminalinizde ve loglarda uyarı/hata olarak gösterilecektir.