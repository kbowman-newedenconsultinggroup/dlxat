set LOGFILE=%SystemDrive%\tckc\hpremoval.log

move Remove-HPbloatware.ps1 %SystemDrive%\tckc\.

powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Start-Process powershell.exe -Verb RunAs -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File %SystemDrive%\tckc\Remove-HPbloatware.ps1' >>%LOGFILE% "

echo result: %ERRORLEVEL% >> %LOGFILE%