import json
import re

class CatalogNormalizer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.raw_data = []
        self.normalized_data = []

    def load_data(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Eğer veri doğrudan bir listeyse sorun yok
            if isinstance(data, list):
                self.raw_data = data
            # Eğer veri bir sözlükse (dict), içindeki listeyi bulalım (ör: data["products"])
            elif isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        self.raw_data = value
                        break
                # Eğer içinde liste bulamazsa, verinin kendisini tek elemanlı bir liste yapar
                if not self.raw_data:
                    self.raw_data = [data]

    def _clean_price(self, price_val):
        if price_val is None or str(price_val).strip() == "":
            return None
        match = re.search(r'[\d\,\.]+', str(price_val))
        if match:
            clean_str = match.group().replace(',', '.')
            try:
                return float(clean_str)
            except ValueError:
                return None
        return None

    def _clean_stock(self, stock_val):
        if not stock_val:
            return "out_of_stock"
        val = str(stock_val).lower().strip()
        if "in" in val and "stock" in val: return "in_stock"
        if val in ["var", "stokta", "yes", "true", "1"]: return "in_stock"
        return "out_of_stock"

    def normalize(self):
        self.load_data()
        for item in self.raw_data:
            # item string ise veya dictionary değilse atla (hataları önlemek için)
            if not isinstance(item, dict):
                continue
                
            base_price = self._clean_price(item.get("price"))
            max_price = self._clean_price(item.get("price_max"))
            
            normalized_item = {
                "id": item.get("id", "UNKNOWN"),
                "name": item.get("name", "İsimsiz Ürün"),
                "url": item.get("url", ""),
                "price": base_price,
                "price_max": max_price,
                "currency": str(item.get("currency", "USD")).upper().strip(),
                "stock_status": self._clean_stock(item.get("stock_status")),
                "category": str(item.get("category")).strip() if item.get("category") else "Uncategorized",
                "rating": float(item.get("rating")) if item.get("rating") else 0.0,
                "review_count": int(item.get("review_count")) if item.get("review_count") else 0
            }
            self.normalized_data.append(normalized_item)
        return self.normalized_data