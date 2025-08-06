# db_test.ps1
Set-Location -Path "C:\YEDEK\Deep_Muhasebe"
.\.venv\Scripts\activate
python -c "import sqlite3; conn=sqlite3.connect('muhasebe.db'); cursor=conn.cursor(); cursor.execute('SELECT sqlite_version()'); print('SQLite sürümü:', cursor.fetchone()[0]); conn.close()"
deactivate
