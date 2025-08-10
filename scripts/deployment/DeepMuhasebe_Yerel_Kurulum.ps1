# DeepMuhasebe_Yerel_Kurulum.ps1

Write-Host "Deep Muhasebe Yerel Kurulum Aracı" -ForegroundColor Cyan
Write-Host "--------------------------------"

# 1. Ön kontroller
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python bulunamadı. Lütfen Python 3.10+ yükleyin." -ForegroundColor Red
    Write-Host "İndirme linki: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git bulunamadı. Lütfen Git for Windows'u yükleyin." -ForegroundColor Red
    Write-Host "İndirme linki: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit
}

# 2. Proje bilgilerini alma
$githubLink = Read-Host "GitHub proje linkini girin (Örnek: https://github.com/karyenic/DeepMuhasebe)"
$kurulumYolu = Read-Host "Kurulum yolu girin (Varsayılan: C:\DeepMuhasebe)" -Default "C:\DeepMuhasebe"

# 3. Projeyi klonlama
New-Item -Path $kurulumYolu -ItemType Directory -Force | Out-Null
Set-Location $kurulumYolu
git clone $githubLink .

# 4. Sanal ortam ve bağımlılıklar
python -m venv venv
.\venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

# 5. Yapılandırma
New-Item -Path ".\veriler" -ItemType Directory -Force | Out-Null
New-Item -Path ".\yedekler" -ItemType Directory -Force | Out-Null

# Ana veritabanını oluştur
$dbPath = ".\veriler\muhasebe.db"
if (-not (Test-Path $dbPath)) {
    [System.IO.File]::WriteAllBytes($dbPath, [byte[]]@())
    Write-Host "Ana veritabanı oluşturuldu: $dbPath" -ForegroundColor Green
}

Write-Host "`nKurulum başarıyla tamamlandı!" -ForegroundColor Green
Write-Host "Uygulamayı başlatmak için:" -ForegroundColor Cyan
Write-Host "1. PowerShell'i yönetici olarak açın" -ForegroundColor Yellow
Write-Host "2. Şu komutları sırayla çalıştırın:" -ForegroundColor Yellow
Write-Host "   cd '$kurulumYolu'" -ForegroundColor Green
Write-Host "   .\venv\Scripts\activate" -ForegroundColor Green
Write-Host "   python app.py" -ForegroundColor Green