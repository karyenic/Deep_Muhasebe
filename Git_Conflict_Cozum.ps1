# Git_Conflict_Cozum.ps1
Write-Host "Git Uzak Repo Çakışma Çözüm Aracı" -ForegroundColor Cyan
Write-Host "---------------------------------"

# 1. Proje dizinine git
Set-Location -Path "C:\YEDEK\Deep_Muhasebe\Deep_Muhasebe-main"

# 2. Uzak repo değişikliklerini al ve birleştir
Write-Host "`n[1/4] Uzak repo değişiklikleri alınıyor ve birleştiriliyor..." -ForegroundColor Green
git pull origin main --allow-unrelated-histories

# 3. Çakışmaları çöz (eğer varsa)
Write-Host "`n[2/4] Çakışmalar kontrol ediliyor..." -ForegroundColor Green
$conflicts = git diff --name-only --diff-filter=U

if ($conflicts) {
    Write-Host "Çakışan dosyalar bulundu:" -ForegroundColor Yellow
    $conflicts
    
    # Çakışmaları çöz (yerel dosyaları koru)
    foreach ($file in $conflicts) {
        Write-Host "`n$file için çakışma çözülüyor..." -ForegroundColor Cyan
        git checkout --ours $file
        git add $file
    }
    
    git commit -m "Çakışmalar çözüldü (yerel sürümler korundu)"
}

# 4. Değişiklikleri tekrar gönder
Write-Host "`n[3/4] Değişiklikler GitHub'a gönderiliyor..." -ForegroundColor Green
git push -u origin main

# 5. Son durumu kontrol et
Write-Host "`n[4/4] Son durum kontrol ediliyor..." -ForegroundColor Green
git status
git log --oneline -n 3

Write-Host "`nİşlem başarıyla tamamlandı!" -ForegroundColor Green
Write-Host "Projeniz şu adreste: https://github.com/karyenic/Deep_Muhasebe" -ForegroundColor Cyan