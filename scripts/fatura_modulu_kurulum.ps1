# Proje ana dizinini belirle
$projeAnaDizini = "C:\YEDEK\Deep_Muhasebe\Deep_Muhasebe-main"

# Betiğin çalışacağı dizine git
Set-Location -Path $projeAnaDizini

Write-Host "Fatura-İrsaliye modülü için dosyalar oluşturuluyor ve güncelleniyor..."

#----------------------------------------------------
# 1. core/models/fatura.py dosyasını oluştur
#----------------------------------------------------
Write-Host "core\models\fatura.py dosyası oluşturuluyor..."
$faturaKodu = @"
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base
from core.models.cari_hesap import CariHesap

class Fatura(Base):
    __tablename__ = "faturalar"

    id = Column(Integer, primary_key=True, index=True)
    fatura_no = Column(String, index=True, unique=True)
    tarih = Column(DateTime, default=datetime.now)
    vade_tarihi = Column(DateTime, nullable=True)
    cari_hesap_id = Column(Integer, ForeignKey("cari_hesaplar.id"))
    is_irsaliye = Column(Boolean, default=False)
    
    cari_hesap = relationship("CariHesap", back_populates="faturalar")
    kalemler = relationship("FaturaKalem", back_populates="fatura")

    def __repr__(self):
        return f"<Fatura(fatura_no='{self.fatura_no}', tarih='{self.tarih}')>"

class FaturaKalem(Base):
    __tablename__ = "fatura_kalemleri"

    id = Column(Integer, primary_key=True, index=True)
    fatura_id = Column(Integer, ForeignKey("faturalar.id"))
    urun_adi = Column(String)
    miktar = Column(Float)
    birim_fiyat = Column(Float)
    kdv_orani = Column(Float, default=18.0) # Varsayılan KDV oranı
    
    fatura = relationship("Fatura", back_populates="kalemler")

    def __repr__(self):
        return f"<FaturaKalem(urun='{self.urun_adi}', miktar='{self.miktar}')>"
"@
$faturaKodu | Out-File -FilePath "core\models\fatura.py" -Encoding UTF8 -Force
Write-Host "fatura.py dosyası oluşturuldu."

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

    # Siparişler ve Faturalar ile ilişkiyi tanımla
    siparisler = relationship("Siparis", back_populates="cari_hesap")
    faturalar = relationship("Fatura", back_populates="cari_hesap") # Yeni eklenen satır

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
from core.models.fatura import Fatura, FaturaKalem # Yeni eklenen satır

if __name__ == "__main__":
    print("Veritabanı tabloları oluşturuluyor...")
    create_tables()
    print("Tablolar başarıyla oluşturuldu!")
"@
$createDbKodu | Out-File -FilePath "scripts\create_db.py" -Encoding UTF8 -Force
Write-Host "create_db.py dosyası güncellendi."

#----------------------------------------------------
# 4. gui/fatura_irsaliye.py dosyasını oluştur
#----------------------------------------------------
Write-Host "gui\fatura_irsaliye.py dosyası oluşturuluyor..."
$guiKodu = @"
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from datetime import datetime
import locale

# Proje ana dizinini Python'ın arama yoluna ekle
ana_dizin = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ana_dizin)

from core.database import SessionLocal, create_tables
from core.models.fatura import Fatura, FaturaKalem
from core.models.cari_hesap import CariHesap

# Veritabanı tablolarını oluştur
create_tables()

