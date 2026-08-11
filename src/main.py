import os
import json
from normalizer import CatalogNormalizer
from agent import RecommendationAgent

def main():
    # 1. Veri Yükleme ve Normalizasyon
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'alfiq_catalog_snapshot.json')
    
    print("1. Katalog yükleniyor ve normalize ediliyor...")
    normalizer = CatalogNormalizer(data_path)
    clean_catalog = normalizer.normalize()
    
    print(f"Toplam {len(clean_catalog)} ürün işlendi.")
    
    # Normalizasyon Testi: İlk 2 ürünü ekrana basalım (Hata var mı diye görmek için)
    print("\n--- NORMALİZASYON TESTİ (İlk 2 Ürün) ---")
    print(json.dumps(clean_catalog[:2], indent=2, ensure_ascii=False))
    print("----------------------------------------\n")

    # 2. Ajanı Başlatma (Ollama)
    print("2. Ajan başlatılıyor (Lokal Ollama). Lütfen arkaplanda çalıştığından emin olun...")
    agent = RecommendationAgent(model_name="llama3.2") # İndirdiğiniz modele göre ismi değiştirebilirsiniz

    # 3. Test Sorguları
    test_queries = [
        "100 dolar altında, iyi puanlı, hediyelik bir ürün öner",
        "Bir spa işletmesi için 300 dolar bütçeyle 2 ürün öner",
        "Türk kahvesi seven birine hediye arıyorum, stokta olsun"
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"{'='*50}\nSenaryo {i}: '{query}'\n{'='*50}")
        try:
            result = agent.get_recommendations(query, clean_catalog)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"HATA: {e}")
        print("\n")

if __name__ == "__main__":
    main()