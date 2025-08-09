# Deep Muhasebe Otomasyon Sistemi v1.2
param(
    [string]$Komut,
    [string]$Mod
)

Clear-Host
Write-Host ""
Write-Host "    D E E P   M U H A S E B E" -ForegroundColor Cyan
Write-Host "    ---------------------------" -ForegroundColor Cyan
Write-Host "    Otomasyon Sistemi Aktif" -ForegroundColor Cyan
Write-Host ""

# Komut kontrolu
if (-not $Komut) {
    Write-Host "HATA: Komut belirtilmedi!" -ForegroundColor Red
    Write-Host "Kullanim: .\muhasebe.ps1 -Komut Baslat -Mod Full" -ForegroundColor Yellow
    exit
}

Write-Host "Sistem baslatiliyor..." -ForegroundColor Green
Write-Host "Komut: $Komut" -ForegroundColor Cyan
Write-Host "Mod: $Mod" -ForegroundColor Cyan
Write-Host "Calisma Dizini: $pwd" -ForegroundColor Yellow

# Klasor kontrolleri
$klasorler = @("docs", "faturalar", "yedekler")
foreach ($klasor in $klasorler) {
    if (-not (Test-Path $klasor)) {
        New-Item -ItemType Directory -Name $klasor | Out-Null
        Write-Host "KLASOR OLUSTURULDU: $klasor"
    }
}

# Test verisi olustur
$veri = "Tarih,Musteri,Tutar,Aciklama`n"
$veri += "$(Get-Date -Format 'dd.MM.yyyy'),Test Musteri,1000,Test Faturasi"

$veri | Out-File -FilePath ".\faturalar\test_faturasi.csv" -Encoding UTF8

# Basari mesaji
Write-Host ""
Write-Host "SISTEM BASARIYLA KURULDU!" -ForegroundColor Green
Write-Host "Test faturasi olusturuldu: .\faturalar\test_faturasi.csv" -ForegroundColor Cyan
Write-Host "Sonraki adim: GitHub Desktop ile Commit & Push yapin" -ForegroundColor Yellow