# Yerel ayarları Türkçe'ye ayarla
try:
    locale.setlocale(locale.LC_TIME, 'tr_TR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'turkish')
    except locale.Error:
        pass

class FaturaIrsaliyeYonetimi(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Fatura & İrsaliye Yönetimi")
        self.geometry("1000x700")
        self.db_session = SessionLocal()
        
        self.create_widgets()
        self.load_cari_hesaplar()
        self.protocol("WM_DELETE_WINDOW", self.on_kapat)

    def on_kapat(self):
        self.db_session.close()
        self.destroy()

    def create_widgets(self):
        # Fatura Başlık Bölümü
        header_frame = ttk.LabelFrame(self, text="Belge Bilgileri")
        header_frame.pack(padx=10, pady=5, fill="x")

        ttk.Label(header_frame, text="Belge Tipi:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.belge_tipi_combobox = ttk.Combobox(header_frame, values=["Fatura", "İrsaliye"], state="readonly")
        self.belge_tipi_combobox.set("Fatura")
        self.belge_tipi_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(header_frame, text="Belge No:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.belge_no_entry = ttk.Entry(header_frame)
        self.belge_no_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        
        ttk.Label(header_frame, text="Tarih:").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.tarih_entry = ttk.Entry(header_frame)
        self.tarih_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.tarih_entry.grid(row=0, column=5, padx=5, pady=5, sticky="ew")
        
        ttk.Label(header_frame, text="Cari Hesap:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.cari_hesap_combobox = ttk.Combobox(header_frame, state="readonly")
        self.cari_hesap_combobox.grid(row=1, column=1, columnspan=5, padx=5, pady=5, sticky="ew")

        ttk.Button(header_frame, text="Siparişten Aktar", command=self.siparis_aktar).grid(row=2, column=5, padx=5, pady=5, sticky="e")
        
        # Kalemler Bölümü
        kalem_frame = ttk.LabelFrame(self, text="Kalemler")
        kalem_frame.pack(padx=10, pady=5, fill="both", expand=True)

        columns = ("urun_adi", "miktar", "birim_fiyat", "kdv_orani", "tutar")
        self.kalem_tree = ttk.Treeview(kalem_frame, columns=columns, show="headings")
        self.kalem_tree.heading("urun_adi", text="Ürün Adı")
        self.kalem_tree.heading("miktar", text="Miktar")
        self.kalem_tree.heading("birim_fiyat", text="Birim Fiyat")
        self.kalem_tree.heading("kdv_orani", text="KDV Oranı (%)")
        self.kalem_tree.heading("tutar", text="Toplam Tutar")
        self.kalem_tree.pack(fill="both", expand=True)
        
        kalem_buttons_frame = ttk.Frame(kalem_frame)
        kalem_buttons_frame.pack(fill="x")
        ttk.Button(kalem_buttons_frame, text="Satır Ekle", command=self.add_kalem_row).pack(side="left", padx=5, pady=5)
        ttk.Button(kalem_buttons_frame, text="Satır Sil", command=self.remove_kalem_row).pack(side="left", padx=5, pady=5)
        
        # Toplamlar Bölümü
        summary_frame = ttk.Frame(self)
        summary_frame.pack(padx=10, pady=5, fill="x")
        self.toplam_etiket = ttk.Label(summary_frame, text="Genel Toplam: 0.00 TL", font=("Helvetica", 12, "bold"))
        self.toplam_etiket.pack(side="right")
        
        # İşlem Butonları Bölümü
        action_frame = ttk.Frame(self)
        action_frame.pack(padx=10, pady=10, fill="x")
        ttk.Button(action_frame, text="Kaydet", command=self.belge_kaydet).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Temizle", command=self.temizle_form).pack(side="right", padx=5)

    def load_cari_hesaplar(self):
        cari_hesaplar = self.db_session.query(CariHesap).all()
        self.cari_hesaplar_map = {hesap.cari_adi: hesap.id for hesap in cari_hesaplar}
        self.cari_hesap_combobox['values'] = list(self.cari_hesaplar_map.keys())

    def add_kalem_row(self):
        self.kalem_tree.insert("", "end", values=("", "", "", 18.0, 0.0))

    def remove_kalem_row(self):
        selected_item = self.kalem_tree.selection()
        if selected_item:
            self.kalem_tree.delete(selected_item)

    def siparis_aktar(self):
        # Siparişten kalemleri aktarma mantığı burada geliştirilecek
        messagebox.showinfo("Bilgi", "Siparişten kalem aktarma fonksiyonu henüz geliştirilmedi.")

    def belge_kaydet(self):
        belge_no = self.belge_no_entry.get()
        tarih_str = self.tarih_entry.get()
        cari_adi = self.cari_hesap_combobox.get()
        belge_tipi = self.belge_tipi_combobox.get()
        is_irsaliye = (belge_tipi == "İrsaliye")

        if not belge_no or not tarih_str or not cari_adi:
            messagebox.showerror("Hata", "Belge No, Tarih ve Cari Hesap boş bırakılamaz!")
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
            
        yeni_belge = Fatura(
            fatura_no=belge_no,
            tarih=tarih,
            cari_hesap_id=cari_hesap_id,
            is_irsaliye=is_irsaliye
        )

        try:
            self.db_session.add(yeni_belge)
            self.db_session.commit()
            
            belge_id = yeni_belge.id
            for item in self.kalem_tree.get_children():
                values = self.kalem_tree.item(item, "values")
                if all(values):
                    kalem = FaturaKalem(
                        fatura_id=belge_id,
                        urun_adi=values[0],
                        miktar=float(values[1]),
                        birim_fiyat=float(values[2]),
                        kdv_orani=float(values[3])
                    )
                    self.db_session.add(kalem)
            
            self.db_session.commit()
            messagebox.showinfo("Başarılı", f"'{belge_no}' numaralı {belge_tipi} başarıyla kaydedildi.")
            self.temizle_form()
            
        except Exception as e:
            self.db_session.rollback()
            messagebox.showerror("Hata", f"Belge kaydedilirken bir hata oluştu: {e}")

    def temizle_form(self):
        self.belge_no_entry.delete(0, tk.END)
        self.tarih_entry.delete(0, tk.END)
        self.tarih_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.cari_hesap_combobox.set('')
        for item in self.kalem_tree.get_children():
            self.kalem_tree.delete(item)
        self.toplam_etiket.config(text="Genel Toplam: 0.00 TL")
        self.belge_tipi_combobox.set("Fatura")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    fatura_ekrani = FaturaIrsaliyeYonetimi(root)
    fatura_ekrani.mainloop()
"@
$guiKodu | Out-File -FilePath "gui\fatura_irsaliye.py" -Encoding UTF8 -Force
Write-Host "fatura_irsaliye.py dosyası oluşturuldu."

#----------------------------------------------------
# 5. Gerekli kütüphaneleri yükle ve git işlemlerini yap
#----------------------------------------------------
Write-Host "Veritabanı tabloları güncelleniyor..."
python scripts/create_db.py

Write-Host "Yerel değişiklikler sahneleniyor ve commit yapılıyor..."
git add .
git commit -m "Fatura-Irsaliye modulu veritabani modelleri ve GUI taslagi eklendi"

Write-Host "Değişiklikler GitHub'a gönderiliyor..."
git push origin main

Write-Host "Fatura-Irsaliye modülü başarıyla oluşturuldu ve GitHub'a senkronize edildi."