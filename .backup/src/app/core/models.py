# -*- coding: utf-8 -*-
from src.core.database import'u önlemek için

class Firm(Base):
    __tablename__ = 'firmalar'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    address = Column(String)
    tax_number = Column(String)

class User(Base):
    __tablename__ = 'kullanicilar'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    firm_id = Column(Integer, nullable=False)




