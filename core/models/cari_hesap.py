from sqlalchemy import Column, Integer, String, Boolean
from core.database import Base

class CariHesap(Base):
    __tablename__ = "cari_hesaplar"

    id = Column(Integer, primary_key=True, index=True)
    cari_adi = Column(String, index=True, unique=True)
    adres = Column(String)
    telefon = Column(String)
    vergi_dairesi = Column(String)
    vergi_no = Column(String)
    musteri = Column(Boolean, default=True) # True ise müşteri, False ise tedarikçi

    def __repr__(self):
        return f"<CariHesap(cari_adi='{self.cari_adi}')>"
