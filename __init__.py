# -*- coding: utf-8 -*-
import sys
import locale
# TÃƒÆ’Ã†â€™Ãƒâ€š¼rkÃƒÆ’Ã†â€™Ãƒâ€š§e locale ayarları
try:
    locale.setlocale(locale.LC_ALL, 'turkish')
except BaseException:
    pass
    # UTF-8 kodlama ayarı
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
# App.py'da __init__ içine ekleyin
self.root.iconbitmap("static/icon.ico")  # Kendi simge dosyanızı kullanın

