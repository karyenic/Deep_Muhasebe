# Proje ana dizinini belirle
$projeAnaDizini = "C:\YEDEK\Deep_Muhasebe\Deep_Muhasebe-main"

# Betiğin çalışacağı dizini belirle
Set-Location -Path $projeAnaDizini

Write-Host "GitHub'daki en son değişiklikler çekiliyor..."
# GitHub'daki en son değişiklikleri çek
git pull origin main

Write-Host "Değişiklikler birleştirildi. Şimdi yerel değişiklikler GitHub'a gönderiliyor..."
# Yerel değişiklikleri GitHub'a gönder
git push origin main

Write-Host "Tüm değişiklikler başarıyla senkronize edildi."