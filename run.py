import sys
import os

# Proje ana dizinini Python'ın arama yoluna ekle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# app.py dosyasını ana menü olarak çalıştır
from app import AnaMenu

if __name__ == "__main__":
    app = AnaMenu()
    app.mainloop()
