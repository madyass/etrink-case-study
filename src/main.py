import os
import json
import logging
from utils import setup_logging
from fetcher import fetch_live_data, load_local_data
from normalizer import CatalogNormalizer
from agent import RecommendationAgent
from exporter import export_to_csv

def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("=== Alfiq AI Agent Başlatıldı ===")

    # 1. Veri Kaynağını Belirle (Önce Canlı, Bozulursa Lokal)
    raw_data = None
    try:
        raw_data = fetch_live_data()
    except Exception as e:
        logger.warning(f"Canlı veriye erişilemedi: {e}")
        local_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'alfiq_catalog_snapshot.json')
        raw_data = load_local_data(local_path)

    # 2. Normalizasyon
    normalizer = CatalogNormalizer()
    normalizer.set_data(raw_data)
    clean_catalog = normalizer.normalize()

    # 3. Ajan ve Senaryolar
    agent = RecommendationAgent(model_name="llama3.2")
    test_queries = [
        "100 dolar altında, iyi puanlı, hediyelik bir ürün öner",
        "Bir spa işletmesi için 300 dolar bütçeyle 2 ürün öner",
        "Türk kahvesi seven birine hediye arıyorum, stokta olsun"
    ]

    all_results = []
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*50}\nSenaryo {i}: '{query}'\n{'='*50}")
        try:
            result = agent.get_recommendations(query, clean_catalog)
            all_results.append(result)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        except Exception as e:
            logger.error(f"Senaryo {i} işlenirken kritik hata: {e}")

    # 4. CSV Çıktısı (Bonus)
    if all_results:
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
        export_to_csv(all_results, output_dir)
        
    logger.info("=== İşlem Tamamlandı ===")

if __name__ == "__main__":
    main()