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
            
            if isinstance(data, list):
                self.raw_data = data
            elif isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        self.raw_data = value
                        break
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

    def _clean_rating(self, rating_val):
        if not rating_val:
            return 0.0
        try:
            # Virgülü noktaya çevir ("5,0" -> "5.0")
            clean_str = str(rating_val).replace(',', '.').strip()
            return float(clean_str)
        except ValueError:
            return 0.0

    def _clean_review_count(self, review_val):
        if not review_val:
            return 0
        try:
            # Metin içindeki harfleri temizle, sadece rakamları al
            clean_str = re.sub(r'\D', '', str(review_val))
            return int(clean_str) if clean_str else 0
        except ValueError:
            return 0

    def normalize(self):
        self.load_data()
        for item in self.raw_data:
            if not isinstance(item, dict):
                continue
                
            base_price = self._clean_price(item.get("price"))
            max_price = self._clean_price(item.get("price_max"))
            
            normalized_item = {
                "id": str(item.get("id", "UNKNOWN")).strip(),
                "name": str(item.get("name", "İsimsiz Ürün")).strip(),
                "url": str(item.get("url", "")).strip(),
                "price": base_price,
                "price_max": max_price,
                "currency": str(item.get("currency", "USD")).upper().strip(),
                "stock_status": self._clean_stock(item.get("stock_status")),
                "category": str(item.get("category")).strip() if item.get("category") else "Uncategorized",
                "rating": self._clean_rating(item.get("rating")),
                "review_count": self._clean_review_count(item.get("review_count"))
            }
            self.normalized_data.append(normalized_item)
        return self.normalized_data