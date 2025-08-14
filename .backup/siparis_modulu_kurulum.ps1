# Proje ana dizinini belirle
$projeAnaDizini = "C:\YEDEK\Deep_Muhasebe\Deep_Muhasebe-main"

# Betiğin çalışacağı dizine git
Set-Location -Path $projeAnaDizini

Write-Host "Sipariş modülü için dosyalar oluşturuluyor ve güncelleniyor..."

#----------------------------------------------------
# 1. core/models/siparis.py dosyasını güncelle
#----------------------------------------------------
Write-Host "core\models\siparis.py dosyası güncelleniyor..."
$siparisKodu = @"
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base
from core.models.cari_hesap import CariHesap

class Siparis(Base):
    __tablename__ = "siparisler"

    id = Column(Integer, primary_key=True, index=True)
    siparis_no = Column(String, index=True, unique=True)
    tarih = Column(DateTime, default=datetime.now)
    cari_hesap_id = Column(Integer, ForeignKey("cari_hesaplar.id"))
    
    cari_hesap = relationship("CariHesap", back_populates="siparisler")
    kalemler = relationship("SiparisKalem", back_populates="siparis")

    def __repr__(self):
        return f"<Siparis(siparis_no='{self.siparis_no}', tarih='{self.tarih}')>"

class SiparisKalem(Base):
    __tablename__ = "siparis_kalemleri"

    id = Column(Integer, primary_key=True, index=True)
    siparis_id = Column(Integer, ForeignKey("siparisler.id"))
    urun_adi = Column(String)
    miktar = Column(Float)
    birim_fiyat = Column(Float)
    
    siparis = relationship("Siparis", back_populates="kalemler")

    def __repr__(self):
        return f"<SiparisKalem(urun='{self.urun_adi}', miktar='{self.miktar}')>"
"@
$siparisKodu | Out-File -FilePath "core\models\siparis.py" -Encoding UTF8 -Force
Write-Host "siparis.py dosyası güncellendi."

#----------------------------------------------------
# 2. core/models/cari_hesap.py dosyasını güncelle
#----------------------------------------------------
Write-Host "core\models\cari_hesap.py dosyası güncelleniyor..."
$cariHesapKodu = @"
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from core.database import Base

class CariHesap(Base):
    __tablename__ = "cari_hesaplar"

    id = Column(Integer, primary_key=True, index=True)
    cari_adi = Column(String, index=True, unique=True)
    adres = Column(String)
    telefon = Column(String)
    vergi_dairesi = Column(String)
    vergi_no = Column(String)
    musteri = Column(Boolean, default=True) # True ise müşteri, False ise tedarikçi

    # Siparişler ile ilişkiyi tanımla
    siparisler = relationship("Siparis", back_populates="cari_hesap")

    def __repr__(self):
        return f"<CariHesap(cari_adi='{self.cari_adi}')>"
"@
$cariHesapKodu | Out-File -FilePath "core\models\cari_hesap.py" -Encoding UTF8 -Force
Write-Host "cari_hesap.py dosyası güncellendi."

#----------------------------------------------------
# 3. scripts/create_db.py dosyasını güncelle
#----------------------------------------------------
Write-Host "scripts\create_db.py dosyası güncelleniyor..."
$createDbKodu = @"
from core.database import create_tables
from core.models.firma import Firma
from core.models.kullanici import Kullanici
from core.models.cari_hesap import CariHesap
from core.models.siparis import Siparis, SiparisKalem

if __name__ == "__main__":
    print("Veritabanı tabloları oluşturuluyor...")
    create_tables()
    print("Tablolar başarıyla oluşturuldu!")
"@
$createDbKodu | Out-File -FilePath "scripts\create_db.py" -Encoding UTF8 -Force
Write-Host "create_db.py dosyası güncellendi."

#----------------------------------------------------
# 4. gui/siparis_yonetimi.py dosyasını oluştur
#----------------------------------------------------
Write-Host "gui\siparis_yonetimi.py dosyası oluşturuluyor..."
$guiKodu = @"
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from datetime import datetime

# Proje ana dizinini Python'ın arama yoluna ekle
ana_dizin = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ana_dizin)

from core.database import SessionLocal, create_tables
from core.models.siparis import Siparis, SiparisKalem
from core.models.cari_hesap import CariHesap

# Veritabanı tablolarını oluştur
create_tables()

