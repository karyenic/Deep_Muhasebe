# -*- coding: utf-8 -*-
from tkinter import ttk, messagebox
import os
import json

try:
    from ortak.paths import SIPARIS_VERI_DOSYASI
except ImportError:
    SIPARIS_VERI_DOSYASI = os.path.join(os.path.dirname(__file__), "siparisler.json")

ORNEK_STOK = {
    "Ürün A": 10,
    "Ürün B": 5,
    "Ürün C": 0,
    "Ürün D": 20
}

class SiparislerModulu(ttk.Frame):
    DURUMLAR = ["Beklemede", "Onaylandı", "İptal"]

    def __init__(self, master=None):
        super().__init__(master)
        self.siparisler = []
        self.create_widgets()
        self.load_siparisler()

    def create_widgets(self):
        filter_frame = tk.Frame(self)
        filter_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(filter_frame, text="Ara (Müşteri / Ürün):").pack(side="left")
        self.filter_var = tk.StringVar()
        self.filter_var.trace_add("write", lambda *args: self.filtrele())
        entry_filter = tk.Entry(filter_frame, textvariable=self.filter_var)
        entry_filter.pack(side="left", padx=5)

        columns = ("siparis_id", "musteri", "urun", "adet", "durum", "stok_durumu")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col, txt in zip(columns, ["Sipariş ID", "Müşteri", "Ürün", "Adet", "Durum", "Stok Durumu"]):
            self.tree.heading(col, text=txt)
            self.tree.column(col, width=120 if col != "urun" else 180, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(btn_frame, text="Yeni Sipariş Ekle", command=self.yeni_siparis_ekle).pack(side="left")
        tk.Button(btn_frame, text="Siparişleri Yenile", command=self.load_siparisler).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Siparişi Onayla", command=self.siparis_onayla).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Siparişi İptal Et", command=self.siparis_iptal).pack(side="left", padx=5)

    def load_siparisler(self):
        if os.path.exists(SIPARIS_VERI_DOSYASI):
            try:
                with open(SIPARIS_VERI_DOSYASI, "r", encoding="utf-8") as f:
                    self.siparisler = json.load(f)
            except Exception:
                self.siparisler = []
        else:
            self.siparisler = []

        self.tum_siparisler = list(self.siparisler)
        self.filtrele()

    def filtrele(self):
        filtre = self.filter_var.get().lower()
        self.tree.delete(*self.tree.get_children())

        for sip in self.tum_siparisler:
            if filtre in sip.get("musteri", "").lower() or filtre in sip.get("urun", "").lower():
                stok_durum = self.stok_kontrol(sip.get("urun"), int(sip.get("adet", 0)))
                self.tree.insert("", "end", values=(
                    sip.get("siparis_id", ""),
                    sip.get("musteri", ""),
                    sip.get("urun", ""),
                    sip.get("adet", ""),
                    sip.get("durum", ""),
                    stok_durum
                ))

    def stok_kontrol(self, urun, adet):
        mevcut = ORNEK_STOK.get(urun, 0)
        if mevcut >= adet:
            return f"Var ({mevcut})"
        elif mevcut > 0:
            return f"Yetersiz ({mevcut})"
        else:
            return "Stok Yok"

    def yeni_siparis_ekle(self):
        def kaydet():
            sip_id = entry_id.get().strip()
            musteri = entry_musteri.get().strip()
            urun = entry_urun.get().strip()
            try:
                adet = int(entry_adet.get().strip())
            except:
                messagebox.showerror("Hata", "Adet sayı olmalı!")
                return

            if not (sip_id and musteri and urun and adet > 0):
                messagebox.showerror("Hata", "Tüm alanlar doldurulmalı!")
                return

            yeni_siparis = {
                "siparis_id": sip_id,
                "musteri": musteri,
                "urun": urun,
                "adet": adet,
                "durum": "Beklemede"
            }
            self.siparisler.append(yeni_siparis)
            self.siparis_kaydet()
            popup.destroy()
            self.load_siparisler()

        popup = tk.Toplevel(self)
        popup.title("Yeni Sipariş Ekle")
        popup.geometry("320x280")
        popup.transient(self)
        popup.grab_set()

        tk.Label(popup, text="Sipariş ID:").pack(pady=3)
        entry_id = tk.Entry(popup)
        entry_id.pack(pady=3)

        tk.Label(popup, text="Müşteri:").pack(pady=3)
        entry_musteri = tk.Entry(popup)
        entry_musteri.pack(pady=3)

        tk.Label(popup, text="Ürün:").pack(pady=3)
        entry_urun = tk.Entry(popup)
        entry_urun.pack(pady=3)

        tk.Label(popup, text="Adet:").pack(pady=3)
        entry_adet = tk.Entry(popup)
        entry_adet.pack(pady=3)

        tk.Button(popup, text="Kaydet", command=kaydet).pack(pady=10)

    def siparis_kaydet(self):
        with open(SIPARIS_VERI_DOSYASI, "w", encoding="utf-8") as f:
            json.dump(self.siparisler, f, ensure_ascii=False, indent=4)

    def _secili_siparis(self):
        secili = self.tree.focus()
        if not secili:
            messagebox.showwarning("Uyarı", "Önce bir sipariş seçiniz!")
            return None
        return self.tree.item(secili)["values"]

    def siparis_onayla(self):
        secili = self._secili_siparis()
        if secili is None:
            return
        siparis_id = secili[0]

        for sip in self.siparisler:
            if sip["siparis_id"] == siparis_id:
                sip["durum"] = "Onaylandı"
                break

        self.siparis_kaydet()
        self.load_siparisler()
        messagebox.showinfo("Bilgi", f"Sipariş {siparis_id} onaylandı.")

    def siparis_iptal(self):
        secili = self._secili_siparis()
        if secili is None:
            return
        siparis_id = secili[0]

        for sip in self.siparisler:
            if sip["siparis_id"] == siparis_id:
                sip["durum"] = "İptal"
                break

        self.siparis_kaydet()
        self.load_siparisler()
        messagebox.showinfo("Bilgi", f"Sipariş {siparis_id} iptal edildi.")


