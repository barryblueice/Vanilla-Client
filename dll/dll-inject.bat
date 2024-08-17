@echo off

set currentDir=%~dp0

set dllPath=%currentDir%wxhelper.dll

.\ConsoleApplication.exe -i WeChat.exe -p %dllPath%

pause