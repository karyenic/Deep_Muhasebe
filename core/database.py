from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Veritabanı dosyasının yolu
DATABASE_URL = "sqlite:///./database/main.db"

# Veritabanı motorunu oluştur
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Modeller için temel sınıf
Base = declarative_base()

# Veritabanı oturumunu oluştur
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Veritabanı oturumu almak için kullanılan fonksiyon
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """
    Veritabanı tablolarını oluşturur.
    """
    Base.metadata.create_all(bind=engine)