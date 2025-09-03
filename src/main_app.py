# -*- coding: utf-8 -*-
import sys
import os
from pathlib import Path

# OTOMATİK PATH DÜZELTME
def fix_paths():
    # 1. Proje kök yolunu bul
    PROJE_KOKU = Path(__file__).resolve().parent.parent
    
    # 2. src dizinini Python yoluna ekle (CRITICAL FIX!)
    src_path = PROJE_KOKU / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
        print(f"[PATH DÜZELTME] Eklendi src: {src_path}")
    
    # 3. Sanal ortam site-packages ekle
    venv_path = PROJE_KOKU / "venv"
    
    # Windows ve Linux uyumlu yol
    site_packages = venv_path / "Lib" / "site-packages"
    if not site_packages.exists():
        site_packages = venv_path / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"
    
    if site_packages.exists() and str(site_packages) not in sys.path:
        sys.path.insert(0, str(site_packages))
        print(f"[PATH DÜZELTME] Eklendi site-packages: {site_packages}")
    
    # 4. Doğrulama çıktısı
    print(f"[PATH DÜZELTME] Proje Kök: {PROJE_KOKU}")
    print(f"[PATH DÜZELTME] Python Yürütücü: {sys.executable}")

# Yolu düzeltmeyi uygula
fix_paths()

# VERİTABANI BAŞLATMA
try:
    from core.database import create_tables
    print("Veritabanı tabloları oluşturuluyor...")
    create_tables()
    print("✅ Tablolar başarıyla oluşturuldu!")
except Exception as e:
    print(f"❌ Veritabanı hatası: {str(e)}")

# UYGULAMA SONU
input("\nUygulamayı kapatmak için Enter'a basın...")
