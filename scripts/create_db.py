from core.database import create_tables
from core.models.firma import Firma
from core.models.kullanici import Kullanici
from core.models.siparis import Siparis, SiparisKalem
from core.models.cari_hesap import CariHesap # Yeni eklenen satır

if __name__ == "__main__":
    print("Veritabanı tabloları oluşturuluyor...")
    create_tables()
    print("Tablolar başarıyla oluşturuldu!")
