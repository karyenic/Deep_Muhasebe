# Uygulama başlatma ve GitHub senkronizasyon scripti

# 1. Python ortamını ayarla
$env:PYTHONPATH = "$PWD\src;$PWD"

# 2. Uygulamayı başlat
Write-Host "Deep Muhasebe Uygulaması Başlatılıyor..." -ForegroundColor Cyan
python -X utf8 main_app.py

# 3. GitHub senkronizasyonu
Write-Host "`nGitHub'a gönderiliyor..." -ForegroundColor Yellow
Start-Sleep -Seconds 1
.\push.ps1
