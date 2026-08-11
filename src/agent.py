import json
import datetime
import urllib.request
import urllib.error
import logging
from utils import retry

logger = logging.getLogger(__name__)

class RecommendationAgent:
    def __init__(self, model_name="llama3.2"):
        self.model_name = model_name
        self.api_url = "http://localhost:11434/api/generate"

    @retry(max_attempts=3, delay=1, exceptions=(Exception,))
    def get_recommendations(self, query: str, catalog_data: list):
        logger.info(f"LLM sorgusu başlatılıyor: '{query}'")
        
        available_catalog = [
            item for item in catalog_data 
            if item['stock_status'] == 'in_stock' and item['price'] is not None
        ]

        prompt = f"""Sen bir JSON üreten alışveriş asistanısın. Aşağıdaki kataloğa bakarak kullanıcının isteğine uygun ürünleri seç ve SADECE JSON formatında cevap ver.
Kullanıcı İsteği: "{query}"
Katalog:
{json.dumps(available_catalog, ensure_ascii=False)}
Çıktı Şablonu:
{{
  "kullanici_talebi": "{query}",
  "onerilen_urunler": [
    {{"id": "...", "ad": "...", "fiyat": 0.0, "url": "...", "secim_gerekcesi": "..."}}
  ]
}}
"""
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "format": "json",
            "stream": False,
            "options": {"temperature": 0.1}
        }

        req = urllib.request.Request(
            self.api_url, 
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )

        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            
        response_text = result.get("response", "{}")
        
        try:
            result_json = json.loads(response_text)
            result_json["calisma_zamani"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            logger.info("LLM başarılı bir JSON yanıtı üretti.")
            return result_json
        except json.JSONDecodeError:
            logger.error(f"Geçersiz JSON formatı alındı. Yanıt: {response_text}")
            raise ValueError("LLM geçerli bir JSON üretemedi.")