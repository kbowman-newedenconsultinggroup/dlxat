mkdir %SystemDrive%\tckc\
mkdir %SystemDrive%\tckc\Win11Debloat\
set LOGFILE=%SystemDrive%\tckc\Win11Debloat\install_Winn11Debloat.log

echo Expanding Win11Debloat.cab >> %LOGFILE%
expand -r Win11Debloat.cab  -F:* %SystemDrive%\tckc\Win11Debloat\  >> %LOGFILE%
echo result: %ERRORLEVEL% >> %LOGFILE%

echo Running Win11DeBloat >> %LOGFILE%

powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Start-Process powershell.exe -Verb RunAs -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File %SystemDrive%\tckc\Win11Debloat\Win11Debloat.ps1 -Silent -RemoveApps -RunDefaults -Sysprep'" >> %LOGFILE%

echo result: %ERRORLEVEL% >> %LOGFILE%
