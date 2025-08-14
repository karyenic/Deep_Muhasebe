# Proje ana dizinini belirle
$projeAnaDizini = "C:\YEDEK\Deep_Muhasebe\Deep_Muhasebe-main"

# Betiğin çalışacağı dizine git
Set-Location -Path $projeAnaDizini

Write-Host "Veritabanı dosyası kontrol ediliyor ve siliniyor..."

# Veritabanı dosyasının varlığını kontrol et ve sil
if (Test-Path -Path "deep_muhasebe.db") {
    Remove-Item -Path "deep_muhasebe.db" -Force
    Write-Host "deep_muhasebe.db veritabanı dosyası başarıyla silindi."
} else {
    Write-Host "deep_muhasebe.db veritabanı dosyası bulunamadı, silme işlemi atlandı."
}

Write-Host "kullanici_yonetimi.py dosyasındaki hatalı parametre düzeltiliyor..."

# kullanici_yonetimi.py dosyasını güncelle
$kullaniciYonetimiKodu = Get-Content "gui\kullanici_yonetimi.py" | ForEach-Object {
    # 'is_admin' parametresini 'yetkili' olarak düzelt
    $_ -replace 'is_admin=yetkili', 'yetkili=is_admin'
}
$kullaniciYonetimiKodu | Out-File -FilePath "gui\kullanici_yonetimi.py" -Encoding UTF8 -Force
Write-Host "kullanici_yonetimi.py dosyası başarıyla güncellendi."

#----------------------------------------------------
# 3. Değişiklikleri GitHub'a Gönderme
#----------------------------------------------------
Write-Host "Yerel değişiklikler sahneleniyor ve commit yapılıyor..."
git add .
git commit -m "Son hata duzeltildi: db silindi, kullanici_yonetimi.py dosyasindaki 'is_admin' parametresi 'yetkili' olarak duzeltildi"

Write-Host "Değişiklikler GitHub'a gönderiliyor..."
git push origin main

Write-Host "Proje başarıyla güncellendi ve GitHub'a senkronize edildi."

Write-Host "Lütfen tekrar 'python run.py' komutunu çalıştırın."