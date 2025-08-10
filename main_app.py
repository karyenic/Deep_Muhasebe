import tkinter as tk
from tkinter import ttk, messagebox

# GUI modüllerini doğrudan içe aktar
import gui.cari_hesap
import gui.fatura_irsaliye
import gui.kullanici
import gui.siparis_yonetimi

class AnaMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Deep Muhasebe - Ana Menü")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)

        header_label = ttk.Label(main_frame, text="Deep Muhasebe Yönetim Paneli", font=("Helvetica", 16, "bold"))
        header_label.pack(pady=20)

        # Modül butonları için bir çerçeve oluştur
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        # Cari Hesap Yönetimi butonu
        ttk.Button(button_frame, text="Cari Hesap Yönetimi", command=self.open_cari_hesap).pack(fill="x", pady=5)
        
        # Sipariş Yönetimi butonu
        ttk.Button(button_frame, text="Sipariş Yönetimi", command=self.open_siparis_yonetimi).pack(fill="x", pady=5)

        # Fatura & İrsaliye Yönetimi butonu
        ttk.Button(button_frame, text="Fatura & İrsaliye Yönetimi", command=self.open_fatura_irsaliye).pack(fill="x", pady=5)

        # Kullanıcı Yönetimi butonu
        ttk.Button(button_frame, text="Kullanıcı Yönetimi", command=self.open_kullanici_yonetimi).pack(fill="x", pady=5)

    def open_cari_hesap(self):
        gui.cari_hesap.CariHesapYonetimi(self)

    def open_siparis_yonetimi(self):
        gui.siparis_yonetimi.SiparisYonetimi(self)

    def open_fatura_irsaliye(self):
        gui.fatura_irsaliye.FaturaIrsaliyeYonetimi(self)

    def open_kullanici_yonetimi(self):
        gui.kullanici.KullaniciYonetimi(self)

if __name__ == "__main__":
    app = AnaMenu()
    app.mainloop()
