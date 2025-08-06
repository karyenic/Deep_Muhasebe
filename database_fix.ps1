# database_fix.ps1
$filePath = "C:\YEDEK\Deep_Muhasebe\core\database.py"

# Hatayı düzeltecek içerik
$fixedContent = @"
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite veritabanı URL'i (bu satırda girinti OLMAMALI)
DATABASE_URL = "sqlite:///./muhasebe.db"

# Veritabanı motorunu oluştur
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"@

# Dosyayı düzeltilmiş içerikle yeniden yaz
$fixedContent | Out-File -FilePath $filePath -Encoding utf8

Write-Host "database.py dosyasındaki girinti hatası düzeltildi!" -ForegroundColor Green
