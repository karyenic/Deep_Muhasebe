# Geliştirilmiş siparisler.py kodunu PowerShell içinde string olarak tanımla
$siparislerKod = @'
import tkinter as tk
from tkinter import ttk, messagebox

class SiparisModulu(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Sipariş Modülü")
        self.geometry("1000x600")
        self.configure(bg="#f0f0f0")
        self.init_ui()

    def init_ui(self):
        # Başlık
        lbl_baslik = tk.Label(self, text="🛒 Sipariş Modülü", font=("Segoe UI", 16, "bold"), bg="#f0f0f0", fg="#333")
        lbl_baslik.pack(pady=10)

        # Arama ve filtre çerçevesi
        frame_filtre = tk.Frame(self, bg="#f0f0f0")
        frame_filtre.pack(pady=5)

        tk.Label(frame_filtre, text="Müşteri Adı:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=2)
        self.entry_musteri_adi = ttk.Entry(frame_filtre, width=30)
        self.entry_musteri_adi.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_filtre, text="Durum:", bg="#f0f0f0").grid(row=0, column=2, padx=5, pady=2)
        self.combo_durum = ttk.Combobox(frame_filtre, values=["Tümü", "Hazırlanıyor", "Tamamlandı", "Eksik Ürün Var"])
        self.combo_durum.current(0)
        self.combo_durum.grid(row=0, column=3, padx=5, pady=2)

        btn_ara = ttk.Button(frame_filtre, text="Ara", command=self.siparis_ara)
        btn_ara.grid(row=0, column=4, padx=10)

        # Sipariş Listesi
        self.tree = ttk.Treeview(self, columns=("id", "tarih", "musteri", "durum", "toplam"), show="headings", height=20)
        self.tree.heading("id", text="ID")
        self.tree.heading("tarih", text="Tarih")
        self.tree.heading("musteri", text="Müşteri")
        self.tree.heading("durum", text="Durum")
        self.tree.heading("toplam", text="Toplam")

        self.tree.column("id", width=50)
        self.tree.column("tarih", width=120)
        self.tree.column("musteri", width=200)
        self.tree.column("durum", width=150)
        self.tree.column("toplam", width=100)

        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        # Butonlar
        frame_butonlar = tk.Frame(self, bg="#f0f0f0")
        frame_butonlar.pack(pady=10)

        ttk.Button(frame_butonlar, text="➕ Yeni Sipariş", command=self.yeni_siparis).grid(row=0, column=0, padx=5)
        ttk.Button(frame_butonlar, text="📝 Düzenle", command=self.duzenle).grid(row=0, column=1, padx=5)
        ttk.Button(frame_butonlar, text="🗑️ Sil", command=self.sil).grid(row=0, column=2, padx=5)
        ttk.Button(frame_butonlar, text="📦 Faturalandır", command=self.faturalandir).grid(row=0, column=3, padx=5)

    def siparis_ara(self):
        musteri_adi = self.entry_musteri_adi.get()
        durum = self.combo_durum.get()
        messagebox.showinfo("Ara", f"{musteri_adi} - {durum} ile arama yapılıyor (örnek).")

    def yeni_siparis(self):
        messagebox.showinfo("Yeni Sipariş", "Yeni sipariş formu açılır (örnek).")

    def duzenle(self):
        messagebox.showinfo("Düzenle", "Seçilen sipariş düzenlenir (örnek).")

    def sil(self):
        messagebox.showinfo("Sil", "Seçilen sipariş silinir (örnek).")

    def faturalandir(self):
        messagebox.showinfo("Faturalandır", "Seçilen sipariş faturalandırılır (örnek).")

# Test amaçlı doğrudan çalıştırılabilir
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    pencere = SiparisModulu()
    pencere.mainloop()
'@

# Kodun yazılacağı dizini tanımla
$modulKlasoru = "modules\siparisler"
if (-Not (Test-Path $modulKlasoru)) {
    New-Item -Path $modulKlasoru -ItemType Directory
}

# siparisler.py dosyasını oluştur
$siparislerDosyasi = Join-Path $modulKlasoru "siparisler.py"
$siparislerKod | Out-File -Encoding utf8 -FilePath $siparislerDosyasi
Write-Host "✅ siparisler.py dosyası oluşturuldu: $siparislerDosyasi"

# Python yüklü mü kontrol et
$pythonVersion = & python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "`n🟢 Python bulundu: $pythonVersion"
    Write-Host "🚀 siparisler modülü çalıştırılıyor..."
    & python $siparislerDosyasi
} else {
    Write-Warning "❌ Python bulunamadı, modül oluşturuldu ama çalıştırılamadı."
}
