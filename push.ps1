cd $PSScriptRoot
git add .
git commit -m "Acil güncelleme: $(Get-Date -Format 'HH:mm')"
git push
Write-Host "✅ GitHub'a gönderildi!" -ForegroundColor Green
