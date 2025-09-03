from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.core.database import Base

class Firma(Base):
    __tablename__ = "firmalar"

    id = Column(Integer, primary_key=True, index=True)
    unvan = Column(String, unique=True, index=True)
    adres = Column(String)
    vergi_dairesi = Column(String)
    vergi_no = Column(String)

    kullanicilar = relationship("Kullanici", back_populates="firma")
    # Siparişler ile firma arasında doğrudan bir ilişki yok, bu nedenle ilişki tanımı kaldırıldı.
    
    def __repr__(self):
        return f"<Firma(unvan='{self.unvan}')>"


