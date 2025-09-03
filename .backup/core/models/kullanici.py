from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.core.database import Base

class Kullanici(Base):
    __tablename__ = "kullanicilar"

    id = Column(Integer, primary_key=True, index=True)
    kullanici_adi = Column(String, unique=True, index=True)
    sifre = Column(String)
    yetkili = Column(Boolean, default=False)
    
    # Firma tablosuna yabancı anahtar ekleniyor
    firma_id = Column(Integer, ForeignKey("firmalar.id"))
    
    # Firma ile ilişki kuruluyor
    firma = relationship("Firma", back_populates="kullanicilar")

    def __repr__(self):
        return f"<Kullanici(kullanici_adi='{self.kullanici_adi}')>"


