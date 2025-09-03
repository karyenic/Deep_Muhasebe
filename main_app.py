import os
import sys

# Python yoluna ana dizini ve src'yi ekle
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, 'src'))
sys.path.insert(0, BASE_DIR)

from src.core.database import create_all_tables


def kullanici_islemleri():
    """Kullanıcı işlemleri menüsü"""
    print("\nKullanıcı İşlemleri:")
    print("1. Yeni Kullanıcı Ekle")
    print("2. Kullanıcı Listele")
    print("3. Kullanıcı Düzenle")
    print("0. Ana Menüye Dön")
    
    secim = input("Seçiminiz: ")
    print(f"{secim} numaralı işlem seçildi")

def fatura_islemleri():
    """Fatura işlemleri menüsü"""
    print("\nFatura İşlemleri:")
    print("1. Yeni Fatura Oluştur")
    print("2. Faturaları Listele")
    print("3. Fatura Düzenle")
    print("0. Ana Menüye Dön")
    
    secim = input("Seçiminiz: ")
    print(f"{secim} numaralı işlem seçildi")

def raporlar():
    """Raporlar menüsü"""
    print("\nRaporlar:")
    print("1. Aylık Rapor")
    print("2. Yıllık Rapor")
    print("3. Özel Rapor")
    print("0. Ana Menüye Dön")
    
    secim = input("Seçiminiz: ")
    print(f"{secim} numaralı işlem seçildi")

def ana_menu():
    """Ana menü"""
    while True:
        print("\n" + "="*50)
        print("DEEP MUHASEBE ANA MENÜ")
        print("="*50)
        print("1. Kullanıcı İşlemleri")
        print("2. Fatura İşlemleri")
        print("3. Raporlar")
        print("0. Çıkış")
        
        secim = input("Seçiminiz: ")
        
        if secim == "1":
            kullanici_islemleri()
        elif secim == "2":
            fatura_islemleri()
        elif secim == "3":
            raporlar()
        elif secim == "0":
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim! Tekrar deneyin.")


def kullanici_islemleri():
    """Kullanıcı işlemleri menüsü"""
    print("\nKullanıcı İşlemleri:")
    print("1. Yeni Kullanıcı Ekle")
    print("2. Kullanıcı Listele")
    print("3. Kullanıcı Düzenle")
    print("0. Ana Menüye Dön")
    
    secim = input("Seçiminiz: ")
    print(f"{secim} numaralı işlem seçildi")

def fatura_islemleri():
    """Fatura işlemleri menüsü"""
    print("\nFatura İşlemleri:")
    print("1. Yeni Fatura Oluştur")
    print("2. Faturaları Listele")
    print("3. Fatura Düzenle")
    print("0. Ana Menüye Dön")
    
    secim = input("Seçiminiz: ")
    print(f"{secim} numaralı işlem seçildi")

def raporlar():
    """Raporlar menüsü"""
    print("\nRaporlar:")
    print("1. Aylık Rapor")
    print("2. Yıllık Rapor")
    print("3. Özel Rapor")
    print("0. Ana Menüye Dön")
    
    secim = input("Seçiminiz: ")
    print(f"{secim} numaralı işlem seçildi")

def ana_menu():
    """Ana menü"""
    while True:
        print("\n" + "="*50)
        print("DEEP MUHASEBE ANA MENÜ")
        print("="*50)
        print("1. Kullanıcı İşlemleri")
        print("2. Fatura İşlemleri")
        print("3. Raporlar")
        print("0. Çıkış")
        
        secim = input("Seçiminiz: ")
        
        if secim == "1":
            kullanici_islemleri()
        elif secim == "2":
            fatura_islemleri()
        elif secim == "3":
            raporlar()
        elif secim == "0":
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim! Tekrar deneyin.")

def main():
    print("=" * 50)
    print("Deep Muhasebe Uygulaması Başlatılıyor...")
    print("=" * 50)
    
    # Veritabanı tablolarını oluştur
    create_all_tables()
    
    print("Uygulama başarıyla başlatıldı!")
    input("\nÇıkmak için Enter'a basın...")

if __name__ == "__main__":
    main()





