Write-Host "###################"
Write-Host "#                 #"
Write-Host "# Create CAB file #"
Write-Host "#                 #"
Write-Host "###################"
Write-Host " "

# Get folder path dropped onto the bat file
$cabFolder = $($env:cabFolder)
# Remove " added to the start and end of the folder path
$cabFolder = $cabFolder -Replace """",""

# Extract foldername as the new CAB filename, then append "_Updated.cab" to the new filename
$cabFilename = ($cabFolder -replace '.*\\') + "_Updated.cab"

Write-Host " "
Write-Host "CAB folder: ""$cabFolder"""
Write-Host "CAB filename: ""$cabFilename"""

# Cleanup
Remove-Item "$($PWD)\setup.inf" -Force -Confirm:$false -ErrorAction SilentlyContinue
Remove-Item "$($PWD)\setup.rpt" -Force -Confirm:$false -ErrorAction SilentlyContinue
Remove-Item "$($PWD)\files.ddf" -Force -Confirm:$false -ErrorAction SilentlyContinue
Remove-Item "$($PWD)\$cabFilename" -Force -Confirm:$false -ErrorAction SilentlyContinue

# Import Create CAB functions (the root folder is where the BAT file is located) 
. PS\CreateCABFunctions.ps1

# Create DDF file
Write-Host " "
Write-Host "Populate DDF file ""$($PWD)\files.ddf"" with the files and folders from ""$cabFolder"""
Create-CAB-DDF "$cabFolder" "$cabFolder"

# Create CAB file
Write-Host " "
Write-Host "Create the CAB file ""$cabFilename"" based on ""$($PWD)\files.ddf"""
Create-CAB "$($PWD)\files.ddf" "$cabFilename"

# Cleanup (remove these two lines if you want to keep these two setup files that makecab creates)
Remove-Item "$($PWD)\setup.inf" -Force -Confirm:$false -ErrorAction SilentlyContinue
Remove-Item "$($PWD)\setup.rpt" -Force -Confirm:$false -ErrorAction SilentlyContinue