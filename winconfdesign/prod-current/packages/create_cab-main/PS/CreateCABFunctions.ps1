$ddf
function Create-CAB-DDF([string]$RootDir, [string]$CurrentDir){
	# Add folder tag for subfolders (skip for root files)
	if($RootDir -ne $CurrentDir){
		$RootDirWithBackslash = "$($RootDir)\"
		$ddfDir = $CurrentDir -Replace [regex]::Escape($RootDirWithBackslash),""
		
		$script:ddf += ".Set DestinationDir=$($ddfDir)"
	}
	
	# Add files in current folder to DDF
	$script:ddf+=(Get-ChildItem -Path "$CurrentDir" -File -Name).ForEach({"""$($CurrentDir)\{0}""" -f $_}) # Note that we add " around each file entry
	
	# Recursive call for each sub folder
	(Get-ChildItem -Path "$CurrentDir" -Directory -Name).ForEach({ Create-CAB-DDF "$($RootDir)" "$($CurrentDir)\$_" })
	
	# Run at the end in the original function call, so we only do it once
	if($RootDir -eq $CurrentDir){
		Write-Host " "
		Write-Host "Write DDF content to the file ""$($PWD)\files.ddf"" (in the ASCII format)."
		$script:ddf | Out-File "$($PWD)\files.ddf" -Encoding Ascii # IT'S REALLY IMPORTANT that we generate an ASCII text file. UTF8 causes errors
		
		Write-Host " "
		Write-Host "Finished creating the DDF file!"
	}
		
	# Source: https://stackoverflow.com/questions/21652659/windows-cabinet-file-for-sub-directories
	#         https://stackoverflow.com/questions/45306085/convert-text-file-to-ansi-format
}

function Create-CAB([string]$InputDDF, [string]$OutputCAB){
	Write-Host " "
	Write-Host "Create CAB ""$OutputCAB"""
	
	Write-Host "The command: makecab /D CabinetNameTemplate=""$OutputCAB"" /D DiskDirectory1=""$PWD"" /D MaxDiskSize=0 /D Cabinet=on /D Compress=on /D CompressionType=MSZIP /f ""$InputDDF"""
	makecab /D CabinetNameTemplate="$OutputCAB" /D DiskDirectory1="$PWD" /D MaxDiskSize=0 /D Cabinet=on /D Compress=on /D CompressionType=MSZIP /f "$InputDDF"
}