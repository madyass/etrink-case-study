import csv
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def export_to_csv(results_list, output_dir="outputs"):
    if not results_list:
        logger.warning("Dışa aktarılacak sonuç bulunamadı.")
        return

    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_dir, f"recommendations_{timestamp}.csv")
    
    try:
        with open(filename, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            # Başlıklar
            writer.writerow(["Kullanici Talebi", "Zaman", "Urun ID", "Urun Adi", "Fiyat", "URL", "Secim Gerekcesi"])
            
            for res in results_list:
                talep = res.get("kullanici_talebi", "")
                zaman = res.get("calisma_zamani", "")
                for urun in res.get("onerilen_urunler", []):
                    writer.writerow([
                        talep, zaman, 
                        urun.get("id"), urun.get("ad"), 
                        urun.get("fiyat"), urun.get("url"), 
                        urun.get("secim_gerekcesi")
                    ])
        logger.info(f"Sonuçlar CSV dosyasına aktarıldı: {filename} (Google Sheets ile içeri aktarabilirsiniz)")
    except Exception as e:
        logger.error(f"CSV dışa aktarım hatası: {e}")