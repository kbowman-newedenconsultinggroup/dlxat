@echo off

rem Set the current directory to be the one we run the scripts from
SET currentDir=%~dp0
cd /d %currentDir%

rem Populate the environment variabel cabFolder with the folder dropped onto this bat file
set cabFolder=%*

rem Start the CreateDDFOnly script in PowerShell
powershell -f PS\CreateDDFOnly.ps1

pause