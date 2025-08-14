import sys
import os

# Python yoluna ana dizin ve src klasörünü ekle
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, 'src'))
sys.path.insert(0, BASE_DIR)

# Doğru import yolu
from src.core.database import create_all_tables

def main():
    print("="*50)
    print("Deep Muhasebe Uygulaması Başlatılıyor...")
    print(f"Çalışma Dizini: {os.getcwd()}")
    print(f"Python Yolu: {sys.path}")
    print("="*50)
    
    print("Veritabanı tabloları oluşturuluyor...")
    create_all_tables()
    print("✅ Tablolar başarıyla oluşturuldu!")
    
    input("\nUygulamayı kapatmak için Enter'a basın...")

if __name__ == "__main__":
    main()
