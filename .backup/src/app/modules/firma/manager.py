# -*- coding: utf-8 -*-
from core.models import Firm
from src.core.database import get_session

def create_firm(name: str, address: str, tax_number: str):
    """Yeni firma oluşturur"""
    with get_session() as session:
        # Firma adının benzersiz olup olmadığını kontrol et
        existing_firm = session.query(Firm).filter(Firm.name == name).first()
        if existing_firm:
            return False, "Bu isimde zaten bir firma var!"
        
        # Yeni firma oluştur
        new_firm = Firm(
            name=name,
            address=address,
            tax_number=tax_number
        )
        
        session.add(new_firm)
        session.commit()
        return True, "Firma başarıyla oluşturuldu!"

def get_all_firms():
    """Tüm firmaları listeler"""
    with get_session() as session:
        return session.query(Firm).all()




