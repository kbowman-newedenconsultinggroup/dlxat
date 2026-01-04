Write-Host "Inside powershell script"
winget install "Microsoft Family Safety" --source msstore
Get-AppXPackage Microsoft.OutlookForWindows | Remove-AppxPackage
Get-AppXPackage Advanc* | Remove-AppXPackage
Get-AppXPackage RealtekSemiconductorCorp.HPAudio* | Remove-AppXPackage

D:\importBookmarks.ps1
D:\importBookmarks-Healthcare.ps1

Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Start\Companions\Microsoft.YourPhone_8wekyb3d8bbwe" -Name "IsEnabled" -Value 0

try {
    # Create a restore point with a custom description
    Checkpoint-Computer -Description "Manual Restore Point" -RestorePointType "MODIFY_SETTINGS"

    Write-Host "System Restore Point created successfully." -ForegroundColor Green
}
catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}
