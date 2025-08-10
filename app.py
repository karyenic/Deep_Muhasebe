import tkinter as tk
from tkinter import ttk, messagebox

# GUI modÃ¼llerini iÃ§e aktar
from gui.cari_hesap import CariHesapYonetimi
from gui.fatura_irsaliye import FaturaIrsaliyeYonetimi
from gui.kullanici import KullaniciYonetimi
from gui.siparis_yonetimi import SiparisYonetimi

class AnaMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Deep Muhasebe - Ana MenÃ¼")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)

        header_label = ttk.Label(main_frame, text="Deep Muhasebe YÃ¶netim Paneli", font=("Helvetica", 16, "bold"))
        header_label.pack(pady=20)

        # ModÃ¼l butonlarÄ± iÃ§in bir Ã§erÃ§eve oluÅŸtur
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        # Cari Hesap YÃ¶netimi butonu
        ttk.Button(button_frame, text="Cari Hesap YÃ¶netimi", command=self.open_cari_hesap).pack(fill="x", pady=5)
        
        # SipariÅŸ YÃ¶netimi butonu
        ttk.Button(button_frame, text="SipariÅŸ YÃ¶netimi", command=self.open_siparis_yonetimi).pack(fill="x", pady=5)

        # Fatura & Ä°rsaliye YÃ¶netimi butonu
        ttk.Button(button_frame, text="Fatura & Ä°rsaliye YÃ¶netimi", command=self.open_fatura_irsaliye).pack(fill="x", pady=5)

        # KullanÄ±cÄ± YÃ¶netimi butonu
        ttk.Button(button_frame, text="KullanÄ±cÄ± YÃ¶netimi", command=self.open_kullanici_yonetimi).pack(fill="x", pady=5)

    def open_cari_hesap(self):
        CariHesapYonetimi(self)

    def open_siparis_yonetimi(self):
        SiparisYonetimi(self)

    def open_fatura_irsaliye(self):
        FaturaIrsaliyeYonetimi(self)

    def open_kullanici_yonetimi(self):
        KullaniciYonetimi(self)

if __name__ == "__main__":
    app = AnaMenu()
    app.mainloop()
