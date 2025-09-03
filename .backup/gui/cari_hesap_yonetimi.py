import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox

# Proje ana dizinini Python'ın arama yoluna ekle
ana_dizin = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ana_dizin)

from src.core.database import SessionLocal, create_all_tables
from core.models.cari_hesap import CariHesap

# Veritabanı tablolarını oluştur
create_all_tables()

class CariHesapYonetimi(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Cari Hesap Yönetimi")
        self.geometry("600x400")
        self.db_session = SessionLocal()

        self.create_widgets()
        self.listele_cari_hesaplar()
        self.protocol("WM_DELETE_WINDOW", self.on_kapat)

    def on_kapat(self):
        self.db_session.close()
        self.destroy()

    def create_widgets(self):
        # Sekme kontrolü
        self.tabControl = ttk.Notebook(self)
        self.ekle_tab = ttk.Frame(self.tabControl)
        self.listele_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.ekle_tab, text="Cari Hesap Ekle")
        self.tabControl.add(self.listele_tab, text="Cari Hesapları Listele")
        self.tabControl.pack(expand=1, fill="both")

        # Cari Hesap Ekleme Sekmesi
        ekle_frame = ttk.LabelFrame(self.ekle_tab, text="Yeni Cari Hesap Bilgileri")
        ekle_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(ekle_frame, text="Adı:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.adi_entry = ttk.Entry(ekle_frame)
        self.adi_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(ekle_frame, text="Adres:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.adres_entry = ttk.Entry(ekle_frame)
        self.adres_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(ekle_frame, text="Telefon:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.telefon_entry = ttk.Entry(ekle_frame)
        self.telefon_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(ekle_frame, text="Vergi Dairesi:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.vergi_dairesi_entry = ttk.Entry(ekle_frame)
        self.vergi_dairesi_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(ekle_frame, text="Vergi No:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.vergi_no_entry = ttk.Entry(ekle_frame)
        self.vergi_no_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        self.hesap_tipi_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(ekle_frame, text="Müşteri (seçili) / Tedarikçi", variable=self.hesap_tipi_var).grid(row=5, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Button(ekle_frame, text="Kaydet", command=self.cari_hesap_ekle).grid(row=6, column=1, padx=5, pady=10, sticky="e")

        # Cari Hesapları Listeleme Sekmesi
        listele_frame = ttk.LabelFrame(self.listele_tab, text="Kayıtlı Cari Hesaplar")
        listele_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.cari_listbox = tk.Listbox(listele_frame)
        self.cari_listbox.pack(padx=5, pady=5, fill="both", expand=True)
        self.cari_listbox.bind("<<ListboxSelect>>", self.cari_hesap_sec)

    def cari_hesap_ekle(self):
        cari_adi = self.adi_entry.get()
        if not cari_adi:
            messagebox.showerror("Hata", "Cari hesap adı boş bırakılamaz!")
            return

        yeni_cari = CariHesap(
            cari_adi=cari_adi,
            adres=self.adres_entry.get(),
            telefon=self.telefon_entry.get(),
            vergi_dairesi=self.vergi_dairesi_entry.get(),
            vergi_no=self.vergi_no_entry.get(),
            musteri=self.hesap_tipi_var.get()
        )
        
        self.db_session.add(yeni_cari)
        self.db_session.commit()
        messagebox.showinfo("Başarılı", f"'{cari_adi}' adlı cari hesap başarıyla eklendi.")
        self.listele_cari_hesaplar()
        self.temizle_form()

    def listele_cari_hesaplar(self):
        self.cari_listbox.delete(0, tk.END)
        cari_hesaplar = self.db_session.query(CariHesap).all()
        for cari in cari_hesaplar:
            tipi = "Müşteri" if cari.musteri else "Tedarikçi"
            self.cari_listbox.insert(tk.END, f"{cari.cari_adi} ({tipi})")

    def cari_hesap_sec(self, event):
        # Seçilen cari hesaba özel işlemler burada yapılabilir
        pass

    def temizle_form(self):
        self.adi_entry.delete(0, tk.END)
        self.adres_entry.delete(0, tk.END)
        self.telefon_entry.delete(0, tk.END)
        self.vergi_dairesi_entry.delete(0, tk.END)
        self.vergi_no_entry.delete(0, tk.END)
        self.hesap_tipi_var.set(True)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    cari_hesap_ekrani = CariHesapYonetimi(root)
    cari_hesap_ekrani.mainloop()


