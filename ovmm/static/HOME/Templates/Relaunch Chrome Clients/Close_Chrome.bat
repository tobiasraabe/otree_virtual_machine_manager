ECHO OFF

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

for /L %%I IN (%IP_min%, 1, %IP_max%) DO (
   SET /A client = %%I - 10
   ECHO Aktuelle Client ID: !client!
   ECHO Aktuelle IP-Adresse: %%I
   taskkill /s %CLIENT%.%%I /u %CUSER% /p %CPWD% /im chrome*
)

ECHO Schlieﬂen von Chrome beendet.

ECHO OFF

PAUSE

REM PING 1.1.1.1 -n 1 -w 15000

REM wmic process where "caption='vlc.exe'" get processId
REM taskkill /f /pid pidOfProcess
REM taskkill /f /im vlc*
REM taskkill /s {remote pc} /u {domain | username} /p {password} /PID {process id} 
