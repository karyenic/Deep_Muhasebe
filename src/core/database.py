import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# TAM YOL ile veritabanı bağlantısı
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "veriler", "muhasebe.db")

# Dizini oluştur
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modeller
class Kullanici(Base):
    __tablename__ = "kullanicilar"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    ad = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    sifre = Column(String)
    kayit_tarihi = Column(DateTime)

# İhtiyaca göre diğer modelleri buraya ekleyin

def create_all_tables():
    """Tüm tabloları oluşturur"""
    try:
        Base.metadata.create_all(bind=engine)
        print(f"✅ Tablolar başarıyla oluşturuldu! Veritabanı: {DB_PATH}")
    except Exception as e:
        print(f"❌ Veritabanı hatası: {e}")
        raise

def get_db():
    """Veritabanı bağlantısı sağlar"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