class SiparisYonetimi(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Sipariş Yönetimi")
        self.geometry("800x600")
        self.db_session = SessionLocal()
        
        self.create_widgets()
        self.load_cari_hesaplar()
        self.protocol("WM_DELETE_WINDOW", self.on_kapat)

    def on_kapat(self):
        self.db_session.close()
        self.destroy()

    def create_widgets(self):
        # Sipariş Başlık Bölümü
        header_frame = ttk.LabelFrame(self, text="Sipariş Bilgileri")
        header_frame.pack(padx=10, pady=5, fill="x")

        ttk.Label(header_frame, text="Sipariş No:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.siparis_no_entry = ttk.Entry(header_frame)
        self.siparis_no_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(header_frame, text="Tarih:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.tarih_entry = ttk.Entry(header_frame)
        self.tarih_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.tarih_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(header_frame, text="Cari Hesap:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.cari_hesap_combobox = ttk.Combobox(header_frame, state="readonly")
        self.cari_hesap_combobox.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="ew")
        
        # Sipariş Kalemleri Bölümü
        kalem_frame = ttk.LabelFrame(self, text="Sipariş Kalemleri")
        kalem_frame.pack(padx=10, pady=5, fill="both", expand=True)

        columns = ("urun_adi", "miktar", "birim_fiyat")
        self.kalem_tree = ttk.Treeview(kalem_frame, columns=columns, show="headings")
        self.kalem_tree.heading("urun_adi", text="Ürün Adı")
        self.kalem_tree.heading("miktar", text="Miktar")
        self.kalem_tree.heading("birim_fiyat", text="Birim Fiyat")
        self.kalem_tree.pack(fill="both", expand=True)
        
        kalem_buttons_frame = ttk.Frame(kalem_frame)
        kalem_buttons_frame.pack(fill="x")
        ttk.Button(kalem_buttons_frame, text="Satır Ekle", command=self.add_kalem_row).pack(side="left", padx=5, pady=5)
        ttk.Button(kalem_buttons_frame, text="Satır Sil", command=self.remove_kalem_row).pack(side="left", padx=5, pady=5)
        
        # İşlem Butonları Bölümü
        action_frame = ttk.Frame(self)
        action_frame.pack(padx=10, pady=10, fill="x")
        ttk.Button(action_frame, text="Kaydet", command=self.siparis_kaydet).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Sevkiyat/İrsaliye Oluştur", command=self.irsaliye_olustur).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Fatura Oluştur", command=self.fatura_olustur).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Temizle", command=self.temizle_form).pack(side="right", padx=5)

    def load_cari_hesaplar(self):
        cari_hesaplar = self.db_session.query(CariHesap).all()
        self.cari_hesaplar_map = {hesap.cari_adi: hesap.id for hesap in cari_hesaplar}
        self.cari_hesap_combobox['values'] = list(self.cari_hesaplar_map.keys())

    def add_kalem_row(self):
        self.kalem_tree.insert("", "end", values=("", "", ""))

    def remove_kalem_row(self):
        selected_item = self.kalem_tree.selection()
        if selected_item:
            self.kalem_tree.delete(selected_item)

    def siparis_kaydet(self):
        # Kayıt mantığı
        siparis_no = self.siparis_no_entry.get()
        tarih_str = self.tarih_entry.get()
        cari_adi = self.cari_hesap_combobox.get()

        if not siparis_no or not tarih_str or not cari_adi:
            messagebox.showerror("Hata", "Sipariş No, Tarih ve Cari Hesap boş bırakılamaz!")
            return

        try:
            tarih = datetime.strptime(tarih_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Hata", "Geçersiz tarih formatı! (YYYY-MM-DD)")
            return

        cari_hesap_id = self.cari_hesaplar_map.get(cari_adi)
        if cari_hesap_id is None:
            messagebox.showerror("Hata", "Geçersiz Cari Hesap!")
            return

        yeni_siparis = Siparis(
            siparis_no=siparis_no,
            tarih=tarih,
            cari_hesap_id=cari_hesap_id
        )

        try:
            self.db_session.add(yeni_siparis)
            self.db_session.commit()
            
            siparis_id = yeni_siparis.id
            for item in self.kalem_tree.get_children():
                values = self.kalem_tree.item(item, "values")
                if all(values):
                    kalem = SiparisKalem(
                        siparis_id=siparis_id,
                        urun_adi=values[0],
                        miktar=float(values[1]),
                        birim_fiyat=float(values[2])
                    )
                    self.db_session.add(kalem)
            
            self.db_session.commit()
            messagebox.showinfo("Başarılı", f"Sipariş '{siparis_no}' başarıyla kaydedildi.")
            self.temizle_form()
            
        except Exception as e:
            self.db_session.rollback()
            messagebox.showerror("Hata", f"Sipariş kaydedilirken bir hata oluştu: {e}")
            
    def irsaliye_olustur(self):
        messagebox.showinfo("Bilgi", "İrsaliye oluşturma fonksiyonu henüz geliştirilmedi.")

    def fatura_olustur(self):
        messagebox.showinfo("Bilgi", "Fatura oluşturma fonksiyonu henüz geliştirilmedi.")

    def temizle_form(self):
        self.siparis_no_entry.delete(0, tk.END)
        self.tarih_entry.delete(0, tk.END)
        self.cari_hesap_combobox.set('')
        for item in self.kalem_tree.get_children():
            self.kalem_tree.delete(item)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    siparis_ekrani = SiparisYonetimi(root)
    siparis_ekrani.mainloop()
"@
$guiKodu | Out-File -FilePath "gui\siparis_yonetimi.py" -Encoding UTF8 -Force
Write-Host "siparis_yonetimi.py dosyası oluşturuldu."


#----------------------------------------------------
# 5. Gerekli kütüphaneleri yükle ve git işlemlerini yap
#----------------------------------------------------
Write-Host "Veritabanı tabloları güncelleniyor (Sipariş tabloları eklenecek)..."
python scripts/create_db.py

Write-Host "Yerel değişiklikler sahneleniyor ve commit yapılıyor..."
git add .
git commit -m "Siparis modulu veritabani modelleri ve GUI taslagi eklendi"

Write-Host "Değişiklikler GitHub'a gönderiliyor..."
git push origin main

Write-Host "Sipariş modülü başarıyla oluşturuldu ve GitHub'a senkronize edildi."