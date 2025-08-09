# C:\YEDEK\Deep_Muhasebe\Deep_Muhasebe-main\app.py
import tkinter as tk
from tkinter import ttk
import sqlite3

class FirmaYonetimi(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.status_var = tk.StringVar()
        self.status_var.set("Firma Yönetim Modülü")
        self.create_widgets()
        self.connect_db()
        self.load_firmalar()
        
    def connect_db(self):
        """Veritabanı bağlantısını oluştur"""
        self.conn = sqlite3.connect('veriler/muhasebe.db')
        self.c = self.conn.cursor()
        
        # Firmalar tablosu yoksa oluştur
        self.c.execute('''CREATE TABLE IF NOT EXISTS firmalar (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            ad TEXT NOT NULL,
                            vergi_no TEXT UNIQUE,
                            telefon TEXT,
                            adres TEXT)''')
        self.conn.commit()

    def create_widgets(self):
        """Arayüz bileşenlerini oluştur"""
        # Form Alanları
        form_frame = ttk.LabelFrame(self, text="Firma Bilgileri")
        form_frame.pack(fill="x", padx=10, pady=5, ipadx=5, ipady=5)
        
        # Firma Adı
        ttk.Label(form_frame, text="Firma Adı:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.firma_ad = ttk.Entry(form_frame, width=40)
        self.firma_ad.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Vergi No
        ttk.Label(form_frame, text="Vergi No:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.vergi_no = ttk.Entry(form_frame, width=20)
        self.vergi_no.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Telefon
        ttk.Label(form_frame, text="Telefon:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.telefon = ttk.Entry(form_frame, width=20)
        self.telefon.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        # Adres
        ttk.Label(form_frame, text="Adres:").grid(row=3, column=0, padx=5, pady=5, sticky="nw")
        self.adres = tk.Text(form_frame, width=30, height=4)
        self.adres.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        
        # Butonlar
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(btn_frame, text="Kaydet", command=self.save_firma).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Temizle", command=self.clear_form).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Yenile", command=self.load_firmalar).pack(side="left", padx=5)
        
        # Firma Listesi
        list_frame = ttk.LabelFrame(self, text="Kayıtlı Firmalar")
        list_frame.pack(fill="both", expand=True, padx=10, pady=5, ipadx=5, ipady=5)
        
        columns = ("id", "ad", "vergi_no", "telefon")
        self.firma_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Sütun başlıkları
        self.firma_tree.heading("id", text="ID")
        self.firma_tree.heading("ad", text="Firma Adı")
        self.firma_tree.heading("vergi_no", text="Vergi No")
        self.firma_tree.heading("telefon", text="Telefon")
        
        # Sütun genişlikleri
        self.firma_tree.column("id", width=50, anchor="center")
        self.firma_tree.column("ad", width=200)
        self.firma_tree.column("vergi_no", width=100)
        self.firma_tree.column("telefon", width=120)
        
        self.firma_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Durum çubuğu
        status_bar = ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w")
        status_bar.pack(side="bottom", fill="x")
        
        # Seçim olayı
        self.firma_tree.bind("<<TreeviewSelect>>", self.on_select)

    def save_firma(self):
        """Firma bilgilerini veritabanına kaydet"""
        ad = self.firma_ad.get().strip()
        vergi_no = self.vergi_no.get().strip()
        telefon = self.telefon.get().strip()
        adres = self.adres.get("1.0", tk.END).strip()
        
        if not ad:
            self.status_var.set("Hata: Firma adı boş olamaz")
            return
            
        try:
            self.c.execute("INSERT INTO firmalar (ad, vergi_no, telefon, adres) VALUES (?, ?, ?, ?)",
                          (ad, vergi_no, telefon, adres))
            self.conn.commit()
            self.status_var.set(f"{ad} firması başarıyla kaydedildi")
            self.clear_form()
            self.load_firmalar()
        except sqlite3.IntegrityError:
            self.status_var.set("Hata: Bu vergi numarası zaten kayıtlı")

    def clear_form(self):
        """Form alanlarını temizle"""
        self.firma_ad.delete(0, tk.END)
        self.vergi_no.delete(0, tk.END)
        self.telefon.delete(0, tk.END)
        self.adres.delete("1.0", tk.END)
        self.status_var.set("Form temizlendi")

    def load_firmalar(self):
        """Firmaları veritabanından yükle ve listele"""
        # Önce mevcut verileri temizle
        for row in self.firma_tree.get_children():
            self.firma_tree.delete(row)
        
        # Veritabanından firmaları al
        self.c.execute("SELECT id, ad, vergi_no, telefon FROM firmalar ORDER BY ad")
        firmalar = self.c.fetchall()
        
        # Treeview'a ekle
        for firma in firmalar:
            self.firma_tree.insert("", tk.END, values=firma)
        
        self.status_var.set(f"Toplam {len(firmalar)} firma yüklendi")

    def on_select(self, event):
        """Seçilen firmayı forma yükle"""
        selected = self.firma_tree.focus()
        if not selected:
            return
            
        values = self.firma_tree.item(selected, "values")
        if not values:
            return
            
        self.clear_form()
        self.firma_ad.insert(0, values[1])
        self.vergi_no.insert(0, values[2])
        self.telefon.insert(0, values[3])
        
        # Adresi veritabanından al
        self.c.execute("SELECT adres FROM firmalar WHERE id=?", (values[0],))
        adres = self.c.fetchone()
        if adres and adres[0]:
            self.adres.insert("1.0", adres[0])
        
        self.status_var.set(f"{values[1]} firması yüklendi")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Deep Muhasebe - Firma Yönetimi")
    root.geometry("800x600")
    
    app = FirmaYonetimi(root)
    app.pack(fill="both", expand=True)
    
    root.mainloop()
