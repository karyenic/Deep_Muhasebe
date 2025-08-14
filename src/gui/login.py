# -*- coding: utf-8 -*-
from tkinter import ttk
from core.database import get_session
from core.models import Firm, User
from modules.auth.manager import check_password

class LoginWindow:
    def __init__(self, app):
        self.app = app
        self.session = get_session()
        self.create_widgets()

    def create_widgets(self):
        # Font ayarı
        self.font = ("Arial", 10)
        
        self.frame = ttk.Frame(self.app.root, padding=20)
        self.frame.grid(row=0, column=0, sticky="nsew")
        
        # Diğer widget'lar buraya...
        # (Orijinal login.py içeriğiniz burada kalacak)


