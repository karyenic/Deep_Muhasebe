from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base

class Firma(Base):
    __tablename__ = "firmalar"

    id = Column(Integer, primary_key=True, index=True)
    firma_adi = Column(String, index=True, unique=True)
    adres = Column(String)
    vergi_dairesi = Column(String)
    vergi_no = Column(String)
    telefon = Column(String)

    # Siparişler ile ilişkiyi tanımla
    siparisler = relationship("Siparis", back_populates="firma")

    def __repr__(self):
        return f"<Firma(firma_adi='{self.firma_adi}')>"
