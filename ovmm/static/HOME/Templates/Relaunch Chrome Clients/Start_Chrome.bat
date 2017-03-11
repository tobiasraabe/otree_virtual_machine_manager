ECHO ON

SETLOCAL ENABLEDELAYEDEXPANSION 


:: clients' username and password
set /A CUSER = client_username
set /A CPWD = client_password

:: number of clients
set /A client_min =  1
set /A client_max = 24

:: first 3 digits of clients' IP4 IP
set /A CLIENT = 123.456.789

:: last number of the clients IP; here client ID + 10 ... 11, 12, 13 ...
set /A IP_min = %client_min% + 10
set /A IP_max = %client_max% + 10

:: server address
set /A HOST = http://127.0.0.1

set "curr_dir=%cd%"



:: loop over all clients and start chrome browser
for /L %%I IN (%IP_min%, 1, %IP_max%) DO (
   SET /A client = %%I - 10
   ECHO Aktuelle Client ID: !client!
   ECHO Aktuelle IP-Adresse: %%I
   if !client! LSS 10 (
      psexec /accepteula \\%CLIENT%.%%I -u %CUSER% -p %CPWD% -d -i "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --kiosk %HOST%/room/econ101/?participant_label=PC_!client!
   )
   if !client! GEQ 10 (
      psexec /accepteula \\%CLIENT%.%%I -u %CUSER% -p %CPWD% -d -i "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --kiosk %HOST%/room/econ101/?participant_label=PC_!client!
   )
:: 3 sec intermission between client launches to avoid odd numbering of clients
   timeout /t 3 /nobreak
)

ECHO Chrome should now have been launched on clients %client_min% through %client_max%.

ECHO OFF

PAUSE
 

 
