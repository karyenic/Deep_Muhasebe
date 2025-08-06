# -*- coding: utf-8 -*-
import sqlite3
                conn = sqlite3.connect('main.db')
cursor = conn.cursor()
                try:
                                                                                                                                cursor.execute(
                                                                                                                                    "ALTER TABLE firms ADD COLUMN website VARCHAR(255);")
                                                                                                                                print(
                                                                                                                                    "SÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€š¼tun eklendi.")
except sqlite3.OperationalError as e:
                                                                                                                                print(
                                                                                                                                    "Hata:", e)
                conn.commit()
conn.close()
                

