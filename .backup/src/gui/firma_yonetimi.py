import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox

# Proje ana dizinini Python'ın arama yoluna ekle
ana_dizin = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ana_dizin)

from src.core.database import SessionLocal, create_tables
from core.models.firma import Firma

# Veritabanı tablolarını oluştur
create_tables()

class FirmaYonetimi(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Firma Yönetimi")
        self.geometry("600x400")

        self.db_session = SessionLocal()
        self.firmalar = self.get_firmalar()

        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_kapat)

    def on_kapat(self):
        self.db_session.close()
        self.destroy()

    def create_widgets(self):
        # Sekme kontrolü
        self.tabControl = ttk.Notebook(self)
        self.ekle_tab = ttk.Frame(self.tabControl)
        self.listele_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.ekle_tab, text="Firma Ekle")
        self.tabControl.add(self.listele_tab, text="Firmaları Listele")
        self.tabControl.pack(expand=1, fill="both")

        # Firma Ekleme Sekmesi
        ekle_frame = ttk.LabelFrame(self.ekle_tab, text="Yeni Firma Bilgileri")
        ekle_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(ekle_frame, text="Firma Adı:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.firma_adi_entry = ttk.Entry(ekle_frame)
        self.firma_adi_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(ekle_frame, text="Adres:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.adres_entry = ttk.Entry(ekle_frame)
        self.adres_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(ekle_frame, text="Vergi Dairesi:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.vergi_dairesi_entry = ttk.Entry(ekle_frame)
        self.vergi_dairesi_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(ekle_frame, text="Vergi No:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.vergi_no_entry = ttk.Entry(ekle_frame)
        self.vergi_no_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(ekle_frame, text="Telefon:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.telefon_entry = ttk.Entry(ekle_frame)
        self.telefon_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(ekle_frame, text="Kaydet", command=self.firma_ekle).grid(row=5, column=1, padx=5, pady=10, sticky="e")

        # Firmaları Listeleme Sekmesi
        listele_frame = ttk.LabelFrame(self.listele_tab, text="Kayıtlı Firmalar")
        listele_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.firma_listbox = tk.Listbox(listele_frame)
        self.firma_listbox.pack(padx=5, pady=5, fill="both", expand=True)
        self.firma_listbox.bind("<<ListboxSelect>>", self.firma_sec)

        self.firmalari_listele()

    def get_firmalar(self):
        return self.db_session.query(Firma).all()

    def firmalari_listele(self):
        self.firma_listbox.delete(0, tk.END)
        self.firmalar = self.get_firmalar()
        for firma in self.firmalar:
            self.firma_listbox.insert(tk.END, firma.firma_adi)

    def firma_ekle(self):
        firma_adi = self.firma_adi_entry.get()
        if not firma_adi:
            messagebox.showerror("Hata", "Firma adı boş bırakılamaz!")
            return

        yeni_firma = Firma(
            firma_adi=firma_adi,
            adres=self.adres_entry.get(),
            vergi_dairesi=self.vergi_dairesi_entry.get(),
            vergi_no=self.vergi_no_entry.get(),
            telefon=self.telefon_entry.get()
        )

        self.db_session.add(yeni_firma)
        self.db_session.commit()
        messagebox.showinfo("Başarılı", f"'{firma_adi}' adlı firma başarıyla eklendi.")
        self.firmalari_listele()
        self.temizle_form()

    def firma_sec(self, event):
        secili_index = self.firma_listbox.curselection()
        if secili_index:
            firma = self.firmalar[secili_index[0]]
            messagebox.showinfo("Firma Seçildi", f"Seçilen Firma: {firma.firma_adi}")

    def temizle_form(self):
        self.firma_adi_entry.delete(0, tk.END)
        self.adres_entry.delete(0, tk.END)
        self.vergi_dairesi_entry.delete(0, tk.END)
        self.vergi_no_entry.delete(0, tk.END)
        self.telefon_entry.delete(0, tk.END)

if __name__ == "__main__":
    # Ana pencere (gizli)
    root = tk.Tk()
    root.withdraw()

    # Firma yönetimi penceresini aç
    firma_ekrani = FirmaYonetimi(root)
    firma_ekrani.mainloop()

