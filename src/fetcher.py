import requests
import json
import logging
from utils import retry

logger = logging.getLogger(__name__)

@retry(max_attempts=3, delay=2)
def fetch_live_data(url="https://alfiqcopper.com/products.json?limit=250"):
    logger.info(f"Canlı veriye bağlanılıyor: {url}")
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    logger.info("Canlı veri başarıyla çekildi.")
    return data

def load_local_data(filepath):
    logger.info(f"Yerel veriye (Fallback) dönülüyor: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)