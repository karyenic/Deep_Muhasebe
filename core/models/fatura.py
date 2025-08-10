from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base
# CariHesap modelini import etmeye gerek kalmadı

class Fatura(Base):
    __tablename__ = "faturalar"

    id = Column(Integer, primary_key=True, index=True)
    fatura_no = Column(String, index=True, unique=True)
    tarih = Column(DateTime, default=datetime.now)
    vade_tarihi = Column(DateTime, nullable=True)
    cari_hesap_id = Column(Integer, ForeignKey("cari_hesaplar.id"))
    is_irsaliye = Column(Boolean, default=False)
    
    # İlişkiyi string olarak tanımlıyoruz
    cari_hesap = relationship("CariHesap", back_populates="faturalar")
    kalemler = relationship("FaturaKalem", back_populates="fatura")

    def __repr__(self):
        return f"<Fatura(fatura_no='{self.fatura_no}', tarih='{self.tarih}')>"

class FaturaKalem(Base):
    __tablename__ = "fatura_kalemleri"

    id = Column(Integer, primary_key=True, index=True)
    fatura_id = Column(Integer, ForeignKey("faturalar.id"))
    urun_adi = Column(String)
    miktar = Column(Float)
    birim_fiyat = Column(Float)
    kdv_orani = Column(Float, default=18.0) # Varsayılan KDV oranı
    
    fatura = relationship("Fatura", back_populates="kalemler")

    def __repr__(self):
        return f"<FaturaKalem(urun='{self.urun_adi}', miktar='{self.miktar}')>"
