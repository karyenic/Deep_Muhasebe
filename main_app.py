import os
import sys

# Python yoluna ana dizini ve src'yi ekle
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, 'src'))
sys.path.insert(0, BASE_DIR)

from src.core.database import create_all_tables

def main():
    print("=" * 50)
    print("Deep Muhasebe Uygulaması Başlatılıyor...")
    print("=" * 50)
    
    # Veritabanı tablolarını oluştur
    create_all_tables()
    
    print("Uygulama başarıyla başlatıldı!")
    input("\nÇıkmak için Enter'a basın...")

if __name__ == "__main__":
    main()
