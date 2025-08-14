# -*- coding: utf-8 -*-
from tkinter import font


def apply_font_fix(root):
    # TÃƒÆ’Ã†â€™Ãƒâ€š¼rkÃƒÆ’Ã†â€™Ãƒâ€š§e karakterleri destekleyen fontlar
    turkish_fonts = [
         "Arial", "Segoe UI", "DejaVu Sans",
         "Verdana", "Tahoma", "Calibri"
         ]
                                                                                   # Sistemde
                                                                                   # mevcut
                                                                                   # fontları
                                                                                   # kontrol
                                                                                   # et
     available_fonts = list(font.families())
      selected_font = "Arial"
                                                                                   # Tercih
                                                                                   # sırasına
                                                                                   # gÃƒÆ’Ã†â€™Ãƒâ€š¶re
                                                                                   # font
                                                                                   # seÃƒÆ’Ã†â€™Ãƒâ€š§
       for f in turkish_fonts:
            if f in available_fonts:
                selected_font = f
                break
                                                                                   # TÃƒÆ’Ã†â€™Ãƒâ€š¼m
                                                                                   # widget'lara
                                                                                   # uygula
        root.option_add("*Font", (selected_font, 10))
                                                                                   # ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“zel durumlar
        root.option_add("*Label.Font", (selected_font, 10))
        root.option_add("*Button.Font", (selected_font, 10))
        root.option_add("*Entry.Font", (selected_font, 10))
        root.option_add("*Listbox.Font", (selected_font, 10))
        root.option_add("*Combobox.Font", (selected_font, 10))




