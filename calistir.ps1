# calistir.ps1
$logFile = "C:\YEDEK\Deep_Muhasebe\app_run_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
Set-Location -Path "C:\YEDEK\Deep_Muhasebe"
.\.venv\Scripts\activate
python app.py 2>&1 | Tee-Object -FilePath $logFile
deactivate
Write-Host "Uygulama logları kaydedildi: $logFile" -ForegroundColor Cyan
