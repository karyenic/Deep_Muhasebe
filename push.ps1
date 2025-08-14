# GitHub Senkronizasyon Scripti
Set-Location -Path $PSScriptRoot

git add .
$commitMessage = "PC Güncellemesi: $(Get-Date -Format 'dd.MM.yyyy HH:mm')"
git commit -m $commitMessage
git push

Write-Host "✅ GitHub'a gönderildi!" -ForegroundColor Green
Start-Sleep -Seconds 3
