@echo off

rem Set the current directory to be the one we run the scripts from
SET currentDir=%~dp0
cd /d %currentDir%

rem Populate the environment variabel cabFolder with the folder dropped onto this bat file
set cabFolder=%*

rem Start the CreateCAB script in PowerShell
powershell -f PS\CreateCAB.ps1

pause