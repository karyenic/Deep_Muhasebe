import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from datetime import datetime
import locale

# Proje ana dizinini Python'Ä±n arama yoluna ekle
ana_dizin = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ana_dizin)

from core.database import SessionLocal, create_all_tables
from core.models.fatura import Fatura, FaturaKalem
from core.models.cari_hesap import CariHesap

# VeritabanÄ± tablolarÄ±nÄ± oluÅŸtur
create_tables()

# Yerel ayarlarÄ± TÃ¼rkÃ§e'ye ayarla
try:
    locale.setlocale(locale.LC_TIME, 'tr_TR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'turkish')
    except locale.Error:
        pass

class FaturaIrsaliyeYonetimi(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Fatura & Ä°rsaliye YÃ¶netimi")
        self.geometry("1000x700")
        self.db_session = SessionLocal()
        
        self.create_widgets()
        self.load_cari_hesaplar()
        self.protocol("WM_DELETE_WINDOW", self.on_kapat)

    def on_kapat(self):
        self.db_session.close()
        self.destroy()

    def create_widgets(self):
        # Fatura BaÅŸlÄ±k BÃ¶lÃ¼mÃ¼
        header_frame = ttk.LabelFrame(self, text="Belge Bilgileri")
        header_frame.pack(padx=10, pady=5, fill="x")

        ttk.Label(header_frame, text="Belge Tipi:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.belge_tipi_combobox = ttk.Combobox(header_frame, values=["Fatura", "Ä°rsaliye"], state="readonly")
        self.belge_tipi_combobox.set("Fatura")
        self.belge_tipi_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(header_frame, text="Belge No:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.belge_no_entry = ttk.Entry(header_frame)
        self.belge_no_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        
        ttk.Label(header_frame, text="Tarih:").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.tarih_entry = ttk.Entry(header_frame)
        self.tarih_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.tarih_entry.grid(row=0, column=5, padx=5, pady=5, sticky="ew")
        
        ttk.Label(header_frame, text="Cari Hesap:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.cari_hesap_combobox = ttk.Combobox(header_frame, state="readonly")
        self.cari_hesap_combobox.grid(row=1, column=1, columnspan=5, padx=5, pady=5, sticky="ew")

        ttk.Button(header_frame, text="SipariÅŸten Aktar", command=self.siparis_aktar).grid(row=2, column=5, padx=5, pady=5, sticky="e")
        
        # Kalemler BÃ¶lÃ¼mÃ¼
        kalem_frame = ttk.LabelFrame(self, text="Kalemler")
        kalem_frame.pack(padx=10, pady=5, fill="both", expand=True)

        columns = ("urun_adi", "miktar", "birim_fiyat", "kdv_orani", "tutar")
        self.kalem_tree = ttk.Treeview(kalem_frame, columns=columns, show="headings")
        self.kalem_tree.heading("urun_adi", text="ÃœrÃ¼n AdÄ±")
        self.kalem_tree.heading("miktar", text="Miktar")
        self.kalem_tree.heading("birim_fiyat", text="Birim Fiyat")
        self.kalem_tree.heading("kdv_orani", text="KDV OranÄ± (%)")
        self.kalem_tree.heading("tutar", text="Toplam Tutar")
        self.kalem_tree.pack(fill="both", expand=True)
        
        kalem_buttons_frame = ttk.Frame(kalem_frame)
        kalem_buttons_frame.pack(fill="x")
        ttk.Button(kalem_buttons_frame, text="SatÄ±r Ekle", command=self.add_kalem_row).pack(side="left", padx=5, pady=5)
        ttk.Button(kalem_buttons_frame, text="SatÄ±r Sil", command=self.remove_kalem_row).pack(side="left", padx=5, pady=5)
        
        # Toplamlar BÃ¶lÃ¼mÃ¼
        summary_frame = ttk.Frame(self)
        summary_frame.pack(padx=10, pady=5, fill="x")
        self.toplam_etiket = ttk.Label(summary_frame, text="Genel Toplam: 0.00 TL", font=("Helvetica", 12, "bold"))
        self.toplam_etiket.pack(side="right")
        
        # Ä°ÅŸlem ButonlarÄ± BÃ¶lÃ¼mÃ¼
        action_frame = ttk.Frame(self)
        action_frame.pack(padx=10, pady=10, fill="x")
        ttk.Button(action_frame, text="Kaydet", command=self.belge_kaydet).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Temizle", command=self.temizle_form).pack(side="right", padx=5)

    def load_cari_hesaplar(self):
        cari_hesaplar = self.db_session.query(CariHesap).all()
        self.cari_hesaplar_map = {hesap.cari_adi: hesap.id for hesap in cari_hesaplar}
        self.cari_hesap_combobox['values'] = list(self.cari_hesaplar_map.keys())

    def add_kalem_row(self):
        self.kalem_tree.insert("", "end", values=("", "", "", 18.0, 0.0))

    def remove_kalem_row(self):
        selected_item = self.kalem_tree.selection()
        if selected_item:
            self.kalem_tree.delete(selected_item)

    def siparis_aktar(self):
        # SipariÅŸten kalemleri aktarma mantÄ±ÄŸÄ± burada geliÅŸtirilecek
        messagebox.showinfo("Bilgi", "SipariÅŸten kalem aktarma fonksiyonu henÃ¼z geliÅŸtirilmedi.")

    def belge_kaydet(self):
        belge_no = self.belge_no_entry.get()
        tarih_str = self.tarih_entry.get()
        cari_adi = self.cari_hesap_combobox.get()
        belge_tipi = self.belge_tipi_combobox.get()
        is_irsaliye = (belge_tipi == "Ä°rsaliye")

        if not belge_no or not tarih_str or not cari_adi:
            messagebox.showerror("Hata", "Belge No, Tarih ve Cari Hesap boÅŸ bÄ±rakÄ±lamaz!")
            return

        try:
            tarih = datetime.strptime(tarih_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Hata", "GeÃ§ersiz tarih formatÄ±! (YYYY-MM-DD)")
            return

        cari_hesap_id = self.cari_hesaplar_map.get(cari_adi)
        if cari_hesap_id is None:
            messagebox.showerror("Hata", "GeÃ§ersiz Cari Hesap!")
            return
            
        yeni_belge = Fatura(
            fatura_no=belge_no,
            tarih=tarih,
            cari_hesap_id=cari_hesap_id,
            is_irsaliye=is_irsaliye
        )

        try:
            self.db_session.add(yeni_belge)
            self.db_session.commit()
            
            belge_id = yeni_belge.id
            for item in self.kalem_tree.get_children():
                values = self.kalem_tree.item(item, "values")
                if all(values):
                    kalem = FaturaKalem(
                        fatura_id=belge_id,
                        urun_adi=values[0],
                        miktar=float(values[1]),
                        birim_fiyat=float(values[2]),
                        kdv_orani=float(values[3])
                    )
                    self.db_session.add(kalem)
            
            self.db_session.commit()
            messagebox.showinfo("BaÅŸarÄ±lÄ±", f"'{belge_no}' numaralÄ± {belge_tipi} baÅŸarÄ±yla kaydedildi.")
            self.temizle_form()
            
        except Exception as e:
            self.db_session.rollback()
            messagebox.showerror("Hata", f"Belge kaydedilirken bir hata oluÅŸtu: {e}")

    def temizle_form(self):
        self.belge_no_entry.delete(0, tk.END)
        self.tarih_entry.delete(0, tk.END)
        self.tarih_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.cari_hesap_combobox.set('')
        for item in self.kalem_tree.get_children():
            self.kalem_tree.delete(item)
        self.toplam_etiket.config(text="Genel Toplam: 0.00 TL")
        self.belge_tipi_combobox.set("Fatura")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    fatura_ekrani = FaturaIrsaliyeYonetimi(root)
    fatura_ekrani.mainloop()
