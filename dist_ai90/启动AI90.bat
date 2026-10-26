@echo off
cd /d "%~dp0"
where python >nul 2>nul || (echo 请先安装 Python 3.10+ & pause & exit /b 1)
python ai90_app.py
pause
