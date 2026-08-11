import json
import datetime
import urllib.request
import urllib.error

class RecommendationAgent:
    def __init__(self, model_name="llama3.2"):
        self.model_name = model_name
        self.api_url = "http://localhost:11434/api/generate"

    def get_recommendations(self, query: str, catalog_data: list):
        available_catalog = [
            item for item in catalog_data 
            if item['stock_status'] == 'in_stock' and item['price'] is not None
        ]

        # Llama modeli için özel formatlanmış prompt
        prompt = f"""Sen bir JSON üreten alışveriş asistanısın. Aşağıdaki kataloğa bakarak kullanıcının isteğine uygun ürünleri seç ve SADECE JSON formatında cevap ver. Başka hiçbir açıklama yazma.

Kullanıcı İsteği: "{query}"

Katalog (Sadece stoktakiler):
{json.dumps(available_catalog, ensure_ascii=False)}

Çıktı Şablonu:
{{
  "kullanici_talebi": "{query}",
  "onerilen_urunler": [
    {{
      "id": "...",
      "ad": "...",
      "fiyat": 0.0,
      "url": "...",
      "secim_gerekcesi": "..."
    }}
  ]
}}
"""
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "format": "json", # Ollama'nın JSON formatında yanıt vermeye zorlanması
            "stream": False,
            "options": {
                "temperature": 0.1
            }
        }

        req = urllib.request.Request(
            self.api_url, 
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )

        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                
            response_text = result.get("response", "{}")
            result_json = json.loads(response_text)
            
            # Zaman damgasını Python eklesin
            result_json["calisma_zamani"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            return result_json
            
        except urllib.error.URLError:
            raise Exception("Ollama sunucusuna ulaşılamadı. Lütfen terminalde 'ollama serve' veya 'ollama run llama3.2' çalıştığından emin olun.")
        except json.JSONDecodeError:
            raise Exception(f"Model JSON formatını bozdu. Gelen yanıt: {response_text}")