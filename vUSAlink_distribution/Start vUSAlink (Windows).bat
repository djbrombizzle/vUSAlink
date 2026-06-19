@echo off
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 ( py vUSAlink.py & goto :eof )
where python >nul 2>nul
if errorlevel 1 (
  echo.
  echo  Python was not found.
  echo  Install it from https://www.python.org/downloads/
  echo  and tick "Add Python to PATH" during setup, then run this again.
  echo.
  pause
  goto :eof
)
python vUSAlink.py
