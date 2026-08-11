import time
import logging
from functools import wraps
import os

def setup_logging():
    # Logların hem dosyaya hem de ekrana yazdırılmasını sağlar
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - [%(module)s] %(message)s',
        handlers=[
            logging.FileHandler("agent_flow.log", encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def retry(max_attempts=3, delay=2, backoff=2, exceptions=(Exception,)):
    """Geçici hatalarda fonksiyonun tekrar çalıştırılmasını sağlayan decorator."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            mtries, mdelay = max_attempts, delay
            while mtries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    logging.warning(f"{func.__name__} başarisiz oldu: {e}. {mdelay} saniye sonra tekrar deneniyor... (Kalan: {mtries-1})")
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            # Son deneme
            return func(*args, **kwargs)
        return wrapper
    return decorator