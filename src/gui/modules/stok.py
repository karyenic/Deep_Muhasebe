# -*- coding: utf-8 -*-
from tkinter import ttk
from core.database import get_session
from core.models import Product
class StokModule(ttk.Frame):
def __init__(
self, parent):
super().__init__(parent)
self.create_widgets()
def create_widgets(
self):
# Basit
# stok
# arayÃƒÆ’Ã†â€™Ãƒâ€š¼zÃƒÆ’Ã†â€™Ãƒâ€š¼
toolbar = ttk.Frame(
self)
toolbar.pack(
fill=tk.X, pady=5)
ttk.Button(toolbar, text="Yeni ÃƒÆ’Ã†â€™Ãƒâ€¦Ã¢â‚¬Å“rÃƒÆ’Ã†â€™Ãƒâ€š¼n", command=self.new_product).pack(
side=tk.LEFT, padx=5)
# Stok
# listesi
columns = (
"id", "code", "name", "stock", "price")
self.tree = ttk.Treeview(
self, columns=columns, show="headings")
self.tree.pack(
fill=tk.BOTH, expand=True, padx=10, pady=5)
# Baİ¦Ãƒâ€¦¸lıklar
self.tree.heading(
"id", text="ID")
self.tree.heading(
"code", text="Stok Kodu")
self.tree.heading(
"name", text="ÃƒÆ’Ã†â€™Ãƒâ€¦Ã¢â‚¬Å“rÃƒÆ’Ã†â€™Ãƒâ€š¼n Adı")
self.tree.heading(
"stock", text="Stok Miktarı")
self.tree.heading(
"price", text="Birim Fiyat")
self.load_products()
def load_products(self):
# Veritabanından ÃƒÆ’Ã†â€™Ãƒâ€š¼rÃƒÆ’Ã†â€™Ãƒâ€š¼nleri yÃƒÆ’Ã†â€™Ãƒâ€š¼kle
session = get_session()
products = session.query(Product).all()
for product in products:
self.tree.insert("", "end", values=(
product.id,
product.code,
product.name,
product.stock_quantity,
f"{product.unit_price:.2f} ÃƒÆ’¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šº"
))
def new_product(self):
# Yeni ÃƒÆ’Ã†â€™Ãƒâ€š¼rÃƒÆ’Ã†â€™Ãƒâ€š¼n formu
print("Yeni ÃƒÆ’Ã†â€™Ãƒâ€š¼rÃƒÆ’Ã†â€™Ãƒâ€š¼n formu aÃƒÆ’Ã†â€™Ãƒâ€š§ılacak")




