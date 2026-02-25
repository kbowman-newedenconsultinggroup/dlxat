Write-Host "########################"
Write-Host "#                      #"
Write-Host "# Create DDF file only #"
Write-Host "#                      #"
Write-Host "########################"
Write-Host " "

# Get folder path dropped onto the bat file
$cabFolder = $($env:cabFolder)
# Remove " added to the start and end of the folder path
$cabFolder = $cabFolder -Replace """",""

Write-Host " "
Write-Host "CAB folder: ""$cabFolder"""

# Cleanup
Remove-Item "$($PWD)\files.ddf" -Force -Confirm:$false -ErrorAction SilentlyContinue

# Import Create CAB functions (the root folder is where the BAT file is located) 
. PS\CreateCABFunctions.ps1

# Create DDF file
Write-Host " "
Write-Host "Populate DDF file ""$($PWD)\files.ddf"" with the files and folders from ""$cabFolder"""
Create-CAB-DDF "$cabFolder" "$cabFolder"
