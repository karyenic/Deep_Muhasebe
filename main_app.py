import sys
import os

# Kritik yol ayarları
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, 'src')

# Python yoluna ekle
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, SRC_DIR)

try:
    # Doğru import
    from core.database import create_all_tables
    print("="*50)
    print("✅ Modül yolları başarıyla ayarlandı!")
    print(f"Ana Dizin: {BASE_DIR}")
    print(f"Kaynak Dizin: {SRC_DIR}")
    print("="*50)
except ImportError as e:
    print(f"❌ Import Hatası: {e}")
    print("Python Yolları:")
    for p in sys.path:
        print(f" - {p}")
    input("Devam etmek için Enter'a basın...")
    exit(1)

def main():
    print("Veritabanı tabloları oluşturuluyor...")
    create_all_tables()
    print("✅ Tablolar başarıyla oluşturuldu!")
    input("\nUygulamayı kapatmak için Enter'a basın...")

if __name__ == "__main__":
    main()
