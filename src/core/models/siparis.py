from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base
from core.models.cari_hesap import CariHesap

class Siparis(Base):
    __tablename__ = "siparisler"

    id = Column(Integer, primary_key=True, index=True)
    siparis_no = Column(String, index=True, unique=True)
    tarih = Column(DateTime, default=datetime.now)
    cari_hesap_id = Column(Integer, ForeignKey("cari_hesaplar.id"))
    
    cari_hesap = relationship("CariHesap", back_populates="siparisler")
    kalemler = relationship("SiparisKalem", back_populates="siparis")

    def __repr__(self):
        return f"<Siparis(siparis_no='{self.siparis_no}', tarih='{self.tarih}')>"

class SiparisKalem(Base):
    __tablename__ = "siparis_kalemleri"

    id = Column(Integer, primary_key=True, index=True)
    siparis_id = Column(Integer, ForeignKey("siparisler.id"))
    urun_adi = Column(String)
    miktar = Column(Float)
    birim_fiyat = Column(Float)
    
    siparis = relationship("Siparis", back_populates="kalemler")

    def __repr__(self):
        return f"<SiparisKalem(urun='{self.urun_adi}', miktar='{self.miktar}')>"
