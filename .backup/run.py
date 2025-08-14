import sys
import os

# Projenin ana dizinini Python'ın arama yoluna ekle
ana_dizin = os.path.dirname(os.path.abspath(__file__))
if ana_dizin not in sys.path:
    sys.path.append(ana_dizin)

# main_app.py dosyasından ana menüyü içe aktar
from main_app import AnaMenu

if __name__ == "__main__":
    app = AnaMenu()
    app.mainloop()
