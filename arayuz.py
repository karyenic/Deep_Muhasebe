import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar

root = tk.Tk()
root.title("Deep Muhasebe - Yeni Arayüz")
root.geometry("1200x700")

# Üst Menü Çubuğu
menu_bar = tk.Menu(root)
menu_items = {
    "Stok": ["Stok Listesi", "Yeni Stok Ekle", "Stok Raporu"],
    "Cari": ["Cari Kartlar", "Hareketler", "Raporlar"],
    "Kasa": ["Kasa Girişi", "Kasa Çıkışı", "Kasa Raporu"],
    "Fatura": ["Alış Faturası", "Satış Faturası", "Fatura Listesi"]
}
for menu_name, commands in menu_items.items():
    m = tk.Menu(menu_bar, tearoff=0)
    for cmd in commands:
        m.add_command(label=cmd)
    menu_bar.add_cascade(label=menu_name, menu=m)
root.config(menu=menu_bar)

# Sol Panel (Kısayollar)
sidebar = tk.Frame(root, width=200, bg="#e6e6e6")
sidebar.pack(side="left", fill="y")
shortcut_buttons = [
    "Cari", "Stok", "Alış F.", "Satış F.",
    "Üretim", "Servis", "Döviz", "Evrak Kayıt", "Yardım"
]
for name in shortcut_buttons:
    btn = tk.Button(sidebar, text=name, width=18, height=2, bg="white")
    btn.pack(pady=3, padx=5)

# Sağ Panel (Takvim + Notlar)
rightbar = tk.Frame(root, width=250, bg="#f7f7f7")
rightbar.pack(side="right", fill="y")

tk.Label(rightbar, text="Takvim", font=("Arial", 12, "bold"), bg="#f7f7f7").pack(pady=5)
cal = Calendar(rightbar, selectmode="day")
cal.pack(pady=10)

tk.Label(rightbar, text="Notlar", font=("Arial", 12, "bold"), bg="#f7f7f7").pack(pady=5)
notes = tk.Text(rightbar, width=28, height=15)
notes.pack(padx=5, pady=5)

# Orta Alan (İçerik)
content = tk.Frame(root, bg="white")
content.pack(side="left", expand=True, fill="both")
tk.Label(content, text="Deep Muhasebe'ye Hoş Geldiniz",
         font=("Arial", 18), bg="white").pack(pady=20)

root.mainloop()
