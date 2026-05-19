@echo off
chcp 65001 >nul
"D:\tools\python\python313\python.exe" "D:\code\O&M_Platform_restart\restart_platform\main.py" 2>"D:\code\O&M_Platform_restart\error.log"
if %errorlevel% neq 0 (
    echo.
    echo [Error] exit code: %errorlevel%
    type "D:\code\O&M_Platform_restart\error.log"
)
echo.
pause
