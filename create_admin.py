from core.database import get_session, init_db
from core.models import Firm, User
from modules.auth.manager import hash_password
   def create_admin():
        session = next(get_session())
        try:
            # Firma oluİ¦Ãƒâ€¦¸tur
            firma = Firm(
                unvan="Admin Firma",
                kisa_ad="ADMIN",
                vergi_dairesi="ÃƒÆ’Ã¢â‚¬Å¾Ãƒâ€š°stanbul",
                vergi_no="1234567890"
            )
            session.add(firma)
            session.commit()
                                                                                                                                                           # Admin
                                                                                                                                                           # kullanıcı
                                                                                                                                                           # oluİ¦Ãƒâ€¦¸tur
            admin = User(
                username="admin",
                password_hash=hash_password("admin123"),
                role="admin",
                email="admin@admin.com",
                firma_id=firma.id
            )
            session.add(admin)
            session.commit()
            print("Admin kullanıcı baİ¦Ãƒâ€¦¸arıyla oluİ¦Ãƒâ€¦¸turuldu!")
        except Exception as e:
            print(f"Hata: {str(e)}")
            session.rollback()
        finally:
            session.close()
    if __name__ == "__main__":
        init_db()  # Veritabanını baİ¦Ãƒâ€¦¸lat
        create_admin()


