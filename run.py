import sys
import os

# Proje ana dizinini Python'Ä±n arama yoluna ekle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# app.py dosyasÄ±nÄ± ana menÃ¼ olarak Ã§alÄ±ÅŸtÄ±r
from app import AnaMenu

if __name__ == "__main__":
    app = AnaMenu()
    app.mainloop()
