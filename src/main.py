import os
import json
from dotenv import load_dotenv
from normalizer import CatalogNormalizer
from agent import RecommendationAgent

# .env dosyasından OPENAI_API_KEY okumak için
load_dotenv()

def main():
    # 1. Veri Yükleme ve Normalizasyon
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'alfiq_catalog_snapshot-etrink.json')
    
    print("Katalog yükleniyor ve normalize ediliyor...")
    normalizer = CatalogNormalizer(data_path)
    clean_catalog = normalizer.normalize()
    print(f"Toplam {len(clean_catalog)} ürün işlendi.\n")

    # 2. Ajanı Başlatma
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("HATA: OPENAI_API_KEY bulunamadı. Lütfen çevre değişkeni olarak ayarlayın.")
        return
        
    agent = RecommendationAgent(api_key=api_key)

    # 3. Test Sorguları
    test_queries = [
        "100 dolar altında, iyi puanlı, hediyelik bir ürün öner",
        "Bir spa işletmesi için 300 dolar bütçeyle 2 ürün öner",
        "Türk kahvesi seven birine hediye arıyorum, stokta olsun"
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"{'-'*50}\nSenaryo {i}: '{query}'\n{'-'*50}")
        try:
            result = agent.get_recommendations(query, clean_catalog)
            # JSON formatında güzelce yazdır
            print(json.dumps(result, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"Sorgu işlenirken hata oluştu: {e}")
        print("\n")

if __name__ == "__main__":
    main()