# Deep Muhasebe Uygulaması Başlatma Scripti
$PROJE_KOKU = $PSScriptRoot
Set-Location $PROJE_KOKU

Write-Host "Deep Muhasebe Uygulaması Başlatılıyor..."
Write-Host "=================================================="

# Sanal ortamı etkinleştir
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    .\venv\Scripts\Activate.ps1
    Write-Host "Sanal ortam etkinleştirildi"
} else {
    Write-Host "UYARI: Sanal ortam bulunamadı!" -ForegroundColor Yellow
}

# Python yürütücü bilgisi
$pythonYolu = (Get-Command python).Path
Write-Host "Python Yolu: $pythonYolu"

# Ana uygulamayı başlat
Write-Host "Uygulama başlatılıyor..."
python -m src.main_app

# Uygulama kapandığında
Write-Host "=================================================="
Write-Host "Uygulama kapatıldı"
