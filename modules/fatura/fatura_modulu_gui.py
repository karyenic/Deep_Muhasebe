# -*- coding: utf-8 -*-
# fatura_modulu_gui.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime
# Sabit dosya yollarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±
CARI_HESAPLAR_DOSYASI = "cari_hesaplar.json"
STOK_URUNLER_DOSYASI = "stok_urunler.json"
FATURALAR_DOSYASI = "faturalar.json"
STOK_HAREKETLERI_DOSYASI = "stok_hareketleri.json"  # Yeni eklendi
class FaturaModuluGUI:
def __init__(
self, master):
self.master = master
master.title(
"Fatura ModÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼lÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼")
master.geometry(
"1200x800")
# Veri
# yÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼kleme
# (Uygulama
# baÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±nda
# bir
# kez
# yÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼klenir)
self.cari_hesaplar = self._load_json_data(
CARI_HESAPLAR_DOSYASI)
self.stok_urunleri = self._load_json_data(
STOK_URUNLER_DOSYASI)
self.faturalar = self._load_json_data(
FATURALAR_DOSYASI)
# GeÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§erli
# faturadaki
# kalemleri
# tutar
# {urun_kodu:
# {miktar,
# birim_fiyat,
# kdv_orani}}
self.current_fatura_items = {}
self._configure_styles()
self.create_widgets()
# Uygulama
# baÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸latÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±ldÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±nda
# combobox'larÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±
# doldur
# ve
# yeni
# fatura
# bilgilerini
# yÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼kle
self._load_fatura_bilgileri()
self._populate_cari_hesap_combobox()
self._populate_urun_combobox()  # ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢İ¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼n combobox'ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±nÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± da baÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸langÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§ta doldur
# Sekme
# deÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸iÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸imi
# olayÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±nÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±
# baÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸la
self.notebook.bind(
"<<NotebookTabChanged>>", self._on_tab_change)
def _configure_styles(self):
style = ttk.Style()
# default_font_size ve diÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸er font boyutlarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± burada tanÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±mlanmalÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±
default_font_size = 12
header_font_size = 14
header_label_color = "#1F4E79" # Koyu Mavi
value_label_color = "#333333" # Koyu Gri
style.configure(".", font=("Arial", default_font_size))
style.configure("TLabel", font=("Arial", default_font_size))
style.configure("Header.TLabel", font=("Arial", default_font_size, "bold"), foreground=header_label_color)
style.configure("TEntry", font=("Arial", default_font_size))
style.configure("TCombobox", font=("Arial", default_font_size)) # Combobox fontu iÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§in
style.configure("TButton", font=("Arial", default_font_size), padding=8)
style.configure("TNotebook.Tab", font=("Arial", default_font_size + 1, "bold"))
style.configure("TLabelframe.Label", font=("Arial", header_font_size, "bold"), foreground=header_label_color)
style.configure("Treeview.Heading", font=("Arial", default_font_size + 1, "bold"), foreground=header_label_color)
style.configure("Treeview", font=("Arial", default_font_size))
style.map("Treeview", background=[('selected', '#B0D0E0')]) # SeÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§ili satÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±r rengi
def _load_json_data(self, filename):
if os.path.exists(filename):
try:
with open(filename, 'r', encoding='utf-8') as f:
data = json.load(f)
# BoÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸ liste yerine boÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸ sÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¶zlÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼k dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¶ndÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼rmeli, ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼nkÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼ veriler genelde sÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¶zlÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼k olarak saklanÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±r
if isinstance(data, list):
return {}
return data
except json.JSONDecodeError:
messagebox.showerror("Hata", f"{filename} dosyasÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± bozuk veya geÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§ersiz JSON formatÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±nda. Dosya sÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±fÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±rlanacaktÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±r.")
# Dosya bozuksa boÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸ bir sÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¶zlÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼k oluÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸turup geri dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¶ndÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼r
with open(filename, 'w', encoding='utf-8') as f:
json.dump({}, f)
return {}
return {} # Dosya yoksa boÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸ bir sÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¶zlÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼k dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¶ndÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼r
def _save_json_data(self, data, filename):
try:
with open(filename, 'w', encoding='utf-8') as f:
json.dump(data, f, indent=4, ensure_ascii=False)
except Exception as e:
messagebox.showerror("Kaydetme HatasÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±", f"{filename} kaydedilirken bir hata oluÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸tu: {e}")
def create_widgets(self):
self.notebook = ttk.Notebook(self.master)
self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
self.create_fatura_olustur_sekmesi()
self.create_faturalari_listele_sekmesi()
self.create_raporlar_sekmesi() # HenÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼z geliÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸tirilmedi
def create_fatura_olustur_sekmesi(self):
self.fatura_olustur_frame = ttk.Frame(self.notebook, padding="15 15 15 15")
self.notebook.add(self.fatura_olustur_frame, text="Fatura OluÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸tur")
# Fatura Bilgileri Frame
fatura_bilgileri_frame = ttk.LabelFrame(self.fatura_olustur_frame, text="Fatura Bilgileri", padding="15")
fatura_bilgileri_frame.pack(fill=tk.X, pady=10)
fatura_bilgileri_frame.grid_columnconfigure(1, weight=1)
fatura_bilgileri_frame.grid_columnconfigure(3, weight=1)
ttk.Label(fatura_bilgileri_frame, text="Firma SeÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§:", style="Header.TLabel").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
# state="readonly" combobox'ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±n sadece listeden seÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§im yapÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±lmasÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±na izin verir, manuel giriÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸i engeller.
# EÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸er manuel giriÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸ de isteniyorsa, state kaldÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±rÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±labilir veya "normal" yapÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±labilir.
self.firma_sec_combobox = ttk.Combobox(fatura_bilgileri_frame, state="readonly", width=27)
self.firma_sec_combobox.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)
self.firma_sec_combobox.bind("<<ComboboxSelected>>", self._on_firma_select)
ttk.Label(fatura_bilgileri_frame, text="Firma UnvanÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±:", style="Header.TLabel").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
self.firma_unvan_label = ttk.Label(fatura_bilgileri_frame, text="", foreground="#333333")
self.firma_unvan_label.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
ttk.Label(fatura_bilgileri_frame, text="Fatura No:", style="Header.TLabel").grid(row=0, column=2, sticky=tk.W, pady=5, padx=5)
self.fatura_no_label = ttk.Label(fatura_bilgileri_frame, text="", foreground="#333333")
self.fatura_no_label.grid(row=0, column=3, sticky=tk.W, pady=5, padx=5)
ttk.Label(fatura_bilgileri_frame, text="Fatura Tarihi:", style="Header.TLabel").grid(row=1, column=2, sticky=tk.W, pady=5, padx=5)
self.fatura_tarihi_label = ttk.Label(fatura_bilgileri_frame, text=datetime.now().strftime("%Y-%m-%d"), foreground="#333333")
self.fatura_tarihi_label.grid(row=1, column=3, sticky=tk.W, pady=5, padx=5)
# Fatura Kalemi Ekle Frame
fatura_kalemi_ekle_frame = ttk.LabelFrame(self.fatura_olustur_frame, text="Fatura Kalemi Ekle", padding="15")
fatura_kalemi_ekle_frame.pack(fill=tk.X, pady=10)
fatura_kalemi_ekle_frame.grid_columnconfigure(1, weight=1)
fatura_kalemi_ekle_frame.grid_columnconfigure(3, weight=1)
ttk.Label(fatura_kalemi_ekle_frame, text="ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢İ¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼n Kodu:", style="Header.TLabel").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
self.urun_kodu_combobox = ttk.Combobox(fatura_kalemi_ekle_frame, state="readonly", width=27)
self.urun_kodu_combobox.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)
self.urun_kodu_combobox.bind("<<ComboboxSelected>>", self._on_urun_select)
ttk.Label(fatura_kalemi_ekle_frame, text="ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢İ¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼n AdÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±:", style="Header.TLabel").grid(row=0, column=2, sticky=tk.W, pady=5, padx=5)
self.urun_adi_label = ttk.Label(fatura_kalemi_ekle_frame, text="", foreground="#333333")
self.urun_adi_label.grid(row=0, column=3, sticky=tk.W, pady=5, padx=5)
ttk.Label(fatura_kalemi_ekle_frame, text="Miktar:", style="Header.TLabel").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
self.miktar_entry = ttk.Entry(fatura_kalemi_ekle_frame, width=30, foreground="#333333")
self.miktar_entry.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=5)
ttk.Label(fatura_kalemi_ekle_frame, text="Birim Fiyat:", style="Header.TLabel").grid(row=1, column=2, sticky=tk.W, pady=5, padx=5)
self.birim_fiyat_label = ttk.Label(fatura_kalemi_ekle_frame, text="0.00", foreground="#333333")
self.birim_fiyat_label.grid(row=1, column=3, sticky=tk.W, pady=5, padx=5)
ttk.Button(fatura_kalemi_ekle_frame, text="Kalemi Ekle", command=self._add_fatura_kalemi).grid(row=2, column=0, columnspan=4, pady=10)
# Fatura Kalemleri Treeview
fatura_kalemleri_frame = ttk.LabelFrame(self.fatura_olustur_frame, text="Fatura Kalemleri", padding="15")
fatura_kalemleri_frame.pack(fill=tk.BOTH, expand=True, pady=10)
kalem_columns = ("ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢İ¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼n Kodu", "ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢İ¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼n AdÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±", "Miktar", "Birim Fiyat", "KDV OranÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± (%)", "Toplam Tutar")
self.fatura_kalemleri_tree = ttk.Treeview(fatura_kalemleri_frame, columns=kalem_columns, show="headings")
self.fatura_kalemleri_tree.pack(fill=tk.BOTH, expand=True)
for col in kalem_columns:
self.fatura_kalemleri_tree.heading(col, text=col, anchor=tk.W)
self.fatura_kalemleri_tree.column(col, width=100, stretch=tk.YES)
self.fatura_kalemleri_tree.column("Miktar", width=70, stretch=tk.NO)
self.fatura_kalemleri_tree.column("Birim Fiyat", width=90, stretch=tk.NO)
self.fatura_kalemleri_tree.column("KDV OranÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± (%)", width=90, stretch=tk.NO)
self.fatura_kalemleri_tree.column("Toplam Tutar", width=100, stretch=tk.NO)
kalem_scrollbar = ttk.Scrollbar(fatura_kalemleri_frame, orient="vertical", command=self.fatura_kalemleri_tree.yview)
self.fatura_kalemleri_tree.configure(yscrollcommand=kalem_scrollbar.set)
kalem_scrollbar.pack(side="right", fill="y")
# Fatura ToplamlarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± Frame
fatura_toplamlari_frame = ttk.LabelFrame(self.fatura_olustur_frame, text="Fatura ToplamlarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±", padding="15")
fatura_toplamlari_frame.pack(fill=tk.X, pady=10)
fatura_toplamlari_frame.grid_columnconfigure(1, weight=1)
fatura_toplamlari_frame.grid_columnconfigure(3, weight=1)
ttk.Label(fatura_toplamlari_frame, text="Toplam Tutar (KDV HariÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§):", style="Header.TLabel").grid(row=0, column=0, sticky=tk.W, pady=2, padx=5)
self.toplam_tutar_label = ttk.Label(fatura_toplamlari_frame, text="0.00", foreground="#333333", font=("Arial", default_font_size, "bold"))
self.toplam_tutar_label.grid(row=0, column=1, sticky=tk.W, pady=2, padx=5)
ttk.Label(fatura_toplamlari_frame, text="Ambalaj/Nakliye MasrafÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±:", style="Header.TLabel").grid(row=1, column=0, sticky=tk.W, pady=2, padx=5)
self.nakliye_masraf_entry = ttk.Entry(fatura_toplamlari_frame, width=10, foreground="#333333")
self.nakliye_masraf_entry.grid(row=1, column=1, sticky=tk.W, pady=2, padx=5)
self.nakliye_masraf_entry.insert(0, "0.00")
# TypeError'ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¶nlemek iÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§in lambda e: kullanÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±ldÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±
self.nakliye_masraf_entry.bind("<FocusOut>", lambda e: self._calculate_totals())
self.nakliye_masraf_entry.bind("<Return>", lambda e: self._calculate_totals())
ttk.Label(fatura_toplamlari_frame, text="ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š°skonto OranÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± (%):", style="Header.TLabel").grid(row=2, column=0, sticky=tk.W, pady=2, padx=5)
self.iskonto_oran_entry = ttk.Entry(fatura_toplamlari_frame, width=10, foreground="#333333")
self.iskonto_oran_entry.grid(row=2, column=1, sticky=tk.W, pady=2, padx=5)
self.iskonto_oran_entry.insert(0, "0")
# TypeError'ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¶nlemek iÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§in lambda e: kullanÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±ldÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±
self.iskonto_oran_entry.bind("<FocusOut>", lambda e: self._calculate_totals())
self.iskonto_oran_entry.bind("<Return>", lambda e: self._calculate_totals())
ttk.Label(fatura_toplamlari_frame, text="ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š°skonto TutarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±:", style="Header.TLabel").grid(row=3, column=0, sticky=tk.W, pady=2, padx=5)
self.iskonto_tutar_label = ttk.Label(fatura_toplamlari_frame, text="0.00", foreground="#333333", font=("Arial", default_font_size, "bold"))
self.iskonto_tutar_label.grid(row=3, column=1, sticky=tk.W, pady=2, padx=5)
ttk.Label(fatura_toplamlari_frame, text="KDV OranÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± (%):", style="Header.TLabel").grid(row=0, column=2, sticky=tk.W, pady=2, padx=5)
self.kdv_oran_label = ttk.Label(fatura_toplamlari_frame, text="0", foreground="#333333") # KDV OranÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±nÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± gÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¶stermek iÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§in
self.kdv_oran_label.grid(row=0, column=3, sticky=tk.W, pady=2, padx=5)
ttk.Label(fatura_toplamlari_frame, text="KDV TutarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±:", style="Header.TLabel").grid(row=1, column=2, sticky=tk.W, pady=2, padx=5)
self.kdv_tutar_label = ttk.Label(fatura_toplamlari_frame, text="0.00", foreground="#333333", font=("Arial", default_font_size, "bold"))
self.kdv_tutar_label.grid(row=1, column=3, sticky=tk.W, pady=2, padx=5)
ttk.Label(fatura_toplamlari_frame, text="GENEL TOPLAM:", style="Header.TLabel", font=("Arial", default_font_size + 2, "bold"), foreground="#005B96").grid(row=4, column=2, sticky=tk.W, pady=10, padx=5)
self.genel_toplam_label = ttk.Label(fatura_toplamlari_frame, text="0.00", foreground="#005B96", font=("Arial", default_font_size + 2, "bold"))
self.genel_toplam_label.grid(row=4, column=3, sticky=tk.W, pady=10, padx=5)
# Butonlar
button_frame = ttk.Frame(self.fatura_olustur_frame)
button_frame.pack(pady=10)
ttk.Button(button_frame, text="Yeni Fatura", command=self._clear_fatura_form).pack(side=tk.LEFT, padx=5)
ttk.Button(button_frame, text="FaturayÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± Kaydet", command=self._save_fatura).pack(side=tk.LEFT, padx=5)
ttk.Button(button_frame, text="SeÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§ili Kalemi Sil", command=self._delete_fatura_kalemi).pack(side=tk.LEFT, padx=5)
def create_faturalari_listele_sekmesi(self):
self.listele_frame = ttk.Frame(self.notebook, padding="15 15 15 15")
self.notebook.add(self.listele_frame, text="FaturalarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± Listele")
list_columns = ("Fatura No", "Tarih", "Firma Kodu", "Firma UnvanÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±", "Toplam Tutar (KDV Dahil)")
self.faturalar_tree = ttk.Treeview(self.listele_frame, columns=list_columns, show="headings")
self.faturalar_tree.pack(fill=tk.BOTH, expand=True)
for col in list_columns:
self.faturalar_tree.heading(col, text=col, anchor=tk.W)
self.faturalar_tree.column(col, width=100, stretch=tk.YES)
self.faturalar_tree.column("Fatura No", width=80, stretch=tk.NO)
self.faturalar_tree.column("Tarih", width=100, stretch=tk.NO)
self.faturalar_tree.column("Firma Kodu", width=90, stretch=tk.NO)
self.faturalar_tree.column("Toplam Tutar (KDV Dahil)", width=150, stretch=tk.NO)
list_scrollbar = ttk.Scrollbar(self.listele_frame, orient="vertical", command=self.faturalar_tree.yview)
self.faturalar_tree.configure(yscrollcommand=list_scrollbar.set)
list_scrollbar.pack(side="right", fill="y")
self.faturalar_tree.bind("<<TreeviewSelect>>", self._on_fatura_select_for_detail)
button_frame = ttk.Frame(self.listele_frame)
button_frame.pack(pady=10)
ttk.Button(button_frame, text="Listeyi Yenile", command=self._list_faturalar).pack(side=tk.LEFT, padx=5)
ttk.Button(button_frame, text="FaturayÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± Sil", command=self._delete_fatura).pack(side=tk.LEFT, padx=5)
ttk.Button(button_frame, text="DetaylarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± GÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¶rÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼ntÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼le", command=self._show_fatura_detail).pack(side=tk.LEFT, padx=5)
def create_raporlar_sekmesi(self):
self.raporlar_frame = ttk.Frame(self.notebook, padding="15 15 15 15")
self.notebook.add(self.raporlar_frame, text="Raporlar")
ttk.Label(self.raporlar_frame, text="Fatura raporlarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± burada gÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¶rÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼ntÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼lenecektir. (HenÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼z geliÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸tirilmedi)", style="Header.TLabel").pack(pady=50)
def _load_fatura_bilgileri(self):
self.faturalar = self._load_json_data(FATURALAR_DOSYASI)
next_fatura_no = 1
if self.faturalar:
max_fatura_no = 0
# Fatura ID'si "Fatura No" olarak kullanÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±lÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±yorsa
for fatura_id, fatura_data in self.faturalar.items():
try:
fatura_no_int = int(fatura_data.get("Fatura No", fatura_id)) # Hem Fatura No'yu hem de ID'yi kontrol et
max_fatura_no = max(max_fatura_no, fatura_no_int)
except ValueError:
continue # SayÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±sal olmayan ID'leri atla
next_fatura_no = max_fatura_no + 1
self.fatura_no_label.config(text=str(next_fatura_no))
self.fatura_tarihi_label.config(text=datetime.now().strftime("%Y-%m-%d"))
def _populate_cari_hesap_combobox(self):
# JSON dosyasÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±ndan cari hesaplarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± yeniden yÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼kle
self.cari_hesaplar = self._load_json_data(CARI_HESAPLAR_DOSYASI)
firma_kodlari = sorted(list(self.cari_hesaplar.keys()))
self.firma_sec_combobox['values'] = firma_kodlari
# EÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸er liste boÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸ deÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸ilse ilkini seÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§, deÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸ilse boÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸ bÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±rak
if firma_kodlari:
self.firma_sec_combobox.set(firma_kodlari[0])
self._on_firma_select(None) # ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š°lk firmayÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± otomatik seÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§ ve bilgilerini doldur
else:
self.firma_sec_combobox.set("")
self.firma_unvan_label.config(text="")
# Bu metod ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§aÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸rÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±ldÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±nda, aynÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± zamanda ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼rÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼n combobox'ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± da gÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼ncellenmeli
# Ancak _populate_urun_combobox zaten __init__ iÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§inde de ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§aÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸rÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±ldÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± iÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§in burada tekrar ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§aÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±rmaya gerek yok
# veya sadece veri deÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸iÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸tiÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸inde ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§aÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸rÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±labilir. ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¾imdilik bu kÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±smÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± yoruma alÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±yorum.
# self._populate_urun_combobox()
def _on_firma_select(self, event):
selected_firma_kodu = self.firma_sec_combobox.get()
if selected_firma_kodu and selected_firma_kodu in self.cari_hesaplar:
firma_unvan = self.cari_hesaplar[selected_firma_kodu].get("Unvan", "")
self.firma_unvan_label.config(text=firma_unvan)
else:
self.firma_unvan_label.config(text="")
def _populate_urun_combobox(self):
# JSON dosyasÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±ndan stok ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼rÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼nlerini yeniden yÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼kle
self.stok_urunleri = self._load_json_data(STOK_URUNLER_DOSYASI)
urun_kodlari = sorted(list(self.stok_urunleri.keys()))
self.urun_kodu_combobox['values'] = urun_kodlari
# EÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸er liste boÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸ deÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸ilse ilkini seÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§, deÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸ilse boÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸ bÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±rak
if urun_kodlari:
self.urun_kodu_combobox.set(urun_kodlari[0])
self._on_urun_select(None) # ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š°lk ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼rÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼nÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼ otomatik seÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§ ve bilgilerini doldur
else:
self.urun_kodu_combobox.set("")
self.urun_adi_label.config(text="")
self.birim_fiyat_label.config(text="0.00")
def _on_urun_select(self, event):
selected_urun_kodu = self.urun_kodu_combobox.get()
if selected_urun_kodu and selected_urun_kodu in self.stok_urunleri:
urun_data = self.stok_urunleri[selected_urun_kodu]
urun_adi = urun_data.get("ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢İ¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼n AdÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±", "")
birim_fiyat = urun_data.get("SatÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸ Birim FiyatÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±", 0.0)
self.urun_adi_label.config(text=urun_adi)
self.birim_fiyat_label.config(text=f"{birim_fiyat:.2f}")
else:
self.urun_adi_label.config(text="")
self.birim_fiyat_label.config(text="0.00")
def _add_fatura_kalemi(self):
urun_kodu = self.urun_kodu_combobox.get()
miktar_str = self.miktar_entry.get().strip()
if not urun_kodu or not miktar_str:
messagebox.showwarning("Eksik Bilgi", "ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢İ¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼n Kodu ve Miktar boÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸ bÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±rakÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±lamaz.")
return
if urun_kodu not in self.stok_urunleri:
messagebox.showerror("Hata", "SeÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§ilen ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼rÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼n stokta bulunamadÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±. LÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼tfen Stok ModÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼lÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼'nden ekleyiniz.")
return
try:
miktar = float(miktar_str.replace(",", "."))
if miktar <= 0:
messagebox.showwarning("GeÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§ersiz Miktar", "Miktar sÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±fÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±rdan bÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼yÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼k olmalÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±dÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±r.")
return
except ValueError:
messagebox.showerror("Hata", "Miktar alanÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±na geÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§erli bir sayÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± giriniz.")
return
urun_data = self.stok_urunleri[urun_kodu]
birim_fiyat = urun_data.get("SatÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸ Birim FiyatÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±", 0.0)
kdv_orani = urun_data.get("KDV OranÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± (%)", 0.0)
# Stok kontrolÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼
mevcut_stok = urun_data.get("Stok MiktarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±", 0.0)
if mevcut_stok < miktar:
response = messagebox.askyesno("Yetersiz Stok", f"'{urun_data.get('ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢İ¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼n AdÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±')}' ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼rÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼nÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼nde yeterli stok ({mevcut_stok:.2f}) bulunmamaktadÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±r. Yetersiz stoÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸a raÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸men eklemek ister misiniz?")
if not response:
return
# EÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸er kalem daha ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¶nce eklendiyse miktarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± gÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼ncelle, yoksa yeni kalem ekle
if urun_kodu in self.current_fatura_items:
self.current_fatura_items[urun_kodu]["Miktar"] += miktar
else:
self.current_fatura_items[urun_kodu] = {
"ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢İ¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼n AdÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±": urun_data.get("ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢İ¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼n AdÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±", ""),
"Miktar": miktar,
"Birim Fiyat": birim_fiyat,
"KDV OranÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± (%)": kdv_orani
}
self._list_fatura_kalemleri()
self._calculate_totals()
self.miktar_entry.delete(0, tk.END) # Miktar alanÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±nÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± temizle
def _list_fatura_kalemleri(self):
for item in self.fatura_kalemleri_tree.get_children():
self.fatura_kalemleri_tree.delete(item)
if not self.current_fatura_items:
self.fatura_kalemleri_tree.insert("", tk.END, values=("", "Faturada kalem bulunmamaktadÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±r.", "", "", "", ""), tags=('empty',))
self.fatura_kalemleri_tree.tag_configure('empty', foreground='blue')
return
for urun_kodu, item_data in self.current_fatura_items.items():
toplam_tutar_kdv_haric = item_data["Miktar"] * item_data["Birim Fiyat"]
self.fatura_kalemleri_tree.insert("", tk.END, values=(
urun_kodu,
item_data["ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢İ¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼n AdÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±"],
f"{item_data['Miktar']:.2f}",
f"{item_data['Birim Fiyat']:.2f}",
f"{item_data['KDV OranÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± (%)']:.0f}",
f"{toplam_tutar_kdv_haric:.2f}"
))
def _delete_fatura_kalemi(self):
selected_item = self.fatura_kalemleri_tree.selection()
if not selected_item:
messagebox.showwarning("UyarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±", "LÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼tfen silmek istediÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸iniz fatura kalemini seÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§in.")
return
if self.fatura_kalemleri_tree.item(selected_item[0], 'tags') == ('empty',):
return
urun_kodu_to_delete = self.fatura_kalemleri_tree.item(selected_item, 'values')[0]
response = messagebox.askyesno("Onay", f"'{urun_kodu_to_delete}' ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼rÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼nÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼nÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼ fatura kalemlerinden silmek istediÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸inizden emin misiniz?")
if response:
if urun_kodu_to_delete in self.current_fatura_items:
del self.current_fatura_items[urun_kodu_to_delete]
self._list_fatura_kalemleri()
self._calculate_totals()
else:
messagebox.showerror("Hata", "Silinecek fatura kalemi bulunamadÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±.")
def _calculate_totals(self):
total_kdv_haric = 0.0
# Faturadaki en yÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼ksek KDV oranÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±nÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± deÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸il, kalemlerin KDV oranlarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±nÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± ayrÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± ayrÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± hesaplamak daha doÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸ru olur.
# Basitlik adÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±na ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸u an iÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§in en yÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼ksek KDV oranÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±nÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± alÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±p genel KDV'yi hesaplayalÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±m.
# GerÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§ek bir uygulamada, her kalemin kendi KDV'si toplanÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±r.
max_kdv_oran = 0.0
total_kdv_dahil_tum_kalemler = 0.0 # KDV dahil toplamÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± da hesaplamak iÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§in
for item_data in self.current_fatura_items.values():
item_total = item_data["Miktar"] * item_data["Birim Fiyat"]
total_kdv_haric += item_total
if item_data["KDV OranÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± (%)"] > max_kdv_oran:
max_kdv_oran = item_data["KDV OranÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± (%)"]
# Her kalemin KDV dahil tutarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±nÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± ayrÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± ayrÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± hesaplayÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±p toplayabiliriz.
# kdv_faktor = (100 + item_data["KDV OranÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± (%)"]) / 100
# total_kdv_dahil_tum_kalemler += item_total * kdv_faktor
self.toplam_tutar_label.config(text=f"{total_kdv_haric:.2f}")
# Masraf ve ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š°skonto hesaplamalarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±
try:
nakliye_masraf = float(self.nakliye_masraf_entry.get().replace(",", "."))
except ValueError:
nakliye_masraf = 0.0
# messagebox.showwarning("GeÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§ersiz GiriÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸", "Nakliye masrafÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± iÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§in geÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§erli bir sayÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± giriniz.") # SÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼rekli uyarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± vermesin
self.nakliye_masraf_entry.delete(0, tk.END)
self.nakliye_masraf_entry.insert(0, "0.00")
try:
iskonto_oran = float(self.iskonto_oran_entry.get().replace(",", "."))
if not (0 <= iskonto_oran <= 100):
messagebox.showwarning("GeÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§ersiz ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š°skonto OranÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±", "ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š°skonto oranÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± 0 ile 100 arasÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±nda olmalÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±dÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±r.")
iskonto_oran = 0.0
self.iskonto_oran_entry.delete(0, tk.END)
self.iskonto_oran_entry.insert(0, "0")
except ValueError:
iskonto_oran = 0.0
# messagebox.showwarning("GeÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§ersiz GiriÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸", "ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š°skonto oranÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± iÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§in geÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§erli bir sayÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± giriniz.") # SÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼rekli uyarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± vermesin
self.iskonto_oran_entry.delete(0, tk.END)
self.iskonto_oran_entry.insert(0, "0")
# ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š°skonto KDV HariÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§ toplam ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼zerinden dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼lÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼r
iskonto_tutar = total_kdv_haric * (iskonto_oran / 100)
self.iskonto_tutar_label.config(text=f"{iskonto_tutar:.2f}")
kdv_matrahi = (total_kdv_haric - iskonto_tutar) + nakliye_masraf
kdv_tutar = kdv_matrahi * (max_kdv_oran / 100) # En yÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼ksek KDV oranÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼zerinden hesaplama
self.kdv_oran_label.config(text=f"{max_kdv_oran:.0f}")
self.kdv_tutar_label.config(text=f"{kdv_tutar:.2f}")
genel_toplam = kdv_matrahi + kdv_tutar
self.genel_toplam_label.config(text=f"{genel_toplam:.2f}")
def _save_fatura(self):
fatura_no = self.fatura_no_label.cget("text")
fatura_tarihi = self.fatura_tarihi_label.cget("text")
firma_kodu = self.firma_sec_combobox.get()
firma_unvan = self.firma_unvan_label.cget("text")
if not firma_kodu:
messagebox.showwarning("Eksik Bilgi", "LÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼tfen bir firma seÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§iniz.")
return
if not self.current_fatura_items:
messagebox.showwarning("Eksik Bilgi", "Faturaya en az bir kalem eklemelisiniz.")
return
# ToplamlarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± son bir kez hesapla
self._calculate_totals()
toplam_tutar_kdv_haric = float(self.toplam_tutar_label.cget("text"))
nakliye_masraf = float(self.nakliye_masraf_entry.get().replace(",", "."))
iskonto_oran = float(self.iskonto_oran_entry.get().replace(",", "."))
iskonto_tutar = float(self.iskonto_tutar_label.cget("text"))
kdv_oran = float(self.kdv_oran_label.cget("text"))
kdv_tutar = float(self.kdv_tutar_label.cget("text"))
genel_toplam = float(self.genel_toplam_label.cget("text"))
fatura_data = {
"Fatura No": fatura_no,
"Tarih": fatura_tarihi,
"Firma Kodu": firma_kodu,
"Firma UnvanÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±": firma_unvan,
"Kalemler": [
{
"ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢İ¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼n Kodu": k,
"ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢İ¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼n AdÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±": v["ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢İ¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼n AdÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±"],
"Miktar": v["Miktar"],
"Birim Fiyat": v["Birim Fiyat"],
"KDV OranÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± (%)": v["KDV OranÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± (%)"],
"Toplam Tutar (KDV HariÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§)": v["Miktar"] * v["Birim Fiyat"]
} for k, v in self.current_fatura_items.items()
],
"Toplam Tutar (KDV HariÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§)": toplam_tutar_kdv_haric,
"Ambalaj/Nakliye MasrafÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±": nakliye_masraf,
"ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š°skonto OranÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± (%)": iskonto_oran,
"ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š°skonto TutarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±": iskonto_tutar,
"KDV OranÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± (%)": kdv_oran,
"KDV TutarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±": kdv_tutar,
"Genel Toplam": genel_toplam
}
# Stoktan dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸me iÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸lemi ve Stok hareketleri kaydetme
self.stok_urunleri = self._load_json_data(STOK_URUNLER_DOSYASI) # GÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼ncel stok durumunu tekrar yÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼kle
stok_hareketleri_to_save = self._load_json_data(STOK_HAREKETLERI_DOSYASI) # Stok hareketlerini yÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼kle
for urun_kodu, item_data in self.current_fatura_items.items():
if urun_kodu in self.stok_urunleri:
if self.stok_urunleri[urun_kodu].get("Stok MiktarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±", 0.0) >= item_data["Miktar"]:
self.stok_urunleri[urun_kodu]["Stok MiktarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±"] -= item_data["Miktar"]
else:
# Yetersiz stok durumunda kullanÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±cÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±ya bilgi verilir, fatura yine de kaydedilebilir.
messagebox.showwarning("Stok UyarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±sÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±", f"Fatura kaydedildi ancak '{urun_kodu}' iÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§in yeterli stok bulunamadÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±ndan ({self.stok_urunleri[urun_kodu].get('Stok MiktarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±', 0.0):.2f}) tÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼m miktar dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼lememiÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸ olabilir. Manuel kontrol gerekebilir.")
self.stok_urunleri[urun_kodu]["Stok MiktarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±"] = 0.0 # StoÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸u sÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±fÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±rla
# Stok hareketini kaydet
# Yeni bir hareket ID'si oluÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸tur (mevcut hareket sayÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±sÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±nÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±n bir fazlasÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±)
next_hareket_id = str(int(max(stok_hareketleri_to_save.keys(), key=int, default="0")) + 1)
hareket_data = {
"Tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
"ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢İ¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼n Kodu": urun_kodu,
"ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢İ¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼n AdÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±": item_data["ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢İ¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼n AdÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±"],
"Hareket Tipi": f"ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’¢ÃƒÂ¢Ã¢â‚¬Å¡¬Ãƒâ€š¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±kÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸ (Fatura No: {fatura_no})",
"Miktar": item_data["Miktar"],
"AÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±klama": f"Fatura No {fatura_no} ile ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼rÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼n satÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±"
}
stok_hareketleri_to_save[next_hareket_id] = hareket_data
else:
messagebox.showwarning("Stok UyarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±sÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±", f"Fatura kaydedildi ancak '{urun_kodu}' stokta bulunamadÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±. Stok hareketi kaydedilemedi. Manuel kontrol gerekebilir.")
self._save_json_data(self.stok_urunleri, STOK_URUNLER_DOSYASI) # GÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼ncellenmiÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸ stoÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸u kaydet
self._save_json_data(stok_hareketleri_to_save, STOK_HAREKETLERI_DOSYASI) # GÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼ncellenmiÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸ stok hareketlerini kaydet
self.faturalar[fatura_no] = fatura_data
self._save_json_data(self.faturalar, FATURALAR_DOSYASI)
messagebox.showinfo("BaÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸arÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±lÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±", f"Fatura No: {fatura_no} baÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸arÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±yla kaydedildi ve stoklar gÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼ncellendi.")
self._clear_fatura_form()
self._list_faturalar() # Faturalar listesi sekmesini gÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼ncelle
def _clear_fatura_form(self):
self.current_fatura_items = {}
self._list_fatura_kalemleri() # Kalemler listesini temizle
self.miktar_entry.delete(0, tk.END)
self.urun_kodu_combobox.set("")
self.urun_adi_label.config(text="")
self.birim_fiyat_label.config(text="0.00")
self.nakliye_masraf_entry.delete(0, tk.END)
self.nakliye_masraf_entry.insert(0, "0.00")
self.iskonto_oran_entry.delete(0, tk.END)
self.iskonto_oran_entry.insert(0, "0")
self.toplam_tutar_label.config(text="0.00")
self.iskonto_tutar_label.config(text="0.00")
self.kdv_oran_label.config(text="0")
self.kdv_tutar_label.config(text="0.00")
self.genel_toplam_label.config(text="0.00")
self._load_fatura_bilgileri() # Yeni fatura numarasÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± yÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼kle
self._populate_cari_hesap_combobox() # Firma combobox'ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±nÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± yenile ve ilkini seÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§
self._populate_urun_combobox() # ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢İ¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼n combobox'ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±nÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± yenile ve ilkini seÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§
def _list_faturalar(self):
for item in self.faturalar_tree.get_children():
self.faturalar_tree.delete(item)
self.faturalar = self._load_json_data(FATURALAR_DOSYASI)
if not self.faturalar:
self.faturalar_tree.insert("", tk.END, values=("", "KayÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±tlÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± fatura bulunmamaktadÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±r.", "", "", ""), tags=('empty',))
self.faturalar_tree.tag_configure('empty', foreground='blue')
return
# Fatura numarasÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±na gÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¶re sÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±ralama
sorted_faturalar = sorted(self.faturalar.items(), key=lambda item: int(item[0]))
for fatura_no, data in sorted_faturalar:
self.faturalar_tree.insert("", tk.END, values=(
data.get("Fatura No", ""),
data.get("Tarih", ""),
data.get("Firma Kodu", ""),
data.get("Firma UnvanÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±", ""),
f"{data.get('Genel Toplam', 0.0):.2f}"
))
def _on_fatura_select_for_detail(self, event):
# Bu fonksiyon sadece seÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§im yapÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±ldÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±nda ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§alÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±r, detayÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± gÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¶rmek iÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§in butona basÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±lmasÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± gerekir.
pass
def _show_fatura_detail(self):
selected_item = self.faturalar_tree.selection()
if not selected_item:
messagebox.showwarning("UyarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±", "LÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼tfen detaylarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±nÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± gÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¶rmek istediÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸iniz faturayÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± seÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§in.")
return
if self.faturalar_tree.item(selected_item[0], 'tags') == ('empty',):
return
fatura_no_to_show = self.faturalar_tree.item(selected_item, 'values')[0]
if fatura_no_to_show in self.faturalar:
fatura_data = self.faturalar[fatura_no_to_show]
detail_window = tk.Toplevel(self.master)
detail_window.title(f"Fatura DetayÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±: Fatura No {fatura_no_to_show}")
detail_window.geometry("800x600")
detail_window.transient(self.master) # Ana pencere ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼zerinde kalmasÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±nÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± saÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸lar
detail_window.grab_set() # Ana pencere etkileÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸imini engeller
detail_frame = ttk.Frame(detail_window, padding="15")
detail_frame.pack(fill=tk.BOTH, expand=True)
# Fatura Bilgileri
ttk.Label(detail_frame, text="Fatura No:", style="Header.TLabel").grid(row=0, column=0, sticky=tk.W, pady=2, padx=5)
ttk.Label(detail_frame, text=fatura_data.get("Fatura No", ""), foreground="#333333").grid(row=0, column=1, sticky=tk.W, pady=2, padx=5)
ttk.Label(detail_frame, text="Fatura Tarihi:", style="Header.TLabel").grid(row=1, column=0, sticky=tk.W, pady=2, padx=5)
ttk.Label(detail_frame, text=fatura_data.get("Tarih", ""), foreground="#333333").grid(row=1, column=1, sticky=tk.W, pady=2, padx=5)
ttk.Label(detail_frame, text="Firma Kodu:", style="Header.TLabel").grid(row=2, column=0, sticky=tk.W, pady=2, padx=5)
ttk.Label(detail_frame, text=fatura_data.get("Firma Kodu", ""), foreground="#333333").grid(row=2, column=1, sticky=tk.W, pady=2, padx=5)
ttk.Label(detail_frame, text="Firma UnvanÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±:", style="Header.TLabel").grid(row=3, column=0, sticky=tk.W, pady=2, padx=5)
ttk.Label(detail_frame, text=fatura_data.get("Firma UnvanÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±", ""), foreground="#333333").grid(row=3, column=1, sticky=tk.W, pady=2, padx=5)
ttk.Label(detail_frame, text="--- Kalemler ---", style="Header.TLabel").grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=10, padx=5)
# Fatura Kalemleri Treeview
kalem_detail_columns = ("ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢İ¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼n Kodu", "ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢İ¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼n AdÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±", "Miktar", "Birim Fiyat", "KDV OranÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± (%)", "Toplam Tutar")
kalem_detail_tree = ttk.Treeview(detail_frame, columns=kalem_detail_columns, show="headings", height=5)
kalem_detail_tree.grid(row=5, column=0, columnspan=4, sticky=tk.NSEW, pady=5)
for col in kalem_detail_columns:
kalem_detail_tree.heading(col, text=col, anchor=tk.W)
kalem_detail_tree.column(col, width=100, stretch=tk.YES)
kalem_detail_tree.column("Miktar", width=70, stretch=tk.NO)
kalem_detail_tree.column("Birim Fiyat", width=90, stretch=tk.NO)
kalem_detail_tree.column("KDV OranÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± (%)", width=90, stretch=tk.NO)
kalem_detail_tree.column("Toplam Tutar", width=100, stretch=tk.NO)
kalem_detail_scrollbar = ttk.Scrollbar(detail_frame, orient="vertical", command=kalem_detail_tree.yview)
kalem_detail_tree.configure(yscrollcommand=kalem_detail_scrollbar.set)
kalem_detail_scrollbar.grid(row=5, column=4, sticky=tk.NS)
for item in fatura_data.get("Kalemler", []):
kalem_detail_tree.insert("", tk.END, values=(
item.get("ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢İ¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼n Kodu", ""),
item.get("ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢İ¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œrÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼n AdÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±", ""),
f"{item.get('Miktar', 0.0):.2f}",
f"{item.get('Birim Fiyat', 0.0):.2f}",
f"{item.get('KDV OranÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± (%)', 0.0):.0f}",
f"{item.get('Toplam Tutar (KDV HariÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§)', 0.0):.2f}"
))
# Fatura ToplamlarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±
ttk.Label(detail_frame, text="--- Toplamlar ---", style="Header.TLabel").grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=10, padx=5)
ttk.Label(detail_frame, text="Toplam Tutar (KDV HariÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§):", style="Header.TLabel").grid(row=7, column=0, sticky=tk.W, pady=2, padx=5)
ttk.Label(detail_frame, text=f"{fatura_data.get('Toplam Tutar (KDV HariÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§)', 0.0):.2f}", foreground="#333333").grid(row=7, column=1, sticky=tk.W, pady=2, padx=5)
ttk.Label(detail_frame, text="Ambalaj/Nakliye MasrafÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±:", style="Header.TLabel").grid(row=8, column=0, sticky=tk.W, pady=2, padx=5)
ttk.Label(detail_frame, text=f"{fatura_data.get('Ambalaj/Nakliye MasrafÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±', 0.0):.2f}", foreground="#333333").grid(row=8, column=1, sticky=tk.W, pady=2, padx=5)
ttk.Label(detail_frame, text="ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š°skonto OranÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± (%):", style="Header.TLabel").grid(row=9, column=0, sticky=tk.W, pady=2, padx=5)
ttk.Label(detail_frame, text=f"{fatura_data.get('ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š°skonto OranÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± (%)', 0.0):.0f}", foreground="#333333").grid(row=9, column=1, sticky=tk.W, pady=2, padx=5)
ttk.Label(detail_frame, text="ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š°skonto TutarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±:", style="Header.TLabel").grid(row=10, column=0, sticky=tk.W, pady=2, padx=5)
ttk.Label(detail_frame, text=f"{fatura_data.get('ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š°skonto TutarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±', 0.0):.2f}", foreground="#333333").grid(row=10, column=1, sticky=tk.W, pady=2, padx=5)
ttk.Label(detail_frame, text="KDV OranÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± (%):", style="Header.TLabel").grid(row=7, column=2, sticky=tk.W, pady=2, padx=5)
ttk.Label(detail_frame, text=f"{fatura_data.get('KDV OranÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± (%)', 0.0):.0f}", foreground="#333333").grid(row=7, column=3, sticky=tk.W, pady=2, padx=5)
ttk.Label(detail_frame, text="KDV TutarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±:", style="Header.TLabel").grid(row=8, column=2, sticky=tk.W, pady=2, padx=5)
ttk.Label(detail_frame, text=f"{fatura_data.get('KDV TutarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±', 0.0):.2f}", foreground="#333333").grid(row=8, column=3, sticky=tk.W, pady=2, padx=5)
ttk.Label(detail_frame, text="GENEL TOPLAM:", style="Header.TLabel", font=("Arial", 14, "bold"), foreground="#005B96").grid(row=11, column=2, sticky=tk.W, pady=10, padx=5)
ttk.Label(detail_frame, text=f"{fatura_data.get('Genel Toplam', 0.0):.2f}", foreground="#005B96", font=("Arial", 14, "bold")).grid(row=11, column=3, sticky=tk.W, pady=10, padx=5)
detail_window.wait_window(detail_window) # Pencere kapanana kadar bekler
else:
messagebox.showerror("Hata", "SeÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§ilen fatura bulunamadÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±.")
def _delete_fatura(self):
selected_item = self.faturalar_tree.selection()
if not selected_item:
messagebox.showwarning("UyarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±", "LÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼tfen silmek istediÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸iniz faturayÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± seÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§in.")
return
if self.faturalar_tree.item(selected_item[0], 'tags') == ('empty',):
return
fatura_no_to_delete = self.faturalar_tree.item(selected_item, 'values')[0]
firma_unvan_to_delete = self.faturalar_tree.item(selected_item, 'values')[3]
response = messagebox.askyesno("Onay", f"Fatura No: {fatura_no_to_delete} ({firma_unvan_to_delete}) silmek istediÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸inizden emin misiniz? Bu iÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸lem geri alÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±namaz ve stoklarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± GERÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š° GETÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š°RMEZ!")
if response:
if fatura_no_to_delete in self.faturalar:
# StoklarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± geri dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¶ndÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼rme (burada sadece uyarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± veriyoruz, manuel dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼zeltme gerekebilir)
# NOT: GerÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§ek bir uygulamada, fatura silindiÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸inde stoklarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±n geri alÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±nmasÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± karmaÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±k bir iÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸tir
# ve iÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸ mantÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±na gÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¶re deÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸iÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸ir (iade mi, iptal mi vb.). Burada basitlik adÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±na yapmÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±yoruz.
messagebox.showinfo("Bilgi", "Fatura siliniyor. Stok dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸leri bu iÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸lemle geri alÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±nmayacaktÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±r. Gerekirse manuel dÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼zeltme yapÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±nÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±z.")
del self.faturalar[fatura_no_to_delete]
self._save_json_data(self.faturalar, FATURALAR_DOSYASI)
messagebox.showinfo("BaÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸arÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±lÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±", "Fatura baÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸arÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±yla silindi.")
self._list_faturalar()
self._load_fatura_bilgileri() # Yeni fatura numarasÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±nÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± gÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼ncelle
else:
messagebox.showerror("Hata", "Silinecek fatura bulunamadÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±.")
def _on_tab_change(self, event):
selected_tab = self.notebook.tab(self.notebook.select(), "text")
if selected_tab == "Fatura OluÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸tur":
self._clear_fatura_form() # Yeni faturaya geÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§iÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸te formu temizle ve combobox'larÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± yenile
elif selected_tab == "FaturalarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± Listele":
self._list_faturalar()
elif selected_tab == "Raporlar":
pass # BurasÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± boÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬¦İ¦Ãƒâ€š¸ kalabilir veya ileride raporlama fonksiyonlarÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š± ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š§aÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾İ¦Ãƒâ€š¸rÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¾ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š±labilir
if __name__ == "__main__":
root = tk.Tk()
app = FaturaModuluGUI(root)
root.mainloop()


