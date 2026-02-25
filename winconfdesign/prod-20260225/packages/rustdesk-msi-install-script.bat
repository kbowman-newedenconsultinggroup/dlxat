@echo off

REM Assign the value random password to the password variable
setlocal ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION
set alfanum=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789
REM set rustdesk_pw="secretpassword"
REM for /L %%b in (1, 1, 12) do (
REM     set /A rnd_num=!RANDOM! %% 62
REM     for %%c in (!rnd_num!) do (
REM         set rustdesk_pw=!rustdesk_pw!!alfanum:~%%c,1!
REM     )
REM )

set rustdesk_pw="secretpassword"

REM Get your config string from your Web portal and Fill Below
REM set rustdesk_cfg="configstring"

REM rustdesk.exe --config "host=1.2.3.4,key=THEKEY"
set rustdesk_cfg="host=rdtest.techconnectkc.io,key=baWLQqV2vpulL3TlGChfsJLpkdu3WelU1brGtgR9gJg="

REM ############################### Please Do Not Edit Below This Line #########################################

if not exist C:\Temp\ md C:\Temp\
cd C:\Temp\

curl -L "https://github.com/rustdesk/rustdesk/releases/download/1.2.6/rustdesk-1.2.6-x86_64.exe" -o rustdesk.exe

rustdesk.exe --silent-install
timeout /t 20

cd "C:\Program Files\RustDesk\"
rustdesk.exe --install-service
timeout /t 20

for /f "delims=" %%i in ('rustdesk.exe --get-id ^| more') do set rustdesk_id=%%i

rustdesk.exe --config %rustdesk_cfg%

rustdesk.exe --password %rustdesk_pw%

echo ...............................................
REM Show the value of the ID Variable
echo RustDesk ID: %rustdesk_id%

REM Show the value of the Password Variable
echo Password: %rustdesk_pw%
echo ...............................................