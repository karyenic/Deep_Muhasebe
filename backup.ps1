param(
    [string] = "C:\YEDEK\OK2_muhasebe\backups"
)
 = Get-Date -Format "yyyyMMdd_HHmmss"
 = Join-Path -Path  -ChildPath "backup_.zip"
Compress-Archive -Path "C:\YEDEK\OK2_muhasebe\*" -DestinationPath 
Write-Host "Yedek oluşturuldu: "
