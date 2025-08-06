# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base
 class Firm(Base):
      """
        Firma modeli - Her firma muhasebe verilerini iÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§eren baÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±msÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±z bir birimdir
        """
       __tablename__ = 'firms'
         id = Column(Integer, primary_key=True, index=True)
        name = Column(
            String(100),
            nullable=False,
            unique=True,
            comment="Firma AdÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±")
        address = Column(String(200), comment="Firma Adresi")
        tax_number = Column(String(20), unique=True, comment="Vergi NumarasÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±")
        phone = Column(String(15), comment="Telefon NumarasÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±")
        email = Column(String(100), comment="ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š°letiÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸im E-postasÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±")
         # ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š°liÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸kiler
        users = relationship(
            "User",
            back_populates="firm",
            cascade="all, delete-orphan")
        invoices = relationship("Invoice", back_populates="firm")
        accounts = relationship("Account", back_populates="firm")
         def __repr__(self):
              return f"<Firm(id={self.id}, name='{self.name}')>"


