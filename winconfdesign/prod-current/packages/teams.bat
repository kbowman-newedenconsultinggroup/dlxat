set LOGFILE=%SystemDrive%\tckc\teams.log

echo Expanding teams.cab >> %LOGFILE%
expand -r teams.cab  -F:* %SystemDrive%\tckc\  >> %LOGFILE%
echo result: %ERRORLEVEL% >> %LOGFILE%

echo Running teamsbootstrapper >> %LOGFILE%

c:\tckc\teamsbootstrapper.exe -p -o "c:\tckc\MSTeams-x64.msix"

echo result: %ERRORLEVEL% >> %LOGFILE%