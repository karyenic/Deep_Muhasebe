from core.database import create_tables
from core.models.firma import Firma
from core.models.kullanici import Kullanici
from core.models.cari_hesap import CariHesap
from core.models.siparis import Siparis, SiparisKalem
from core.models.fatura import Fatura, FaturaKalem # Yeni eklenen satÄ±r

if __name__ == "__main__":
    print("VeritabanÄ± tablolarÄ± oluÅŸturuluyor...")
    create_tables()
    print("Tablolar baÅŸarÄ±yla oluÅŸturuldu!")
