from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Veritabanı bağlantısı - DÜZELTİLMİŞ YOL
SQLALCHEMY_DATABASE_URL = "sqlite:///./veriler/muhasebe.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def create_all_tables():
    """Tüm tabloları oluşturur"""
    Base.metadata.create_all(bind=engine)
    print("✅ Tablolar başarıyla oluşturuldu!")

def get_db():
    """Veritabanı bağlantısı sağlar"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
