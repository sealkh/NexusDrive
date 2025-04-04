@echo off
:: Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found in PATH
    pause
    exit /b 1
)

:: Configure paths
set PY_MAIN=NexusDrive.py
set VENV_DIR=venv

:: Create virtual environment if missing
if not exist "%VENV_DIR%" (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
)

:: Activate venv
call %VENV_DIR%\Scripts\activate

:: Install dependency analyzer
pip install pipreqs --quiet --disable-pip-version-check

:: Generate requirements.txt
echo Analyzing project dependencies...
pipreqs ./ --recursive --force --mode gt

:: Install dependencies
echo Installing required packages...
pip install -r requirements.txt --quiet --disable-pip-version-check

:: Launch application
echo.
echo ===== Starting Application =====
python %PY_MAIN%