# Ana uygulamayı başlat
Write-Host "Deep Muhasebe Uygulaması Başlatılıyor..." -ForegroundColor Cyan
python -X utf8 main_app.py

# Uygulama kapandıktan sonra GitHub'a gönder
Write-Host "`nGitHub'a gönderiliyor..." -ForegroundColor Yellow
Start-Sleep -Seconds 1
.\push.ps1
