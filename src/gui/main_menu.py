# -*- coding: utf-8 -*-
from tkinter import ttk, messagebox
from core.database import get_session
from modules.firma.manager import get_all_firms

class MainMenuWindow:
    def __init__(self, app):
        self.app = app
        self.create_widgets()
        
    def create_widgets(self):
        try:
            # Ana çerçeve
            self.frame = ttk.Frame(self.app.root)
            self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Başlık
            lbl_title = ttk.Label(self.frame, text="Deep Muhasebe - Ana Menü", font=("Arial", 16, "bold"))
            lbl_title.pack(pady=20)
            
            # Firma bilgileri
            lbl_firm_title = ttk.Label(self.frame, text="Kayıtlı Firmalar", font=("Arial", 12))
            lbl_firm_title.pack(pady=10)
            
            firm_frame = ttk.Frame(self.frame)
            firm_frame.pack(fill=tk.X, padx=50, pady=10)
            
            with get_session() as session:
                firms = get_all_firms()
                if firms:
                    for i, firm in enumerate(firms):
                        row = ttk.Frame(firm_frame)
                        row.pack(fill=tk.X, pady=5)
                        
                        ttk.Label(row, text=f"{i+1}.", width=3).pack(side=tk.LEFT)
                        ttk.Label(row, text=firm.name, width=30, anchor="w").pack(side=tk.LEFT)
                        ttk.Label(row, text=firm.tax_number, width=15).pack(side=tk.LEFT)
                else:
                    ttk.Label(firm_frame, text="Henüz firma kaydı bulunmamaktadır", foreground="gray").pack(pady=20)
            
            # Butonlar
            btn_frame = ttk.Frame(self.frame)
            btn_frame.pack(pady=30)
            
            btn_new = ttk.Button(btn_frame, text="Yeni Firma Ekle", command=self.add_firm)
            btn_new.pack(side=tk.LEFT, padx=10)
            
            btn_test = ttk.Button(btn_frame, text="Test", command=self.test_function)
            btn_test.pack(side=tk.LEFT, padx=10)
            
            btn_exit = ttk.Button(btn_frame, text="Çıkış", command=self.app.root.destroy)
            btn_exit.pack(side=tk.LEFT, padx=10)
        except Exception as e:
            messagebox.showerror("Hata", f"Arayüz oluşturulamadı: {str(e)}")
    
    def add_firm(self):
        messagebox.showinfo("Bilgi", "Yeni firma ekleme işlevi aktif değil")
    
    def test_function(self):
        messagebox.showinfo("Test", "Uygulama çalışıyor!\nTürkçe karakter testi: ğüşiöçĞÜŞİÖÇ")


