# Veritabani_Onarim.ps1
Write-Host "Veritabanı Onarım Aracı" -ForegroundColor Cyan
Write-Host "-----------------------"

# 1. Veritabanı dosyasının yolunu belirle
$dbPath = "C:\YEDEK\Deep_Muhasebe\Deep_Muhasebe-main\veriler\muhasebe.db"

# 2. Yedek al
$backupDir = "C:\YEDEK\Deep_Muhasebe\Deep_Muhasebe-main\yedekler"
if (-not (Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir | Out-Null
}

$date = Get-Date -Format "yyyyMMdd_HHmmss"
$backupFile = "$backupDir\muhasebe_$date.db"

if (Test-Path $dbPath) {
    Copy-Item $dbPath $backupFile
    Write-Host "Veritabanı yedeklendi: $backupFile" -ForegroundColor Green
} else {
    Write-Host "Uyarı: Veritabanı dosyası bulunamadı" -ForegroundColor Yellow
}

# 3. SQLite ile veritabanını onar
if (Test-Path $dbPath) {
    # SQL komutlarını doğrudan sqlite3'e ilet
    $sqlCommands = @"
BEGIN TRANSACTION;
DROP TABLE IF EXISTS firmalar;
CREATE TABLE firmalar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad TEXT NOT NULL,
    vergi_no TEXT UNIQUE,
    telefon TEXT,
    adres TEXT
);
COMMIT;
"@

    # Komutları doğrudan sqlite3'e gönder
    $sqlCommands | & sqlite3 $dbPath
    
    Write-Host "Veritabanı şeması başarıyla güncellendi" -ForegroundColor Green
} else {
    # Veritabanı dosyası yoksa oluştur
    [System.IO.File]::WriteAllBytes($dbPath, [byte[]]@())
    Write-Host "Yeni veritabanı oluşturuldu: $dbPath" -ForegroundColor Green
    
    # Yeni tabloyu oluştur
    $sqlCommands = @"
CREATE TABLE firmalar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad TEXT NOT NULL,
    vergi_no TEXT UNIQUE,
    telefon TEXT,
    adres TEXT
);
"@
    $sqlCommands | & sqlite3 $dbPath
}

# 4. Uygulamayı başlat
Write-Host "`nUygulamayı başlatmak için: python app.py" -ForegroundColor Cyan