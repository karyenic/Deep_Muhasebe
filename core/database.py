# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import event
from sqlalchemy.engine import Engine
from contextlib import contextmanager

# SQLite veritabanı URL'i
DATABASE_URL = "sqlite:///./muhasebe.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FOREIGN KEY desteği için
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# Tabloları oluşturma fonksiyonu
def init_db():
    # Döngüsel import'u önlemek için içeriye alındı
    from core.models import Firm, User
    Base.metadata.create_all(bind=engine)

# Düzeltilmiş session yöneticisi
@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


