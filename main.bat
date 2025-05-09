@echo off

:launch
call venv/Scripts/activate
py src/main.py
pause
exit /b

echo Starting Game...
goto :launch