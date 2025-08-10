from sqlalchemy import Column, Integer, String, Boolean
from core.database import Base
from passlib.context import CryptContext

# Şifre yönetimi için bağlam oluştur
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Kullanici(Base):
    __tablename__ = "kullanicilar"

    id = Column(Integer, primary_key=True, index=True)
    kullanici_adi = Column(String, index=True, unique=True)
    hashed_sifre = Column(String)
    is_admin = Column(Boolean, default=False)

    def verify_password(self, password: str):
        """
        Kullanıcı tarafından girilen şifreyi, veritabanındaki hashed şifre ile karşılaştırır.
        """
        return pwd_context.verify(password, self.hashed_sifre)

def get_password_hash(password: str):
    """
    Şifreyi güvenli bir şekilde hash'ler.
    """
    return pwd_context.hash(password)
