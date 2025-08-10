import tkinter as tk
from tkinter import ttk, messagebox
from core.database import SessionLocal, create_tables
from core.models.kullanici import Kullanici, get_password_hash
import sys
import os

# Proje ana dizinini Python'ın arama yoluna ekle
ana_dizin = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ana_dizin)

# Veritabanı tablolarını oluştur
create_tables()

class KullaniciYonetimi(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Kullanıcı Yönetimi")
        self.geometry("500x350")
        self.db_session = SessionLocal()

        self.create_widgets()
        self.listele_kullanicilar()
        self.protocol("WM_DELETE_WINDOW", self.on_kapat)

    def on_kapat(self):
        self.db_session.close()
        self.destroy()

    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Kullanıcı Ekleme Formu
        ekle_frame = ttk.LabelFrame(main_frame, text="Kullanıcı Ekle/Düzenle")
        ekle_frame.pack(padx=5, pady=5, fill="x")

        ttk.Label(ekle_frame, text="Kullanıcı Adı:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.kullanici_adi_entry = ttk.Entry(ekle_frame)
        self.kullanici_adi_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(ekle_frame, text="Şifre:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.sifre_entry = ttk.Entry(ekle_frame, show="*")
        self.sifre_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.is_admin_var = tk.BooleanVar()
        self.is_admin_check = ttk.Checkbutton(ekle_frame, text="Yönetici (Admin) Yetkisi", variable=self.is_admin_var)
        self.is_admin_check.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(ekle_frame, text="Kaydet", command=self.kullanici_kaydet).grid(row=3, column=1, padx=5, pady=10, sticky="e")

        # Kullanıcı Listeleme Bölümü
        listele_frame = ttk.LabelFrame(main_frame, text="Kullanıcı Listesi")
        listele_frame.pack(padx=5, pady=5, fill="both", expand=True)

        self.kullanici_listbox = tk.Listbox(listele_frame)
        self.kullanici_listbox.pack(padx=5, pady=5, fill="both", expand=True)
        self.kullanici_listbox.bind("<<ListboxSelect>>", self.kullanici_sec)
        
        self.listele_kullanicilar()

    def kullanici_kaydet(self):
        kullanici_adi = self.kullanici_adi_entry.get()
        sifre = self.sifre_entry.get()
        is_admin = self.is_admin_var.get()

        if not kullanici_adi or not sifre:
            messagebox.showerror("Hata", "Kullanıcı adı ve şifre boş bırakılamaz!")
            return

        hashed_sifre = get_password_hash(sifre)

        yeni_kullanici = Kullanici(
            kullanici_adi=kullanici_adi,
            hashed_sifre=hashed_sifre,
            is_admin=is_admin
        )
        
        self.db_session.add(yeni_kullanici)
        self.db_session.commit()
        messagebox.showinfo("Başarılı", f"'{kullanici_adi}' adlı kullanıcı başarıyla eklendi.")
        self.listele_kullanicilar()
        self.temizle_form()

    def listele_kullanicilar(self):
        self.kullanici_listbox.delete(0, tk.END)
        kullanicilar = self.db_session.query(Kullanici).all()
        for kullanici in kullanicilar:
            yetki = " (Yönetici)" if kullanici.is_admin else ""
            self.kullanici_listbox.insert(tk.END, f"{kullanici.kullanici_adi}{yetki}")

    def kullanici_sec(self, event):
        # Bu kısımda seçilen kullanıcının bilgileri çekilip düzenleme formuna yerleştirilebilir
        pass

    def temizle_form(self):
        self.kullanici_adi_entry.delete(0, tk.END)
        self.sifre_entry.delete(0, tk.END)
        self.is_admin_var.set(False)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    kullanici_ekrani = KullaniciYonetimi(root)
    kullanici_ekrani.mainloop()
