import re
import logging

logger = logging.getLogger(__name__)

class CatalogNormalizer:
    def __init__(self):
        self.raw_data = []
        self.normalized_data = []

    def set_data(self, data):
        # Shopify products.json formatı mı yoksa test veri setimiz mi algıla
        if isinstance(data, dict) and "products" in data:
            logger.info("Şema Algılandı: Shopify Live Endpoint")
            self.raw_data = data["products"]
            self.is_shopify = True
        else:
            logger.info("Şema Algılandı: Test Veri Seti (alfiq_catalog_snapshot)")
            self.is_shopify = False
            
            # Sözlük / Liste karışıklığı çözümü
            if isinstance(data, list):
                self.raw_data = data
            elif isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        self.raw_data = value
                        break

    def _clean_price(self, price_val):
        if not price_val: return None
        match = re.search(r'[\d\,\.]+', str(price_val))
        if match:
            try: return float(match.group().replace(',', '.'))
            except: return None
        return None

    def normalize(self):
        logger.info("Normalizasyon işlemi başlatıldı.")
        for item in self.raw_data:
            if not isinstance(item, dict): continue
            
            if self.is_shopify:
                # Shopify Canlı Veri Haritalaması
                variants = item.get("variants", [{}])
                base_price = self._clean_price(variants[0].get("price"))
                
                norm_item = {
                    "id": str(item.get("id")),
                    "name": item.get("title", "İsimsiz Ürün"),
                    "url": "https://alfiqcopper.com/products/" + item.get("handle", ""),
                    "price": base_price,
                    "currency": "USD",
                    "stock_status": "in_stock" if variants[0].get("available", True) else "out_of_stock",
                    "category": item.get("product_type", "Uncategorized"),
                    "rating": 5.0, # Canlı veride puan yoksa varsayılan
                    "review_count": 0
                }
            else:
                # Orijinal Test Verisi Haritalaması (önceki kod)
                norm_item = {
                    "id": str(item.get("id", "UNKNOWN")).strip(),
                    "name": str(item.get("name", "İsimsiz Ürün")).strip(),
                    "url": str(item.get("url", "")).strip(),
                    "price": self._clean_price(item.get("price")),
                    "currency": str(item.get("currency", "USD")).upper().strip(),
                    "stock_status": "in_stock" if "in" in str(item.get("stock_status")).lower() or str(item.get("stock_status")).lower() in ["var", "stokta"] else "out_of_stock",
                    "category": str(item.get("category")).strip() if item.get("category") else "Uncategorized",
                    "rating": self._clean_price(item.get("rating")) or 0.0,
                }
            self.normalized_data.append(norm_item)
            
        logger.info(f"Normalizasyon tamamlandı. İşlenen ürün: {len(self.normalized_data)}")
        return self.normalized_data