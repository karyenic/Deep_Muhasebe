import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime

class DeepMuhasebeUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Deep Muhasebe - Yeni Arayüz")
        self.geometry("900x600")

        self.create_widgets()

    def create_widgets(self):
        # Üst başlık
        title = tk.Label(self, text="Deep Muhasebe", font=("Segoe UI", 20, "bold"))
        title.pack(pady=10)

        # Ana çerçeve
        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Sol taraf (Takvim)
        cal_frame = tk.LabelFrame(frame, text="Takvim")
        cal_frame.pack(side="left", fill="y", padx=5, pady=5)

        self.cal = Calendar(cal_frame, selectmode="day", date_pattern="dd/mm/yyyy")
        self.cal.pack(padx=10, pady=10)

        # Orta panel (Notlar)
        notes_frame = tk.LabelFrame(frame, text="Günlük Notlar")
        notes_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.notes_text = tk.Text(notes_frame, wrap="word")
        self.notes_text.pack(fill="both", expand=True)

        # Sağ panel (İşlem listesi)
        ops_frame = tk.LabelFrame(frame, text="İşlem Listesi")
        ops_frame.pack(side="left", fill="y", padx=5, pady=5)

        self.ops_list = tk.Listbox(ops_frame)
        self.ops_list.pack(fill="y", expand=True)
        for i in range(1, 6):
            self.ops_list.insert("end", f"İşlem {i}")

if __name__ == "__main__":
    app = DeepMuhasebeUI()
    app.mainloop()
