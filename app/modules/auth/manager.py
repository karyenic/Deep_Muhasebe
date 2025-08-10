# -*- coding: utf-8 -*-
"""Şifreyi hash'ler (bcrypt kullanılarak)."""
    # Basit bir hash fonksiyonu (gerçekte bcrypt kullanılmalı)
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(hashed_password: str, user_password: str) -> bool:
    """Hashlenmiş şifre ile kullanıcı şifresini karşılaştırır."""
    return hashed_password == hash_password(user_password)

def create_user(username: str, password: str, firm_id: int):
    """Yeni kullanıcı oluşturur."""
    from core.database import get_session
    from core.models import User
    
    with get_session() as session:
        new_user = User(
            username=username,
            password=hash_password(password),
            firm_id=firm_id
        )
        session.add(new_user)
        session.commit()




