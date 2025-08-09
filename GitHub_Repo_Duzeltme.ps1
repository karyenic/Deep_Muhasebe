# GitHub_Repo_Duzeltme.ps1
Write-Host "GitHub Repo Bağlantı Düzeltme Aracı" -ForegroundColor Cyan
Write-Host "----------------------------------"

# 1. Proje dizinine git
Set-Location -Path "C:\YEDEK\Deep_Muhasebe\Deep_Muhasebe-main"

# 2. Mevcut uzak repo ayarlarını kontrol et
Write-Host "`n[1/4] Mevcut uzak repo ayarları kontrol ediliyor..." -ForegroundColor Green
git remote -v

# 3. Yanlış uzak repo bağlantısını kaldır
Write-Host "`n[2/4] Yanlış uzak repo bağlantısı kaldırılıyor..." -ForegroundColor Green
git remote remove origin

# 4. Doğru uzak repo bağlantısını ekle
Write-Host "`n[3/4] Doğru GitHub repo bağlantısı ekleniyor..." -ForegroundColor Green
$correctURL = "https://github.com/karyenic/Deep_Muhasebe.git"
git remote add origin $correctURL

# 5. Değişiklikleri GitHub'a gönder
Write-Host "`n[4/4] Değişiklikler GitHub'a gönderiliyor..." -ForegroundColor Green
git push -u origin main

Write-Host "`nİşlem başarıyla tamamlandı!" -ForegroundColor Green
Write-Host "Projeniz şu adreste: $correctURL" -ForegroundColor Cyan