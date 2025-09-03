# Yedekleme Scripti
$tarih = Get-Date -Format "yyyyMMdd_HHmmss"
$yedekDosya = "yedekler\muhasebe_$tarih.db"
Copy-Item "veriler\muhasebe.db" $yedekDosya
Write-Host "? Yedek olusturuldu: $yedekDosya" -ForegroundColor Green
