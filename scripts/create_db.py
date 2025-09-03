from src.core.database import create_tables
from core.models import *

if __name__ == "__main__":
    print("Veritabanı tabloları oluşturuluyor...")
    create_tables()
    print("Tablolar başarıyla oluşturuldu!")

