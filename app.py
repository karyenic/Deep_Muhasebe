import tkinter as tk
from tkinter import font, messagebox
from gui.main_menu import MainMenuWindow
import logging
import os

# Loglama ayarları
logging.basicConfig(
    filename='app_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Deep Muhasebe")
        self.root.geometry("1024x768")
        
        try:
            # Font ayarı (Türkçe karakter desteği)
            default_font = font.nametofont("TkDefaultFont")
            default_font.configure(family="Arial", size=10)
            self.root.option_add("*Font", default_font)
            
            # Ana menüyü aç
            self.main_menu = MainMenuWindow(self)
            logging.info("Uygulama başarıyla başlatıldı")
        except Exception as e:
            logging.error(f"Başlatma hatası: {str(e)}")
            messagebox.showerror("Kritik Hata", f"Uygulama başlatılamadı: {str(e)}")
            self.root.destroy()

        self.root.mainloop()

if __name__ == "__main__":
    # Çalışma dizinini ayarla (GUI resimleri için)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app = MainApp()
